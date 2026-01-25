# PubMed MCP Server for Neurology

[English](README.md) | [日本語](README.ja.md)

MCP server for searching PubMed from AI agents (Claude Desktop, Cursor, etc.). Optimized for neurology/neuroscience research.

## Origin

Based on [m0370/mcp-pubmed-server](https://github.com/m0370/mcp-pubmed-server). We replaced the high-impact journal list with neurology-focused journals.

## Features

- Keyword search with automatic prioritization of original research
- Filter by author, journal, publication date
- Find similar papers using PubMed's built-in algorithm
- Retrieve abstracts, DOIs, and full-text links
- Optional high-impact journal filter (neurology-specific)
- NCBI API key support (3 req/s → 10 req/s)

## Requirements

- Python 3.10+
- Claude Desktop or other MCP-compatible client
- NCBI API key (optional, recommended)

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/mcp-pubmed-neurology.git
cd mcp-pubmed-neurology
pip install -r requirements.txt
```

Get NCBI API key (optional): https://www.ncbi.nlm.nih.gov/account/

### Claude Desktop Configuration

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "pubmed": {
      "command": "python",
      "args": ["-m", "mcp_pubmed_server"],
      "cwd": "/absolute/path/to/mcp-pubmed-neurology",
      "env": {
        "NCBI_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

Restart Claude Desktop. Check for 🔨 icon.

## Usage

```
Search PubMed for Parkinson's disease papers
→ Returns PMID, title, authors, date, journal

Find papers by Wichmann T about basal ganglia from 2020-2024
→ Uses author and date filters

Get abstract and DOI for PMID 26409114
→ Returns full details including links

Find similar papers to PMID 31216379 in high-impact journals
→ Uses PubMed's similarity algorithm with journal filter
```

## High-Impact Neurology Journals

When using `high_impact_only` filter:

- **General Medical**: NEJM, Lancet, JAMA, BMJ, Nature Medicine  
- **Clinical Neurology**: Lancet Neurology, JAMA Neurology, Neurology, Brain, Annals of Neurology, J Neurol Neurosurg Psychiatry  
- **Neuroscience**: Nature, Science, Cell, Neuron, Nature Reviews Neurology  
- **Movement Disorders**: Movement Disorders, Movement Disorders Clinical Practice, Parkinsonism & Related Disorders, npj Parkinson's Disease, Journal of Parkinson's Disease  
- **Specialized**: Stroke, Multiple Sclerosis Journal, Epilepsia, Sleep, Amyloid

## Changes from Original

- Journal list replaced with neurology/neuroscience focus
- Search prioritizes original research over reviews
- Maintained all core functionality

## Troubleshooting

**MCP not appearing**: Check JSON syntax, use absolute paths, restart Claude  
**Rate limits**: Add API key, reduce frequency  
**No results**: Try broader terms, remove filters

## Authors

**Jun Tanimura** - Neurology adaptation  
**m0370** - Original implementation

## Acknowledgments

Original project: [m0370/mcp-pubmed-server](https://github.com/m0370/mcp-pubmed-server)

## License

MIT License. See [LICENSE](LICENSE) for details.
