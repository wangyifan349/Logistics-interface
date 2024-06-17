import sqlite3
from flask import Flask, request, jsonify

# 创建 Flask 应用
app = Flask(__name__)

# 连接到 SQLite 数据库（如果数据库不存在则会自动创建）
conn = sqlite3.connect('logistics.db')
cursor = conn.cursor()

# 创建包裹表格，如果它们不存在
cursor.execute('''
    CREATE TABLE IF NOT EXISTS packages (
        id INTEGER PRIMARY KEY,  # 包裹ID，主键
        shipment_number TEXT,  # 包裹编号
        type TEXT,  # 包裹类型
        weight REAL,  # 包裹重量
        dimensions TEXT,  # 包裹尺寸
        sender_name TEXT,  # 发件人姓名
        sender_address TEXT,  # 发件人地址
        recipient_name TEXT,  # 收件人姓名
        recipient_address TEXT,  # 收件人地址
        status TEXT  # 包裹状态
    )
''')

# 创建运输表格，如果它们不存在
cursor.execute('''
    CREATE TABLE IF NOT EXISTS shipments (
        id INTEGER PRIMARY KEY,  # 运输ID，主键
        shipment_number TEXT,  # 运输编号
        package_id INTEGER,  # 包裹ID，外键
        carrier TEXT,  # 运输公司
        tracking_number TEXT,  # 追踪编号
        estimated_delivery_date DATE,  # 预计交货日期
        FOREIGN KEY (package_id) REFERENCES packages (id)  # 外键约束，引用包裹表的ID
    )
''')

# 创建追踪更新表格，如果它们不存在
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tracking_updates (
        id INTEGER PRIMARY KEY,  # 追踪更新ID，主键
        shipment_id INTEGER,  # 运输ID，外键
        update_date DATE,  # 更新日期
        status TEXT,  # 运输状态
        location TEXT,  # 运输位置
        FOREIGN KEY (shipment_id) REFERENCES shipments (id)  # 外键约束，引用运输表的ID
    )
''')

# 提交更改
conn.commit()

# 关闭游标和连接
cursor.close()
conn.close()

# 定义 API 端点来创建包裹
@app.route('/packages', methods=['POST'])
def create_package():
    data = request.get_json()  # 从请求中获取JSON数据
    conn = sqlite3.connect('logistics.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO packages (shipment_number, type, weight, dimensions, sender_name, sender_address, recipient_name, recipient_address, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['shipment_number'],
        data['type'],
        data['weight'],
        data['dimensions'],
        data['sender_name'],
        data['sender_address'],
        data['recipient_name'],
        data['recipient_address'],
        data['status']
    ))
    conn.commit()  # 提交更改
    cursor.close()
    conn.close()
    return jsonify({'message': '包裹创建成功'})  # 返回成功信息

# 定义 API 端点来获取所有包裹
@app.route('/packages', methods=['GET'])
def get_packages():
    conn = sqlite3.connect('logistics.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM packages')  # 查询所有包裹
    packages = cursor.fetchall()  # 获取查询结果
    cursor.close()
    conn.close()
    return jsonify([dict(package) for package in packages])  # 将结果转换为JSON格式并返回

# 定义 API 端点来获取单个包裹
@app.route('/packages/<int:id>', methods=['GET'])
def get_package(id):
    conn = sqlite3.connect('logistics.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM packages WHERE id = ?', (id,))  # 查询指定ID的包裹
    package = cursor.fetchone()  # 获取查询结果
    cursor.close()
    conn.close()
    return jsonify(dict(package))  # 将结果转换为JSON格式并返回

# 定义 API 端点来更新包裹
@app.route('/packages/<int:id>', methods=['PUT'])
def update_package(id):
    data = request.get_json()  # 从请求中获取JSON数据
    conn = sqlite3.connect('logistics.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE packages
        SET shipment_number = ?, type = ?, weight = ?, dimensions = ?, sender_name = ?, sender_address = ?, recipient_name = ?, recipient_address = ?, status = ?
        WHERE id = ?
    ''', (
        data['shipment_number'],
        data['type'],
        data['weight'],
        data['dimensions'],
        data['sender_name'],
        data['sender_address'],
        data['recipient_name'],
        data['recipient_address'],
        data['status'],
        id
    ))
    conn.commit()  # 提交更改
    cursor.close()
    conn.close()
    return jsonify({'message': '包裹更新成功'})  # 返回成功信息

# 定义 API 端点来删除包裹
@app.route('/packages/<int:id>', methods=['DELETE'])
def delete_package(id):
    conn = sqlite3.connect('logistics.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM packages WHERE id = ?', (id,))  # 删除指定ID的包裹
    conn.commit()  # 提交更改
    cursor.close()
    conn.close()
    return jsonify({'message': '包裹删除成功'})  # 返回成功信息

# 定义 API 端点来创建运输
@app.route('/shipments', methods=['POST'])
def create_shipment():
    data = request.get_json()  # 从请求中获取JSON数据
    conn = sqlite3.connect('logistics.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO shipments (shipment_number, package_id, carrier, tracking_number, estimated_delivery_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        data['shipment_number'],
        data['package_id'],
        data['carrier'],
        data['tracking_number'],
        data['estimated_delivery_date']
    ))
    conn.commit()  # 提交更改
    cursor.close()
    conn.close()
    return jsonify({'message': '运输创建成功'})  # 返回成功信息

# 定义 API 端点来获取所有运输
@app.route('/shipments', methods=['GET'])
def get_shipments():
    conn = sqlite3.connect('logistics.db')
    cursor = conn.cursor()
    cursor.exe
