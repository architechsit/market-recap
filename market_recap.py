import yfinance as yf
from datetime import datetime
from tabulate import tabulate
from colorama import Fore, Style, init
import csv

init(autoreset=True)

# ====================== MAPPINGS ======================
INDEXES = {
    "DJIA": "^DJI",
    "S&P 500": "^GSPC",
    "NASDAQ": "^IXIC",
    "Russell 2000": "^RUT",
}

FUTURES_AND_YIELDS = {
    "DJIA": "YM=F",
    "S&P 500": "ES=F",
    "NASDAQ": "NQ=F",
    "WTI": "CL=F",
    "US 10Y": "^TNX",
    "US 2Y": "^IRX",
}
# ===================================================

def get_quote(ticker):
    try:
        data = yf.Ticker(ticker).info
        price = data.get('regularMarketPrice') or data.get('previousClose')
        prev_close = data.get('previousClose')
        
        if price is None or prev_close is None:
            hist = yf.Ticker(ticker).history(period="2d")
            if not hist.empty:
                price = hist['Close'].iloc[-1]
                prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else price
        
        change = price - prev_close if prev_close else 0
        pct = (change / prev_close * 100) if prev_close else 0
        
        return round(price, 4) if price else None, round(change, 4), round(pct, 2)
    except:
        return None, None, None

def print_table(title, symbols_dict):
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f" {title}")
    print(f"{'='*70}{Style.RESET_ALL}\n")

    table = []
    for name, symbol in symbols_dict.items():
        price, change, pct = get_quote(symbol)
        
        if price is None:
            row = [name, "N/A", "N/A", symbol]
        else:
            change_str = f"{Fore.GREEN if change >= 0 else Fore.RED}{change:+.2f} ({pct:+.2f}%)"
            row = [name, f"{price:,.2f}", change_str, symbol]
        table.append(row)

    headers = ["Index / Asset", "Price", "Change", "Symbol"]
    print(tabulate(table, headers=headers, tablefmt="grid"))
    print()

def save_to_csv():
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"Market_Recap_{timestamp}.csv"
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        
        writer.writerow(["Market Recap as of", now.strftime('%Y-%m-%d %H:%M:%S')])
        writer.writerow([])
        
        # Market Recap section
        writer.writerow(["Market Recap - Previous Close (as of 4pm previous day)"])
        writer.writerow(["Index / Asset", "Price", "Change", "Symbol"])
        for name, symbol in INDEXES.items():
            price, change, pct = get_quote(symbol)
            change_str = f"{change:+.2f} ({pct:+.2f}%)" if price is not None else "N/A"
            price_str = f"{price:,.2f}" if price is not None else "N/A"
            writer.writerow([name, price_str, change_str, symbol])
        
        writer.writerow([])
        
        # Market Outlook section
        writer.writerow(["Market Outlook - Futures & Yields Snapshot"])
        writer.writerow(["Index / Asset", "Price", "Change", "Symbol"])
        for name, symbol in FUTURES_AND_YIELDS.items():
            price, change, pct = get_quote(symbol)
            change_str = f"{change:+.2f} ({pct:+.2f}%)" if price is not None else "N/A"
            price_str = f"{price:,.2f}" if price is not None else "N/A"
            writer.writerow([name, price_str, change_str, symbol])
    
    print(f"{Fore.GREEN}✓ Saved to: {filename}{Style.RESET_ALL}")

# ====================== MAIN ======================
if __name__ == "__main__":
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{Fore.YELLOW}Market Recap as of: {now}\n")

    print_table("Market Recap Previous Close (as of 4pm previous day)", INDEXES)
    print_table("Market Outlook Futures & Yields Snapshot", FUTURES_AND_YIELDS)
    
    save_to_csv()

