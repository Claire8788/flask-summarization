from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO,emit
db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO()
# socketio = SocketIO(cors_allowed_origins="*")  # 允许所有域的跨域请求
