# PubMed MCP Server for Neurology

PubMedから論文を検索・取得するためのツールを提供するMCP (Model Context Protocol) サーバーです。**Neurology（神経学）領域に特化**しています。

Claude DesktopやAntigravity, Cursor などのAIエージェントが、Pubmed に直接アクセスすることを可能にし、神経学関連の研究論文を効率的に検索できます。

## 由来（Origin）

このプロジェクトは [m0370/mcp-pubmed-server](https://github.com/m0370/mcp-pubmed-server) をベースに、Neurology 領域に特化するようカスタマイズしたものです。

元のプロジェクトの Pumed MCP Server 実装に感謝します。

## 特徴 (もとのプロジェクトからのコピペをもとにしています）

- **PubMed検索**: キーワードを使用して論文を検索できます。
- **高度な絞り込み検索**: 著者名、雑誌名、発行日などで絞り込んだ検索が可能です。自然言語での指示にも対応しています。
- **関連論文の推薦**: 特定の論文（PMID）から関連論文を自動的に見つけます。高IF雑誌優先モードでは、高品質論文を優先的に表示し、不足時は自動的に他の論文も含めます。レビュー論文・メタアナリシスは自動検出して明示します。
  -- 高 IF ジャーナルのリストは、オリジナルプロジェクトでは腫瘍分野に特化されていましたが、このプロジェクトでは神経学・神経科学分野に変更しました。
- **論文詳細の取得**: 特定の論文のアブストラクト（要約）、著者、書誌情報、DOI、全文リンク（PubMed Central、DOI）などを取得できます。
- **API Key対応**: NCBI API Keyを設定することで、レート制限を緩和（最大10リクエスト/秒）できます。
- **Stdio通信**: 標準入出力（Stdio）を使用して通信するため、外部HTTPサーバーを立てる必要がなく、安全かつ高速です。
         
          - ## 前提条件
         
          - - Python 3.10 以上
            - - ライブラリ: httpx, xmltodict
             
              - ## セットアップ手順
             
              - 1. **リポジトリのクローン**:
                2.    ```
                         git clone https://github.com/tanimurajun/mcp-pubmed-neurology.git mcp-pubmed-neurology
                         cd mcp-pubmed-neurology
                         ```

                      2. **仮想環境の作成**:
                      3.    ```
                               python3 -m venv .venv
                               ```

                            3. **依存ライブラリのインストール**:
                            4.    ```
                                     ./.venv/bin/pip install -r requirements.txt
                                     ```

                                  ## 設定 (Configuration)

                              MCPクライアントの設定ファイル（例: `claude_desktop_config.json`）に以下の設定を追加してください。

                        ```json
                        {
                          "mcpServers": {
                            "pubmed": {
                              "command": "/absolute/path/to/mcp-pubmed-neurology/.venv/bin/python3",
                              "args": ["/absolute/path/to/mcp-pubmed-neurology/server_stdio.py"],
                              "env": {
                                "NCBI_API_KEY": "YOUR_API_KEY_HERE"
                              }
                            }
                          }
                        }
                        ```

                        **注意事項:**

                  - `/absolute/path/to/...` の部分は、実際にこのリポジトリを配置したディレクトリの絶対パスに書き換えてください。
                  - - **API Keyの設定（任意）**: `env` セクションに `NCBI_API_KEY` を設定すると、APIのレート制限が緩和されます（キーなし: 3回/秒 → キーあり: 10回/秒）。
                   
                    - ### VS Code + Claude Codeでの利用
                   
                    - VS Codeで「Claude Code」拡張機能を使用している場合も、同様にMCPサーバーを利用できます。
                   
                    - 1. **VS Codeの設定ファイルを開く**:
                      2.    - `Cmd + Shift + P` (macOS) または `Ctrl + Shift + P` (Windows/Linux) でコマンドパレットを開く
                            -    - 「Preferences: Open User Settings (JSON)」を選択
                             
                                 - 2. **設定を追加**: `settings.json` に以下を追加してください。
                                  
                                   3.    ```json
                                            {
                                              "claude.mcpServers": {
                                                "pubmed": {
                                                  "command": "/absolute/path/to/mcp-pubmed-neurology/.venv/bin/python3",
                                                  "args": ["/absolute/path/to/mcp-pubmed-neurology/server_stdio.py"],
                                                  "env": {
                                                    "NCBI_API_KEY": "YOUR_API_KEY_HERE"
                                                  }
                                                }
                                              }
                                            }
                                            ```

                                         3. **VS Codeを再起動**: 設定を反映させるため、VS Codeを再起動してください。
                                     
                                         4. **注意**: 拡張機能によって設定キーが異なる場合があります（`claude.mcpServers` または `mcpServers` など）。詳細は各拡張機能のドキュメントをご確認ください。
                                     
                                         5. ## 使い方
                                     
                                         6. 設定完了後、AIに対して以下のように話しかけることで機能を利用できます。
                                     
                                         7. ### 基本的な検索
                                     
                                         8. 「HER2陽性胃癌の治療に関する最新の論文を検索して」
                                     
                                         9. ### 高度な絞り込み検索
                                     
                                         10. - 「Smithさんの2023年の胃癌に関する論文を探して」
                                             - - 「NEJMに掲載された免疫療法の論文を検索して」
                                               - - 「2020年から2024年の間に発表されたPD-1阻害薬の論文を見つけて」
                                                
                                                 - ### 論文詳細の取得
                                                
                                                 - - 「PMID 12345678 のアブストラクトを取得して要約して」
                                                   - - 「この論文の全文リンクを教えて」
                                                    
                                                     - ### 関連論文の推薦
                                                    
                                                     - - 「PMID 39282917 に関連する論文を探して」
                                                       - - 「この論文に関連する高IF雑誌の論文だけ教えて」
                                                         - - 「NEJM、Lancet、Natureなどの一流雑誌に掲載された関連論文を見つけて」
                                                          
                                                           - ## 仕組み
                                                          
                                                           - - **MCPプロトコル**: JSON-RPC 2.0 プロトコルを使用し、標準入力（stdin）でリクエストを受け取り、標準出力（stdout）でレスポンスを返します。
                                                             - - **PubMed API**: 内部で NCBI E-utilities API (esearch, efetch) を呼び出し、データを取得しています。
                                                               - - **ローカル実行**: HTTPサーバーではなく、MCPクライアントのサブプロセスとしてローカルで動作するため、セキュリティリスクが低く、レスポンスも高速です。
                                                                
                                                                 - ## ファイル構成
                                                                
                                                                 - - **server_stdio.py**: メインのサーバー実装（Stdio版）。通常はこちらを使用します。
                                                                   - - **requirements.txt**: 必要なPythonライブラリ一覧。
                                                                     - - **server.py**: (旧版) mcp SDKを使用した実装例。環境によっては動作しない場合があります。

                                                                     ## ライセンス

                                                                     MIT - 元のプロジェクト m0370/mcp-pubmed-server に敬意を払います。
