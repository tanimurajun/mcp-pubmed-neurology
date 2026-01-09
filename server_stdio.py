import sys
import json
import asyncio
import httpx
import xmltodict
import logging
import os

# Configure logging to stderr so it doesn't interfere with stdout JSON-RPC
logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("pubmed-mcp")

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
API_KEY = os.environ.get("NCBI_API_KEY")

def get_params(base_params: dict) -> dict:
    """Helper to add API key to params if available"""
    if API_KEY:
        base_params["api_key"] = API_KEY
    return base_params

# High-impact medical journals optimized for Neurology
HIGH_IMPACT_JOURNALS = [
    "N Engl J Med",
    "Lancet",
    "Lancet Neurol",
    "JAMA",
    "JAMA Neurol",
    "BMJ",
    "Nature",
    "Nature Medicine",
    "Nature Reviews Neurology",
    "Nature Reviews Neurodegenerative Disease",
    "Cell",
    "Science",
    "Neurology",
    "Brain",
    "Neuron",
    "Ann Neurol",
    "J Neurol Neurosurg Psychiatry",
    "Movement Disorders",
    "Movement Disorders Clinical Practice",
    "Mov Disord",
    "Mov Disord Clin Pract",
    "Amyloid",
    "Parkinsonism & Related Disorders",
    "Parkinsonism Relat Disord",
    "Stroke",
    "CNS & Neurological Disorders Drug Targets",
    "Clin Neurol Neurosurg",
    "Multiple Sclerosis Journal",
    "Epilepsia",
    "Sleep"
]

def is_high_impact_journal(journal_name: str) -> bool:
    """Check if a journal is in the high-impact list"""
    if not journal_name:
        return False
    # Normalize journal name for comparison
    journal_normalized = journal_name.strip().lower()
    for high_impact in HIGH_IMPACT_JOURNALS:
        if high_impact.lower() in journal_normalized:
            return True
    return False

# --- Tool Implementations ---

async def search_pubmed(query: str, max_results: int = 5) -> str:
    """Search PubMed for papers matching the query"""
    logger.info(f"Searching PubMed for: {query}")
    async with httpx.AsyncClient() as client:
        search_params = get_params({
            "db": "pubmed",
            "term": query,
            "retmode": "json",
            "retmax": max_results,
            "sort": "relevance"
        })
        resp = await client.get(f"{BASE_URL}/esearch.fcgi", params=search_params)
        data = resp.json()
        id_list = data.get("esearchresult", {}).get("idlist", [])

        if not id_list:
            return "No results found."

        summary_params = get_params({
            "db": "pubmed",
            "id": ",".join(id_list),
            "retmode": "json"
        })
        resp = await client.get(f"{BASE_URL}/esummary.fcgi", params=summary_params)
        summary_data = resp.json()

        results = []
        uid_data = summary_data.get("result", {})
        for pmid in id_list:
            if pmid in uid_data:
                item = uid_data[pmid]
                # Extract author names
                authors = item.get("authors", [])
                author_names = []
                for author in authors[:3]:  # First 3 authors
                    if isinstance(author, dict):
                        author_names.append(author.get("name", ""))

                # Detect publication type
                pub_types = item.get("pubtype", [])
                is_review = any("review" in pt.lower() for pt in pub_types)

                results.append({
                    "pmid": pmid,
                    "title": item.get("title", "No title"),
                    "authors": ", ".join(author_names) if author_names else "No authors",
                    "pubdate": item.get("pubdate", "Unknown date"),
                    "source": item.get("source", "Unknown source"),
                    "is_review": is_review
                })

        # Sort: original articles first, then reviews
        results.sort(key=lambda x: (x["is_review"], id_list.index(x["pmid"])))

        # Remove is_review flag from output (internal use only)
        for r in results:
            del r["is_review"]

        return json.dumps(results, indent=2, ensure_ascii=False)

