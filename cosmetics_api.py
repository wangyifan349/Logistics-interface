# cosmetics_api.py

from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# 连接数据库
conn = sqlite3.connect('cosmetics.db')
cursor = conn.cursor()

# ���建化妆品信息表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cosmetics (
        id INTEGER PRIMARY KEY,
        name TEXT,
        brand TEXT,
        ingredients TEXT,
        registration TEXT,
        description TEXT,
        image_url TEXT
    )
''')
conn.commit()

# 添加化妆品信息
@app.route('/add', methods=['POST'])
def add_cosmetic():
    """
    添加新的化妆品信息
    """
    data = request.get_json()
    name = data.get('name')
    brand = data.get('brand')
    ingredients = data.get('ingredients')
    registration = data.get('registration')
    description = data.get('description')
    image_url = data.get('image_url')
    if name and brand and ingredients and registration:
        cursor.execute('INSERT INTO cosmetics (name, brand, ingredients, registration, description, image_url) VALUES (?, ?, ?, ?, ?, ?)', (name, brand, ingredients, registration, description, image_url))
        conn.commit()
        return jsonify({'message': '添加成功'})
    return jsonify({'message': '参数错误'}), 400

# 获取化妆品信息
@app.route('/get', methods=['GET'])
def get_cosmetic():
    """
    获取化妆品信息
    """
    id = request.args.get('id')
    if id:
        cursor.execute('SELECT * FROM cosmetics WHERE id = ?', (id,))
        result = cursor.fetchone()
        if result:
            return jsonify({
                'id': result[0],
                'name': result[1],
                'brand': result[2],
                'ingredients': result[3],
                'registration': result[4],
                'description': result[5],
                'image_url': result[6]
            })
        return jsonify({'message': '化妆品不存在'}), 404
    return jsonify({'message': '参数错误'}), 400

# 更新化妆品信息
@app.route('/update', methods=['PUT'])
def update_cosmetic():
    """
    更新化妆品信息
    """
    data = request.get_json()
    id = data.get('id')
    name = data.get('name')
    brand = data.get('brand')
    ingredients = data.get('ingredients')
    registration = data.get('registration')
    description = data.get('description')
    image_url = data.get('image_url')
    if id and name and brand and ingredients and registration:
        cursor.execute('UPDATE cosmetics SET name = ?, brand = ?, ingredients = ?, registration = ?, description = ?, image_url = ? WHERE id = ?', (name, brand, ingredients, registration, description, image_url, id))
        conn.commit()
        return jsonify({'message': '更新成功'})
    return jsonify({'message': '参数错误'}), 400

# 删除化妆品信息
@app.route('/delete', methods=['DELETE'])
def delete_cosmetic():
    """
    删除化妆品信息
    """
    id = request.args.get('id')
    if id:
        cursor.execute('DELETE FROM cosmetics WHERE id = ?', (id,))
        conn.commit()
        return jsonify({'message': '删除成功'})
    return jsonify({'message': '参数错误'}), 400

# 获取所有化妆品信息
@app.route('/all', methods=['GET'])
def get_all_cosmetics():
    """
    获取所有化妆品信息
    """
    cursor.execute('SELECT * FROM cosmetics')
    results = cursor.fetchall()
    cosmetics = []
    for result in results:
        cosmetics.append({
            'id': result[0],
            'name': result[1],
            'brand': result[2],
            'ingredients': result[3],
            'registration': result[4],
            'description': result[5],
            'image_url': result[6]
        })
    return jsonify(cosmetics)

# 搜索化妆品信息
@app.route('/search', methods=['GET'])
def search_cosmetics():
    """
    搜索化妆品信息
    """
    keyword = request.args.get('keyword')
    if keyword:
        cursor.execute('SELECT * FROM cosmetics WHERE name LIKE ? OR brand LIKE ? OR ingredients LIKE ?', ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))
        results = cursor.fetchall()
        cosmetics = []
        for result in results:
            cosmetics.append({
                'id': result[0],
                'name': result[1],
                'brand': result[2],
                'ingredients': result[3],
                'registration': result[4],
                'description': result[5],
                'image_url': result[6]
            })
        return jsonify(cosmetics)
    return jsonify({'message': '参数错误'}), 400

if __name__ == '__main__':
    app.run(debug=True)
