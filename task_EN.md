# Project: AI Business Card OCR Service

**Objective:** Build an automated workflow where users can take photos of business cards via iPhone Shortcuts, call a backend AI service for text recognition (OCR) and data processing, and ultimately save structured contact information to a designated Google Sheet.

## Tech Stack

- **Frontend Trigger:** Apple iPhone "Shortcuts" App
- **Backend Service Framework:** Python (using FastAPI)
- **AI Vision Model API:** Gemini 2.5 Flash (via Poe API)
- **Data Storage:** Google Sheets API
- **Development/Testing Tool:** ngrok (to expose local API to iPhone during development)

---

## ✅ Phase 1: Environment Setup & Prerequisites (Completed)

**Objective:** Ensure all necessary tools, API keys, and permissions are ready.

### Task 1.1: Prepare Google Sheet & API Permissions
- 1.1.1: Create a new spreadsheet in Google Sheets named `Business_Card_Contacts`
- 1.1.2: Set column headers: Name, Company, Title, Mobile_Phone, Office_Phone, Email, Website, Address, Timestamp
- 1.1.3: Go to Google Cloud Console and create a new project
- 1.1.4: Enable Google Sheets API and Google Drive API in the project
- 1.1.5: Create a Service Account, download its JSON credential key (`credentials.json`), and keep it secure
- 1.1.6: Add the service account email (format: `...@...gserviceaccount.com`) as "Editor" to your Google Sheet

### Task 1.2: Obtain AI Model API Key
- Choose one:
  - **Option A (Poe):** Log in to Poe account and obtain your API Key
  - **Option B (Azure):** Create AI service resource in Azure Portal, get Gemini model Endpoint and API Key

### Task 1.3: Setup Local Development Environment
- 1.3.1: Install Python 3.9+
- 1.3.2: Install required Python packages:
  ```bash
  pip install -r requirements.txt
  ```
- 1.3.3: Download and configure ngrok to expose local API service to public internet during development

---

## ✅ Phase 2: Core AI Logic Development (Completed)

**Objective:** Develop Python functions to receive images, call AI models for recognition, and return structured JSON data.

### ✅ Task 2.1: Design AI Prompt (Completed)

### ✅ Task 2.2: Develop OCR & Data Processing Function (`ocr_service.py`) (Completed)
- 2.2.1: Create a Python function `extract_card_data(image_path: str) -> list[dict]`
- 2.2.2: Use `fastapi-poe`'s `upload_file_async` to upload images
- 2.2.3: Call Poe API (Gemini-2.5-Flash) with the image and designed prompt
- 2.2.4: Process API response, parse returned JSON array, convert to Python list
- 2.2.5: Implement error handling mechanism. Return `None` if AI returns invalid JSON or recognition fails
- 2.2.6: **Support multiple card recognition**: If there are multiple cards in a single image, return a list containing all card data

---

## ✅ Phase 3: Backend API Service Development (Completed)

**Objective:** Build a FastAPI service with an endpoint to receive image uploads.

### ✅ Task 3.1: Create Google Sheets Write Function (`google_sheets_handler.py`) (Completed)
- 3.1.1: Create a function `append_to_sheet(data: dict | list[dict])`
- 3.1.2: Use Service Account credentials (JSON file) for Google API authentication
- 3.1.3: Organize incoming data into a list according to Google Sheet column order
- 3.1.4: Call Google Sheets API (`spreadsheets.values.append`) to append data as new rows to the specified spreadsheet tab
- 3.1.5: **Support batch write**: If multiple card data is passed (`list[dict]`), write multiple rows at once
- 3.1.6: **Auto-add timestamp**: Each record automatically includes current time (YYYY-MM-DD HH:MM:SS)

### ✅ Task 3.2: Create API Endpoint (`main.py`) (Completed)
- 3.2.1: Initialize FastAPI application, configure CORS middleware
- 3.2.2: Create POST endpoint `/ocr/business-card`
- 3.2.3: This endpoint receives File type upload (UploadFile), supports JPG/PNG image formats
- 3.2.4: Endpoint logic:
  - Validate uploaded file type
  - Read uploaded image file content (`await file.read()`)
  - Save image to temporary file
  - Call `extract_card_data()` function to process image, get card list
  - Call `append_to_sheet()` function to write all card data to Google Sheet
  - Return JSON response: `{"status": "success", "cards_count": N, "data": [...], "saved_to_sheet": true}`
  - Error handling: return error message when any step fails
  - Clean up temporary files
- 3.2.5: **Support multiple cards**: All cards in a single image will be recognized and written to Google Sheets
- 3.2.6: Create health check endpoint `/health`

---

## 📱 Phase 4: iPhone Shortcuts Setup (Frontend Integration)

**Objective:** Create an iPhone Shortcut that allows users to easily take photos and call the backend API.

### Task 4.1: Develop and Test Shortcut
- 4.1.1: On local computer, run FastAPI service using uvicorn and expose it to public internet using ngrok. Example: `ngrok http 8000`. Note down the ngrok-provided `https://*.ngrok-free.app` URL
- 4.1.2: Open "Shortcuts" App on iPhone and create a new shortcut
- 4.1.3: Design shortcut workflow:
  - **"Take Photo"**: Capture a new photo from camera
  - **"Get Contents of URL"**:
    - URL: Enter the ngrok-provided URL with endpoint path (e.g., `https://your-ngrok-url.ngrok-free.app/ocr/business-card`)
    - Method: POST
    - Request Body: Select "Form" and add a field:
      - Key: `file` (must match the file parameter name in FastAPI endpoint)
      - Type: File
      - Value: Select "Photo" magic variable
- 4.1.4: (Optional) Add "Show Notification" or "Speak Text" action to display "Upload Successful" or "Recognition Failed" based on API response status
- 4.1.5: Name this shortcut "Scan Business Card", and optionally "Add to Home Screen" for quick launch

---

## 🚀 Phase 5: Deployment & Optimization

**Objective:** Deploy service to stable cloud environment and perform optimization.

### Task 5.1: Deploy Backend Service
- Deploy FastAPI application to cloud platform, such as Vercel (supports Python Serverless), Heroku, or AWS/GCP virtual machines/container services
- Update URL in iPhone Shortcut from ngrok's temporary URL to permanent deployment URL

---

## 📦 Package Installation

All required packages are listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Package List
- `fastapi==0.124.0` - Web framework
- `fastapi-poe==0.0.81` - Poe API client
- `google-api-python-client==2.175.0` - Google Sheets API
- `nest-asyncio==1.6.0` - Async event loop support
- `protobuf==6.33.2` - Protocol buffers
- `python-dotenv==1.2.1` - Environment variable management
- `uvicorn==0.38.0` - ASGI server

---

## 🎯 Project Status

- ✅ Phase 1: Environment Setup - **Completed**
- ✅ Phase 2: Core AI Logic - **Completed**
- ✅ Phase 3: Backend API Service - **Completed**
- 🔄 Phase 4: iPhone Shortcuts Setup - **In Progress**
- ⏳ Phase 5: Deployment & Optimization - **Pending**
