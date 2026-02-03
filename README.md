# 🚀 Smart Money Tracker - 一鍵部署

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/kevin77627tpe-web/smart-money-tracker)

## 快速部署（3 種方式）

### 🔥 方式 1: Render（推薦 - 最簡單）

**點擊上面的 "Deploy to Render" 按鈕，自動完成：**
- ✅ 創建 PostgreSQL 數據庫
- ✅ 部署 FastAPI 後端
- ✅ 配置所有環境變量
- ✅ 生成公開 URL

**或手動部署：**
1. 訪問：https://dashboard.render.com/
2. 點擊 "New +" → "Blueprint"
3. 連接此 repository
4. Render 會自動檢測 `render.yaml` 並部署

---

### 🚄 方式 2: Railway

1. 訪問：https://railway.app/new
2. 選擇 "Deploy from GitHub repo"
3. 選擇此 repository
4. 添加 PostgreSQL 數據庫
5. 生成公開域名

---

### ✈️ 方式 3: Fly.io

```bash
# 安裝 CLI
curl -L https://fly.io/install.sh | sh

# 部署
fly launch
fly postgres create
fly postgres attach
fly deploy
```

---

## 📦 項目結構

```
smart-money-tracker/
├── backend/           # FastAPI 後端
│   ├── main.py       # API 主文件
│   ├── models.py     # 數據模型
│   ├── database.py   # 數據庫配置
│   └── requirements.txt
├── public/           # 前端展示頁面
│   └── index.html
├── Dockerfile        # Docker 配置
└── render.yaml       # Render 部署配置
```

---

## 🔌 API 端點

部署完成後，訪問：

- 📚 **API 文檔**: `https://your-app.onrender.com/docs`
- ✅ **健康檢查**: `https://your-app.onrender.com/health`
- 💰 **錢包列表**: `https://your-app.onrender.com/api/v1/wallets`
- 🏆 **排行榜**: `https://your-app.onrender.com/api/v1/leaderboard`

---

## 💻 本地開發

```bash
# 克隆 repository
git clone https://github.com/kevin77627tpe-web/smart-money-tracker.git
cd smart-money-tracker/backend

# 安裝依賴
pip install -r requirements.txt

# 運行開發服務器
uvicorn main:app --reload

# 訪問
open http://localhost:8000/docs
```

---

## 🎯 功能特性

- 💎 **專業錢包追蹤** - 追蹤 Smart Money 交易行為
- 📊 **實時排行榜** - 根據盈利率和勝率排名
- 🔔 **智能提醒** - 大額交易和異常活動警報
- 📈 **歷史回測** - 分析過往交易表現
- 🔐 **用戶訂閱** - 多層級訂閱方案

---

## 📊 免費資源配額

| 平台 | RAM | 存儲 | 數據庫 | 備註 |
|------|-----|------|--------|------|
| Render | 512MB | ∞ | PostgreSQL 1GB | 推薦 ⭐ |
| Railway | 512MB | 1GB | PostgreSQL 1GB | $5/月額度 |
| Fly.io | 256MB | 3GB | PostgreSQL 3GB | 全球部署 |

---

## 🛠️ 技術棧

- **後端**: FastAPI + Python 3.11
- **數據庫**: PostgreSQL 16
- **ORM**: SQLAlchemy
- **容器**: Docker
- **部署**: Render / Railway / Fly.io

---

## 📝 License

MIT License

---

**立即開始部署！** 🚀
