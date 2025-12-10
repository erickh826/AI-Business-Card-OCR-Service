import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import tempfile
from typing import Dict, Any

# 引入我們自己開發的模組
from ocr_service import extract_card_data
from google_sheets_handler import append_to_sheet

# --- 初始化 FastAPI 應用 ---
app = FastAPI(
    title="Business Card OCR API",
    description="API for extracting business card information and saving to Google Sheets",
    version="1.0.0"
)

# --- CORS 設定（允許前端跨域請求）---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生產環境應該設定具體的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 根路徑（健康檢查）---
@app.get("/")
async def root():
    """API 健康檢查端點"""
    return {
        "status": "running",
        "message": "Business Card OCR API is running",
        "version": "1.0.0"
    }

# --- 名片 OCR 端點 ---
@app.post("/ocr/business-card")
async def process_business_card(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    接收名片圖片上傳，進行 OCR 辨識，並將結果寫入 Google Sheets
    
    Args:
        file: 上傳的圖片檔案（支援 JPG, PNG 等格式）
    
    Returns:
        包含狀態和辨識資料的 JSON 響應
    """
    temp_file_path = None
    
    try:
        # --- 1. 驗證檔案類型 ---
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type: {file.content_type}. Please upload an image file."
            )
        
        print(f"📥 Received file: {file.filename} ({file.content_type})")
        
        # --- 2. 讀取上傳的圖片內容 ---
        image_bytes = await file.read()
        
        if not image_bytes:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty"
            )
        
        # --- 3. 將圖片儲存到臨時檔案（因為 extract_card_data 需要檔案路徑）---
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            temp_file.write(image_bytes)
            temp_file_path = temp_file.name
        
        print(f"💾 Saved to temporary file: {temp_file_path}")
        
        # --- 4. 呼叫 OCR 函式進行辨識（可能返回多張名片）---
        print("🔍 Starting OCR processing...")
        extracted_data = extract_card_data(temp_file_path)
        
        if not extracted_data or len(extracted_data) == 0:
            raise HTTPException(
                status_code=500,
                detail="OCR processing failed. Unable to extract data from the image."
            )
        
        print(f"✅ OCR completed. Extracted {len(extracted_data)} card(s): {extracted_data}")
        
        # --- 5. 將辨識結果寫入 Google Sheets ---
        print("📊 Writing data to Google Sheets...")
        sheet_success = append_to_sheet(extracted_data)
        
        if not sheet_success:
            # 即使 Google Sheets 寫入失敗，仍然回傳 OCR 結果
            return JSONResponse(
                status_code=200,
                content={
                    "status": "partial_success",
                    "message": f"OCR found {len(extracted_data)} card(s) but failed to save to Google Sheets",
                    "cards_count": len(extracted_data),
                    "data": extracted_data,
                    "saved_to_sheet": False
                }
            )
        
        # --- 6. 成功回應 ---
        return {
            "status": "success",
            "message": f"Successfully processed {len(extracted_data)} business card(s)",
            "cards_count": len(extracted_data),
            "data": extracted_data,
            "saved_to_sheet": True
        }
    
    except HTTPException:
        # 重新拋出 HTTP 異常
        raise
    
    except Exception as e:
        # 捕捉所有其他錯誤
        print(f"❌ Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )
    
    finally:
        # --- 清理臨時檔案 ---
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
                print(f"🗑️ Cleaned up temporary file: {temp_file_path}")
            except Exception as e:
                print(f"⚠️ Failed to delete temporary file: {e}")


# --- 查詢端點（可選）---
@app.get("/health")
async def health_check():
    """詳細的健康檢查，包含各服務狀態"""
    status = {
        "api": "running",
        "poe_api_configured": bool(os.getenv("POE_API_TOKEN")),
        "google_sheets_configured": bool(os.getenv("GOOGLE_SHEET_ID"))
    }
    
    return {
        "status": "healthy" if all(status.values()) else "degraded",
        "services": status
    }


# --- 啟動說明 ---
if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("🚀 Starting Business Card OCR API Server")
    print("=" * 60)
    print("\n📝 To start the server, run:")
    print("   uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    print("\n📖 API Documentation will be available at:")
    print("   http://localhost:8000/docs")
    print("\n" + "=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
