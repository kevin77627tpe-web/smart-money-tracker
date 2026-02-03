"""
Smart Money Tracker - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
import uvicorn

app = FastAPI(
    title="Smart Money Tracker API",
    description="API for tracking professional crypto trader wallets",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# Data Models
# ============================================

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    plan: str = "free"
    created_at: datetime

class WalletCreate(BaseModel):
    address: str
    name: Optional[str] = None
    tags: List[str] = []

class Wallet(BaseModel):
    id: int
    user_id: int
    address: str
    name: Optional[str]
    balance: str
    pnl_24h: float
    pnl_7d: float
    pnl_30d: float
    grade: str
    last_activity: str
    tags: List[str]
    created_at: datetime

class Transaction(BaseModel):
    id: int
    wallet_id: int
    wallet_name: str
    tx_type: str  # BUY, SELL, SWAP
    token: str
    amount: str
    value: str
    timestamp: datetime

class BacktestResult(BaseModel):
    wallet_id: int
    annual_return_pct: float
    sharpe_ratio: float
    max_drawdown_pct: float
    win_rate: float
    total_trades: int
    grade: str

# ============================================
# Mock Database (In-memory)
# ============================================

# Mock data storage
users_db = []
wallets_db = []
transactions_db = []

# Mock data
mock_wallets = [
    {
        "id": 1,
        "user_id": 1,
        "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0a4B2",
        "name": "DeFi Whale",
        "balance": "$2,347,891",
        "pnl_24h": 12.4,
        "pnl_7d": 38.7,
        "pnl_30d": 156.3,
        "grade": "S",
        "last_activity": "2 hours ago",
        "tags": ["DeFi", "Arbitrage"],
        "created_at": datetime.now()
    },
    {
        "id": 2,
        "user_id": 1,
        "address": "0x9f3c8E3C8d8E3f8e8C8D8E3F8E8C8D8E3F8E7E21",
        "name": "Smart Trader",
        "balance": "$1,892,453",
        "pnl_24h": 8.9,
        "pnl_7d": 25.2,
        "pnl_30d": 118.6,
        "grade": "S",
        "last_activity": "5 hours ago",
        "tags": ["Swing Trading"],
        "created_at": datetime.now()
    }
]

mock_transactions = [
    {
        "id": 1,
        "wallet_id": 1,
        "wallet_name": "DeFi Whale",
        "tx_type": "BUY",
        "token": "ETH",
        "amount": "15.5 ETH",
        "value": "$42,350",
        "timestamp": datetime.now()
    },
    {
        "id": 2,
        "wallet_id": 2,
        "wallet_name": "Smart Trader",
        "tx_type": "SELL",
        "token": "UNI",
        "amount": "2,500 UNI",
        "value": "$18,750",
        "timestamp": datetime.now()
    }
]

# ============================================
# API Routes
# ============================================

@app.get("/")
def root():
    """API health check"""
    return {
        "status": "healthy",
        "service": "Smart Money Tracker API",
        "version": "1.0.0"
    }

# ============================================
# User Routes
# ============================================

@app.post("/api/auth/signup", response_model=User)
def signup(user: UserCreate):
    """Create new user account"""
    # Check if user already exists
    if any(u["email"] == user.email for u in users_db):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = {
        "id": len(users_db) + 1,
        "name": user.name,
        "email": user.email,
        "plan": "free",
        "created_at": datetime.now()
    }
    users_db.append(new_user)
    return new_user

@app.post("/api/auth/login")
def login(credentials: UserLogin):
    """User login"""
    # Find user by email
    user = next((u for u in users_db if u["email"] == credentials.email), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {
        "access_token": "mock_token_" + str(user["id"]),
        "token_type": "bearer",
        "user": user
    }

@app.get("/api/users/me", response_model=User)
def get_current_user():
    """Get current user profile"""
    # Mock: return first user
    if not users_db:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return users_db[0]

# ============================================
# Wallet Routes
# ============================================

@app.get("/api/wallets", response_model=List[Wallet])
def list_wallets(user_id: int = 1):
    """List user's tracked wallets"""
    user_wallets = [w for w in mock_wallets if w["user_id"] == user_id]
    return user_wallets

@app.post("/api/wallets", response_model=Wallet)
def create_wallet(wallet: WalletCreate, user_id: int = 1):
    """Add new wallet to track"""
    new_wallet = {
        "id": len(mock_wallets) + 1,
        "user_id": user_id,
        "address": wallet.address,
        "name": wallet.name or f"Wallet {len(mock_wallets) + 1}",
        "balance": "$0",
        "pnl_24h": 0.0,
        "pnl_7d": 0.0,
        "pnl_30d": 0.0,
        "grade": "C",
        "last_activity": "Just added",
        "tags": wallet.tags,
        "created_at": datetime.now()
    }
    mock_wallets.append(new_wallet)
    return new_wallet

