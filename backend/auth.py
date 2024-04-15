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
    user = Admin.query.filter_by(username=username, password=password,status=1).first()

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
    email = data.get("email")

    # 检查用户名是否已存在
    if Admin.query.filter_by(username=username).first():
        return jsonify({'message': '用户名已存在，请选择其他用户名'}), 400
    
    # 检查邮箱是否已存在
    existing_user = Admin.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': '该邮箱已被注册，请选择其他邮箱'}), 400


    # 创建新用户实例并保存到数据库
    new_user = Admin(username=username, password=password,email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': '注册成功'})



@auth_blueprint.route('/api/queryUser', methods=['POST'])
def query_user():
    data = request.get_json()
    username = data.get('username')
    
    # 如果用户名为空，则返回所有用户信息
    if not username:
        users = Admin.query.all()
        user_list = [{'id':user.id,'username': user.username, 'password': user.password, 'email': user.email, 'created_at': user.created_at, 'status': user.status} for user in users]
        return jsonify({'message': '查询成功', 'users': user_list})
    
    # 否则，根据用户名查询用户信息
    users = Admin.query.filter(Admin.username.ilike(f'%{username}%')).all()

    if users:
        user_list = [{'id':user.id,'username': user.username, 'password': user.password, 'email': user.email, 'created_at': user.created_at, 'status': user.status} for user in users]
        return jsonify({'message': '查询成功', 'users': user_list})
    else:
        return jsonify({'message': '未找到相关用户'}), 404







# 编写更新数据的路由处理函数
@auth_blueprint.route('/api/updateAdmin', methods=['PUT'])
def update_data():
    try:
        # 从请求体中获取更新后的数据
        data = request.json
        
        # 根据数据中的 ID 查询对应的记录
        Admin_id = data.get('id')
        admin_info = Admin.query.get(Admin_id)
        
        if admin_info:
            # 更新记录的内容
            admin_info.password = data.get('password')
            # summary.summary = data.get('summary')
            # 其他字段的更新操作...

            # 提交到数据库
            db.session.commit()
            
            return jsonify({'message': '数据更新成功'}), 200
        else:
            return jsonify({'message': '未找到对应ID的数据'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# 删除数据
@auth_blueprint.route('/api/deleteAdmin', methods=['DELETE'])
def delete_data():
    try:
        data = request.get_json()
        admin_id = data.get('id')
        # 查询对应ID的数据
        admin_info = Admin.query.get(admin_id)
        if admin_info:
            # 将对应数据的 status 设置为 0
            admin_info.status = 0
            db.session.commit()
            return jsonify({'message': '删除成功'}), 200
        else:
            return jsonify({'message': '未找到对应ID的数据'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    




# 在原有的路由下添加新的路由处理函数
@auth_blueprint.route('/api/updatePassword', methods=['PUT'])
def update_password():
    try:
        # 从请求体中获取用户名和密码信息
        data = request.get_json()
        username = data.get('username')
        old_password = data.get('oldPassword')
        new_password = data.get('newPassword')

        # 查询对应用户名的用户
        user = Admin.query.filter_by(username=username).first()

        if user:
            # 验证旧密码是否正确
            if user.password == old_password:
                # 更新密码
                user.password = new_password
                db.session.commit()
                return jsonify({'message': '密码更新成功'}), 200
            else:
                return jsonify({'message': '旧密码不正确'}), 400
        else:
            return jsonify({'message': '用户不存在'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500