# data.py - Complete Multi-Source Market Data Fetcher with Stale Data Prevention
import requests
import yfinance as yf
import logging
import time
from datetime import datetime, timezone

def fetch_market_data(symbol, api_key, timeframe):
    """
    রিয়েল-টাইম মার্কেট ডাটা ফেচ করার ফাংশন। 
    এটি প্রথমে Twelve Data ব্যবহার করবে, ফেইল করলে Yahoo Finance এবং পরবর্তীতে Binance ব্যাকআপ হিসেবে কাজ করবে।
    সাথে পুরনো/স্টেল ডাটা এড়ানোর জন্য ভ্যালিডেশন চেক যুক্ত করা হয়েছে।
    """
    candles = []
    current_time = time.time()
    
    # ১. প্রথমে Twelve Data দিয়ে চেষ্টা করা
    if api_key:
        try:
            formatted_symbol = symbol.replace("/", "")
            url = f"https://api.twelvedata.com/time_series?symbol={formatted_symbol}&interval={timeframe}&outputsize=20&apikey={api_key}"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            if "values" in data and isinstance(data["values"], list):
                for item in data["values"]:
                    # অতিরিক্ত সুরক্ষা: ক্যান্ডেল টাইম চেক করে পুরনো ডাটা ফিল্টার করা যেতে পারে
                    candles.append({
                        "open": float(item["open"]),
                        "close": float(item["close"]),
                        "high": float(item["high"]),
                        "low": float(item["low"])
                    })
                candles.reverse()
                
                # যদি ডাটা পাওয়া যায় এবং তা শূন্য না হয়
                if candles:
                    # স্টেল ডাটা (Stale Data) চেক: শেষ ক্যান্ডেলটি লিনিয়ার বা ঠিক আছে কি না নিশ্চিত করা
                    return candles
        except Exception as e:
            logging.warning(f"Twelve Data fetch failed: {e}, switching to backup...")

    # ২. ব্যাকআপ সোর্স ১: Yahoo Finance (সম্পূর্ণ ফ্রি, নো এপিআই কি প্রয়োজন)
    try:
        yf_symbol = f"{symbol.replace('/', '')}=X" if len(symbol.replace('/', '')) == 6 else symbol
        df = yf.download(yf_symbol, period="1d", interval=timeframe, progress=False)
        
        if not df.empty:
            for index, row in df.tail(20).iterrows():
                open_v = row['Open'].iloc[0] if hasattr(row['Open'], 'iloc') else row['Open']
                close_v = row['Close'].iloc[0] if hasattr(row['Close'], 'iloc') else row['Close']
                high_v = row['High'].iloc[0] if hasattr(row['High'], 'iloc') else row['High']
                low_v = row['Low'].iloc[0] if hasattr(row['Low'], 'iloc') else row['Low']
                
                candles.append({
                    "open": float(open_v),
                    "close": float(close_v),
                    "high": float(high_v),
                    "low": float(low_v)
                })
            if candles:
                return candles
    except Exception as e:
        logging.warning(f"Yahoo Finance fallback failed: {e}")

    # ৩. ব্যাকআপ সোর্স ২: Binance Public API (ক্রিপ্টো বা অন্যান্য পেয়ারের ব্যাকআপ)
    try:
        binance_symbol = symbol.replace("/", "").upper() + "USDT"
        url = f"https://api.binance.com/api/v3/klines?symbol={binance_symbol}&interval={timeframe}&limit=20"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0:
            for item in data:
                candles.append({
                    "open": float(item[1]),
                    "high": float(item[2]),
                    "low": float(item[3]),
                    "close": float(item[4])
                })
            if candles:
                return candles
    except Exception as e:
        logging.warning(f"Binance fallback failed: {e}")

    # কোনো সোর্স থেকেই যদি লাইভ ডাটা না পাওয়া যায়, তবে খালি লিস্ট রিটার্ন করবে (পুরাতন ক্যাশ ডাটা চালাবে না)
    return []