# 🚀 Business Card Scanner - 設定指南

## 📋 必要的 API 金鑰與憑證

在開始使用本專案之前，請準備以下 API 金鑰和憑證：

---

## 1️⃣ Poe API Token

### 用途
用於呼叫 Gemini-2.5-Flash 模型進行名片 OCR 辨識

### 取得方式
1. 前往 **Poe 官方網站**：https://poe.com/
2. 登入您的帳號
3. 前往 **API 設定頁面**：https://poe.com/api_key
4. 點擊「Create API Key」建立新的 API 金鑰
5. 複製產生的 API Token（格式：`poe-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`）

### 注意事項
- ⚠️ API Token 只會顯示一次，請立即儲存
- 💰 Poe API 為付費服務，請確認您的帳戶餘額充足
- 📊 查看使用量：https://poe.com/api_usage

### 環境變數設定
```bash
POE_API_TOKEN=poe-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 2️⃣ Google Sheets API 憑證

### 用途
用於將辨識結果自動寫入 Google Sheets

### 取得方式

#### Step 1: 建立 Google Cloud 專案
1. 前往 **Google Cloud Console**：https://console.cloud.google.com/
2. 點擊「選取專案」→「新增專案」
3. 輸入專案名稱（例如：`business-card-scanner`）
4. 點擊「建立」

#### Step 2: 啟用 Google Sheets API
1. 在 Google Cloud Console 中，選擇您剛建立的專案
2. 前往「API 和服務」→「程式庫」
3. 搜尋「Google Sheets API」
4. 點擊「啟用」

#### Step 3: 建立 Service Account
1. 前往「API 和服務」→「憑證」
2. 點擊「建立憑證」→「服務帳戶」
3. 輸入服務帳戶名稱（例如：`sheets-writer`）
4. 點擊「建立並繼續」
5. 角色選擇「編輯者」（Editor）
6. 點擊「完成」

#### Step 4: 下載 JSON 憑證檔
1. 在「憑證」頁面，找到剛建立的服務帳戶
2. 點擊服務帳戶名稱
3. 切換到「金鑰」分頁
4. 點擊「新增金鑰」→「建立新金鑰」
5. 選擇「JSON」格式
6. 點擊「建立」，JSON 檔案會自動下載
7. 將下載的 JSON 檔案重新命名並放到專案根目錄：
   ```
   /Users/{your }/project/ai_model/business_card_scanner/credentials.json
   ```

#### Step 5: 建立 Google Sheets 並設定權限
1. 前往 **Google Sheets**：https://sheets.google.com/
2. 建立新的試算表（或使用現有的）
3. 在試算表中建立欄位標題（建議第一行）：
   ```
   姓名 | 公司 | 職稱 | 手機 | 辦公室電話 | Email | 網站 | 地址 | 時間戳記
   ```
4. 點擊右上角「共用」按鈕
5. 複製 JSON 憑證檔中的 `client_email` 欄位值（格式：`xxx@xxx.iam.gserviceaccount.com`）
6. 將此電子郵件地址加入共用對象，權限設為「編輯者」
7. 複製試算表 URL 中的 Spreadsheet ID：
   ```
   https://docs.google.com/spreadsheets/d/SPREADSHEET_ID_HERE/edit
   ```

### 環境變數設定
```bash
GOOGLE_SHEET_ID=你的試算表ID
GOOGLE_SHEET_NAME=Sheet1
```

---

## 3️⃣ Ngrok Authtoken（用於 iPhone 捷徑）

### 用途
用於將本地端 FastAPI 服務暴露到公網，讓 iPhone 可以存取

### 取得方式
1. 前往 **Ngrok 官方網站**：https://ngrok.com/
2. 註冊或登入帳號
3. 前往 Dashboard：https://dashboard.ngrok.com/
4. 複製您的 Authtoken（在「Getting Started」→「Your Authtoken」區塊）

### 設定方式
```bash
ngrok config add-authtoken YOUR_AUTHTOKEN_HERE
```

### 注意事項
- 🆓 免費版每次重啟 ngrok 會產生新的 URL
- ⚠️ 每次 URL 改變時需要更新 iPhone 捷徑中的 API URL
- 💎 付費版可以使用固定的自訂網域

---

## 📝 完整 .env 檔案範例

在專案根目錄建立 `.env` 檔案（或複製 `.env.example`）：

```bash
# Poe API Token (for OCR)
POE_API_TOKEN=poe-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Google Sheets Configuration
GOOGLE_SHEET_ID=1234567890abcdefghijklmnopqrstuvwxyz
GOOGLE_SHEET_NAME=Sheet1
```

---

## ✅ 檢查清單

設定完成後，請確認以下檔案和設定都已就緒：

- [ ] `.env` 檔案已建立並包含 `POE_API_TOKEN`
- [ ] `.env` 檔案已包含 `GOOGLE_SHEET_ID` 和 `GOOGLE_SHEET_NAME`
- [ ] `credentials.json` 或 `gtin-search-*.json` 已放置在專案根目錄
- [ ] Google Sheets 已將 Service Account 的 email 加入共用（編輯者權限）
- [ ] Ngrok authtoken 已設定（執行 `ngrok config add-authtoken`）
- [ ] 已安裝所有必要的 Python 套件：
  ```bash
  pip install -r requirements.txt
  ```
  或手動安裝：
  ```bash
  pip install fastapi==0.124.0 fastapi-poe==0.0.81 google-api-python-client==2.175.0 nest-asyncio==1.6.0 protobuf==6.33.2 python-dotenv==1.2.1 uvicorn==0.38.0
  ```

---

## 🧪 測試設定

### 測試 1: 檢查環境變數
```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('POE_API_TOKEN:', 'OK' if os.getenv('POE_API_TOKEN') else 'MISSING'); print('GOOGLE_SHEET_ID:', 'OK' if os.getenv('GOOGLE_SHEET_ID') else 'MISSING')"
```

### 測試 2: 測試 Google Sheets 連線
```bash
python google_sheets_handler.py
```

### 測試 3: 測試 OCR 功能
```bash
python ocr_service.py
```

### 測試 4: 啟動 FastAPI 服務
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
然後訪問：http://localhost:8000/docs

### 測試 5: 啟動 Ngrok
```bash
ngrok http 8000
```

---

## 🆘 常見問題

### Q1: Poe API 回傳 401 Unauthorized
**A:** 檢查 `POE_API_TOKEN` 是否正確，並確認帳戶有足夠餘額

### Q2: Google Sheets API 回傳 403 Forbidden
**A:** 確認 Service Account 的 email 已加入試算表的共用對象

### Q3: Ngrok 連線失敗
**A:** 確認 authtoken 已正確設定：`ngrok config check`

### Q4: iPhone 捷徑回傳 422 錯誤
**A:** 檢查捷徑中的「要求本文」是否設為「表單」，且欄位名稱為 `file`

---

## 📚 相關連結

- **Poe API 文件**：https://creator.poe.com/docs/quick-start
- **Google Sheets API 文件**：https://developers.google.com/sheets/api/guides/concepts
- **Ngrok 文件**：https://ngrok.com/docs
- **FastAPI 文件**：https://fastapi.tiangolo.com/

---

## 🔐 安全提醒

⚠️ **重要**：
- 不要將 `.env` 檔案和 `credentials.json` 提交到 Git
- 不要在公開場合分享您的 API Token
- 定期檢查 API 使用量，避免超額費用
- 使用 `.gitignore` 確保敏感資訊不會被上傳

---

**設定完成後，請參考 `README.md` 開始使用本專案！** 🎉
