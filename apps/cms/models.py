#encoding: utf-8
from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

Column = db.Column
model = db.Model

class CMSPermission(object):
    #以二进制的方式来表示权限
    ALL_PERMISSION = 0b11111111
    #1、访问者权限
    VISITOR =        0b00000001
    #2、管理帖子权限
    POSTER =         0b00000010
    #3、管理评论的权限
    COMMENTER =      0b00000100
    #4、管理板块的权限
    BORDER =         0b00001000
    #5、管理前台用户的权限
    FRONTUSER =      0b00010000
    #6、管理后台用户的权限
    CMSUSER =        0b00100000
    #7、管理后台管理员的权限
    ADMINER =        0b01000000

cms_role_user = db.Table(
    'cms_role_user',
    Column('cms_role_id',db.Integer,db.ForeignKey('cms_role.id'),primary_key=True),
    Column('cms_user_id',db.Integer,db.ForeignKey('cms_user.id'),primary_key=True)
)

class CMSRole(model):
    __tablename__ = 'cms_role'
    id = Column(db.Integer,primary_key=True,autoincrement=True)
    name = Column(db.String(50),nullable=False)
    desc = Column(db.String(100),nullable=False)
    create_time = Column(db.DateTime,default=datetime.now)
    permissions = Column(db.Integer,default=CMSPermission.VISITOR)
    user = db.relationship('CmsUser',secondary='cms_role_user',backref='roles')

class CmsUser(model):
    __tablename__ = 'cms_user'
    id = Column(db.Integer,primary_key=True,autoincrement=True)
    username = Column(db.String(50),nullable=False)
    _password = Column(db.String(100),nullable=False)
    email = Column(db.String(50),nullable=False,unique=True)
    join_time = Column(db.DateTime,default=datetime.now)

    def __init__(self,username,password,email):
        self.username = username
        self.password = password
        self.email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self,raw_password):
        result = check_password_hash(self._password,raw_password)
        return result

    @property
    def permissions(self):
        if not self.roles:
            return 0
        all_permissions = 0
        for role in self.roles:
            permission = role.permissions
            all_permissions |= permission
        return all_permissions

    def has_permission(self,permission):
        # all_permissions = self.permissions
        # result = all_permissions&permission == permission
        # return result
        return self.permissions&permission == permission

    @property
    def is_developer(self):
        return self.has_permission(CMSPermission.ALL_PERMISSION)

# user = CmsUser()
# print(user.password)
# user.password = 'abc'