@app.get("/api/wallets/{wallet_id}", response_model=Wallet)
def get_wallet(wallet_id: int):
    """Get wallet details"""
    wallet = next((w for w in mock_wallets if w["id"] == wallet_id), None)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet

@app.delete("/api/wallets/{wallet_id}")
def delete_wallet(wallet_id: int):
    """Remove wallet from tracking"""
    global mock_wallets
    wallet = next((w for w in mock_wallets if w["id"] == wallet_id), None)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    mock_wallets = [w for w in mock_wallets if w["id"] != wallet_id]
    return {"message": "Wallet removed successfully"}

# ============================================
# Transaction Routes
# ============================================

@app.get("/api/transactions", response_model=List[Transaction])
def list_transactions(wallet_id: Optional[int] = None, limit: int = 20):
    """List recent transactions"""
    txs = mock_transactions
    if wallet_id:
        txs = [tx for tx in txs if tx["wallet_id"] == wallet_id]
    return txs[:limit]

@app.get("/api/transactions/{wallet_id}", response_model=List[Transaction])
def get_wallet_transactions(wallet_id: int, limit: int = 50):
    """Get transactions for specific wallet"""
    txs = [tx for tx in mock_transactions if tx["wallet_id"] == wallet_id]
    return txs[:limit]

# ============================================
# Leaderboard Routes
# ============================================

@app.get("/api/leaderboard")
def get_leaderboard(sort_by: str = "annual_return_pct", limit: int = 50):
    """Get wallet performance leaderboard"""
    leaderboard = [
        {
            "rank": 1,
            "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0a4B2",
            "name": "DeFi Whale",
            "annual_return_pct": 287.4,
            "sharpe_ratio": 3.2,
            "max_drawdown_pct": -12.5,
            "win_rate": 78.3,
            "total_trades": 342,
            "grade": "S",
            "tags": ["DeFi", "Arbitrage", "High Freq"]
        },
        {
            "rank": 2,
            "address": "0x9f3c8E3C8d8E3f8e8C8D8E3F8E8C8D8E3F8E7E21",
            "name": "Smart Trader",
            "annual_return_pct": 215.8,
            "sharpe_ratio": 2.8,
            "max_drawdown_pct": -18.2,
            "win_rate": 72.1,
            "total_trades": 198,
            "grade": "S",
            "tags": ["Swing Trading", "Blue Chips"]
        },
        {
            "rank": 3,
            "address": "0x1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9C9D4",
            "name": "Yield Hunter",
            "annual_return_pct": 189.3,
            "sharpe_ratio": 2.5,
            "max_drawdown_pct": -15.7,
            "win_rate": 69.4,
            "total_trades": 267,
            "grade": "A",
            "tags": ["Yield Farming", "Staking"]
        }
    ]
    return leaderboard[:limit]

# ============================================
# Backtest Routes
# ============================================

@app.get("/api/backtest/{wallet_id}", response_model=BacktestResult)
def get_backtest_result(wallet_id: int):
    """Get backtest results for wallet"""
    wallet = next((w for w in mock_wallets if w["id"] == wallet_id), None)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    # Return mock backtest data
    return {
        "wallet_id": wallet_id,
        "annual_return_pct": wallet["pnl_30d"] * 12 / 30,
        "sharpe_ratio": 2.5,
        "max_drawdown_pct": -15.0,
        "win_rate": 68.5,
        "total_trades": 150,
        "grade": wallet["grade"]
    }

@app.post("/api/backtest/{wallet_id}")
def run_backtest(wallet_id: int):
    """Run backtest for wallet"""
    wallet = next((w for w in mock_wallets if w["id"] == wallet_id), None)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    # Simulate backtest execution
    return {
        "message": "Backtest started",
        "wallet_id": wallet_id,
        "status": "processing"
    }

# ============================================
# Stats Routes
# ============================================

@app.get("/api/stats/dashboard")
def get_dashboard_stats(user_id: int = 1):
    """Get dashboard statistics"""
    user_wallets = [w for w in mock_wallets if w["user_id"] == user_id]
    
    return {
        "total_wallets": len(user_wallets),
        "total_value": "$4,983,344",
        "total_pnl_24h": 10.2,
        "total_pnl_7d": 31.5,
        "total_pnl_30d": 137.4,
        "alerts_today": 4,
        "transactions_today": 12
    }

# ============================================
# Run Server
# ============================================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
