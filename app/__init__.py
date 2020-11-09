# app/__init__.py

import click
import os
from flask import Flask
# 引入配置字典
from app.configs import configs
from app.libs.extensions import db, migrate, get_login_manager, csrf_protect, mail ,  whooshee
from app.libs.fake_data import FakeData
from app.models import Post, Category, post_category_middle, Comment, Admin, Link
# 引入 datetime
from datetime import datetime
from app.libs.custom_filters import switch_link_tag , get_search_part




def create_app(config="development"):
    """
    工厂函数
    """
    app = Flask(__name__)
    app.config.from_object(configs[config])
    register_extensions(app)

    # 注册蓝图
    register_blueprints(app)

    # 调用函数
    register_template_context(app)

    # 注册自定义过滤器
    add_template_filters(app)

    # 调用注册命令函数
    register_cli(app)

    return app



def add_template_filters(app):
    """
    注册自定义模板验证器
    """
    app.add_template_filter(switch_link_tag)
    app.add_template_filter(get_search_part)

def register_blueprints(app):
    """
    注册蓝图
    """
    # 因为我们只会在这里用到 `web` 蓝图实例，所以就再函数内部引用它
    from app.web import web

    app.register_blueprint(web)




def register_extensions(app):
    """
    注册第三方插件
    """
    db.init_app(app)
    migrate.init_app(app, db)
    csrf_protect.init_app(app)
    # 获取 login_manager 并调用 init_app 方法将其注册到 Flask 核心对象上
    login_manager = get_login_manager()
    login_manager.init_app(app)
    mail.init_app(app)
    whooshee.init_app(app)


# 我们需要在工厂函数中注册，所以需要构建一个函数在工厂函数中调用
def register_template_context(app):
    """
    注册模板全局变量
    """
    @app.context_processor
    def generate_template_context():
        admin = Admin.query.first()
        categories = Category.query.all()
        links = Link.query.all()
        # 当前年份，页脚所需数据
        current_year = datetime.now().year
        return {"admin": admin, "categories": categories, "links": links, "current_year": current_year}



# 然后给 initdb 命令添加一个参数
def register_cli(app: Flask):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='删除数据表并重建')
    # --_init 参数是为了再内部初始化数据库时不再二次确认用的
    @click.option('--_init', is_flag=True, help='删除并重建数据表 (内部调用)')
    def initdb(drop, _init):
        """初始化数据库"""

        if drop:
            click.confirm('确定要删除所有数据表？', abort=True)
            db.drop_all()
            click.echo('数据表删除成功')

        # 如果传递的是 --_init 参数，那么会直接删除数据库
        if _init:
            db.drop_all()
            click.echo('数据表删除成功')
        db.create_all()
        # 初始化数据后在分类表中添加一条记录作为默认默认分类
        with db.auto_commit():
            category = Category()
            category.alias = 'default'
            db.session.add(category)
        click.echo('数据表已成功创建')

    @app.cli.command()
    @click.option('--category', type=int, help='要生成的Blog分类数量，默认 9')
    @click.option('--post', type=int, help='要生成的Blog文章数量，默认 50')
    @click.option('--comment', type=int, help='要生成的评论数量，默认 1000')
    def fake(category, post, comment):
        """生成虚拟数据"""
        click.confirm('该操作会删除现有数据表并重建，确定吗？', abort=True)
        # 通过 os.system 我们在这个命令的内部执行了初始化数据库的命令
        os.system('flask initdb --_init')
        click.echo('数据表已重建，开始生成虚拟数据...')
        click.echo('生成管理员与Blog设置数据中...')
        FakeData.fake_admin()
        click.echo('Done!')
        click.echo('生成Blog分类数据中...')
        FakeData.fake_categories(category) if category else FakeData.fake_categories()
        click.echo('Done!')
        click.echo('生成Blog文章数据中...')
        FakeData.fake_posts(post) if post else FakeData.fake_posts()
        click.echo('Done!')
        click.echo('生成Blog评论数据中...')
        FakeData.fake_comments(comment) if comment else FakeData.fake_comments()
        click.echo('Done!')
        click.echo('生成Blog链接数据中...')
        FakeData.fake_links()
        click.echo('Done!')
        click.echo('数据已全部生成完毕！')



    @app.cli.command()
    @click.option('--username', prompt='请输入管理员用户名', help='管理员用户名')
    @click.password_option(prompt='请输入管理员密码', help='管理员密码')
    @click.option('--email',prompt='请输入管理员邮箱', help='管理员邮箱')
    def admin(username, password , email):
        """设置管理员用户名与密码"""
        # 处理 MySQL 错误
        try:
            admin = Admin.query.first()
        except Exception as e:
            if '1146' in str(e.orig):
                click.echo('数据表不存在，请执行 `flask initdb` 创建数据表')
            else:
                print(e)
                click.echo('请检查错误信息')
            return
        with db.auto_commit():
            if admin:
                click.echo('更新管理员账户信息...')
                admin.username = username
                admin.password = password
                admin.email = email
            else:
                click.echo('创建管理员账户中...')
                admin = Admin()
                admin.username = username
                admin.password = password
                admin.email = email
                admin.blog_title = '临时Blog名'
                admin.blog_subtitle = '临时Blog副标题'
                admin.blog_about = '临时Blog关于'
                admin.nickname = '临时昵称'
            db.session.add(admin)
            click.echo('Done.')