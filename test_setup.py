#!/usr/bin/env python3
"""
快速设置测试数据的脚本
"""
import sys
import os

# 添加backend目录到路径
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

from app import app
from extensions import db
from models import User, Key, BorrowRecord

def setup_test_data():
    """创建测试数据"""
    with app.app_context():
        # 创建所有表
        db.create_all()
        
        # 检查是否已有数据
        if User.query.count() > 0:
            print("数据库中已有数据，跳过初始化")
            return
        
        print("创建测试数据...")
        
        # 创建测试用户
        users = [
            User(name="张三", identity="student", student_id="202401", grade="2024", class_="1班"),
            User(name="李四", identity="student", student_id="202402", grade="2024", class_="2班"),
            User(name="王老师", identity="teacher", student_id="T001", office="办公室A"),
            User(name="赵老师", identity="teacher", student_id="T002", office="办公室B"),
        ]
        
        # 创建测试钥匙
        keys = [
            Key(room="101"),
            Key(room="102"),
            Key(room="103"),
            Key(room="201"),
            Key(room="202"),
        ]
        
        # 添加到数据库
        for user in users:
            db.session.add(user)
        
        for key in keys:
            db.session.add(key)
        
        db.session.commit()
        
        print(f"✓ 创建了 {len(users)} 个用户")
        print(f"✓ 创建了 {len(keys)} 把钥匙")
        
        # 创建一些示例借用记录
        from datetime import datetime, timedelta
        
        # 张三借用101房间（已归还）
        record1 = BorrowRecord(
            user_id=users[0].id,
            key_id=keys[0].id,
            reason="需要准备期末考试复习材料",
            borrow_time=datetime.utcnow() - timedelta(days=2),
            return_time=datetime.utcnow() - timedelta(days=1),
            status="returned"
        )
        
        # 李四借用102房间（未归还）
        record2 = BorrowRecord(
            user_id=users[1].id,
            key_id=keys[1].id,
            reason="班级活动准备，需要布置教室",
            borrow_time=datetime.utcnow() - timedelta(hours=3),
            status="borrowed"
        )
        
        # 王老师借用201房间（已归还）
        record3 = BorrowRecord(
            user_id=users[2].id,
            key_id=keys[3].id,
            reason="教学设备检查和维护",
            borrow_time=datetime.utcnow() - timedelta(days=1, hours=2),
            return_time=datetime.utcnow() - timedelta(hours=1),
            status="returned"
        )
        
        # 张三再次借用103房间（未归还）
        record4 = BorrowRecord(
            user_id=users[0].id,
            key_id=keys[2].id,
            reason="社团活动需要使用教室",
            borrow_time=datetime.utcnow() - timedelta(minutes=30),
            status="borrowed"
        )
        
        records = [record1, record2, record3, record4]
        
        for record in records:
            db.session.add(record)
        
        # 更新多对多关系（保持兼容性）
        users[1].keys.append(keys[1])  # 李四借用102
        users[0].keys.append(keys[2])  # 张三借用103
        
        db.session.commit()
        
        print(f"✓ 创建了 {len(records)} 条借用记录")
        print("✓ 测试数据创建完成！")
        
        # 显示统计信息
        print("\n=== 数据统计 ===")
        print(f"用户总数: {User.query.count()}")
        print(f"钥匙总数: {Key.query.count()}")
        print(f"借用记录总数: {BorrowRecord.query.count()}")
        print(f"未归还记录: {BorrowRecord.query.filter_by(status='borrowed').count()}")
        print(f"已归还记录: {BorrowRecord.query.filter_by(status='returned').count()}")

if __name__ == "__main__":
    setup_test_data()