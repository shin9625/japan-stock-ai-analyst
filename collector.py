"""
日本株・主要指標のデータ収集およびテクニカル分析モジュール
yfinance を使用して完全無料・APIキー不要でリアルタイム/ヒストリカルデータを取得します。
"""

import math
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd
import yfinance as yf

# 監視対象のティッカーシンボル一覧
WATCHLIST = {
    "indices": {
        "日経平均": "^N225",
        "TOPIX (ETF)": "1306.T",
        "米S&P500": "^GSPC",
        "米SOX半導体指数": "^SOX",
        "米NYダウ": "^DJI",
    },
    "forex": {
        "ドル/円 (USD/JPY)": "JPY=X",
        "ユーロ/円 (EUR/JPY)": "EURJPY=X",
    },
    "key_stocks": {
        "トヨタ自動車": "7203.T",
        "レーザーテック": "6920.T",
        "アドバンテスト": "6857.T",
        "三菱UFJ FG": "8306.T",
        "ソフトバンクG": "9984.T",
        "東京エレクトロン": "8035.T",
        "ソニーグループ": "6758.T",
    }
}


def calculate_technical_indicators(df: pd.DataFrame) -> Dict[str, Any]:
    """株価データフレームから主要テクニカル指標を計算する"""
    if df.empty or len(df) < 25:
        return {}

    close = df["Close"]
    volume = df["Volume"] if "Volume" in df.columns else None

    # 移動平均線 (SMA)
    sma5 = close.rolling(window=5).mean().iloc[-1] if len(close) >= 5 else None
    sma25 = close.rolling(window=25).mean().iloc[-1] if len(close) >= 25 else None
    sma75 = close.rolling(window=75).mean().iloc[-1] if len(close) >= 75 else None

    current_price = close.iloc[-1]
    prev_price = close.iloc[-2] if len(close) >= 2 else current_price
    price_change = current_price - prev_price
    price_change_pct = (price_change / prev_price) * 100 if prev_price else 0

    # 乖離率
    bias_sma25 = ((current_price - sma25) / sma25) * 100 if sma25 else None

    # RSI (14日)
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi14 = 100 - (100 / (1 + rs)).iloc[-1] if not rs.empty else None

    # MACD (12, 26, 9)
    exp12 = close.ewm(span=12, adjust=False).mean()
    exp26 = close.ewm(span=26, adjust=False).mean()
    macd_line = exp12 - exp26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    macd = macd_line.iloc[-1]
    macd_signal = signal_line.iloc[-1]
    macd_hist = macd - macd_signal

    # ボリンジャーバンド (20日, ±2σ)
    sma20 = close.rolling(window=20).mean().iloc[-1] if len(close) >= 20 else None
    std20 = close.rolling(window=20).std().iloc[-1] if len(close) >= 20 else None
    bb_upper2 = (sma20 + 2 * std20) if sma20 and std20 else None
    bb_lower2 = (sma20 - 2 * std20) if sma20 and std20 else None

    # 出来高変化率
    vol_change_pct = None
    if volume is not None and len(volume) >= 2 and volume.iloc[-2] > 0:
        vol_change_pct = ((volume.iloc[-1] - volume.iloc[-2]) / volume.iloc[-2]) * 100

    return {
        "current_price": round(float(current_price), 2),
        "prev_price": round(float(prev_price), 2),
        "price_change": round(float(price_change), 2),
        "price_change_pct": round(float(price_change_pct), 2),
        "sma5": round(float(sma5), 2) if sma5 and not math.isnan(sma5) else None,
        "sma25": round(float(sma25), 2) if sma25 and not math.isnan(sma25) else None,
        "sma75": round(float(sma75), 2) if sma75 and not math.isnan(sma75) else None,
        "bias_sma25_pct": round(float(bias_sma25), 2) if bias_sma25 and not math.isnan(bias_sma25) else None,
        "rsi14": round(float(rsi14), 2) if rsi14 and not math.isnan(rsi14) else None,
        "macd": round(float(macd), 2) if macd and not math.isnan(macd) else None,
        "macd_signal": round(float(macd_signal), 2) if macd_signal and not math.isnan(macd_signal) else None,
        "macd_hist": round(float(macd_hist), 2) if macd_hist and not math.isnan(macd_hist) else None,
        "bb_upper2": round(float(bb_upper2), 2) if bb_upper2 and not math.isnan(bb_upper2) else None,
        "bb_lower2": round(float(bb_lower2), 2) if bb_lower2 and not math.isnan(bb_lower2) else None,
        "volume": int(volume.iloc[-1]) if volume is not None and not math.isnan(volume.iloc[-1]) else None,
        "vol_change_pct": round(float(vol_change_pct), 2) if vol_change_pct and not math.isnan(vol_change_pct) else None,
    }


def fetch_symbol_data(symbol: str, period: str = "6mo") -> Optional[Dict[str, Any]]:
    """指定シンボルのヒストリカルデータを取得し、テクニカル指標を算出する"""
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period)
        if df.empty:
            return None
        tech = calculate_technical_indicators(df)
        return tech
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None


def collect_market_overview() -> Dict[str, Any]:
    """マーケット全体のデータ（指数、為替、主力株）を一括収集する"""
    now_jst = datetime.now()
    report_data = {
        "timestamp": now_jst.strftime("%Y-%m-%d %H:%M:%S"),
        "date_str": now_jst.strftime("%Y年%m月%d日"),
        "indices": {},
        "forex": {},
        "key_stocks": {},
    }

    # 指数取得
    for name, sym in WATCHLIST["indices"].items():
        data = fetch_symbol_data(sym)
        if data:
            report_data["indices"][name] = {"symbol": sym, **data}

    # 為替取得
    for name, sym in WATCHLIST["forex"].items():
        data = fetch_symbol_data(sym)
        if data:
            report_data["forex"][name] = {"symbol": sym, **data}

    # 主力株取得
    for name, sym in WATCHLIST["key_stocks"].items():
        data = fetch_symbol_data(sym)
        if data:
            report_data["key_stocks"][name] = {"symbol": sym, **data}

    return report_data


if __name__ == "__main__":
    import json
    print("データ収集テスト実行中...")
    result = collect_market_overview()
    print(json.dumps(result, ensure_ascii=False, indent=2))
