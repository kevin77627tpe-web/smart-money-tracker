from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI(title="Smart Money Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Smart Money Tracker API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "wallets": "/api/wallets",
            "leaderboard": "/api/leaderboard",
            "documentation": "/docs"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": "2024-02-03T15:00:00Z"}

@app.get("/api/wallets")
async def get_wallets():
    return {
        "wallets": [
            {
                "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
                "label": "Smart Trader #1",
                "total_pnl": 1250000,
                "win_rate": 0.78,
                "total_trades": 145
            },
            {
                "address": "0x28C6c06298d514Db089934071355E5743bf21d60",
                "label": "Whale Investor",
                "total_pnl": 890000,
                "win_rate": 0.72,
                "total_trades": 89
            }
        ]
    }

@app.get("/api/leaderboard")
async def get_leaderboard():
    return {
        "leaderboard": [
            {"rank": 1, "address": "0x742d35Cc", "pnl": 1250000, "win_rate": 78},
            {"rank": 2, "address": "0x28C6c062", "pnl": 890000, "win_rate": 72},
            {"rank": 3, "address": "0x9876abcd", "pnl": 650000, "win_rate": 68}
        ]
    }

# Vercel serverless handler
handler = app
