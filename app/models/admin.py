


# 引入 Flask 核心依赖 werkzeug 的 security 模块，专门处理密码的储存和校验
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.base import Base
from app.libs.extensions import db
# 引入 UserMixin 基类
from flask_login import UserMixin






class Admin(Base , UserMixin):
    """
    管理员及Blog设置数据表模型类
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    _password = db.Column(db.String(256), nullable=False)
    nickname = db.Column(db.String(30), nullable=False)
    blog_title = db.Column(db.String(128), nullable=False)
    blog_subtitle = db.Column(db.String(256), nullable=False)
    blog_about = db.Column(db.Text)

    post_per_page = db.Column(db.Integer, default=10)
    # 评论每页展示数量
    comment_per_page = db.Column(db.Integer, default=10)
    email = db.Column(db.String(64), nullable=False)


    # 处理密码相关的查询、储存、校验工作
    @property
    def password(self):
        return self._password
    @password.setter
    def password(self, row):
        self._password = generate_password_hash(row)
    def check_password(self, row):
        return check_password_hash(self._password, row)