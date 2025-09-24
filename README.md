# Notes API

一個簡潔的 Flask 後端專案，提供使用者認證與筆記 CRUD，並內建 Swagger UI（/docs）。

## 功能

- 使用者註冊 / 登入（JWT）
- 筆記 CRUD、分頁與關鍵字搜尋
- Swagger UI（/docs）& OpenAPI JSON（/openapi.json）
- SQLite（預設）與 PostgreSQL（Docker）

## 架構圖

```
flowchart LR
  subgraph Client
    UI[Swagger UI / curl / Postman]
  end

  UI --> |HTTP JSON| API[Flask App]

  subgraph API[Flask App]
    DIR1[resources (Flask-RESTX Namespaces)]
    DIR2[services (Business Logic)]
    DIR3[models.py (SQLAlchemy ORM)]
    EXT[extensions.py (db/jwt/api/ma)]
  end

  API --> DB[(SQLite / PostgreSQL)]
```

## 目錄結構

```
notes-api/
├─ app.py
├─ extensions.py
├─ models.py
├─ schemas.py
├─ services/
│  └─ note_service.py
├─ resources/
│  ├─ auth.py
│  └─ notes.py
├─ tests/
│  ├─ test.py
├─ Dockerfile
├─ docker-compose.yml
├─ requirements.txt
├─ .env.example
├─ README.md
```

## 安裝與設定

1. clone 專案並進入專案目錄：
```bash
git clone https://github.com/Jiahsiu/notes_api
cd notes_api
```

2. 建立虛擬環境：

在專案資料夾內執行以下命令來建立 Python 虛擬環境
```bash
python -m venv .venv
```

3. 啟動虛擬環境：  

macOS/Linux：
```bash
source .venv/bin/activate
```
Windows：
```bash
.venv\Scripts\activate
```

4. 安裝需求套件：

執行以下命令來安裝專案需要的依賴套件：
```bash
pip install -r requirements.txt
```

5. 配置環境變數：
```bash
cp .env.example .env
```

6. 啟動 Flask 伺服器：
```bash
python -m flask run --port 8080
```

7. 訪問 API：  

開啟瀏覽器並前往 http://localhost:8080/docs 可以看到 Swagger UI，這是用來測試 API 的介面  
也可以透過 Postman 或 curl 測試 API  

## 使用 Docker 及 PostgreSQL

1. clone 專案並進入專案目錄：
```bash
git clone https://github.com/Jiahsiu/notes_api
cd notes_api
```

2. 建立並啟動 Docker 容器：
```bash
docker compose up --build
```

3. 配置 PostgreSQL：  

請在 .env 檔案中將 DATABASE_URL 設為 PostgreSQL 的連接字串：
```bash
DATABASE_URL=postgresql+psycopg2://testuser:changeme@postgres:5432/notesdb
```

4. 訪問 API：

當 Docker 容器啟動後，可以透過 http://localhost:8080/docs 訪問 Swagger UI，並測試 API。

## 執行測試

在專案中，會使用 pytest 進行單元測試。你可以執行以下指令來運行測試：
```bash
pytest -q
```
這會自動執行 tests 資料夾內的測試。
