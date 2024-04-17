from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import timedelta
# from flask_migrate import Migrate
from extension import db, migrate,socketio

# # 注册蓝图
from auth import auth_blueprint
from table import table_blueprint
from summary import summary_blueprint
from audio_to_text import audio_blueprint
app = Flask(__name__)
CORS(app)  # 添加CORS扩展

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/summary?charset=utf8mb4'
db.init_app(app)
migrate.init_app(app, db)
# socketio.init_app(app)
socketio.init_app(app, cors_allowed_origins="*")  # 正确设置 CORS
# socketio.init_app(app, logger=True, engineio_logger=True, cors_allowed_origins="*", async_mode='threading')
# socketio = SocketIO(app, cors_allowed_origins="*")  # 允许所有域的跨域请求



app.register_blueprint(auth_blueprint)
app.register_blueprint(table_blueprint)
app.register_blueprint(summary_blueprint)
app.register_blueprint(audio_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
    # socketio.run(app, debug=True)

