"""
日本株AIアナリスト・自動運用システム メイン実行スクリプト
1. マーケットデータ収集 (collector)
2. Geminiプロフェッショナルリサーチレポート生成 (analyst)
3. 収益化対応HTML生成 (builder)
4. スマホ通知配信 (notifier)
"""

import os
import sys
from datetime import datetime
from collector import collect_market_overview
from analyst import generate_research_report
from builder import build_html_report
from notifier import send_discord_notification


def run_pipeline(output_dir: str = "docs") -> None:
    print("=" * 60)
    print("🚀 日本株AIアナリスト パイプライン実行開始")
    print(f"実行時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 1. データ収集
    print("\n[1/4] 日本株・主要指標のマーケットデータを取得中...")
    market_data = collect_market_overview()
    print("  ✓ データ取得完了")

    # 2. レポート生成
    print("\n[2/4] Gemini AIアナリストによる詳細リサーチレポートを執筆中...")
    report_md = generate_research_report(market_data)
    print("  ✓ レポート生成完了")

    # 3. Webサイトビルド (GitHub Pages用ディレクトリ: docs)
    print(f"\n[3/4] 収益化対応HTMLレポートをビルド中 (出力先: {output_dir})...")
    index_file = build_html_report(market_data, report_md, output_dir=output_dir)
    print(f"  ✓ HTMLビルド完了: {index_file}")

    # 4. スマホ通知
    print("\n[4/4] スマホへの速報通知を配信中...")
    site_url = os.environ.get("SITE_URL")
    send_discord_notification(market_data, report_md, web_url=site_url)

    print("\n" + "=" * 60)
    print("🎉 全工程が正常に完了しました！")
    print("=" * 60)


if __name__ == "__main__":
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "docs"
    run_pipeline(output_dir=out_dir)
