from flask import Flask, request, jsonify, g
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

# 创建 Flask 应用
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # 用于加密 JWT 的密钥

# 连接到 SQLite 数据库
conn = sqlite3.connect('canteen.db', check_same_thread=False)
cursor = conn.cursor()

# 创建数据库表
cursor.executescript("""
    CREATE TABLE IF NOT EXISTS dishes (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        description TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        dish_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        total_price REAL NOT NULL,
        status TEXT DEFAULT 'pending',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (dish_id) REFERENCES dishes(id)
    );

    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        email TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
""")
conn.commit()

# 关闭数据库连接函数
def close_db():
    conn.close()

# 应用上下文结束时关闭数据库连接
@app.teardown_appcontext
def close_db_on_teardown(exception):
    close_db()

# JWT 验证装饰器
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            cursor.execute("SELECT * FROM users WHERE id = ?", (data['user_id'],))
            current_user = cursor.fetchone()
            if not current_user:
                return jsonify({'message': 'User not found!'}), 401
            g.user = {'id': current_user[0], 'username': current_user[1], 'email': current_user[3]}
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(*args, **kwargs)
    return decorated

# 用户注册接口
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", 
                   (data['username'], hashed_password, data['email']))
    conn.commit()
    return jsonify({'message': '用户注册成功'})

