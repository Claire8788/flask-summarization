from flask import Blueprint, jsonify
from flask import Flask, request, jsonify
from model import Admin
from extension import db
auth_blueprint = Blueprint('auth', __name__)


# users = {
#     'admin': {'password': '123'},
#     'user1': {'password': 'password1'},
#     'user2': {'password': 'password2'}
# }

# @auth_blueprint.route('/login', methods=['POST'])
# def login():
#     # 登录功能的视图函数
#     # 你的视图函数代码



@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    #查询是不是管理员
    if username == 'admin' and password == '123':
        return jsonify({'message': '登录成功'})
    # 不是管理员，就去数据库查用户表在数据库中查找用户名和密码是否匹配
    user = Admin.query.filter_by(username=username, password=password).first()

    if user:
        return jsonify({'message': '登录成功'})
    else:
        return jsonify({'message': '用户名或密码错误'}), 401
    
    # 注册路由，处理用户注册请求
@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # 检查用户名是否已存在
    if Admin.query.filter_by(username=username).first():
        return jsonify({'message': '用户名已存在，请选择其他用户名'}), 400

    # 创建新用户实例并保存到数据库
    new_user = Admin(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': '注册成功'})