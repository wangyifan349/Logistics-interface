import requests
import json

# 定义 API 基础 URL
BASE_URL = 'http://127.0.0.1:5000'

def create_package():
    url = f'{BASE_URL}/packages'
    data = {
        'shipment_number': 'SN123456',
        'type': 'Electronics',
        'weight': 1.5,
        'dimensions': '10x10x5',
        'sender_name': 'Alice',
        'sender_address': '123 Sender St.',
        'recipient_name': 'Bob',
        'recipient_address': '456 Recipient Ave.',
        'status': 'Pending'
    }
    response = requests.post(url, json=data)
    print('创建包裹:', response.json())

def get_packages():
    url = f'{BASE_URL}/packages'
    response = requests.get(url)
    print('获取所有包裹:', response.json())

def get_package(package_id):
    url = f'{BASE_URL}/packages/{package_id}'
    response = requests.get(url)
    print(f'获取包裹 {package_id}:', response.json())

def update_package(package_id):
    url = f'{BASE_URL}/packages/{package_id}'
    data = {
        'shipment_number': 'SN123456',
        'type': 'Electronics',
        'weight': 2.0,
        'dimensions': '10x10x5',
        'sender_name': 'Alice',
        'sender_address': '123 Sender St.',
        'recipient_name': 'Bob',
        'recipient_address': '456 Recipient Ave.',
        'status': 'Shipped'
    }
    response = requests.put(url, json=data)
    print(f'更新包裹 {package_id}:', response.json())

def delete_package(package_id):
    url = f'{BASE_URL}/packages/{package_id}'
    response = requests.delete(url)
    print(f'删除包裹 {package_id}:', response.json())

def create_shipment():
    url = f'{BASE_URL}/shipments'
    data = {
        'shipment_number': 'SH123456',
        'package_id': 1,  # 假设包裹ID为1
        'carrier': 'DHL',
        'tracking_number': 'TRK123456',
        'estimated_delivery_date': '2024-06-20'
    }
    response = requests.post(url, json=data)
    print('创建运输:', response.json())

def get_shipments():
    url = f'{BASE_URL}/shipments'
    response = requests.get(url)
    print('获取所有运输:', response.json())

def get_shipment(shipment_id):
    url = f'{BASE_URL}/shipments/{shipment_id}'
    response = requests.get(url)
    print(f'获取运输 {shipment_id}:', response.json())

def update_shipment(shipment_id):
    url = f'{BASE_URL}/shipments/{shipment_id}'
    data = {
        'shipment_number': 'SH123456',
        'package_id': 1,  # 假设包裹ID为1
        'carrier': 'FedEx',
        'tracking_number': 'TRK654321',
        'estimated_delivery_date': '2024-06-21'
    }
    response = requests.put(url, json=data)
    print(f'更新运输 {shipment_id}:', response.json())

def delete_shipment(shipment_id):
    url = f'{BASE_URL}/shipments/{shipment_id}'
    response = requests.delete(url)
    print(f'删除运输 {shipment_id}:', response.json())

def create_tracking_update():
    url = f'{BASE_URL}/tracking_updates'
    data = {
        'shipment_id': 1,  # 假设运输ID为1
        'update_date': '2024-06-17',
        'status': 'In Transit',
        'location': 'New York'
    }
    response = requests.post(url, json=data)
    print('创建追踪更新:', response.json())

def get_tracking_updates():
    url = f'{BASE_URL}/tracking_updates'
    response = requests.get(url)
    print('获取所有追踪更新:', response.json())

def get_tracking_updates_for_shipment(shipment_id):
    url = f'{BASE_URL}/shipments/{shipment_id}/tracking_updates'
    response = requests.get(url)
    print(f'获取运输 {shipment_id} 的所有追踪更新:', response.json())

if __name__ == '__main__':
    # 演示各个功能
    create_package()
    get_packages()
    get_package(1)  # 假设包裹ID为1
    update_package(1)  # 假设包裹ID为1
    delete_package(1)  # 假设包裹ID为1

    create_shipment()
    get_shipments()
    get_shipment(1)  # 假设运输ID为1
    update_shipment(1)  # 假设运输ID为1
    delete_shipment(1)  # 假设运输ID为1

    create_tracking_update()
    get_tracking_updates()
    get_tracking_updates_for_shipment(1)  # 假设运输ID为1
