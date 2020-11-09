


from datetime import datetime
from app.models.base import Base
from app.libs.extensions import db
class Comment(Base):
    """
    文章评论数据表模型类
    """
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(16))
    email = db.Column(db.String(64))
    site = db.Column(db.String(256))
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    from_admin = db.Column(db.Boolean, default=False)
    reviewed = db.Column(db.Boolean, default=False)
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    replied = db.relationship('Comment', remote_side=[id], uselist=False)
    replies = db.relationship('Comment', cascade='all')
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', uselist=False)


"""
id: 主键
author: 评论作者昵称
email: 评论者邮箱
site: 评论者个人站点
content: 评论内容
create_time: 评论时间
from_admin: 是否是管理员评论
reviewed: 是否审核通过
replied_id: 该评论所回复的评论 id
replied: 构建自关联关系
replies: 构建自关联关系
post_id: 评论所属的文章 id
post: 构建与 Post 的关系
"""