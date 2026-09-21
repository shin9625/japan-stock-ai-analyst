"""
スマホGemini連携用 MCP (Model Context Protocol) サーバー
スマホのGeminiアプリやClaudeから呼び出し可能なツールを提供します。
- get_market_summary: 本日の日経平均・為替・市況ダイジェストの取得
- analyze_stock: 個別銘柄（例: 7203 トヨタ）の即時テクニカル分析
- get_forecast_scenarios: 明日以降の相場シナリオ予測
"""

import os
import json
from typing import Dict, Any, Optional
from collector import fetch_symbol_data, collect_market_overview
from analyst import generate_research_report

try:
    from mcp.server.fastmcp import FastMCP
    mcp_available = True
except ImportError:
    mcp_available = False

# FastMCPサーバー初期化
if mcp_available:
    mcp = FastMCP("JapanStockAIAnalyst")

    @mcp.tool()
    def get_market_summary() -> str:
        """本日の日経平均・TOPIX・ドル円為替の最新値およびAIアナリストの要約を取得します。"""
        data = collect_market_overview()
        report = generate_research_report(data)
        # エグゼクティブサマリー部分を返す
        lines = []
        capture = False
        for line in report.split("\n"):
            if "## 1. エグゼクティブ・サマリー" in line:
                capture = True
            elif line.startswith("## 2."):
                break
            if capture:
                lines.append(line)
        return "\n".join(lines) if lines else report[:500]

    @mcp.tool()
    def analyze_stock(ticker: str) -> str:
        """
        指定した日本株銘柄（銘柄コード、例: 7203.T または 7203）のテクニカル指標（RSI、移動平均線、MACD）を分析します。
        """
        symbol = ticker if ticker.endswith(".T") else f"{ticker}.T"
        tech = fetch_symbol_data(symbol)
        if not tech:
            return f"銘柄コード {ticker} のデータを取得できませんでした。コードを確認してください。"

        cur = tech.get("current_price")
        diff = tech.get("price_change")
        diff_pct = tech.get("price_change_pct")
        sma25 = tech.get("sma25")
        bias = tech.get("bias_sma25_pct")
        rsi = tech.get("rsi14")
        macd = tech.get("macd")

        return f"""【{ticker} テクニカル分析結果】
■ 現在値: {cur:,.2f} 円 (前日比 {diff:+,.2f} 円 / {diff_pct:+.2f}%)
■ 25日移動平均線: {sma25:,.2f} 円 (乖離率: {bias:+.2f}%)
■ RSI(14): {rsi:.1f} ({'買われすぎ警戒' if rsi and rsi > 70 else '売られすぎ底値圏' if rsi and rsi < 30 else '中立ゾーン'})
■ MACD: {macd:.2f}
※本指標は参考値であり、投資判断は自己責任で行ってください。"""

    @mcp.tool()
    def get_forecast_scenarios() -> str:
        """明日以降の日経平均のメインシナリオ（確率60%）とリスクシナリオ（確率40%）を取得します。"""
        data = collect_market_overview()
        report = generate_research_report(data)
        lines = []
        capture = False
        for line in report.split("\n"):
            if "## 5. 明日以降のシナリオ予想" in line:
                capture = True
            elif line.startswith("## 6."):
                break
            if capture:
                lines.append(line)
        return "\n".join(lines) if lines else "シナリオ情報を取得できませんでした。"


def run_server(transport: str = "sse", port: int = 8000):
    """MCPサーバーを起動する"""
    if not mcp_available:
        print("エラー: mcp パッケージがインストールされていません。Python 3.10以上で pip install mcp を実行してください。")
        return
    print(f"Starting MCP Server on port {port} with transport={transport}...")
    mcp.run(transport=transport, port=port)


if __name__ == "__main__":
    import sys
    transport_mode = sys.argv[1] if len(sys.argv) > 1 else "sse"
    run_server(transport=transport_mode)
