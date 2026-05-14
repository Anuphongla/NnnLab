# sales_logger.py
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from sheets_client import get_sheet

def main():
    # โหลด env variables จาก .env
    load_dotenv()

    # รับยอดขายจาก command line ในรูปแบบ เมนู:จำนวน:ราคา
    if len(sys.argv) < 2:
        print("Usage: python sales_logger.py 'เมนู:จำนวน:ราคา' ['เมนู:จำนวน:ราคา' ...]")
        sys.exit(1)

    sales_data = []
    total = 0

    for arg in sys.argv[1:]:
        try:
            menu, quantity, price = arg.split(':')
            quantity = int(quantity)
            price = float(price)
            subtotal = quantity * price
            total += subtotal
            # เพิ่มวันที่
            sales_data.append([str(datetime.now().date()), menu, str(quantity), str(price), str(subtotal)])
        except ValueError:
            print(f"Invalid format: {arg}. Expected 'เมนู:จำนวน:ราคา'")
            sys.exit(1)

    # คำนวณยอดรวม
    print(f"Total sales: {total}")

    # ใช้ get_sheet().append_row([...]) เพิ่มแถวใหม่
    try:
        sheet = get_sheet()
        for row in sales_data:
            sheet.append_row(row)
        print("Sales data logged successfully.")
    except Exception as e:
        print(f"Error logging sales: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()