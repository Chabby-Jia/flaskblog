

from flask import render_template, request , flash, url_for, redirect , session
from app.web import web
from app.forms.login import LoginForm
from app.models import Admin
from flask_login import login_user , current_user , logout_user
# 额外引入 abort
# abort 是专门用来主动抛出 HTTP 请求错误的
# 一旦 abort 执行，那么后续的所有代码都不会继续执行
from flask import abort




# route 额外接受一个 methods 参数，因为我们的 login 视图需要处理 post 和 get 两种请求
@web.route('/login', methods=['POST', 'GET'])
def login():
    """登录视图"""

    # 判断用户是否为已登录状态
    # 如果用户已登录则跳转回首页
    if current_user.is_authenticated:
        return redirect(url_for('web.index'))

    # 实例化 LoginForm 表单类，并且向它传递一个参数
    # request 对象可以用来获取客户端传递的各种数据
    # request.form 就是得到前端表单中填写的数据
    # 向表单类传递 request.form 不是必须的，但是如果登录失败，用户填写的数据会保留在表单的输入框中，增加用户体验
    # 保留用户填写的数据除了要在这里传入 request.form，前端表单也需要接收，后面会提到
    form = LoginForm(request.form)

    # flask-wtf 独有的方法，它等同于下面这种写法：
    # if request.method == 'POST' and form.validate():
    if form.validate_on_submit():
        # 表单校验成功，去 admin 表中查询是否有 username 与表单 username 匹配的记录
        admin = Admin.query.filter_by(username=form.username.data).first()
        # 判断记录是否存在并判断密码是否匹配
        # check_password 是我们最开始就写好的校验密码的方法
        if admin and admin.check_password(form.password.data):

            # 配置 session 的 permanent 的值为 True
            # 使 PERMANENT_SESSION_LIFETIME 配置项生效
            session.permanent = True

            # 如果有这条记录，且密码匹配，处理代码写在这里
            # 数据校验通过，执行 login_user 方法
            # 这个方法有一个必须参数，就是登录用户的查询实例
            # remember 参数控制是否记住用户，也就是浏览器关闭之后，再次打开，是否保留登录状态
            login_user(admin, remember=form.remember.data)

            # 通过 request.args.get 获取 next 参数值
            # 自动生成的 next 参数值是一个相对链接
            # 也就是类似 `/admin` 这种形式的
            next_url = request.args.get('next')
            # 如果 next_url 没有值或者 next_url 不是以 `/` 开头的话
            # next_url 的值就等于 url_for('web.index')
            # 否则 next_url 的值就是 next 参数的值
            # url_for 方法接受视图的 endpoint 作为参数，返回的是视图的相对链接
            if not next_url or not next_url.startswith('/'):
                next_url = url_for('web.index')
            # 通过 redirect 执行重定向
            return redirect(next_url)


        else:
            # 如果数据库中没有相应的记录或者密码不匹配，处理代码写在这里
            flash('登录失败！请检查用户名或密码', 'error')
    # 渲染登录页面模板，并传递表单实例
    return render_template('login/login.html', form=form)





@web.route('/logout')
def logout():
    """登出视图"""
    # 如果是未登录用户访问，直接抛出 404 错误
    if not current_user.is_authenticated:
        abort(404)
    logout_user()
    flash('已登出', 'info')
    return redirect(url_for('web.login'))