# 用户登录接口
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    cursor.execute("SELECT * FROM users WHERE username = ?", (data['username'],))
    user = cursor.fetchone()
    if not user or not check_password_hash(user[2], data['password']):
        return jsonify({'message': '用户名或密码错误'}), 401
    token = jwt.encode({'user_id': user[0], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, 
                       app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({'token': token})

# 添加菜单接口（需要认证）
@app.route('/dishes', methods=['POST'])
@token_required
def add_dish():
    data = request.get_json()
    cursor.execute("INSERT INTO dishes (name, price, description) VALUES (?, ?, ?)", 
                   (data['name'], data['price'], data['description']))
    conn.commit()
    return jsonify({'message': '菜单添加成功'})

# 获取所有菜单接口（需要认证）
@app.route('/dishes', methods=['GET'])
@token_required
def get_dishes():
    cursor.execute("SELECT * FROM dishes")
    dishes = cursor.fetchall()
    return jsonify([{'id': dish[0], 'name': dish[1], 'price': dish[2], 'description': dish[3]} for dish in dishes])

# 获取单个菜单接口（需要认证）
@app.route('/dishes/<int:id>', methods=['GET'])
@token_required
def get_dish(id):
    cursor.execute("SELECT * FROM dishes WHERE id = ?", (id,))
    dish = cursor.fetchone()
    if dish:
        return jsonify({'id': dish[0], 'name': dish[1], 'price': dish[2], 'description': dish[3]})
    else:
        return jsonify({'message': '菜单未找到'}), 404

# 更新菜单接口（需要认证）
@app.route('/dishes/<int:id>', methods=['PUT'])
@token_required
def update_dish(id):
    data = request.get_json()
    cursor.execute("UPDATE dishes SET name = ?, price = ?, description = ? WHERE id = ?", 
                   (data['name'], data['price'], data['description'], id))
    conn.commit()
    return jsonify({'message': '菜单更新成功'})

# 删除菜单接口（需要认证）
@app.route('/dishes/<int:id>', methods=['DELETE'])
@token_required
def delete_dish(id):
    cursor.execute("DELETE FROM dishes WHERE id = ?", (id,))
    conn.commit()
    return jsonify({'message': '菜单删除成功'})

# 添加订单接口（需要认证）
@app.route('/orders', methods=['POST'])
@token_required
def add_order():
    data = request.get_json()
    total_price = get_dish_price(data['dish_id']) * data['quantity']
    cursor.execute("INSERT INTO orders (user_id, dish_id, quantity, total_price) VALUES (?, ?, ?, ?)", 
                   (g.user['id'], data['dish_id'], data['quantity'], total_price))
    conn.commit()
    return jsonify({'message': '订单添加成功'})

# 获取用户订单接口（需要认证）
@app.route('/orders', methods=['GET'])
@token_required
def get_orders():
    cursor.execute("SELECT * FROM orders WHERE user_id = ?", (g.user['id'],))
    orders = cursor.fetchall()
    return jsonify([{'id': order[0], 'user_id': order[1], 'dish_id': order[2], 'quantity': order[3], 'total_price': order[4], 'status': order[5]} for order in orders])

# 获取订单详情接口（需要认证）
@app.route('/orders/<int:order_id>', methods=['GET'])
@token_required
def get_order_detail(order_id):
    cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    order = cursor.fetchone()
    if order:
        return jsonify({'id': order[0], 'user_id': order[1], 'dish_id': order[2], 'quantity': order[3], 'total_price': order[4], 'status': order[5]})
    else:
        return jsonify({'message': '订单未找到'}), 404

# 获取菜单价格函数
def get_dish_price(dish_id):
    cursor.execute("SELECT price FROM dishes WHERE id = ?", (dish_id,))
    return cursor.fetchone()[0]

# 获取用户信息接口（需要认证）
@app.route('/user', methods=['GET'])
@token_required
def get_user_info():
    return jsonify({'id': g.user['id'], 'username': g.user['username'], 'email': g.user['email']})

# 更新用户信息接口（需要认证）
@app.route('/user', methods=['PUT'])
@token_required
def update_user_info():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    cursor.execute("UPDATE users SET username = ?, password = ?, email = ? WHERE id = ?", 
                   (data['username'], hashed_password, data['email'], g.user['id']))
    conn.commit()
    return jsonify({'message': '用户信息更新成功'})

# 获取所有订单接口（需要认证，只有管理员可以访问）
@app.route('/all-orders', methods=['GET'])
@token_required
def get_all_orders():
    # 检查用户是否为管理员（这里假设管理员的用户名为 'admin'）
    if g.user['username'] != 'admin':
        return jsonify({'message': '无权限访问'}), 403
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    return jsonify([{'id': order[0], 'user_id': order[1], 'dish_id': order[2], 'quantity': order[3], 'total_price': order[4], 'status': order[5]} for order in orders])

# 更新订单状态接口（需要认证，只有管理员可以访问）
@app.route('/orders/<int:order_id>/status', methods=['PUT'])
@token_required
def update_order_status(order_id):
    # 检查用户是否为管理员（这里假设管理员的用户名为 'admin'）
    if g.user['username'] != 'admin':
        return jsonify({'message': '无权限访问'}), 403
    data = request.get_json()
    cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (data['status'], order_id))
    conn.commit()
    return jsonify({'message': '订单状态更新成功'})

# 添加用户接口（需要认证）
@app.route('/users', methods=['POST'])
@token_required
def add_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", 
                   (data['username'], hashed_password, data['email']))
    conn.commit()
    return jsonify({'message': '用户添加成功'})

# 获取所有用户接口（需要认证）
@app.route('/users', methods=['GET'])
@token_required
def get_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return jsonify([{'id': user[0], 'username': user[1], 'email': user[3]} for user in users])

# 获取单个用户接口（需要认证）
@app.route('/users/<int:id>', methods=['GET'])
@token_required
def get_user(id):
    cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
    user = cursor.fetchone()
    if user:
        return jsonify({'id': user[0], 'username': user[1], 'email': user[3]})
    else:
        return jsonify({'message': '用户未找到'}), 404

# 更新用户接口（需要认证）
@app.route('/users/<int:id>', methods=['PUT'])
@token_required
def update_user(id):
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    cursor.execute("UPDATE users SET username = ?, password = ?, email = ? WHERE id = ?", 
                   (data['username'], hashed_password, data['email'], id))
    conn.commit()
    return jsonify({'message': '用户更新成功'})

# 删除用户接口（需要认证）
@app.route('/users/<int:id>', methods=['DELETE'])
@token_required
def delete_user(id):
    cursor.execute("DELETE FROM users WHERE id = ?", (id,))
    conn.commit()
    return jsonify({'message': '用户删除成功'})

if __name__ == '__main__':
    app.run(debug=True)
