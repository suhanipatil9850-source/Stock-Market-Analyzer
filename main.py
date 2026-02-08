# Stock Market Analyzer – FastAPI + Interactive Dashboard
# Features: stock lookup, price metrics, trend, volume
# Data source: Yahoo Finance (yfinance)
# Run: python main.py

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import yfinance as yf
import pandas as pd

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# -------- Helpers --------
def get_stock_data(ticker: str):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1mo")

    if hist.empty:
        return None

    latest = hist.iloc[-1]
    return {
        "ticker": ticker.upper(),
        "price": round(latest['Close'], 2),
        "high": round(hist['High'].max(), 2),
        "low": round(hist['Low'].min(), 2),
        "volume": int(latest['Volume']),
        "change": round(((latest['Close'] - hist.iloc[0]['Open']) / hist.iloc[0]['Open']) * 100, 2),
        "history": hist.reset_index()[['Date', 'Close']].to_dict('records')
    }

# -------- Routes --------
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze", response_class=HTMLResponse)
def analyze(request: Request, ticker: str = Form(...)):
    data = get_stock_data(ticker)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "data": data
    })

# -------- Run --------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

