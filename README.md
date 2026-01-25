# PubMed MCP Server for Neurology

[English](README.md) | [日本語](README.ja.md)

AIエージェント（Claude Desktop、Cursorなど）から、神経学・神経科学研究を中心に PubMed を検索するためのMCPサーバーです。

## 由来

[m0370/mcp-pubmed-server](https://github.com/m0370/mcp-pubmed-server) をベースに、高インパクトジャーナルリストを神経学分野向けに変更したものです。

## 特徴

- キーワード検索（原著論文を優先する自動ソート）
- 著者・雑誌・発行日によるフィルター
- PubMed組み込みアルゴリズムによる類似論文検索
- アブストラクト、DOI、全文リンクの取得
- 高IF雑誌フィルター（神経学特化）
- NCBI APIキー対応（3回/秒 → 10回/秒）

## 必要な環境

- Python 3.10以降
- Claude Desktop または他のMCP対応クライアント
- NCBI APIキー（任意、推奨）

## セットアップ

```bash
git clone https://github.com/YOUR_USERNAME/mcp-pubmed-neurology.git
cd mcp-pubmed-neurology
pip install -r requirements.txt
```

NCBI APIキー取得（任意）: https://www.ncbi.nlm.nih.gov/account/

### Claude Desktop設定

`~/Library/Application Support/Claude/claude_desktop_config.json`（macOS）または `%APPDATA%\Claude\claude_desktop_config.json`（Windows）を編集：

```json
{
  "mcpServers": {
    "pubmed": {
      "command": "python",
      "args": ["-m", "mcp_pubmed_server"],
      "cwd": "/絶対パス/to/mcp-pubmed-neurology",
      "env": {
        "NCBI_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

Claude Desktopを再起動。🔨アイコンを確認。

## 使い方

```
パーキンソン病の論文をPubMedで検索
→ PMID、タイトル、著者、日付、雑誌を返す

Wichmann Tによる基底核に関する2020-2024年の論文を検索
→ 著者と日付フィルターを使用

PMID 26409114のアブストラクトとDOIを取得
→ リンクを含む詳細情報を返す

PMID 31216379の類似論文を高IF雑誌で検索
→ PubMed類似度アルゴリズムと雑誌フィルターを使用
```

## 高インパクト神経学雑誌

`high_impact_only`フィルター使用時：

**総合誌**: NEJM, Lancet, JAMA, BMJ, Nature Medicine
**臨床神経**: Lancet Neurology, JAMA Neurology, Neurology, Brain, Annals of Neurology, J Neurol Neurosurg Psychiatry  
**神経科学**: Nature, Science, Cell, Neuron, Nature Reviews Neurology  
**運動異常症**: Movement Disorders, Movement Disorders Clinical Practice, Parkinsonism & Related Disorders, Journal of Parkinson's Disease, npj Parkinson's Disease
**専門誌**: Stroke, Multiple Sclerosis Journal, Epilepsia, Sleep, Amyloid

## 変更点

- ジャーナルリストを神経学・神経科学向けに変更
- すべての基本機能を維持

## トラブルシューティング

**MCPが表示されない**: JSON構文確認、絶対パス使用、Claudeを再起動  
**レート制限**: APIキー追加、頻度を下げる  
**結果が出ない**: より広い検索語、フィルター解除

## 作者

**Jun Tanimura** - 神経学向け改変  
**m0370** - 元実装

## 謝辞

元のプロジェクト [m0370/mcp-pubmed-server](https://github.com/m0370/mcp-pubmed-server) に敬意を敬意を表します。

## ライセンス

MIT License - 詳細は[LICENSE](LICENSE)を参照。
