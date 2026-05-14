# Caption generator for MilkLab cafe Instagram posts
# - สร้างแคปชั่นภาษาไทย 3 แบบ
# - รับชื่อเมนูและราคาแล้วโชว์ออกมาแบบเป็นกันเอง
import argparse


def format_price(price: str) -> str:
    price = price.strip()
    if price == "":
        return "ราคาไม่ระบุ"
    if any(char.isdigit() for char in price) and "บาท" not in price:
        return f"{price} บาท"
    return price


def generate_captions(menu: str, price: str) -> list[str]:
    menu = menu.strip()
    price = format_price(price)
    menu_text = menu if menu else "เมนูเด็ด"

    return [
        f"ลองชิม {menu_text} ที่ Nnnab Cafe กันนะคะ 🧁 \nราคาน่ารักแค่ {price} เท่านั้นเอง ฟินคุ้มทุกคำเลย",
        f"เมนูใหม่ของเรา: {menu_text} — {price} \nสวย เรียบง่าย แต่รสชาตินี่ใช่เลย",
        f"สายคาเฟ่จ๋า บอกเลยว่า {menu_text} {price} นี้ต้องลอง 💫 \nคาเฟ่สไตล์ Chill ที่จะทำให้วันธรรมดาของคุณสนุกขึ้น",
    ]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="สร้างแคปชั่น IG ภาษาไทยแบบเป็นกันเองสำหรับ Nnnab Cafe"
    )
    parser.add_argument("--menu", "-m", help="ชื่อเมนู ")
    parser.add_argument("--price", "-p", help="ราคา ")
    args = parser.parse_args()

    menu = args.menu
    price = args.price

    if not menu:
        menu = input("พิมพ์ชื่อเมนูที่ต้องการให้สร้างแคปชั่น: ").strip()
    if not price:
        price = input("พิมพ์ราคาของเมนู : ").strip()

    captions = generate_captions(menu, price)

    print("\n✨ แคปชั่นภาษาไทยสำหรับโพสต์ IG ของคุณ")
    for index, caption in enumerate(captions, start=1):
        print(f"\n[{index}] {caption}")
    print("\nพร้อมแชร์แล้วจ้า! 😄")


if __name__ == "__main__":
    main()

