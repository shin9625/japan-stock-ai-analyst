"""
スマホ通知モジュール (Discord Webhook)
大引け後の市況サマリーおよび新着レポートのURLをスマホに即座に通知します。
"""

import os
import requests
from typing import Dict, Any, Optional


def send_discord_notification(
    market_data: Dict[str, Any],
    report_markdown: str,
    web_url: Optional[str] = None
) -> bool:
    """Discord Webhook へレポートの要約とWebサイトURLを通知する"""
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("Notice: DISCORD_WEBHOOK_URL が設定されていないため、スマホ通知はスキップされました。")
        return False

    date_str = market_data.get("date_str", "本日")
    nikkei = market_data.get("indices", {}).get("日経平均", {})
    usd_jpy = market_data.get("forex", {}).get("ドル/円 (USD/JPY)", {})

    price = nikkei.get("current_price", 0)
    change = nikkei.get("price_change", 0)
    change_pct = nikkei.get("price_change_pct", 0)
    fx_price = usd_jpy.get("current_price", 0)

    # レポート冒頭のサマリーを抽出 (約200文字)
    summary_lines = []
    for line in report_markdown.split("\n"):
        if line.startswith("- ") or line.startswith("  - "):
            summary_lines.append(line.replace("**", ""))
            if len(summary_lines) >= 4:
                break
    summary_text = "\n".join(summary_lines) if summary_lines else "大引け後の市況レポートが発行されました。"

    embed = {
        "title": f"📈 【{date_str}】日本株AIリサーチレポート発行",
        "description": f"日経平均: **{price:,.2f} 円** ({change:+,.2f} / {change_pct:+.2f}%)\n為替: **1ドル = {fx_price:.2f} 円**\n\n**【本日のハイライト】**\n{summary_text}",
        "color": 0xef4444 if change >= 0 else 0x10b981,
        "fields": [
            {
                "name": "🌐 詳細レポート（Web版）",
                "value": f"[こちらからレポート全文を読む]({web_url or 'https://your-domain.github.io/index.html'})",
                "inline": False
            }
        ],
        "footer": {
            "text": "JAPAN STOCK AI ANALYST • 自動配信システム"
        }
    }

    payload = {
        "content": f"🔔 **【大引け速報】本日の日本株AIアナリストレポートが完成しました！**",
        "embeds": [embed]
    }

    try:
        res = requests.post(webhook_url, json=payload, timeout=10)
        if res.status_code in [200, 204]:
            print("Discordへ通知を正常に送信しました！")
            return True
        else:
            print(f"Discord通知送信失敗 (Status {res.status_code}): {res.text}")
            return False
    except Exception as e:
        print(f"Discord通知送信エラー: {e}")
        return False


if __name__ == "__main__":
    from collector import collect_market_overview
    from analyst import generate_research_report

    print("通知テスト中...")
    data = collect_market_overview()
    rep = generate_research_report(data)
    send_discord_notification(data, rep)
