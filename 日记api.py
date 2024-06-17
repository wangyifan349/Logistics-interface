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



curl -X POST -H "Content-Type: application/json" -d '{"id": 1, "text": "今天天气很好"}' http://localhost:5000/add
curl http://localhost:5000/get?id=1

curl -X DELETE http://localhost:5000/delete?id=1


<!-- index.html -->

<!DOCTYPE html>
<html>
<head>
    <title>Diary</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        .container {
            width: 80%;
            margin: 40px auto;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .form-group {
            margin-bottom: 20px;
        }
        .form-control {
            width: 100%;
            height: 40px;
            padding: 10px;
            font-size: 16px;
            border: 1px solid #ccc;
        }
        .btn {
            background-color: #4CAF50;
            color: #fff;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .btn:hover {
            background-color: #3e8e41;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Diary</h1>
        <form id="add-form">
            <div class="form-group">
                <label for="id">ID:</label>
                <input type="number" id="id" class="form-control" required>
            </div>
            <div class="form-group">
                <label for="text">Text:</label>
                <textarea id="text" class="form-control" required></textarea>
            </div>
            <button class="btn" id="add-btn">Add</button>
        </form>
        <hr>
        <form id="get-form">
            <div class="form-group">
                <label for="get-id">ID:</label>
                <input type="number" id="get-id" class="form-control" required>
            </div>
            <button class="btn" id="get-btn">Get</button>
            <div id="get-result"></div>
        </form>
        <hr>
        <form id="delete-form">
            <div class="form-group">
                <label for="delete-id">ID:</label>
                <input type="number" id="delete-id" class="form-control" required>
            </div>
            <button class="btn" id="delete-btn">Delete</button>
        </form>
    </div>

    <script>
        const addForm = document.getElementById('add-form');
        const getForm = document.getElementById('get-form');
        const deleteForm = document.getElementById('delete-form');

        addForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const id = document.getElementById('id').value;
            const text = document.getElementById('text').value;
            fetch('/add', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id, text })
            })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => console.error(error));
        });

        getForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const id = document.getElementById('get-id').value;
            fetch(`/get?id=${id}`)
            .then(response => response.json())
            .then(data => {
                const resultDiv = document.getElementById('get-result');
                resultDiv.innerText = data.text;
            })
            .catch(error => console.error(error));
        });

        deleteForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const id = document.getElementById('delete-id').value;
            fetch(`/delete?id=${id}`, { method: 'DELETE' })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => console.error(error));
        });
    </script>
</body>
</html>


