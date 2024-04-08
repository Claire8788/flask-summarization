from flask import Blueprint, jsonify
from flask import Flask, request
from model import UserSummary
from datetime import datetime
from datetime import timedelta

table_blueprint = Blueprint('table', __name__)


#会议表单获取和查询
@table_blueprint.route('/api/tableData', methods=['GET'])
def get_table_data():
    #导入Username
    # 获取时间参数
    created_at = request.args.get('created_at')

    try:
        if created_at == '':  # 如果时间参数为空字符串，则返回全部数据
            summaries = UserSummary.query.all()
        else:
            # 检查时间参数的格式，根据格式选择不同的筛选方式
            if '-' in created_at:
                # 将时间字符串转换为 datetime 对象
                created_at_datetime = datetime.strptime(created_at, '%Y-%m-%d')
                # 计算日期范围，包括当天的起始时间和次日的起始时间
                next_day = created_at_datetime + timedelta(days=1)
                # 根据日期范围筛选数据
                summaries = UserSummary.query.filter(UserSummary.created_at >= created_at_datetime,
                                                  UserSummary.created_at < next_day).all()
            else:
                # 将时间字符串转换为年份
                year = int(created_at)
                # 计算年份范围，包括该年的起始时间和次年的起始时间
                next_year = datetime(year + 1, 1, 1)
                # 根据年份范围筛选数据
                summaries = UserSummary.query.filter(UserSummary.created_at >= datetime(year, 1, 1),
                                                  UserSummary.created_at < next_year).all()
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