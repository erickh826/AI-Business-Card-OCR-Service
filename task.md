專案名稱：AI 名片 OCR 服務
目標： 建立一個自動化流程，使用者可透過 iPhone 捷徑拍攝名片，呼叫後端 AI 服務進行文字辨識（OCR）與資料整理，最終將結構化的聯絡人資訊存入指定的 Google Sheet。

技術棧：

前端觸發： Apple iPhone 「捷徑」(Shortcuts) App
後端服務框架： Python (使用 FastAPI 或 Flask)
AI 視覺模型 API： Gemini 2.5 Flash (透過 Poe API 或 Azure AI API)
資料儲存： Google Sheets API
開發/測試工具： ngrok (用於在本機開發時暴露 API 給 iPhone)
Phase 1: 環境設定與權限準備 (Prerequisites & Setup)
目標： 確保所有需要的工具、API 金鑰和權限都已就緒。

Task 1.1: 準備 Google Sheet 與 API 權限

1.1.1: 在 Google Sheets 建立一個新的試算表，命名為 Business_Card_Contacts。
1.1.2: 設定表頭欄位，例如：Name, Company, Title, Mobile_Phone, Office_Phone, Email, Website, Address, Timestamp。
1.1.3: 前往 Google Cloud Console，建立一個新的專案。
1.1.4: 在該專案中，啟用 Google Sheets API 和 Google Drive API。
1.1.5: 建立一個「服務帳戶」(Service Account)，下載其 JSON 格式的憑證金鑰 (credentials.json)，並妥善保管。
1.1.6: 將該服務帳戶的電子郵件地址（格式如 ...@...gserviceaccount.com），新增為 Google Sheet 的「編輯者」，以便程式有權限寫入。
Task 1.2: 取得 AI 模型 API 金鑰


選項 A (Poe): 登入 Poe 帳號，取得您的 API Key。
Task 1.3: 設定本地開發環境

1.3.1: 安裝 Python 3.9+。
1.3.2: 安裝必要的 Python 套件：
```bash
pip install -r requirements.txt
```
套件列表：
- `fastapi==0.124.0` - Web 框架
- `fastapi-poe==0.0.81` - Poe API 客戶端
- `google-api-python-client==2.175.0` - Google Sheets API
- `nest-asyncio==1.6.0` - 異步事件循環支援
- `protobuf==6.33.2` - Protocol buffers
- `python-dotenv==1.2.1` - 環境變數管理
- `uvicorn==0.38.0` - ASGI 伺服器

1.3.3: 下載並設定 ngrok，以便在開發階段將本地的 API 服務暴露到公網。
Phase 2: 核心 AI 邏輯開發 (Core AI Logic)
目標： 開發能夠接收圖片、调用 AI 模型進行辨識，並回傳結構化 JSON 資料的 Python 函式。

✅ Task 2.1: 設計 AI Prompt (已完成)
✅ Task 2.2: 開發 OCR 與資料整理函式 (ocr_service.py) (已完成)

2.2.1: 建立一個 Python 函式 extract_card_data(image_path: str) -> list[dict]。
2.2.2: 在函式內，使用 fastapi-poe 的 upload_file_sync 上傳圖片。
2.2.3: 呼叫 Poe API (Gemini-2.5-Flash)，將圖片和設計好的 Prompt 一起發送。
2.2.4: 處理 API 回應，解析回傳的 JSON 陣列，轉換成 Python 列表。
2.2.5: 建立錯誤處理機制。如果 AI 回傳的不是有效的 JSON 或辨識失敗，應回傳 None。
2.2.6: **支援多張名片辨識**：單張圖片中若有多張名片，返回包含所有名片資料的列表。

Phase 3: 後端 API 服務開發 (Backend API Service)
目標： 建立一個 FastAPI 服務，它包含一個接收圖片上傳的端點。

✅ Task 3.1: 建立 Google Sheets 写入函式 (google_sheets_handler.py) (已完成)

