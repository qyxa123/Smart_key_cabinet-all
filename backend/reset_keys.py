
from app import app, db
from models import BorrowRecord, Key
from datetime import datetime

def reset_all_keys():
    with app.app_context():
        print("=== 开始重置所有钥匙状态 ===")
        active_records = BorrowRecord.query.filter_by(status='borrowed').all()
        
        if not active_records:
            print("没有发现未归还的记录，无需重置。")
            return

        count = 0
        for record in active_records:
            print(f"正在归还: 钥匙 {record.key.room} (借用人: {record.user.name})")
            record.status = 'returned'
            record.return_time = datetime.utcnow()
            
            # 同时更新用户和钥匙的多对多关系（如果还在的话）
            if record.key in record.user.keys:
                record.user.keys.remove(record.key)
            
            count += 1
        
        db.session.commit()
        print(f"=== 重置完成，共归还 {count} 把钥匙 ===")

if __name__ == "__main__":
    reset_all_keys()
