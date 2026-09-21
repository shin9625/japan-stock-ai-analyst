"""
収益化対応レスポンシブWebサイト生成モジュール
生成されたレポートを投資リサーチハウス風の洗練されたHTMLに変換し、
広告枠（Google AdSense等）および金融アフィリエイト導線を組み込みます。
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, List
import markdown

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} | 日本株AIアナリスト・エクイティリサーチ</title>
    <meta name="description" content="日経平均・TOPIX・為替の動向をAIシニアアナリストがテクニカル分析とクオンツ指標で徹底解説。明日以降のシナリオ予測付きデイリーレポート。">
    <!-- Google Fonts & Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['"Noto Sans JP"', 'sans-serif'],
                        mono: ['"JetBrains Mono"', 'monospace'],
                    },
                    colors: {
                        brand: {
                            50: '#f0f7ff',
                            100: '#e0effe',
                            600: '#0284c7',
                            700: '#0369a1',
                            900: '#0c4a6e',
                        },
                        market: {
                            up: '#ef4444',     /* 日本株の赤は上昇 */
                            down: '#10b981',   /* 日本株の緑は下落 */
                        }
                    }
                }
            }
        }
    </script>
    <style>
        .report-content h2 {
            font-size: 1.35rem;
            font-weight: 700;
            color: #0f172a;
            border-left: 4px solid #0284c7;
            padding-left: 0.75rem;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }
        .report-content h3 {
            font-size: 1.15rem;
            font-weight: 600;
            color: #1e293b;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
        }
        .report-content ul {
            list-style-type: disc;
            padding-left: 1.5rem;
            margin-bottom: 1rem;
            color: #334155;
            line-height: 1.75;
        }
        .report-content p {
            margin-bottom: 1rem;
            color: #334155;
            line-height: 1.8;
        }
        .report-content strong {
            color: #0f172a;
        }
    </style>
</head>
<body class="bg-slate-50 text-slate-800 font-sans antialiased">

    <!-- ヘッダーナビゲーション -->
    <header class="bg-slate-900 text-white border-b border-slate-800 sticky top-0 z-50">
        <div class="max-w-5xl mx-auto px-4 py-3.5 flex justify-between items-center">
            <div class="flex items-center space-x-3">
                <div class="w-8 h-8 rounded-lg bg-sky-500 flex items-center justify-center font-bold text-white shadow-md">
                    AI
                </div>
                <div>
                    <a href="{{ base_path }}index.html" class="text-lg font-bold tracking-tight hover:text-sky-400 transition">JAPAN STOCK RESEARCH</a>
                    <p class="text-xs text-slate-400 hidden sm:block">AIエクイティリサーチ＆テクニカル分析レポート</p>
                </div>
            </div>
            <div class="flex items-center space-x-4 text-sm">
                <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-950 text-emerald-300 border border-emerald-800">
                    ● Daily Live
                </span>
            </div>
        </div>
    </header>

    <!-- メインコンテンツ -->
    <main class="max-w-5xl mx-auto px-4 py-8">

        <!-- 広告枠 1: ヘッダー下 (Google AdSense等) -->
        <div class="mb-8 p-4 bg-white border border-dashed border-slate-300 rounded-xl text-center text-xs text-slate-400 shadow-sm">
            <div class="font-mono text-slate-400">[ スポンサーリンク / 広告枠 728x90 ]</div>
            <!-- Google AdSense コードをここに挿入 -->
            <p class="mt-1 text-slate-400">※広告収入はサーバー運営費に充当されます</p>
        </div>

        <!-- タイトル＆メタ情報 -->
        <div class="bg-white rounded-2xl p-6 sm:p-8 shadow-sm border border-slate-200/80 mb-8">
            <div class="flex flex-wrap items-center gap-2 mb-3">
                <span class="px-3 py-1 text-xs font-semibold text-sky-700 bg-sky-50 rounded-full border border-sky-200">
                    エクイティ・リサーチ
                </span>
                <span class="text-xs text-slate-500 font-mono">
                    発行日時: {{ report_date }} (東証大引け後速報)
                </span>
            </div>
            <h1 class="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight leading-snug">
                {{ title }}
            </h1>
            <p class="mt-3 text-sm text-slate-600 leading-relaxed">
                本日の日本株式市場（日経平均・TOPIX・ドル円為替・主要銘柄）の価格動向をクオンツ指標とテクニカル分析で徹底解説。明日以降の想定レンジと戦略シナリオを提示します。
            </p>
        </div>

        <!-- 主要マーケット指標カードグリッド -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
            {% for name, item in indices.items() %}
            <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200">
                <div class="text-xs font-semibold text-slate-500 truncate">{{ name }}</div>
                <div class="text-lg sm:text-xl font-bold font-mono mt-1 text-slate-900">
                    {{ "{:,.2f}".format(item.current_price) }}
                </div>
                <div class="text-xs font-mono font-medium mt-1 {{ 'text-red-600' if item.price_change >= 0 else 'text-emerald-600' }}">
                    {{ "{:+,.2f}".format(item.price_change) }} ({{ "{:+.2f}".format(item.price_change_pct) }}%)
                </div>
                {% if item.rsi14 %}
                <div class="text-[10px] text-slate-400 font-mono mt-2 pt-2 border-t border-slate-100">
                    RSI(14): <span class="font-semibold text-slate-600">{{ item.rsi14 }}</span>
                </div>
                {% endif %}
            </div>
            {% endfor %}
            {% for name, item in forex.items() %}
            <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200">
                <div class="text-xs font-semibold text-slate-500 truncate">{{ name }}</div>
                <div class="text-lg sm:text-xl font-bold font-mono mt-1 text-slate-900">
                    {{ "{:,.2f}".format(item.current_price) }}
                </div>
                <div class="text-xs font-mono font-medium mt-1 {{ 'text-red-600' if item.price_change >= 0 else 'text-emerald-600' }}">
                    {{ "{:+,.2f}".format(item.price_change) }} ({{ "{:+.2f}".format(item.price_change_pct) }}%)
                </div>
            </div>
            {% endfor %}
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <!-- レポート本文 (左2カラム) -->
            <div class="lg:col-span-2">
                <article class="bg-white rounded-2xl p-6 sm:p-8 shadow-sm border border-slate-200/80 report-content">
                    {{ report_html | safe }}
                </article>

                <!-- 金融アフィリエイト枠 (記事直下・最も成約率の高い位置) -->
                <div class="mt-8 bg-gradient-to-br from-sky-900 to-indigo-950 text-white rounded-2xl p-6 sm:p-7 shadow-lg">
                    <div class="flex items-center space-x-2 text-sky-400 text-xs font-bold tracking-wider uppercase mb-2">
                        <span>PR</span>
                        <span>•</span>
                        <span>おすすめ取引環境</span>
                    </div>
                    <h3 class="text-lg sm:text-xl font-bold text-white mb-2">
                        テクニカル分析＆日本株取引におすすめのネット証券
                    </h3>
                    <p class="text-xs text-sky-200 mb-5 leading-relaxed">
                        本レポートで解説した移動平均線・RSI・ボリンジャーバンドなどの詳細チャートツールが無料で使える主要証券会社です。
                    </p>
                    <div class="grid sm:grid-cols-2 gap-4">
                        <div class="bg-white/10 backdrop-blur-sm border border-white/15 rounded-xl p-4 flex flex-col justify-between hover:bg-white/15 transition">
                            <div>
                                <div class="font-bold text-sm text-white">SBI証券</div>
                                <p class="text-[11px] text-slate-300 mt-1">日本株売買手数料が無料。プロ御用達の高機能PC/スマホツール搭載。</p>
                            </div>
                            <a href="#affiliate-sbi" class="mt-3 inline-block text-center py-2 px-3 bg-sky-500 hover:bg-sky-400 text-white text-xs font-bold rounded-lg transition shadow-md">
                                無料で口座開設する →
                            </a>
                        </div>
                        <div class="bg-white/10 backdrop-blur-sm border border-white/15 rounded-xl p-4 flex flex-col justify-between hover:bg-white/15 transition">
                            <div>
                                <div class="font-bold text-sm text-white">楽天証券</div>
                                <p class="text-[11px] text-slate-300 mt-1">「マーケットスピードII」など高精度なテクニカル分析環境が充実。</p>
                            </div>
                            <a href="#affiliate-rakuten" class="mt-3 inline-block text-center py-2 px-3 bg-red-600 hover:bg-red-500 text-white text-xs font-bold rounded-lg transition shadow-md">
                                詳細を見る →
                            </a>
                        </div>
                    </div>
                </div>

                <!-- 広告枠 2: 記事フッター下 (レコメンド広告) -->
                <div class="mt-8 p-4 bg-white border border-dashed border-slate-300 rounded-xl text-center text-xs text-slate-400 shadow-sm">
                    <div class="font-mono text-slate-400">[ スポンサーリンク / 広告枠 300x250 x2 ]</div>
                </div>
            </div>

            <!-- サイドバー (右1カラム) -->
            <div class="space-y-6">
                <!-- 過去のレポート・アーカイブ -->
                <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-200">
                    <h3 class="text-sm font-bold text-slate-900 mb-4 pb-2 border-b border-slate-100 flex items-center justify-between">
                        <span>過去のレポート</span>
                        <span class="text-xs font-normal text-slate-400 font-mono">Archive</span>
                    </h3>
                    <ul class="space-y-2.5 text-xs text-slate-600">
                        {% for arch in archives %}
                        <li>
                            <a href="{{ base_path }}{{ arch.path }}" class="hover:text-sky-600 transition flex items-center justify-between group">
                                <span class="group-hover:translate-x-0.5 transition-transform">{{ arch.date }} レポート</span>
                                <span class="font-mono text-slate-400 text-[10px]">閲覧 →</span>
                            </a>
                        </li>
                        {% else %}
                        <li class="text-slate-400 text-xs">過去レポート準備中</li>
                        {% endfor %}
                    </ul>
                </div>

                <!-- 投資本・教材アフィリエイト枠 -->
                <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-200">
                    <div class="text-[10px] text-slate-400 font-bold uppercase tracking-wider mb-2">PR • 必読テクニカル書籍</div>
                    <h4 class="text-sm font-bold text-slate-900 mb-2">テクニカル分析の基礎から応用を学ぶ</h4>
                    <p class="text-xs text-slate-500 mb-4 leading-relaxed">
                        移動平均線やオシレーター分析を体系的に学ぶための定番おすすめ書籍。
                    </p>
                    <a href="#affiliate-book" class="block text-center py-2 px-3 bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold rounded-lg transition">
                        おすすめ書籍一覧をチェック
                    </a>
                </div>

                <!-- 免責事項 -->
                <div class="bg-slate-100/80 rounded-xl p-4 text-[11px] text-slate-500 leading-relaxed border border-slate-200">
                    <div class="font-bold text-slate-700 mb-1">【重要免責事項】</div>
                    本レポートは、AIアナリストによる市場分析および情報提供のみを目的として作成されたものであり、特定の有価証券の売買や投資勧誘を推奨するものではありません。記載されたデータや見通しの正確性を保証するものではなく、最終的な投資判断はご自身の責任において行われますようお願いいたします。
                </div>
            </div>
        </div>
    </main>

    <!-- フッター -->
    <footer class="bg-white border-t border-slate-200 mt-16 py-8 text-center text-xs text-slate-400">
        <div class="max-w-5xl mx-auto px-4">
            <p>© {{ year }} JAPAN STOCK RESEARCH. All Rights Reserved.</p>
            <p class="mt-1 text-[11px] text-slate-400">Powered by Google Gemini & Python Financial Analytics</p>
        </div>
    </footer>

</body>
</html>
"""


