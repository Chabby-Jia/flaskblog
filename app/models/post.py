


from datetime import datetime
from app.models.base import Base
from app.libs.extensions import db , whooshee



# 增加一个装饰器即可
# `register_model` 接受的参数是需要检索的字段名称
@whooshee.register_model('title', 'content')
class Post(Base):
    """
    Blog文章数据表模型类
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    categories = db.relationship('Category', secondary='post_category_middle')
    comments = db.relationship(
        'Comment', cascade='all, delete-orphan'
    )
    can_comment = db.Column(db.Boolean, default=True)
    description = db.Column(db.String(150))
    # 储存 markdown 格式的正文，用以编辑时传递给 markdown 编辑器
    content_markdown = db.Column(db.Text)
    # 储存 HTML 格式正文，用来展示
    content = db.Column(db.Text)
    trash = db.Column(db.Boolean, default=False)
    published = db.Column(db.Boolean, default=True)

"""
id: 主键字段，必不可少
title: 文章标题
content: 文章正文
create_time: 创建时间
categories: 构建与 Category 表关系
comments: 构建与 Comments 表关系
can_comment: 是否允许评论
description: 文章描述，SEO 相关
"""