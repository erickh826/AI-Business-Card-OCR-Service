import os
import json
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# --- 載入環境變數 ---
load_dotenv()

# --- Google Sheets 設定 ---
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CREDENTIALS_FILE = 'gtin-search-1733883862575-6bd198405b47.json'  # Google Service Account 的憑證檔案
SPREADSHEET_ID = os.getenv('GOOGLE_SHEET_ID')  # 從 .env 讀取
SHEET_NAME = os.getenv('GOOGLE_SHEET_NAME', 'Sheet1')  # 預設為 Sheet1

def append_to_sheet(data: dict | list[dict]) -> bool:
    """
    將名片資料寫入 Google Sheets（支援單張或多張名片）
    
    Args:
        data: 單一名片字典或名片字典列表，格式如下：
              單張: {"name": "張三", "title": "總經理", ...}
              多張: [{"name": "張三", ...}, {"name": "李四", ...}]
    
    Returns:
        bool: 成功回傳 True，失敗回傳 False
    """
    try:
        # --- 1. 驗證必要設定 ---
        if not SPREADSHEET_ID:
            raise ValueError("GOOGLE_SHEET_ID not found in .env file")
        
        if not os.path.exists(CREDENTIALS_FILE):
            raise FileNotFoundError(f"Credentials file not found: {CREDENTIALS_FILE}")
        
        # --- 2. 建立 Google API 身份驗證 ---
        credentials = Credentials.from_service_account_file(
            CREDENTIALS_FILE, 
            scopes=SCOPES
        )
        
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()
        
        # --- 3. 確保 data 為列表格式 ---
        if isinstance(data, dict):
            data_list = [data]
        elif isinstance(data, list):
            data_list = data
        else:
            raise ValueError(f"Invalid data type: {type(data)}. Expected dict or list[dict]")
        
        # --- 4. 整理資料成多行列表（按照 Google Sheet 欄位順序）---
        # 欄位順序: 姓名 | 公司 | 職稱 | 手機 | 辦公室電話 | Email | 網站 | 地址 | 時間戳記
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        rows_data = []
        for card in data_list:
            row = [
                card.get('name', ''),
                card.get('company', ''),
                card.get('title', ''),
                card.get('phone_mobile', ''),
                card.get('phone_office', ''),
                card.get('email', ''),
                card.get('website', ''),
                card.get('address', ''),
                timestamp,
            ]
            rows_data.append(row)
        
        # --- 5. 呼叫 Google Sheets API 寫入資料 ---
        range_name = f'{SHEET_NAME}!A:I'  # 資料寫入 A-I 欄（包含時間戳記）
        
        body = {
            'values': rows_data
        }
        
        result = sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name,
            valueInputOption='RAW',  # 或使用 'USER_ENTERED' 讓 Sheets 自動解析格式
            insertDataOption='INSERT_ROWS',
            body=body
        ).execute()
        
        rows_added = result.get('updates').get('updatedRows', 0)
        print(f"✅ Data successfully appended to Google Sheet")
        print(f"   Cards processed: {len(data_list)}")
        print(f"   Updated range: {result.get('updates').get('updatedRange')}")
        print(f"   Rows added: {rows_added}")
        
        return True
        
    except HttpError as error:
        print(f"❌ Google Sheets API error: {error}")
        return False
        
    except Exception as e:
        print(f"❌ Error appending to sheet: {e}")
        return False


# --- 測試函式 ---
if __name__ == "__main__":
    # 測試資料 - 單張名片
    test_single_card = {
        "name": "張三",
        "title": "軟體工程師",
        "company": "科技公司 A",
        "phone_mobile": "0912-345-678",
        "phone_office": "02-1234-5678",
        "email": "zhang@example.com",
        "website": "https://example-a.com",
        "address": "台北市信義區信義路五段7號"
    }
    
    # 測試資料 - 多張名片
    test_multiple_cards = [
        {
            "name": "李四",
            "title": "產品經理",
            "company": "創新企業 B",
            "phone_mobile": "0922-111-222",
            "phone_office": "02-2222-3333",
            "email": "li@company-b.com",
            "website": "https://company-b.com",
            "address": "新北市板橋區文化路一段100號"
        },
        {
            "name": "王五",
            "title": "設計總監",
            "company": "設計工作室 C",
            "phone_mobile": "0933-444-555",
            "phone_office": "02-3333-4444",
            "email": "wang@studio-c.com",
            "website": "https://studio-c.design",
            "address": "台中市西屯區台灣大道三段99號"
        },
        {
            "name": "趙六",
            "title": "行銷總監",
            "company": "廣告代理商 D",
            "phone_mobile": "0944-666-777",
            "phone_office": "07-5555-6666",
            "email": "zhao@agency-d.com",
            "website": "https://agency-d.com.tw",
            "address": "高雄市前鎮區中山二路88號"
        }
    ]
    
    print("=" * 60)
    print("Testing Google Sheets Integration")
    print("=" * 60)
    
    # 測試 1: 單張名片
    print("\n📝 Test 1: Single Card")
    print("-" * 60)
    success1 = append_to_sheet(test_single_card)
    
    if success1:
        print("✅ Single card test passed!")
    else:
        print("❌ Single card test failed!")
    
    # 測試 2: 多張名片
    print("\n📝 Test 2: Multiple Cards (3 cards)")
    print("-" * 60)
    success2 = append_to_sheet(test_multiple_cards)
    
    if success2:
        print("✅ Multiple cards test passed!")
    else:
        print("❌ Multiple cards test failed!")
    
    # 總結
    print("\n" + "=" * 60)
    if success1 and success2:
        print("🎉 All tests passed!")
    else:
        print("⚠️ Some tests failed. Please check error messages above.")
    print("=" * 60)
