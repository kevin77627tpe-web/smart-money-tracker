"""
數據庫初始化腳本
創建所有表結構並添加測試數據
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import os
import random

Base = declarative_base()

# 數據模型定義
class Wallet(Base):
    __tablename__ = 'wallets'

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(42), unique=True, index=True, nullable=False)
    label = Column(String(100))
    total_profit = Column(Float, default=0.0)
    win_rate = Column(Float, default=0.0)
    total_trades = Column(Integer, default=0)
    rank = Column(Integer)
    is_monitored = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Trade(Base):
    __tablename__ = 'trades'

    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, index=True)
    wallet_address = Column(String(42), index=True)
    token_symbol = Column(String(20))
    token_address = Column(String(42))
    action = Column(String(10))  # 'buy' or 'sell'
    amount = Column(Float)
    price = Column(Float)
    profit_loss = Column(Float)
    tx_hash = Column(String(66), unique=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    username = Column(String(50), unique=True)
    subscription_tier = Column(String(20), default='free')  # free, pro, enterprise
    api_key = Column(String(64), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class Alert(Base):
    __tablename__ = 'alerts'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    wallet_address = Column(String(42))
    alert_type = Column(String(50))  # 'large_trade', 'new_position', 'profit_milestone'
    message = Column(Text)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    """初始化數據庫並創建所有表"""

    # 從環境變量獲取數據庫 URL
    database_url = os.getenv('DATABASE_URL')

    if not database_url:
        print("⚠️  DATABASE_URL 環境變量未設置")
        print("💡 本地測試使用: postgresql://localhost/smart_money_tracker")
        database_url = "postgresql://localhost/smart_money_tracker"

    # 修正 Render 的 postgres:// 為 postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)

    print(f"📊 連接數據庫...")
    engine = create_engine(database_url)

    # 創建所有表
    print("🔨 創建表結構...")
    Base.metadata.create_all(bind=engine)
    print("✅ 表結構創建完成")

    return engine

def seed_test_data():
    """添加測試數據"""

    database_url = os.getenv('DATABASE_URL', "postgresql://localhost/smart_money_tracker")
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)

    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    print("\n🌱 添加測試數據...")

    # 生成測試錢包
    test_wallets = [
        {
            'address': '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb',
            'label': 'Smart Whale #1',
            'total_profit': 1250000.50,
            'win_rate': 0.87,
            'total_trades': 156,
            'rank': 1
        },
        {
            'address': '0x123456789abcdef123456789abcdef123456789a',
            'label': 'DeFi Mastermind',
            'total_profit': 980000.25,
            'win_rate': 0.82,
            'total_trades': 203,
            'rank': 2
        },
        {
            'address': '0xabcdef123456789abcdef123456789abcdef1234',
            'label': 'Crypto Titan',
            'total_profit': 750000.75,
            'win_rate': 0.79,
            'total_trades': 128,
            'rank': 3
        },
        {
            'address': '0x9876543210fedcba9876543210fedcba98765432',
            'label': 'Token Hunter',
            'total_profit': 625000.00,
            'win_rate': 0.75,
            'total_trades': 189,
            'rank': 4
        },
        {
            'address': '0xfedcba9876543210fedcba9876543210fedcba98',
            'label': 'Yield Farmer Pro',
            'total_profit': 520000.50,
            'win_rate': 0.71,
            'total_trades': 245,
            'rank': 5
        }
    ]

    for wallet_data in test_wallets:
        # 檢查是否已存在
        existing = session.query(Wallet).filter_by(address=wallet_data['address']).first()
        if not existing:
            wallet = Wallet(**wallet_data)
            session.add(wallet)
            print(f"  ✓ 添加錢包: {wallet_data['label']}")

    # 生成測試交易
    tokens = ['ETH', 'BTC', 'SOL', 'MATIC', 'AVAX', 'LINK', 'UNI', 'AAVE']
    actions = ['buy', 'sell']

    for wallet_data in test_wallets[:3]:  # 只為前3個錢包生成交易
        for _ in range(5):  # 每個錢包5筆交易
            trade = Trade(
                wallet_address=wallet_data['address'],
                token_symbol=random.choice(tokens),
                token_address=f"0x{''.join(random.choices('0123456789abcdef', k=40))}",
                action=random.choice(actions),
                amount=round(random.uniform(0.1, 100), 2),
                price=round(random.uniform(100, 50000), 2),
                profit_loss=round(random.uniform(-1000, 5000), 2),
                tx_hash=f"0x{''.join(random.choices('0123456789abcdef', k=64))}",
                timestamp=datetime.utcnow() - timedelta(hours=random.randint(1, 720))
            )
            session.add(trade)

    print(f"  ✓ 添加 15 筆測試交易")

    # 生成測試用戶
    test_users = [
        {
            'email': 'demo@example.com',
            'username': 'demo_user',
            'subscription_tier': 'pro',
            'api_key': ''.join(random.choices('0123456789abcdef', k=64))
        },
        {
            'email': 'test@example.com',
            'username': 'test_trader',
            'subscription_tier': 'free',
            'api_key': ''.join(random.choices('0123456789abcdef', k=64))
        }
    ]

    for user_data in test_users:
        existing = session.query(User).filter_by(email=user_data['email']).first()
        if not existing:
            user = User(**user_data)
            session.add(user)
            print(f"  ✓ 添加用戶: {user_data['username']}")

    # 提交所有更改
    session.commit()
    print("\n✅ 測試數據添加完成！")

    # 顯示統計
    wallet_count = session.query(Wallet).count()
    trade_count = session.query(Trade).count()
    user_count = session.query(User).count()

    print(f"\n📊 數據庫統計:")
    print(f"  • 錢包數量: {wallet_count}")
    print(f"  • 交易記錄: {trade_count}")
    print(f"  • 用戶數量: {user_count}")

    session.close()

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║   Smart Money Tracker - 數據庫初始化                        ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

    # 初始化數據庫
    engine = init_db()

    # 添加測試數據
    seed_test_data()

    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║   ✅ 數據庫初始化完成！                                      ║
    ║                                                              ║
    ║   下一步: 啟動 API 服務器                                    ║
    ║   命令: uvicorn main:app --reload                            ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
