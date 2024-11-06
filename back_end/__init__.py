from flask import Flask
from flask_cors import CORS
from flask_docs import ApiDoc

from .api import api
# 初始化flaskAPP
app = Flask(__name__, static_folder="static")

# 允许跨域请求
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.register_blueprint(api)

# API文档
app.config["API_DOC_MEMBER"] = ["api"]
ApiDoc(
    app,
    title="API文档"
)

