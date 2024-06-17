# diary.py

from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# 连接数据库
conn = sqlite3.connect('diary.db')
cursor = conn.cursor()

# 创建日记表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS diary (
        id INTEGER PRIMARY KEY,
        text TEXT
    )
''')
conn.commit()

# 添加日记
@app.route('/add', methods=['POST'])
def add_diary():
    data = request.get_json()
    id = data.get('id')
    text = data.get('text')
    if id and text:
        cursor.execute('INSERT INTO diary (id, text) VALUES (?, ?)', (id, text))
        conn.commit()
        return jsonify({'message': '添加成功'})
    return jsonify({'message': '参数错误'}), 400

# 获取日记
@app.route('/get', methods=['GET'])
def get_diary():
    id = request.args.get('id')
    if id:
        cursor.execute('SELECT text FROM diary WHERE id = ?', (id,))
        result = cursor.fetchone()
        if result:
            return jsonify({'text': result[0]})
        return jsonify({'message': '日记不存在'}), 404
    return jsonify({'message': '参数错误'}), 400

# 删除日记
@app.route('/delete', methods=['DELETE'])
def delete_diary():
    id = request.args.get('id')
    if id:
        cursor.execute('DELETE FROM diary WHERE id = ?', (id,))
        conn.commit()
        return jsonify({'message': '删除成功'})
    return jsonify({'message': '参数错误'}), 400

if __name__ == '__main__':
    app.run(debug=True)
