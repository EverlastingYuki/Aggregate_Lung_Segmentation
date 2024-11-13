from flask import Flask, jsonify, request
import os
import json
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 配置上传目录
UPLOAD_FOLDER = r"I:\new_tech\Aggregate_Lung_Segmentation\front_end\test_flask\test_static"
DATA_SOURCE_FILE = r"I:\new_tech\Aggregate_Lung_Segmentation\front_end\test_flask\test_static\workspace.json"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 限制文件大小为10MB

# 创建上传目录
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 获取 dataSource 数据
@app.route('/api/workspace', methods=['GET'])
def get_data_source():
    if not os.path.exists(DATA_SOURCE_FILE):
        return jsonify([])  # 如果文件不存在，返回空数组
    with open(DATA_SOURCE_FILE, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            return jsonify(data)
        except json.JSONDecodeError:
            return jsonify([])

# 更新 dataSource 数据
@app.route('/api/update-workspace', methods=['POST'])
def update_data_source():
    try:
        data = request.json
        with open(DATA_SOURCE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# 上传图片接口
@app.route('/api/upload', methods=['POST'])
def upload_file():
    uploaded_files = []
    try:
        # 获取所有上传的文件
        for file in request.files.getlist('files'):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)  # 保存文件

            # 构造文件信息返回给前端
            uploaded_files.append({
                'name': filename,
                'url': f'./test_flask/test_static/{filename}'
            })

        return jsonify(uploaded_files)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# 启动 Flask 应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
