from flask import Flask, request, render_template_string, send_from_directory, redirect, url_for
import os

app = Flask(__name__)

# 設定儲存上傳檔案的資料夾
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 確保資料夾存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    # 列出上傳資料夾中的檔案
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template_string('''
        <!doctype html>
        <html lang="zh-TW">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>檔案上傳</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f7fc;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                }
                h1, h2 {
                    color: #333;
                }
                .container {
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                    width: 80%;
                    max-width: 600px;
                    margin: 20px;
                }
                .file-upload-form {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }
                .file-upload-form input[type="file"] {
                    padding: 10px;
                    margin-bottom: 20px;
                }
                .file-upload-form input[type="submit"] {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                }
                .file-upload-form input[type="submit"]:hover {
                    background-color: #45a049;
                }
                .file-list {
                    list-style-type: none;
                    padding: 0;
                }
                .file-list li {
                    background-color: #f9f9f9;
                    padding: 10px;
                    border-radius: 5px;
                    margin-bottom: 10px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    box-shadow: 0 1px 5px rgba(0, 0, 0, 0.1);
                }
                .file-list a {
                    text-decoration: none;
                    color: #3498db;
                    margin-right: 10px;
                }
                .file-list a:hover {
                    text-decoration: underline;
                }
                .delete-link {
                    color: #e74c3c;
                    cursor: pointer;
                }
                .delete-link:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>檔案上傳</h1>
                <form method="post" enctype="multipart/form-data" class="file-upload-form">
                    <input type="file" name="file" required><br>
                    <input type="submit" value="上傳">
                </form>

                <h2>已上傳的檔案</h2>
                <ul class="file-list">
                {% for file in files %}
                    <li>
                        <div>
                            <a href="{{ url_for('download_file', filename=file) }}">{{ file }}</a>
                        </div>
                        <a href="{{ url_for('delete_file', filename=file) }}" class="delete-link">刪除</a>
                    </li>
                {% endfor %}
                </ul>
            </div>
        </body>
        </html>
    ''', files=files)

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return '沒有選擇檔案'
    file = request.files['file']
    if file.filename == '':
        return '沒有選擇檔案'
    
    # 儲存檔案到 uploads 資料夾
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return f'檔案 {file.filename} 上傳成功！'

@app.route('/uploads/<filename>')
def download_file(filename):
    # 提供檔案下載
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete/<filename>', methods=['GET'])
def delete_file(filename):
    # 刪除檔案
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # 確認檔案存在後刪除
    if os.path.exists(file_path):
        os.remove(file_path)
        return redirect(url_for('index'))  # 刪除後返回首頁
    else:
        return f"檔案 {filename} 不存在", 404

if __name__ == '__main__':
    app.run(debug=True)