def build_html_report(
    market_data: Dict[str, Any],
    report_markdown: str,
    output_dir: str = "web_output",
    is_archive: bool = False
) -> str:
    """MarkdownレポートからHTMLページを生成して保存する"""
    from jinja2 import Template

    os.makedirs(output_dir, exist_ok=True)
    archive_dir = os.path.join(output_dir, "archive")
    os.makedirs(archive_dir, exist_ok=True)

    # Markdown -> HTML
    html_body = markdown.markdown(report_markdown, extensions=["tables", "fenced_code"])

    date_str = market_data.get("date_str", datetime.now().strftime("%Y年%m月%d日"))
    raw_date = datetime.now().strftime("%Y-%m-%d")
    title = f"{date_str} 日本株デイリー・エクイティリサーチレポート"

    # 既存アーカイブのリスト取得
    archives = []
    if os.path.exists(archive_dir):
        files = sorted(os.listdir(archive_dir), reverse=True)
        for f in files:
            if f.endswith(".html"):
                d = f.replace(".html", "")
                archives.append({"date": d, "path": f"archive/{f}"})

    template = Template(HTML_TEMPLATE)
    rendered_html = template.render(
        title=title,
        report_date=date_str,
        report_html=html_body,
        indices=market_data.get("indices", {}),
        forex=market_data.get("forex", {}),
        archives=archives[:10],
        base_path="../" if is_archive else "",
        year=datetime.now().year
    )

    # index.html として保存 (ルート)
    index_path = os.path.join(output_dir, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)

    # archive/YYYY-MM-DD.html として保存
    archive_path = os.path.join(archive_dir, f"{raw_date}.html")
    with open(archive_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)

    print(f"Webレポートが正常に生成されました:\n  - {index_path}\n  - {archive_path}")
    return index_path


if __name__ == "__main__":
    from collector import collect_market_overview
    from analyst import generate_research_report

    print("HTMLビルドテスト開始...")
    data = collect_market_overview()
    rep = generate_research_report(data)
    build_html_report(data, rep)
