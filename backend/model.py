from extension import db
# 创建管理员模型
class Admin(db.Model):
    __tablename__ = 'Admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True, unique=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    # updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    status = db.Column(db.Integer, default=1)  # 添加 status 字段，默认为 1

# 创建用户摘要模型
class UserSummary(db.Model):
    __tablename__ = 'user_summary'
    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('Admin.id'))
    text = db.Column(db.Text)
    summary = db.Column(db.Text)
    model = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    # updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    status = db.Column(db.Integer, default=1)  # 添加 status 字段，默认为 1