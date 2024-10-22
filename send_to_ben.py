from pathlib import Path

from chart_emailer.scrape import WebDriverManager

urls_files = [
    ("https://www.tradingview.com/chart/ry2ZLXIN/?symbol=TVC%3AUSOIL", "oil"),
    ("https://www.tradingview.com/chart/ry2ZLXIN/?symbol=TVC%3AGOLD", "gold"),
    ("https://www.tradingview.com/chart/ry2ZLXIN/?symbol=ASX%3AXJO", "asx"),
    ("https://www.tradingview.com/chart/ry2ZLXIN/?symbol=FX%3AAUDUSD", "audusd"),
    ("https://www.tradingview.com/chart/ry2ZLXIN/?symbol=BMFBOVESPA%3APETR4", "petrobras"),
    ("https://www.tradingview.com/chart/ry2ZLXIN/?symbol=BMFBOVESPA%3AVALE3", "vale"),
    ("https://www.tradingview.com/chart/ry2ZLXIN/?symbol=SPREADEX%3ANIKKEI", "nikkei"),
    ("https://www.tradingview.com/chart/ry2ZLXIN/?symbol=TVC%3AHSI", "hangseng"),
    ("https://www.tradingview.com/chart/ry2ZLXIN/?symbol=NASDAQ%3ANDX", "nasdaq"),
    ("https://www.tradingview.com/chart/ry2ZLXIN/?symbol=SP%3ASPX", "sp500"),
]

for path in Path("data").glob("*.png"):
    print(f"Deleting {path}")
    path.unlink()

# manager = WebDriverManager()
# for url, filename in urls_files:
#     print(f"Saving {url} to {filename}")
#     manager.save_tradingview_chart_as_image(url, f"data/{filename}.png")
# manager.close_driver()

url, filename = "https://www.fxstreet.com/economic-calendar", "economic-calendar"
manager = WebDriverManager(height=1080 * 4)
print(f"Saving {url} to {filename}")
manager.save_tradingview_chart_as_image(url, f"data/{filename}.png")
manager.close_driver()
