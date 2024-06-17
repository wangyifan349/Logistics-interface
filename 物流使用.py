import requests  # 导入用于发送HTTP请求的requests库
import json  # 导入用于处理JSON数据的json库

# 定义 API 基础 URL
BASE_URL = 'http://127.0.0.1:5000'

def create_package():
    url = f'{BASE_URL}/packages'  # 定义创建包裹的API端点
    data = {
        'shipment_number': 'SN123456',  # 包裹编号
        'type': 'Electronics',  # 包裹类型
        'weight': 1.5,  # 包裹重量
        'dimensions': '10x10x5',  # 包裹尺寸
        'sender_name': 'Alice',  # 发件人姓名
        'sender_address': '123 Sender St.',  # 发件人地址
        'recipient_name': 'Bob',  # 收件人姓名
        'recipient_address': '456 Recipient Ave.',  # 收件人地址
        'status': 'Pending'  # 包裹状态
    }
    response = requests.post(url, json=data)  # 发送POST请求以创建包裹
    print('创建包裹:', response.json())  # 打印服务器返回的响应

def get_packages():
    url = f'{BASE_URL}/packages'  # 定义获取所有包裹的API端点
    response = requests.get(url)  # 发送GET请求以获取所有包裹
    print('获取所有包裹:', response.json())  # 打印服务器返回的响应

def get_package(package_id):
    url = f'{BASE_URL}/packages/{package_id}'  # 定义获取单个包裹的API端点
    response = requests.get(url)  # 发送GET请求以获取指定ID的包裹
    print(f'获取包裹 {package_id}:', response.json())  # 打印服务器返回的响应

def update_package(package_id):
    url = f'{BASE_URL}/packages/{package_id}'  # 定义更新包裹的API端点
    data = {
        'shipment_number': 'SN123456',  # 包裹编号
        'type': 'Electronics',  # 包裹类型
        'weight': 2.0,  # 更新后的包裹重量
        'dimensions': '10x10x5',  # 包裹尺寸
        'sender_name': 'Alice',  # 发件人姓名
        'sender_address': '123 Sender St.',  # 发件人地址
        'recipient_name': 'Bob',  # 收件人姓名
        'recipient_address': '456 Recipient Ave.',  # 收件人地址
        'status': 'Shipped'  # 更新后的包裹状态
    }
    response = requests.put(url, json=data)  # 发送PUT请求以更新包裹
    print(f'更新包裹 {package_id}:', response.json())  # 打印服务器返回的响应

def delete_package(package_id):
    url = f'{BASE_URL}/packages/{package_id}'  # 定义删除包裹的API端点
    response = requests.delete(url)  # 发送DELETE请求以删除指定ID的包裹
    print(f'删除包裹 {package_id}:', response.json())  # 打印服务器返回的响应

def create_shipment():
    url = f'{BASE_URL}/shipments'  # 定义创建运输的API端点
    data = {
        'shipment_number': 'SH123456',  # 运输编号
        'package_id': 1,  # 假设包裹ID为1
        'carrier': 'DHL',  # 运输公司
        'tracking_number': 'TRK123456',  # 追踪编号
        'estimated_delivery_date': '2024-06-20'  # 预计交货日期
    }
    response = requests.post(url, json=data)  # 发送POST请求以创建运输
    print('创建运输:', response.json())  # 打印服务器返回的响应

def get_shipments():
    url = f'{BASE_URL}/shipments'  # 定义获取所有运输的API端点
    response = requests.get(url)  # 发送GET请求以获取所有运输
    print('获取所有运输:', response.json())  # 打印服务器返回的响应

def get_shipment(shipment_id):
    url = f'{BASE_URL}/shipments/{shipment_id}'  # 定义获取单个运输的API端点
    response = requests.get(url)  # 发送GET请求以获取指定ID的运输
    print(f'获取运输 {shipment_id}:', response.json())  # 打印服务器返回的响应

def update_shipment(shipment_id):
    url = f'{BASE_URL}/shipments/{shipment_id}'  # 定义更新运输的API端点
    data = {
        'shipment_number': 'SH123456',  # 运输编号
        'package_id': 1,  # 假设包裹ID为1
        'carrier': 'FedEx',  # 更新后的运输公司
        'tracking_number': 'TRK654321',  # 更新后的追踪编号
        'estimated_delivery_date': '2024-06-21'  # 更新后的预计交货日期
    }
    response = requests.put(url, json=data)  # 发送PUT请求以更新运输
    print(f'更新运输 {shipment_id}:', response.json())  # 打印服务器返回的响应

def delete_shipment(shipment_id):
    url = f'{BASE_URL}/shipments/{shipment_id}'  # 定义删除运输的API端点
    response = requests.delete(url)  # 发送DELETE请求以删除指定ID的运输
    print(f'删除运输 {shipment_id}:', response.json())  # 打印服务器返回的响应

def create_tracking_update():
    url = f'{BASE_URL}/tracking_updates'  # 定义创建追踪更新的API端点
    data = {
        'shipment_id': 1,  # 假设运输ID为1
        'update_date': '2024-06-17',  # 更新日期
        'status': 'In Transit',  # 运输状态
        'location': 'New York'  # 运输位置
    }
    response = requests.post(url, json=data)  # 发送POST请求以创建追踪更新
    print('创建追踪更新:', response.json())  # 打印服务器返回的响应

def get_tracking_updates():
    url = f'{BASE_URL}/tracking_updates'  # 定义获取所有追踪更新的API端点
    response = requests.get(url)  # 发送GET请求以获取所有追踪更新
    print('获取所有追踪更新:', response.json())  # 打印服务器返回的响应

def get_tracking_updates_for_shipment(shipment_id):
    url = f'{BASE_URL}/shipments/{shipment_id}/tracking_updates'  # 定义获取某个运输的所有追踪更新的API端点
    response = requests.get(url)  # 发送GET请求以获取指定运输ID的所有追踪更新
    print(f'获取运输 {shipment_id} 的所有追踪更新:', response.json())  # 打印服务器返回的响应

if __name__ == '__main__':
    # 演示各个功能
    create_package()  # 创建一个包裹
    get_packages()  # 获取所有包裹
    get_package(1)  # 获取ID为1的包裹，假设ID为1
    update_package(1)  # 更新ID为1的包裹，假设ID为1
    delete_package(1)  # 删除ID为1的包裹，假设ID为1

    create_shipment()  # 创建一个运输
    get_shipments()  # 获取所有运输
    get_shipment(1)  # 获取ID为1的运输，假设ID为1
    update_shipment(1)  # 更新ID为1的运输，假设ID为1
    delete_shipment(1)  # 删除ID为1的运输，假设ID为1

    create_tracking_update()  # 创建一个追踪更新
    get_tracking_updates()  # 获取所有追踪更新
    get_tracking_updates_for_shipment(1)  # 获取ID为1的运输的所有追踪更新，假设ID为1
