# PubMed MCP Server for Neurology

PubMedから論文を検索・取得するための **Neurology（神経学）領域に特化した** MCP (Model Context Protocol) サーバーです。Claude Desktop、Cursor、Antigravity などのAIエージェントが、PubMedデータベースに直接アクセスでき、神経学関連の研究論文を効率的に検索できます。

## 由来

このプロジェクトは [m0370/mcp-pubmed-server](https://github.com/m0370/mcp-pubmed-server) をベースに、Neurology 領域に特化するようカスタマイズしたものです。元のプロジェクトの実装に感謝します。

## 特徴

- **PubMed検索**: キーワードを使用して論文を検索
- **高度な絞り込み検索**: 著者名、雑誌名、発行日などで絞り込み
- **関連論文の推薦**: 特定の論文から関連論文を自動検出
- **論文詳細の取得**: アブストラクト、著者、DOI、全文リンクなど
- **API Key対応**: NCBI API Keyでレート制限を緩和（3回/秒 → 10回/秒）
- **Stdio通信**: 安全で高速なローカル実行
- **Neurology最適化**: 神経学領域の高IF雑誌に対応
           
## セットアップと使い方

- 詳しい設定方法、セットアップ手順、使用例については、[元のプロジェクト](https://github.com/m0370/mcp-pubmed-server) をご覧ください。
- このプロジェクトは元のコードをベースにしているため、基本的な使い方は同じです。主な違いは、ジャーナルリストが神経学分野向けにカスタマイズされている点です。

## 主な変更点
           
- 高 IF ジャーナルリストを神経学・神経科学分野に変更しました
- Similarity Search の Description を、より明示的に Pubmed のビルトインアルゴリズムを使用するように書き換えました
- 元のプロジェクトの基本機能はそのまま継承しました
               
## ライセンス
               
- MIT - 元のプロジェクト [m0370/mcp-pubmed-server](https://github.com/m0370/mcp-pubmed-server) に敬意を敬意を表します。
