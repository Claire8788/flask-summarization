from flask import Blueprint, jsonify
from flask import Flask, request
from model import UserSummary,Admin 
from datetime import datetime
from datetime import timedelta
from extension import db

table_blueprint = Blueprint('table', __name__)



# 会议表单获取和查询
@table_blueprint.route('/api/tableData', methods=['GET'])
def get_table_data():
    # 导入Username
    # 获取时间参数
    username = request.args.get('username')
    created_at = request.args.get('created_at')

    try:
        if username == 'admin':
            # 如果是管理员，根据时间参数查询数据
            if created_at == '':  # 如果时间参数为空字符串，则返回全部数据
                # summaries = UserSummary.query.all()
                summaries = UserSummary.query.filter_by(status=1).all()
            else:
                # 检查时间参数的格式，根据格式选择不同的筛选方式
                if '-' in created_at:
                    # 将时间字符串转换为 datetime 对象
                    created_at_datetime = datetime.strptime(created_at, '%Y-%m-%d')
                    # 计算日期范围，包括当天的起始时间和次日的起始时间
                    next_day = created_at_datetime + timedelta(days=1)
                    # 根据日期范围筛选数据
                    summaries = UserSummary.query.filter(UserSummary.status == 1,
                                                         UserSummary.created_at >= created_at_datetime,
                                                         UserSummary.created_at < next_day).all()
                else:
                    # 将时间字符串转换为年份
                    year = int(created_at)
                    # 计算年份范围，包括该年的起始时间和次年的起始时间
                    next_year = datetime(year + 1, 1, 1)
                    # 根据年份范围筛选数据
                    summaries = UserSummary.query.filter(UserSummary.status == 1,
                                                         UserSummary.created_at >= datetime(year, 1, 1),
                                                         UserSummary.created_at < next_year).all()
        else:
            # 如果不是管理员，根据用户名查询对应的管理员信息
            admin = Admin.query.filter_by(username=username,status=1).first()
            if admin:
                # 根据管理员ID和时间参数查询数据
                if created_at == '':
                    summaries = UserSummary.query.filter_by(status=1,user_id=admin.id).all()
                else:
                    # summaries = UserSummary.query.filter(UserSummary.user_id == admin.id,
                    #                                      UserSummary.created_at == created_at).all()
                        # 检查时间参数的格式，根据格式选择不同的筛选方式
                    if '-' in created_at:
                        # 将时间字符串转换为 datetime 对象
                        created_at_datetime = datetime.strptime(created_at, '%Y-%m-%d')
                        # 计算日期范围，包括当天的起始时间和次日的起始时间
                        next_day = created_at_datetime + timedelta(days=1)
                        # 根据日期范围筛选数据
                        summaries = UserSummary.query.filter(UserSummary.status == 1,
                                                             UserSummary.user_id == admin.id,
                                                             UserSummary.created_at >= created_at_datetime,
                                                             UserSummary.created_at < next_day).all()
                    else:
                        # 将时间字符串转换为年份
                        year = int(created_at)
                        # 计算年份范围，包括该年的起始时间和次年的起始时间
                        next_year = datetime(year + 1, 1, 1)
                        # 根据年份范围筛选数据
                        summaries = UserSummary.query.filter(UserSummary.status == 1,
                                                             UserSummary.user_id == admin.id,
                                                             UserSummary.created_at >= datetime(year, 1, 1),
                                                             UserSummary.created_at < next_year).all()
            else:
                return jsonify({'message': '未找到管理员信息'}), 404
        
        # 将查询到的数据转换为字典列表
        summary_list = []
        for summary in summaries:
            summary_dict = {
                'id': summary.id,
                'text': summary.text,
                'summary': summary.summary,
                'model': summary.model,
                'created_at': summary.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            summary_list.append(summary_dict)

        # 返回数据
        return jsonify({'list': summary_list, 'total': len(summary_list)})
    except ValueError:
        # 如果时间格式不正确，则返回错误消息给前端
        return jsonify({'message': '时间格式不正确，请使用格式 %Y-%m-%d 或 %Y'}), 400
    
# 删除数据
# @table_blueprint.route('/api/deleteData', methods=['DELETE'])
# def delete_data():
#     try:
#         data = request.get_json()
#         summary_id = data.get('index')
#         # 查询对应ID的数据
#         summary = UserSummary.query.get(summary_id)
#         if summary:
#             # 删除数据
#             db.session.delete(summary)
#             db.session.commit()
#             return jsonify({'message': '删除成功'}), 200
#         else:
#             return jsonify({'message': '未找到对应ID的数据'}), 404
#     except Exception as e:
#         return jsonify({'message': str(e)}), 500
# 删除数据
@table_blueprint.route('/api/deleteData', methods=['DELETE'])
def delete_data():
    try:
        data = request.get_json()
        summary_id = data.get('id')
        # 查询对应ID的数据
        summary = UserSummary.query.get(summary_id)
        if summary:
            # 将对应数据的 status 设置为 0
            summary.status = 0
            db.session.commit()
            return jsonify({'message': '删除成功'}), 200
        else:
            return jsonify({'message': '未找到对应ID的数据'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    


# 编写更新数据的路由处理函数
@table_blueprint.route('/api/updateData', methods=['PUT'])
def update_data():
    try:
        # 从请求体中获取更新后的数据
        data = request.json
        
        # 根据数据中的 ID 查询对应的记录
        summary_id = data.get('id')
        summary = UserSummary.query.get(summary_id)
        
        if summary:
            # 更新记录的内容
            summary.text = data.get('text')
            summary.summary = data.get('summary')
            # 其他字段的更新操作...

            # 提交到数据库
            db.session.commit()
            
            return jsonify({'message': '数据更新成功'}), 200
        else:
            return jsonify({'message': '未找到对应ID的数据'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500
