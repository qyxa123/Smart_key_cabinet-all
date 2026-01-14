
from app import app, db
from models import BorrowRecord, Key, User

def inspect_db():
    with app.app_context():
        print("=== 正在检查未归还的借用记录 ===")
        active_records = BorrowRecord.query.filter_by(status='borrowed').all()
        
        if not active_records:
            print("没有发现未归还的借用记录。")
        else:
            for record in active_records:
                print(f"记录ID: {record.id}")
                print(f"  钥匙: {record.key.room} (ID: {record.key_id})")
                print(f"  借用人: {record.user.name} (ID: {record.user_id})")
                print(f"  借用时间: {record.borrow_time}")
                print(f"  状态: {record.status}")
                print("-" * 30)

        print("\n=== 检查所有钥匙状态 ===")
        keys = Key.query.all()
        for key in keys:
            # 检查这把钥匙是否有未归还记录
            record = BorrowRecord.query.filter_by(key_id=key.id, status='borrowed').first()
            status = f"被 {record.user.name} 借用" if record else "可用"
            print(f"钥匙 {key.room} (ID: {key.id}): {status}")

if __name__ == "__main__":
    inspect_db()
