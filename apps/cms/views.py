#encoding: utf-8
from flask import (
    Blueprint,
    views,
    render_template,
    request,
    session,
    redirect,
    url_for,
    g,
    make_response)
from werkzeug.wrappers import Response
from .forms import (
    LoginForm,
    ResetpwdForm,
    ResetEmailForm,
    AddBannerForm,
    UpdateBannerForm,
    AddBoardForm,
    UpdateBoardForm
)
from .models import CmsUser,CMSPermission
from ..models import BannerModel,BoardModel,PostModel,HeightLightModel
from .decorators import Login_required,permission_required
import config
from exts import db,mail
from flask_mail import Message
from utils import restful,zlcache
import string
import random
from flask_paginate import Pagination,get_page_parameter
from tasks import send_mail,send_sms_captcha

bp = Blueprint('cms',__name__,url_prefix='/cms')

@bp.route('/')
@Login_required
def index():
    return render_template('cms/cms_index.html')


@bp.route('/logout/')
@Login_required
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))


@bp.route('/profile/')
@Login_required
def profile():
    return render_template('cms/cms_profile.html')


@bp.route('/email_captcha/')
@Login_required
def email_captcha():
    email = request.args.get('email')
    if not email:
        return restful.params_error('请传递邮箱参数！')
    source = list(string.ascii_letters)
    source.extend([str(x) for x in range(10)])
    captcha = ''.join(random.sample(source,6))
    #指定邮箱发送邮件
    # message = Message('Python论坛验证码',recipients=[email],body='您的验证码内容是：%s' %captcha)
    # try:
    #     mail.send(message)
    # except:
    #     return restful.server_error()
    send_mail.delay('Python论坛验证码',[email],'您的验证码内容是：%s' %captcha)
    zlcache.set(email,captcha)
    return restful.success()


@bp.route('/email/')
def send_email():
    message = Message(subject='邮件发送',recipients=['2894226511@qq.com'],body='test')
    mail.send(message)
    return 'success'


@bp.route('/posts/')
@Login_required
@permission_required(CMSPermission.POSTER)
def posts():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * 7
    end = page * 7
    posts_list = PostModel.query.slice(start, end)
    total = PostModel.query.count()
    pagination = Pagination(bs_version=3,page=page,total=total,outer_window=0)
    context = {
        'posts': posts_list,
        'pagination': pagination
    }
    return render_template('cms/cms_posts.html',**context)


@bp.route('/hpost/',methods=['POST'])
@Login_required
@permission_required(CMSPermission.POSTER)
def hpost():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error('请输入帖子id！')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error('没有这篇帖子！')
    heightlight = HeightLightModel()
    heightlight.post = post
    db.session.add(heightlight)
    db.session.commit()
    return restful.success()


@bp.route('/uhpost/',methods=['POST'])
@Login_required
@permission_required(CMSPermission.POSTER)
def uhpost():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error('请输入帖子id！')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error('没有这篇帖子！')
    heightlight = HeightLightModel.query.filter_by(post_id=post_id).first()
    db.session.delete(heightlight)
    db.session.commit()
    return restful.success()


@bp.route('/comments/')
@Login_required
@permission_required(CMSPermission.COMMENTER)
def comments():
    return render_template('cms/cms_comments.html')


@bp.route('/borders/')
@Login_required
@permission_required(CMSPermission.BORDER)
def borders():
    allborders = BoardModel.query.all()
    context = {
        'boards': allborders
    }
    return render_template('cms/cms_borders.html',**context)

@bp.route('/aborder/',methods=['POST'])
@Login_required
@permission_required(CMSPermission.BORDER)
def aboard():
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data
        board = BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/uborder/',methods=['POST'])
@Login_required
@permission_required(CMSPermission.BORDER)
def uboard():
    form = UpdateBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        board = BoardModel.query.get(board_id)
        if board:
            board.name = name
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个板块！')
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/dborder/',methods=['POST'])
@Login_required
@permission_required(CMSPermission.BORDER)
def dboard():
    board_id = request.form.get('board_id')
    board = BoardModel.query.get(board_id)
    if board:
        db.session.delete(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message='没有这个板块！')

@bp.route('/fusers/')
@Login_required
@permission_required(CMSPermission.FRONTUSER)
def fusers():
    return render_template('cms/cms_fusers.html')


@bp.route('/cusers/')
@Login_required
@permission_required(CMSPermission.CMSUSER)
def cusers():
    return render_template('cms/cms_cusers.html')


@bp.route('/croles/')
@Login_required
@permission_required(CMSPermission.ALL_PERMISSION)
def croles():
    return render_template('cms/cms_roles.html')


@bp.route('/banners/')
@Login_required
def banners():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    return render_template('cms/cms_banners.html',banners=banners)


@bp.route('/abanner/',methods=['POST'])
@Login_required
def abanner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name,image_url=image_url,link_url=link_url,priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/ubanner/',methods=['POST'])
@Login_required
def ubanner():
    form = UpdateBannerForm(request.form);
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个轮播图！')
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/dbanner/',methods=['POST'])
@Login_required
def dbanner():
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.params_error(message='请输入轮播图id！')
    banner = BannerModel.query.get(banner_id)
    if not banner:
        return restful.params_error(message='没有这个轮播图！')
    db.session.delete(banner)
    db.session.commit()
    return restful.success()


class LoginView(views.MethodView):

    def get(self,message=None):
        return render_template('cms/cms_login.html',message=message)
    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CmsUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return redirect(url_for('cms.index'))
            else:
                return self.get(message='邮箱或者密码错误！')
        else:
            # message = form.errors.popitem()[1][0]
            message = form.get_error()
            return self.get(message=message)


class ResetPwdView(views.MethodView):
    decorators = [Login_required]
    def get(self):
        return render_template('cms/cms_resetpwd.html')
    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                return restful.success()
            else:
                return restful.params_error(message='旧密码输入错误！')
        else:
            message = form.get_error()
            return restful.params_error(message=message)

class ResetEmailView(views.MethodView):
    decorators = [Login_required]
    def get(self):
        return render_template('cms/cms_resetemail.html')
    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
           return restful.params_error(form.get_error())


bp.add_url_rule('/resetemail/',view_func=ResetEmailView.as_view('resetemail'))
bp.add_url_rule('/resetpwd/',view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))