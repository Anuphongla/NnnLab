# agent_harness.py
import json
import os
from datetime import datetime

from dotenv import load_dotenv

from agent_tools import TOOLS

load_dotenv()

# Demo mode: ถ้าไม่มี API key ให้ใช้ mock LLM
api_key = os.getenv("GOOGLE_API_KEY")
DEMO_MODE = not api_key or api_key == "your_api_key_here"

if not DEMO_MODE:
    from google import genai
    client = genai.Client(api_key=api_key)
    MODEL = "gemini-2.5-flash"

SYSTEM_INSTRUCTION = """
คุณคือ Demi ผู้ช่วย AI ของร้าน MilkLab°
หน้าที่ของคุณคือแปลงคำสั่งภาษาไทยเป็น JSON action
ตอบกลับเป็น JSON เท่านั้น ในรูปแบบ:
{"action": "log_sale", "args": {"menu": "...", "quantity": N, "price": N}}
ถ้าคำสั่งไม่ใช่การบันทึกยอดขาย ตอบ: {"action": "unknown", "args": {}}
"""

TRACE_FILE = "agent_trace.log"


def write_trace(event: str, data: dict) -> None:
    with open(TRACE_FILE, "a", encoding="utf-8") as f:
        record = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            **data,
        }
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def mock_llm_response(user_input: str) -> str:
    """ใช้ simple regex ในโหมด demo เพื่อแปลงคำสั่งภาษาไทยเป็น action"""
    import re
    
    # ลองหา pattern: "บันทึก/ขาย + เมนู + จำนวน + ราคา"
    # เช่น "บันทึกยอดขายลาเต้น้ำผึ้ง 5 แก้ว ราคา 65 บาท"
    pattern = r'(?:บันทึก|ขาย|บันทึกยอดขาย)?(.+?)\s+(\d+)\s+(?:แก้ว|ชิ้น|ที่|อัน)?.*?(?:ราคา)?\s*(\d+(?:\.\d+)?)'
    match = re.search(pattern, user_input)
    
    if match:
        menu = match.group(1).strip()
        quantity = int(match.group(2))
        price = float(match.group(3))
        return json.dumps({
            "action": "log_sale",
            "args": {"menu": menu, "quantity": quantity, "price": price}
        }, ensure_ascii=False)
    
    return json.dumps({"action": "unknown", "args": {}}, ensure_ascii=False)


def run_agent(user_input: str) -> str:
    write_trace("user_input", {"message": user_input})

    if DEMO_MODE:
        raw = mock_llm_response(user_input)
    else:
        response = client.models.generate_content(
            model=MODEL,
            contents=f"{SYSTEM_INSTRUCTION}\n\nคำสั่ง: {user_input}",
        )
        raw = response.text.strip()
    
    write_trace("llm_response", {"raw": raw})

    try:
        action_data = json.loads(raw)
    except json.JSONDecodeError:
        return "❌ AI ตอบกลับในรูปแบบที่ไม่ถูกต้อง"

    action = action_data.get("action")
    args = action_data.get("args", {})

    if action not in TOOLS:
        return f"⚠️ ไม่รู้จัก action: {action}"

    try:
        result = TOOLS[action](**args)
        write_trace("tool_result", {"action": action, "result": result})
        return (
            f"✅ บันทึกสำเร็จ: {result['menu']} "
            f"x{result['quantity']} = {result['total']} บาท"
        )
    except (ValueError, TypeError) as e:
        write_trace("tool_error", {"action": action, "error": str(e)})
        return f"❌ ข้อมูลไม่ถูกต้อง: {e}"


if __name__ == "__main__":
    mode_text = "(Demo Mode ไม่ต้องใช้ API Key)" if DEMO_MODE else "(Production Mode)"
    print(f"🤖 Demi Agent พร้อมรับคำสั่ง {mode_text}")
    print("(พิมพ์ 'exit' เพื่อออก)\n")
    while True:
        user_input = input("คุณ: ").strip()
        if user_input.lower() == "exit":
            break
        print(f"Demi: {run_agent(user_input)}\n")
