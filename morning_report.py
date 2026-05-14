import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests
from sheets_client import get_sheet
from collections import Counter

def get_yesterday_sales():
    """ดึงข้อมูลยอดขายของเมื่อวาน"""
    load_dotenv()
    
    sheet = get_sheet()
    all_rows = sheet.get_all_values()
    
    # Skip header row
    if len(all_rows) <= 1:
        return []
    
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    yesterday_sales = []
    
    for row in all_rows[1:]:
        if len(row) >= 5 and row[0] == yesterday:
            # row: [date, menu, quantity, price, subtotal]
            yesterday_sales.append({
                "date": row[0],
                "menu": row[1],
                "quantity": int(row[2]),
                "price": float(row[3]),
                "subtotal": float(row[4])
            })
    
    return yesterday_sales

def calculate_summary(sales):
    """คำนวณยอดรวมและเมนูที่ขายดีสุด"""
    if not sales:
        return None
    
    total = sum(s["subtotal"] for s in sales)
    
    # หาเมนูที่ขายได้มากสุด (จำนวน)
    menu_quantities = Counter(s["menu"] for s in sales)
    best_menu = menu_quantities.most_common(1)[0][0]
    best_menu_quantity = menu_quantities.most_common(1)[0][1]
    
    # หาเมนูที่ขายได้เงินมากสุด
    menu_revenue = {}
    for s in sales:
        menu_revenue[s["menu"]] = menu_revenue.get(s["menu"], 0) + s["subtotal"]
    
    best_revenue_menu = max(menu_revenue, key=menu_revenue.get)
    best_revenue_amount = menu_revenue[best_revenue_menu]
    
    return {
        "total": total,
        "best_menu": best_menu,
        "best_menu_quantity": best_menu_quantity,
        "best_revenue_menu": best_revenue_menu,
        "best_revenue_amount": best_revenue_amount,
        "total_items": len(sales)
    }

def send_to_telegram(summary):
    """ส่งรายงานไปที่ Telegram"""
    load_dotenv()
    
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not telegram_token or not telegram_chat_id:
        print("❌ ไม่พบ TELEGRAM_BOT_TOKEN หรือ TELEGRAM_CHAT_ID")
        return False
    
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    message = f"""
📊 รายงานเช้าของ NnnLab 📊
วันที่: {yesterday}

💰 ยอดขายรวม: {summary['total']:.2f} บาท
📦 จำนวนรายการ: {summary['total_items']} รายการ

🎯 เมนูที่ขายได้มากสุด: {summary['best_menu']} ({summary['best_menu_quantity']} ชิ้น)
💸 เมนูที่ขายได้เงินมากสุด: {summary['best_revenue_menu']} ({summary['best_revenue_amount']:.2f} บาท)

วันนี้ขายดีมากเลยนะ! 🎉✨
    """
    
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    payload = {
        "chat_id": telegram_chat_id,
        "text": message.strip()
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ ส่งรายงานไปที่ Telegram สำเร็จ!")
            return True
        else:
            print(f"❌ ส่ง Telegram ล้มเหลว: {response.text}")
            return False
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        return False

def main():
    sales = get_yesterday_sales()
    
    if not sales:
        print(f"ไม่มีข้อมูลยอดขายเมื่อวาน")
        return
    
    summary = calculate_summary(sales)
    print(f"\n📊 สรุปยอดขาย:")
    print(f"ยอดรวม: {summary['total']:.2f} บาท")
    print(f"เมนูดาวเด่น: {summary['best_menu']}")
    print()
    
    send_to_telegram(summary)

if __name__ == "__main__":
    main()