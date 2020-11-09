import os
# SEND_FILE_MAX_AGE_DEFAULT 接受 timedelta 对象作为值
from datetime import timedelta
from app.models import Admin, Category, Comment, Link, Post

# 获取项目根目录路径
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
class BaseConfig:
    """
    配置基类，公用配置写在这里
    """
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    # 设置用户勾选了 “记住我” 之后登陆状态保留 31 天
    REMEMBER_COOKIE_DURATION = timedelta(days=31)
    # 设置默认的 session cookie 过期时间，就让它 3 天过期吧
    PERMANENT_SESSION_LIFETIME = timedelta(days=3)
    # 添加一个 MODELS 字典，存放模型名称:模型
    MODELS = {'Admin': Admin, 'Category': Category, 'Comment': Comment, 'Link': Link, 'Post': Post}
    # 后台分页数量
    ADMIN_PER_PAGE = 20
    # 图片文章上传路径
    UPLOAD_FOLDER = os.path.join(basedir, 'app/uploads')
    # 允许上传的文件格式
    ALLOWED_EXTENSIONS = ("jpg", "jpeg", "gif", "png", "bmp", "webp", 'svg')


    # 邮箱配置
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL')
    MAIL_USE_TSL = os.getenv('MAIL_USE_TSL')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')


    #匹配最小搜索字符
    WHOOSHEE_MIN_STRING_LEN = 2



class DevelopmentConfig(BaseConfig):
    """
    开发环境配置类
    """
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    # 设置缓存时间为 1 秒，这样就不存在需要我们手动清空缓存的问题了
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)


class TestConfig(BaseConfig):
    """
    测试环境配置类
    """
    pass


class ProductionConfig(BaseConfig):
    """
    生产环境配置类
    """
    pass


# 配置类字典，根据传递的 key 选择不同的配置类
configs = {
    "development": DevelopmentConfig,
    "test": TestConfig,
    "production": ProductionConfig
}