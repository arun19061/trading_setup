from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strategy import run_strategy
from paper_trade import get_portfolio, get_logs

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/strategy/{symbol}")
def strategy(symbol: str):
    return run_strategy(symbol)

@app.get("/portfolio")
def portfolio():
    return get_portfolio()

@app.get("/logs")
def logs():
    return get_logs()