3.1.1: 建立一個函式 append_to_sheet(data: dict | list[dict])。
3.1.2: 使用 Service Account credentials (JSON 檔) 進行 Google API 身份驗證。
3.1.3: 按照 Google Sheet 的欄位順序，將傳入的資料整理成列表。
3.1.4: 呼叫 Google Sheets API (spreadsheets.values.append)，將資料作為新的行附加到指定的試算表 tab 中。
3.1.5: **支援批次寫入**：若傳入多張名片資料（list[dict]），一次寫入多行。
3.1.6: **自動添加時間戳記**：每筆資料自動加上當前時間 (YYYY-MM-DD HH:MM:SS)。

✅ Task 3.2: 建立 API 端點 (main.py) (已完成)

3.2.1: 初始化 FastAPI 應用，配置 CORS 中間件。
3.2.2: 建立 POST 端點 /ocr/business-card。
3.2.3: 此端點接收 File 類型的上傳（UploadFile），支援 JPG/PNG 等圖片格式。
3.2.4: 端點邏輯：
  - 驗證上傳檔案類型
  - 讀取上傳的圖片檔案內容 (await file.read())
  - 將圖片儲存到臨時檔案
  - 呼叫 extract_card_data() 函式處理圖片，得到名片列表
  - 呼叫 append_to_sheet() 函式將所有名片資料寫入 Google Sheet
  - 回傳 JSON 響應：{"status": "success", "cards_count": N, "data": [...], "saved_to_sheet": true}
  - 錯誤處理：任一步驟失敗時回傳錯誤訊息
  - 清理臨時檔案
3.2.5: **支援多張名片**：單張圖片中的多張名片會全部辨識並寫入 Google Sheets。
3.2.6: 建立健康檢查端點 /health。

Phase 4: iPhone 捷徑設定 (Frontend Integration)
目標： 建立一個 iPhone 捷徑，讓使用者可以輕鬆地拍照並呼叫後端 API。

Task 4.1: 開發與測試捷徑
4.1.1: 在本地端電腦上，使用 uvicorn 運行 FastAPI 服務，並使用 ngrok 將其暴露到公網。例如：ngrok http 8000。記下 ngrok 提供的 https://*.ngrok-free.app URL。
4.1.2: 在 iPhone 上打開「捷徑」App，建立一個新捷徑。
4.1.3: 設計捷徑流程：
「拍照」： 從相機拍攝一張新照片。
「取得 URL 的內容」：
URL: 填入 ngrok 提供的 URL，並加上端點路徑（例如：https://your-ngrok-url.ngrok-free.app/ocr/business-card）。
方式 (Method): POST。
要求本文 (Request Body): 選擇「表單」(Form)，並新增一個欄位：
密鑰 (Key): file (需與 FastAPI 端點中接收的檔案名稱一致)
類型 (Type): File
值 (Value): 選擇包含「照片」的「魔法變數」。
4.1.4: (可選) 新增「顯示通知」或「朗讀文字」的動作，根據 API 回傳的 status 顯示「上傳成功」或「辨識失敗」。
4-1.5: 將此捷徑命名為「掃描名片」，並可選擇將其「加入主畫面」以便快速啟動。

Phase 5: 部署與優化 (Deployment & Optimization)
目標： 將服務部署到穩定的雲端環境，並進行優化。

Task 5.1: 部署後端服務

將 FastAPI 應用程式部署到雲端平台，例如 Vercel (支援 Python Serverless), Heroku, 或 AWS/GCP 的虛擬機/容器服務。
更新 iPhone 捷徑中的 URL，從 ngrok 的臨時 URL 更換為永久的部署 URL。
Task 5.2: (可選) 增加安全性

為您的 API 端點增加一層簡單的 API 金鑰驗證，並在 iPhone 捷徑的請求標頭 (Header) 中帶上此金鑰，防止被他人滥用。
Task 5.3: (可選) 紀錄與監控 (Logging)

在後端服務中加入日誌紀錄，方便追蹤辨識成功率和排查錯誤。