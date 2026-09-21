# 📈 日本株AIアナリスト・エクイティリサーチ自動運用システム
> **完全無料・サーバー代0円・古いPCでもブラウザから運用可能**
> 日経平均・TOPIX・為替のデータを毎営業日自動収集し、Google Gemini がプロ仕様の株式リサーチレポートを執筆。広告・アフィリエイト枠付きのWebサイト（GitHub Pages）へ自動公開＆スマホ通知を行うシステムです。

---

## 🌟 主な機能と特徴

1. **完全無料・APIキー不要のデータ取得**
   - `yfinance` を使い、日経平均 (`^N225`)、TOPIX、ドル円、主要個別株の株価およびテクニカル指標（RSI、MACD、ボリンジャーバンド、移動平均線）を自動計算。
2. **Geminiによるプロ仕様リサーチレポート**
   - 外資系証券・大手投資銀行のシニアアナリストとして、市況要因、詳細テクニカル分析、明日以降の「メインシナリオ（60%）」「リスクシナリオ（40%）」を論理的に執筆。
3. **収益化対応レスポンシブWebサイト自動公開**
   - Google AdSense広告枠、ネット証券口座（SBI証券、楽天証券等）のアフィリエイト紹介枠、免責事項を自動配置した美しいWebレポートをGitHub Pagesで0円公開。
4. **平日15:45の完全自動更新 (GitHub Actions)**
   - 東証大引け後に自動起動し、データ取得 → レポート生成 → HTMLビルド → Web公開 → スマホ（Discord）速報通知まで手放しで自動完結。
5. **スマホGemini対応 (MCPサーバー)**
   - スマホのGeminiアプリから「本日の日経平均の要約を教えて」「トヨタ(7203)のテクニカル分析をして」と対話可能。

---

## 🚀 古いPCから始めるセットアップ手順（ブラウザだけで完結）

手元のパソコンに何かをインストールする必要はありません。GitHubの無料クラウド環境（**GitHub Codespaces**）を使ってブラウザだけで設定できます。

### ステップ 1: GitHubリポジトリの作成
1. [GitHub](https://github.com/) にログインし、新しいリポジトリ（例: `japan-stock-ai-analyst`）を作成します。
2. 本プロジェクトのファイル一式（`collector.py`, `analyst.py`, `builder.py`, `main.py`, `.github/` など）をリポジトリに配置します。
3. リポジトリ画面の **「Code」ボタン ＞「Codespaces」タブ ＞「Create codespace on main」** をクリックすると、ブラウザ上で最新の開発環境（VS Code）が起動します。

### ステップ 2: 無料のAPIキー・通知設定（GitHub Secrets）
GitHubリポジトリの **Settings ＞ Secrets and variables ＞ Actions ＞ New repository secret** から、以下を登録します。

| シークレット名 | 説明 | 取得先 |
| :--- | :--- | :--- |
| `GEMINI_API_KEY` | Geminiの無料APIキー | [Google AI Studio](https://aistudio.google.com/) から無料で即時発行 |
| `DISCORD_WEBHOOK_URL` | スマホ通知用URL（任意） | Discordのチャンネル設定 ＞ 連携サービス ＞ ウェブフック作成 |

※ `GEMINI_API_KEY` が未設定の場合でも、自動でサンプル高品質モックレポートが生成されるため、安全に動作確認できます。

### ステップ 3: GitHub Pages（無料Web公開）の有効化
1. リポジトリの **Settings ＞ Pages** を開きます。
2. **Build and deployment** の **Source** で **「Deploy from a branch」** を選択します。
3. **Branch** で `main`（または `master`）、フォルダを **/docs** に設定して **Save** をクリックします。
4. 数分後、あなた専用のWebサイトURL（`https://<ユーザー名>.github.io/<リポジトリ名>/`）が発行され、世界中に公開されます！

---

## 💰 収益化（マネタイズ）のカスタマイズ

生成されるWebレポート（`builder.py` 内のHTMLテンプレート）には、以下の収益化枠があらかじめ組み込まれています。

1. **Google AdSense（広告収入）**:
   - `builder.py` 内の `[ スポンサーリンク / 広告枠 ]` 部分に、AdSense審査通過後に発行される広告コード（`<ins class="adsbygoogle" ...></ins>`）を貼り付けます。
2. **ネット証券アフィリエイト（高単価成果報酬）**:
   - [A8.net](https://www.a8.net/) や [もしもアフィリエイト](https://af.moshimo.com/) などの無料ASPに登録し、「SBI証券」や「楽天証券」の提携リンクを取得します。
   - `builder.py` 内の `#affiliate-sbi` や `#affiliate-rakuten` をご自身のアフィリエイトリンクに差し替えるだけで、口座開設ごとに数千円〜1万円以上の報酬が発生します。
3. **投資書籍・ツール紹介**:
   - Amazonアソシエイト等のリンクをサイドバーに掲載できます。

---

## 📱 スマホGeminiから呼び出す (MCP連携)

本システムには、スマホのGeminiから個別銘柄のテクニカル分析や本日の市況を聞くことができる MCP サーバー（`mcp_server.py`）が含まれています。

```bash
# Codespaces または Render 等で起動
python mcp_server.py sse
```
発行された公開URLを Web版Gemini の「接続済みアプリ (Connected Apps)」に登録することで、スマホのGeminiアプリからも以下のように対話できます：
* 「本日の日経平均の要約を教えて」
* 「7203（トヨタ）のテクニカル分析をして」
* 「明日以降のメインシナリオとリスクシナリオは？」

---

## 🧪 手動テスト・動作確認

ブラウザの Codespaces ターミナルで以下を実行すると、今すぐ本日のデータ取得・レポート生成・Webページ構築をテストできます。

```bash
# 依存パッケージのインストール
pip install -r requirements.txt

# パイプライン実行（docsフォルダにWebページを出力）
python main.py docs
```
実行後、`docs/index.html` を右クリックして「Open with Live Server」またはプレビューで確認できます。

---

## ⚖️ 免責事項
本システムで生成されるレポートは情報提供のみを目的としており、投資勧誘や個別銘柄の売買推奨を行うものではありません。投資判断は必ずご自身の責任において行われますようお願いいたします。
