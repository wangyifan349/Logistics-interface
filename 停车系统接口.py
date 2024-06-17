from flask import Flask, request, jsonify  # 从 Flask 框架中导入 Flask 类和 request 对象
import sqlite3  # 导入 sqlite3 库，用于操作 SQLite 数据库

# 创建一个名为 app 的 Flask 应用程序
app = Flask(__name__)

# 定义一个函数来初始化数据库
def init_db():
    # 连接到数据库（如果数据库不存在，会自动创建）
    conn = sqlite3.connect('vehicle_tracking.db')
    cursor = conn.cursor()
    
    # 创建 vehicles 表，如果它不存在
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY,  # 主键
            vehicle_id TEXT,  # 车辆 ID
            make TEXT,  # 车辆品牌
            model TEXT,  # 车辆型号
            year INTEGER  # 车辆年份
        )
    ''')
    
    # 创建 trips 表，如果它不存在
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY,  # 主键
            vehicle_id INTEGER,  # 车辆 ID
            start_time TEXT,  # 行程开始时间
            end_time TEXT,  # 行程结束时间
            start_location TEXT,  # 行程开始位置
            end_location TEXT,  # 行程结束位置
            FOREIGN KEY (vehicle_id) REFERENCES vehicles (id)  # 外键关联 vehicles 表
        )
    ''')
    
    # 创建 locations 表，如果它不存在
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY,  # 主键
            trip_id INTEGER,  # 行程 ID
            timestamp TEXT,  # 位置时间戳
            latitude REAL,  # 纬度
            longitude REAL,  # 经度
            FOREIGN KEY (trip_id) REFERENCES trips (id)  # 外键关联 trips 表
        )
    ''')
    
    # 提交数据库更改
    conn.commit()
    # 关闭游标和连接
    cursor.close()
    conn.close()

# 初始化数据库
init_db()

# 定义 API 端点，用于创建车辆
@app.route('/vehicles', methods=['POST'])
def create_vehicle():
    data = request.get_json()  # 获取请求体中的数据
    conn = sqlite3.connect('vehicle_tracking.db')  # 连接到数据库
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO vehicles (vehicle_id, make, model, year)
        VALUES (?, ?, ?, ?)
    ''', (data['vehicle_id'], data['make'], data['model'], data['year']))  # 插入数据到 vehicles 表
    conn.commit()  # 提交数据库更改
    cursor.close()  # 关闭游标
    conn.close()  # 关闭连接
    return jsonify({'message': 'Vehicle created successfully'}), 201  # 返回成功消息，状态码201

# 定义 API 端点，用于获取所有车辆
@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    conn = sqlite3.connect('vehicle_tracking.db')  # 连接到数据库
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vehicles')  # 查询 vehicles 表
    vehicles = cursor.fetchall()  # 获取所有查询结果
    cursor.close()  # 关闭游标
    conn.close()  # 关闭连接
    return jsonify([dict(id=row[0], vehicle_id=row[1], make=row[2], model=row[3], year=row[4]) for row in vehicles])  # 返回查询结果

# 定义 API 端点，用于获取单个车辆
@app.route('/vehicles/<int:id>', methods=['GET'])
def get_vehicle(id):
    conn = sqlite3.connect('vehicle_tracking.db')  # 连接到数据库
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vehicles WHERE id = ?', (id,))  # 查询 vehicles 表
    vehicle = cursor.fetchone()  # 获取查询结果
    cursor.close()  # 关闭游标
    conn.close()  # 关闭连接
    if vehicle:
        return jsonify(dict(id=vehicle[0], vehicle_id=vehicle[1], make=vehicle[2], model=vehicle[3], year=vehicle[4]))  # 返回查询结果
    else:
        return jsonify({'message': 'Vehicle not found'}), 404  # 如果车辆不存在，返回404

