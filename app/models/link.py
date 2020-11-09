# app/models/link.py

from app.models.base import Base
from app.libs.extensions import db


class Link(Base):
    """
    链接数据表模型
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    url = db.Column(db.String(256))
    # tag 字段设置为枚举类型
    tag = db.Column(db.Enum(
        'weixin', 'weibo', 'douban', 'zhihu', 'google', 'linkedin', 'twitter',
        'facebook', 'github', 'telegram', 'other', 'friendLink'
    ))