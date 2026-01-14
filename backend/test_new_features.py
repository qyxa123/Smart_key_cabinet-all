#!/usr/bin/env python3
"""
测试新功能的脚本
"""
import requests
import json
from datetime import datetime

BASE_URL = 'http://localhost:5000/api'

def test_borrow_with_reason():
    """测试带理由的借用功能"""
    print("=== 测试借用钥匙功能 ===")
    
    # 1. 创建测试用户
    user_data = {
        "name": "测试用户",
        "identity": "student",
        "grade": "2024",
        "class_": "1班"
    }
    
    try:
        response = requests.post(f'{BASE_URL}/user/', json=user_data)
        if response.status_code == 201:
            user = response.json()
            print(f"✓ 创建用户成功: {user['name']} (ID: {user['id']})")
        else:
            print(f"✗ 创建用户失败: {response.text}")
            return
    except Exception as e:
        print(f"✗ 创建用户异常: {e}")
        return
    
    # 2. 创建测试钥匙
    key_data = {
        "room": "101"
    }
    
    try:
        response = requests.post(f'{BASE_URL}/key/', json=key_data)
        if response.status_code == 201:
            key = response.json()
            print(f"✓ 创建钥匙成功: {key['room']}号房间 (ID: {key['id']})")
        else:
            print(f"✗ 创建钥匙失败: {response.text}")
            return
    except Exception as e:
        print(f"✗ 创建钥匙异常: {e}")
        return
    
    # 3. 测试借用钥匙（带理由）
    borrow_data = {
        "key_id": key['id'],
        "reason": "需要进入教室准备课程材料"
    }
    
    try:
        response = requests.post(f'{BASE_URL}/user/{user["id"]}/borrow', json=borrow_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✓ 借用钥匙成功")
            print(f"  借用记录ID: {result['borrow_record']['id']}")
            print(f"  借用时间: {result['borrow_record']['borrow_time']}")
            print(f"  借用理由: {result['borrow_record']['reason']}")
        else:
            print(f"✗ 借用钥匙失败: {response.text}")
            return
    except Exception as e:
        print(f"✗ 借用钥匙异常: {e}")
        return
    
    # 4. 测试重复借用（应该失败）
    try:
        response = requests.post(f'{BASE_URL}/user/{user["id"]}/borrow', json=borrow_data)
        if response.status_code == 400:
            print(f"✓ 重复借用正确被拒绝: {response.json()['error']}")
        else:
            print(f"✗ 重复借用应该被拒绝，但返回了: {response.status_code}")
    except Exception as e:
        print(f"✗ 测试重复借用异常: {e}")
    
    # 5. 查看借用记录
    try:
        response = requests.get(f'{BASE_URL}/user/borrow-records')
        if response.status_code == 200:
            records = response.json()
            print(f"✓ 获取借用记录成功，共 {len(records)} 条记录")
            for record in records:
                print(f"  记录: {record['user']['name']} 借用 {record['key']['room']}号房间")
                print(f"    理由: {record['reason']}")
                print(f"    状态: {record['status']}")
        else:
            print(f"✗ 获取借用记录失败: {response.text}")
    except Exception as e:
        print(f"✗ 获取借用记录异常: {e}")
    
    # 6. 测试归还钥匙
    return_data = {
        "key_id": key['id']
    }
    
    try:
        response = requests.post(f'{BASE_URL}/user/{user["id"]}/return', json=return_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✓ 归还钥匙成功")
            print(f"  归还时间: {result['borrow_record']['return_time']}")
        else:
            print(f"✗ 归还钥匙失败: {response.text}")
    except Exception as e:
        print(f"✗ 归还钥匙异常: {e}")
    
    # 7. 再次借用同一把钥匙（测试重复借用记录）
    borrow_data2 = {
        "key_id": key['id'],
        "reason": "第二次借用，需要整理教室"
    }
    
    try:
        response = requests.post(f'{BASE_URL}/user/{user["id"]}/borrow', json=borrow_data2)
        if response.status_code == 200:
            result = response.json()
            print(f"✓ 第二次借用成功")
            print(f"  新借用记录ID: {result['borrow_record']['id']}")
        else:
            print(f"✗ 第二次借用失败: {response.text}")
    except Exception as e:
        print(f"✗ 第二次借用异常: {e}")
    
    # 8. 查看最终的借用记录
    try:
        response = requests.get(f'{BASE_URL}/user/borrow-records')
        if response.status_code == 200:
            records = response.json()
            print(f"✓ 最终借用记录，共 {len(records)} 条记录")
            for i, record in enumerate(records, 1):
                status_text = "未归还" if record['status'] == 'borrowed' else "已归还"
                print(f"  记录{i}: {record['user']['name']} - {record['key']['room']}号房间 - {status_text}")
                print(f"    理由: {record['reason']}")
                print(f"    借用时间: {record['borrow_time']}")
                if record['return_time']:
                    print(f"    归还时间: {record['return_time']}")
        else:
            print(f"✗ 获取最终借用记录失败: {response.text}")
    except Exception as e:
        print(f"✗ 获取最终借用记录异常: {e}")

def test_without_reason():
    """测试不提供理由的情况"""
    print("\n=== 测试不提供理由的情况 ===")
    
    # 创建用户
    user_data = {
        "name": "测试用户2",
        "identity": "teacher",
        "office": "办公室A"
    }
    
    try:
        response = requests.post(f'{BASE_URL}/user/', json=user_data)
        user = response.json()
        print(f"✓ 创建用户成功: {user['name']}")
    except Exception as e:
        print(f"✗ 创建用户异常: {e}")
        return
    
    # 创建钥匙
    key_data = {"room": "102"}
    try:
        response = requests.post(f'{BASE_URL}/key/', json=key_data)
        key = response.json()
        print(f"✓ 创建钥匙成功: {key['room']}号房间")
    except Exception as e:
        print(f"✗ 创建钥匙异常: {e}")
        return
    
    # 尝试不提供理由借用
    borrow_data = {
        "key_id": key['id']
        # 故意不提供 reason
    }
    
    try:
        response = requests.post(f'{BASE_URL}/user/{user["id"]}/borrow', json=borrow_data)
        if response.status_code == 400:
            print(f"✓ 不提供理由正确被拒绝: {response.json()['error']}")
        else:
            print(f"✗ 不提供理由应该被拒绝，但返回了: {response.status_code}")
    except Exception as e:
        print(f"✗ 测试不提供理由异常: {e}")
    
    # 尝试提供空理由
    borrow_data = {
        "key_id": key['id'],
        "reason": "   "  # 只有空格
    }
    
    try:
        response = requests.post(f'{BASE_URL}/user/{user["id"]}/borrow', json=borrow_data)
        if response.status_code == 400:
            print(f"✓ 空理由正确被拒绝: {response.json()['error']}")
        else:
            print(f"✗ 空理由应该被拒绝，但返回了: {response.status_code}")
    except Exception as e:
        print(f"✗ 测试空理由异常: {e}")

if __name__ == "__main__":
    print("开始测试新功能...")
    print("请确保后端服务器正在运行在 http://localhost:5000")
    print()
    
    try:
        # 测试服务器连接
        response = requests.get(f'{BASE_URL}/../')
        print("✓ 后端服务器连接正常")
        print()
    except Exception as e:
        print(f"✗ 无法连接到后端服务器: {e}")
        print("请先启动后端服务器")
        exit(1)
    
    test_borrow_with_reason()
    test_without_reason()
    
    print("\n=== 测试完成 ===")