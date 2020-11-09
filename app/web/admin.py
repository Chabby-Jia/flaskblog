

from flask import render_template
# 引入 login_required
from flask_login import login_required

from app.web import web

@web.route('/admin')
# 只需要给视图函数加上 @login_required 装饰器即可实现访问控制
@login_required
def admin():
    return render_template('admin/admin.html')