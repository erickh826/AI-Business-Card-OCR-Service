import os
import base64
import json
import re # 匯入正規表示式函式庫
import asyncio
from dotenv import load_dotenv
import fastapi_poe as fp

# --- 1. 載入環境變數 ---
load_dotenv()
POE_API_TOKEN = os.getenv("POE_API_TOKEN")

# --- 新增的輔助函式：從字串中提取 JSON ---
def extract_json_from_string(text: str) -> str | None:
    """
    使用正規表示式從可能包含 Markdown 的字串中提取 JSON 物件或陣列。
    """
    # 尋找被 ```json ... ``` 或 ``` ... ``` 包裹的內容（物件或陣列）
    match = re.search(r'```(json)?\s*([\[\{].*?[\]\}])\s*```', text, re.DOTALL)
    if match:
        # 如果找到，回傳第二個捕獲組
        return match.group(2)
    
    # 如果沒有找到 Markdown 區塊，檢查是否為 JSON 物件或陣列
    stripped = text.strip()
    if (stripped.startswith('{') and stripped.endswith('}')) or \
       (stripped.startswith('[') and stripped.endswith(']')):
        return stripped
        
    return None

# --- 2. 定義核心函式 (支援多張名片) ---
async def extract_card_data_async(image_path: str) -> list[dict] | None:
    """
    接收圖片路徑，使用 fastapi-poe 進行 OCR（異步版本），
    並從回傳的字串中提取 JSON 資料。
    
    Returns:
        list[dict]: 名片資料列表，每個元素為一張名片的資訊
                   如果圖片中只有一張名片，返回包含單一元素的列表
                   如果辨識失敗，返回 None
    """
    if not POE_API_TOKEN:
        raise ValueError("POE_API_TOKEN not found in .env file")

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at path: {image_path}")

    prompt_text = """
You are an expert business card OCR data extraction agent. Your task is to analyze the provided image and extract key information from ALL business cards present in the image.

For each business card, extract: name, title, company, phone_mobile, phone_office, email, website, address.

IMPORTANT:
- If there is ONLY ONE card in the image, return a JSON array with one object: [{...}]
- If there are MULTIPLE cards in the image, return a JSON array with multiple objects: [{...}, {...}, ...]
- Your response MUST be a valid JSON array, and NOTHING else.
- Do not include any explanatory text or markdown formatting like ```json.

Example for single card:
[{"name": "John Doe", "title": "Manager", "company": "ABC Corp", "phone_mobile": "0912-345-678", "phone_office": "02-1234-5678", "email": "john@abc.com", "website": "https://abc.com", "address": "123 Main St"}]

Example for multiple cards:
[{"name": "John Doe", ...}, {"name": "Jane Smith", ...}]
"""
    try:
        # --- 使用異步方式上傳圖片 ---
        print("☁️ Uploading file to Poe...")
        with open(image_path, "rb") as f:
            image_upload = fp.upload_file_sync(f, api_key=POE_API_TOKEN)
        
        message = fp.ProtocolMessage(
            role="user",
            content=prompt_text,
            attachments=[image_upload]
        )

        print("🚀 Sending request to Poe...")
        
        full_response_text = ""
        async for partial in fp.get_bot_response(
            messages=[message],
            bot_name="Gemini-2.5-Flash",
            api_key=POE_API_TOKEN
        ):
            full_response_text += partial.text
        
        if not full_response_text.strip():
            print("❌ Error: API returned an empty response.")
            return None

        print(f"✅ API Response Received. Raw content:\n---\n{full_response_text}\n---")

        # --- 使用新的輔助函式來提取 JSON ---
        json_string = extract_json_from_string(full_response_text)
        
        if not json_string:
            print("❌ Error: Could not find a valid JSON object in the API response.")
            return None
            
        print(f"✅ Successfully extracted JSON string:\n---\n{json_string}\n---")
        
        extracted_json = json.loads(json_string)
        
        # 確保返回的是列表
        if isinstance(extracted_json, dict):
            # 如果 AI 返回單一物件而非陣列，將其包裝成陣列
            print("⚠️ Warning: AI returned single object instead of array. Wrapping it.")
            extracted_json = [extracted_json]
        elif not isinstance(extracted_json, list):
            print(f"❌ Error: Unexpected JSON type: {type(extracted_json)}")
            return None
        
        print(f"📋 Extracted {len(extracted_json)} card(s) from image")
        return extracted_json

    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        return None


def extract_card_data(image_path: str) -> list[dict] | None:
    """
    同步包裝函式，內部調用異步版本
    """
    try:
        # 嘗試獲取現有的事件循環
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # 如果循環正在運行，創建新的事件循環
            import nest_asyncio
            nest_asyncio.apply()
            return loop.run_until_complete(extract_card_data_async(image_path))
        else:
            return loop.run_until_complete(extract_card_data_async(image_path))
    except RuntimeError:
        # 如果沒有事件循環，創建一個新的
        return asyncio.run(extract_card_data_async(image_path))

# --- 3. 測試程式碼 ---
if __name__ == "__main__":
    TEST_IMAGE = "test_card.jpg"
    print(f"--- Starting Business Card OCR Test for '{TEST_IMAGE}' ---")
    cards_info = extract_card_data(TEST_IMAGE)
    
    if cards_info:
        print(f"\n--- OCR Result: {len(cards_info)} card(s) found ---")
        print(json.dumps(cards_info, indent=2, ensure_ascii=False))
        print("\n🎉 --- Phase 2 Complete! --- 🎉")
    else:
        print("\n--- Test Failed. Please check the error messages above. ---")