# 定义 API 端点，用于创建行程
@app.route('/trips', methods=['POST'])
def create_trip():
    data = request.get_json()  # 获取请求体中的数据
    conn = sqlite3.connect('vehicle_tracking.db')  # 连接到数据库
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO trips (vehicle_id, start_time, end_time, start_location, end_location)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['vehicle_id'], data['start_time'], data['end_time'], data['start_location'], data['end_location']))  # 插入数据到 trips 表
    conn.commit()  # 提交数据库更改
    cursor.close()  # 关闭游标
    conn.close()  # 关闭连接
    return jsonify({'message': 'Trip created successfully'}), 201  # 返回成功消息，状态码201

# 定义 API 端点，用于获取所有行程
@app.route('/trips', methods=['GET'])
def get_trips():
    conn = sqlite3.connect('vehicle_tracking.db')  # 连接到数据库
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM trips')  # 查询 trips 表
    trips = cursor.fetchall()  # 获取所有查询结果
    cursor.close()  # 关闭游标
    conn.close()  # 关闭连接
    return jsonify([dict(id=row[0], vehicle_id=row[1], start_time=row[2], end_time=row[3], start_location=row[4], end_location=row[5]) for row in trips])  # 返回查询结果

# 定义 API 端点，用于获取单个行程
@app.route('/trips/<int:id>', methods=['GET'])
def get_trip(id):
    conn = sqlite3.connect('vehicle_tracking.db')  # 连接到数据库
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM trips WHERE id = ?', (id,))  # 查询 trips 表
    trip = cursor.fetchone()  # 获取查询结果
    cursor.close()  # 关闭游标
    conn.close()  # 关闭连接
    if trip:
        return jsonify(dict(id=trip[0], vehicle_id=trip[1], start_time=trip[2], end_time=trip[3], start_location=trip[4], end_location=trip[5]))  # 返回查询结果
    else:
        return jsonify({'message': 'Trip not found'}), 404  # 如果行程不存在，返回404

# 定义 API 端点，用于创建位置更新
@app.route('/locations', methods=['POST'])
def create_location():
    data = request.get_json()  # 获取请求体中的数据
    conn = sqlite3.connect('vehicle_tracking.db')  # 连接到数据库
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO locations (trip_id, timestamp, latitude, longitude)
        VALUES (?, ?, ?, ?)
    ''', (data['trip_id'], data['timestamp'], data['latitude'], data['longitude']))  # 插入数据到 locations 表
    conn.commit()  # 提交数据库更改
    cursor.close()  # 关闭游标
    conn.close()  # 关闭连接
    return jsonify({'message': 'Location created successfully'}), 201  # 返回成功消息，状态码201

# 定义 API 端点，用于获取所有位置更新
@app.route('/locations', methods=['GET'])
def get_locations():
    conn = sqlite3.connect('vehicle_tracking.db')  # 连接到数据库
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM locations')  # 查询 locations 表
    locations = cursor.fetchall()  # 获取所有查询结果
    cursor.close()  # 关闭游标
    conn.close()  # 关闭连接
    return jsonify([dict(id=row[0], trip_id=row[1], timestamp=row[2], latitude=row[3], longitude=row[4]) for row in locations])  # 返回查询结果

# 定义 API 端点，用于获取单个位置更新
@app.route('/locations/<int:id>', methods=['GET'])
def get_location(id):
    conn = sqlite3.connect('vehicle_tracking.db')  # 连接到数据库
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM locations WHERE id = ?', (id,))  # 查询 locations 表
    location = cursor.fetchone()  # 获取查询结果
    cursor.close()  # 关闭游标
    conn.close()  # 关闭连接
    if location:
        return jsonify(dict(id=location[0], trip_id=location[1], timestamp=location[2], latitude=location[3], longitude=location[4]))  # 返回查询结果
    else:
        return jsonify({'message': 'Location not found'}), 404  # 如果位置更新不存在，返回404

if __name__ == '__main__':
    app.run(debug=True)  # 运行应用程序，启用调试模式
