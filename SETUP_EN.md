# 🚀 Business Card Scanner - Setup Guide

## 📋 Required API Keys and Credentials

Before using this project, please prepare the following API keys and credentials:

---

## 1️⃣ Poe API Token

### Purpose
Used to call the Gemini-2.5-Flash model for business card OCR recognition

### How to Obtain
1. Go to **Poe Official Website**: https://poe.com/
2. Log in to your account
3. Navigate to **API Settings Page**: https://poe.com/api_key
4. Click "Create API Key" to generate a new API key
5. Copy the generated API Token (format: `poe-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)

### Important Notes
- ⚠️ API Token is displayed only once, save it immediately
- 💰 Poe API is a paid service, ensure your account has sufficient balance
- 📊 Check usage: https://poe.com/api_usage

### Environment Variable Setup
```bash
POE_API_TOKEN=poe-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 2️⃣ Google Sheets API Credentials

### Purpose
Used to automatically write recognition results to Google Sheets

### How to Obtain

#### Step 1: Create a Google Cloud Project
1. Go to **Google Cloud Console**: https://console.cloud.google.com/
2. Click "Select Project" → "New Project"
3. Enter project name (e.g., `business-card-scanner`)
4. Click "Create"

#### Step 2: Enable Google Sheets API
1. In Google Cloud Console, select the project you just created
2. Go to "APIs & Services" → "Library"
3. Search for "Google Sheets API"
4. Click "Enable"

#### Step 3: Create a Service Account
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Enter service account name (e.g., `sheets-writer`)
4. Click "Create and Continue"
5. Select role as "Editor"
6. Click "Done"

#### Step 4: Download JSON Credential File
1. On the "Credentials" page, find the service account you just created
2. Click on the service account name
3. Switch to the "Keys" tab
4. Click "Add Key" → "Create New Key"
5. Select "JSON" format
6. Click "Create", the JSON file will be automatically downloaded
7. Rename the downloaded JSON file and place it in the project root directory:
   ```
   /Users/kahochow/project/ai_model/business_card_scanner/credentials.json
   ```

#### Step 5: Create Google Sheets and Set Permissions
1. Go to **Google Sheets**: https://sheets.google.com/
2. Create a new spreadsheet (or use an existing one)
3. Create column headers in the spreadsheet (recommended for the first row):
   ```
   Name | Company | Title | Mobile | Office Phone | Email | Website | Address | Timestamp
   ```
4. Click the "Share" button in the upper right corner
5. Copy the `client_email` field value from the JSON credential file (format: `xxx@xxx.iam.gserviceaccount.com`)
6. Add this email address to shared users with "Editor" permission
7. Copy the Spreadsheet ID from the spreadsheet URL:
   ```
   https://docs.google.com/spreadsheets/d/SPREADSHEET_ID_HERE/edit
   ```

### Environment Variable Setup
```bash
GOOGLE_SHEET_ID=your_spreadsheet_id_here
GOOGLE_SHEET_NAME=Sheet1
```

---

## 3️⃣ Ngrok Authtoken (for iPhone Shortcuts)

### Purpose
Used to expose local FastAPI service to the public internet, allowing iPhone to access it

### How to Obtain
1. Go to **Ngrok Official Website**: https://ngrok.com/
2. Sign up or log in to your account
3. Go to Dashboard: https://dashboard.ngrok.com/
4. Copy your Authtoken (in the "Getting Started" → "Your Authtoken" section)

### Setup Method
```bash
ngrok config add-authtoken YOUR_AUTHTOKEN_HERE
```

### Important Notes
- 🆓 Free version generates a new URL each time ngrok is restarted
- ⚠️ Need to update API URL in iPhone Shortcuts whenever URL changes
- 💎 Paid version allows fixed custom domains

---

## 📝 Complete .env File Example

Create a `.env` file in the project root directory (or copy `.env.example`):

```bash
# Poe API Token (for OCR)
POE_API_TOKEN=poe-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Google Sheets Configuration
GOOGLE_SHEET_ID=1234567890abcdefghijklmnopqrstuvwxyz
GOOGLE_SHEET_NAME=Sheet1
```

---

## ✅ Checklist

After setup, please confirm the following files and settings are ready:

- [ ] `.env` file created with `POE_API_TOKEN`
- [ ] `.env` file contains `GOOGLE_SHEET_ID` and `GOOGLE_SHEET_NAME`
- [ ] `credentials.json` or `gtin-search-*.json` placed in project root directory
- [ ] Google Sheets has added Service Account email as shared user (Editor permission)
- [ ] Ngrok authtoken configured (run `ngrok config add-authtoken`)
- [ ] All necessary Python packages installed:
  ```bash
  pip install -r requirements.txt
  ```
  Or manually install:
  ```bash
  pip install fastapi==0.124.0 fastapi-poe==0.0.81 google-api-python-client==2.175.0 nest-asyncio==1.6.0 protobuf==6.33.2 python-dotenv==1.2.1 uvicorn==0.38.0
  ```

---

## 🧪 Test Setup

### Test 1: Check Environment Variables
```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('POE_API_TOKEN:', 'OK' if os.getenv('POE_API_TOKEN') else 'MISSING'); print('GOOGLE_SHEET_ID:', 'OK' if os.getenv('GOOGLE_SHEET_ID') else 'MISSING')"
```

### Test 2: Test Google Sheets Connection
```bash
python google_sheets_handler.py
```

### Test 3: Test OCR Functionality
```bash
python ocr_service.py
```

### Test 4: Start FastAPI Service
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
Then visit: http://localhost:8000/docs

### Test 5: Start Ngrok
```bash
ngrok http 8000
```

---

## 🆘 Common Issues

### Q1: Poe API returns 401 Unauthorized
**A:** Check if `POE_API_TOKEN` is correct and ensure account has sufficient balance

### Q2: Google Sheets API returns 403 Forbidden
**A:** Ensure Service Account email has been added to spreadsheet's shared users

### Q3: Ngrok connection failed
**A:** Verify authtoken is configured correctly: `ngrok config check`

### Q4: iPhone Shortcuts returns 422 error
**A:** Check if "Request Body" in Shortcuts is set to "Form" and field name is `file`

---

## 📚 Related Links

- **Poe API Documentation**: https://creator.poe.com/docs/quick-start
- **Google Sheets API Documentation**: https://developers.google.com/sheets/api/guides/concepts
- **Ngrok Documentation**: https://ngrok.com/docs
- **FastAPI Documentation**: https://fastapi.tiangolo.com/

---

## 🔐 Security Reminders

⚠️ **Important**:
- Do not commit `.env` files and `credentials.json` to Git
- Do not share your API Tokens publicly
- Regularly check API usage to avoid excess charges
- Use `.gitignore` to ensure sensitive information is not uploaded

---

**After setup is complete, please refer to `README.md` to start using this project!** 🎉
