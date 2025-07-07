# FastAPI 專案說明

## 專案簡介
本專案使用 FastAPI 框架開發 RESTful API，結合 MySQL 資料庫，並支援 Session 管理與靜態檔案服務，適合作為全端開發學習範例。

---

## 專案架構
- **後端**：FastAPI (Python)
- **前端**：public 資料夾內靜態 HTML、圖片
- **資料庫**：MySQL
- **Session 管理**：Starlette SessionMiddleware

---

## 主要功能

### 1. 使用者歡迎與 Session
- `GET /hello?name=xxx`：設定 session，歡迎使用者
- `GET /talk`：讀取 session，辨識回訪者

### 2. 訊息板 CRUD
- `POST /api/message`：新增訊息（author, content）
- `GET /api/message`：取得所有訊息
- `DELETE /api/message/{id}`：刪除訊息

### 3. 其他 API 範例
- `GET /multiply?n1=3&n2=4`：回傳兩數相乘結果
- `GET /square?number=5`：回傳平方
- `GET /items/?name=xxx`：Query 參數驗證
- `GET /img/logo`：回傳圖片
- `GET /member`：導向 Google

---

## 資料庫設計
- 資料表：`message`
  - `id` (int, PK)
  - `author` (varchar)
  - `content` (text)
  - `create_time` (datetime)

---

## 程式碼亮點
- 使用 Pydantic 定義請求/回應模型，確保資料驗證
- Session 管理，實現簡易登入體驗
- 靜態檔案與 API 路由分離
- 例外處理與資料庫連線管理

---

## 學習收穫
- 熟悉 FastAPI 路由、資料驗證、Session
- 前後端整合與資料庫操作
- RESTful API 設計與實作

---

## 程式碼片段

#### FastAPI 路由註冊
```python
@app.post("/api/message", response_model=MessageResponse)
def createMessage(message: MessageCreate):
    cursor=con.cursor()    
    cursor.execute("INSERT INTO message(author,content) VALUES(%s,%s)",[message.author,message.content])
    con.commit()
    cursor.execute("SELECT * FROM message WHERE id = LAST_INSERT_ID()")
    new_message = cursor.fetchone()
    return {
        "id": new_message[0],
        "author": new_message[1],
        "content": new_message[2],
        "created_at": new_message[3]
    }
```

#### Session 設定
```python
app.add_middleware(SessionMiddleware, secret_key="test20585")
```

#### 靜態檔案服務
```python
app.mount("/", StaticFiles(directory="public", html=True))
```

---

## 啟動方式
```bash
uvicorn main:app --reload
```

---

## 其他
- 可依需求擴充 API 或前端頁面
- 適合全端面試、學習展示 