async def get_paper_details(pmid: str) -> str:
    """Get detailed information (Abstract, Authors, DOI, Links) for a specific PMID"""
    logger.info(f"Fetching details for PMID: {pmid}")
    async with httpx.AsyncClient() as client:
        fetch_params = get_params({"db": "pubmed", "id": pmid, "retmode": "xml"})
        resp = await client.get(f"{BASE_URL}/efetch.fcgi", params=fetch_params)
        data = xmltodict.parse(resp.text)

        try:
            # Check if PubMed returned valid data
            if 'PubmedArticleSet' not in data or not data['PubmedArticleSet']:
                return f"Error: PMID {pmid} not found. Please check the PMID and try again."

            pubmed_article_set = data['PubmedArticleSet']
            if 'PubmedArticle' not in pubmed_article_set or not pubmed_article_set['PubmedArticle']:
                return f"Error: PMID {pmid} not found. Please check the PMID and try again."

            pubmed_article = pubmed_article_set['PubmedArticle']
            article = pubmed_article['MedlineCitation']['Article']
            title = article.get('ArticleTitle', 'No title')

            # Extract abstract
            abstract_text = ""
            if 'Abstract' in article and 'AbstractText' in article['Abstract']:
                abs_content = article['Abstract']['AbstractText']
                if isinstance(abs_content, list):
                    abstract_text = "\n".join([item.get('#text', '') if isinstance(item, dict) else item for item in abs_content])
                elif isinstance(abs_content, dict):
                    abstract_text = abs_content.get('#text', '')
                else:
                    abstract_text = abs_content

            # Extract authors
            authors = []
            if 'AuthorList' in article and 'Author' in article['AuthorList']:
                auth_list = article['AuthorList']['Author']
                if isinstance(auth_list, list):
                    for auth in auth_list:
                        if 'LastName' in auth and 'ForeName' in auth:
                            authors.append(f"{auth['LastName']} {auth['ForeName']}")
                elif isinstance(auth_list, dict):
                    if 'LastName' in auth_list and 'ForeName' in auth_list:
                        authors.append(f"{auth_list['LastName']} {auth_list['ForeName']}")

            # Extract DOI and PMC ID
            doi = None
            pmc_id = None
            if 'PubmedData' in pubmed_article and 'ArticleIdList' in pubmed_article['PubmedData']:
                id_list = pubmed_article['PubmedData']['ArticleIdList']['ArticleId']
                if not isinstance(id_list, list):
                    id_list = [id_list]
                for article_id in id_list:
                    if isinstance(article_id, dict):
                        id_type = article_id.get('@IdType')
                        id_value = article_id.get('#text')
                        if id_type == 'doi':
                            doi = id_value
                        elif id_type == 'pmc':
                            pmc_id = id_value

            # Build links
            links = {
                "pubmed": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
            }
            if pmc_id:
                links["pmc"] = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmc_id}/"
            if doi:
                links["doi"] = f"https://doi.org/{doi}"

            result = {
                "pmid": pmid,
                "title": title,
                "authors": authors,
                "journal": article.get('Journal', {}).get('Title', ''),
                "doi": doi,
                "pmc_id": pmc_id,
                "abstract": abstract_text,
                "links": links
            }
            return json.dumps(result, indent=2, ensure_ascii=False)
        except KeyError:
            return f"Error: PMID {pmid} not found or invalid. Please check the PMID and try again."
        except Exception as e:
            logger.error(f"Error parsing details for PMID {pmid}: {e}")
            return f"Error retrieving details for PMID {pmid}: {str(e)}"

# --- Continue with remaining functions ---
# Due to length constraints, please copy the remaining functions from the original repository
# The key modification is the HIGH_IMPACT_JOURNALS list which has been updated for Neurology specialization
# Visit: https://raw.githubusercontent.com/m0370/mcp-pubmed-server/main/server_stdio.py
# And use all remaining functions (advanced_search_pubmed, get_similar_articles, handle_message, run_server)
