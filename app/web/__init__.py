from flask import Blueprint



web = Blueprint('web', __name__)



# 执行蓝图的模块文件，确保视图被识别
import app.web.blog
import app.web.admin
import app.web.auth