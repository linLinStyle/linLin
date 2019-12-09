#encoding: utf-8
from exts import db
import shortuuid
import enum
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

Column = db.Column

class GenderEnum(enum.Enum):
    MALE = 1
    FEMALE = 2
    SECRET = 3
    UNKNOW = 4

class FrontUser(db.Model):
    __tablename__ = 'front_user'
    id = Column(db.String(50),primary_key=True,default=shortuuid.uuid)
    telephone = Column(db.String(11),nullable=False,unique=True)
    username = Column(db.String(50),nullable=False)
    _password = Column(db.String(100),nullable=False)
    email = Column(db.String(50),unique=True)
    realname = Column(db.String(50))
    avatar = Column(db.String(100))
    signature = Column(db.String(100))
    gender = Column(db.Enum(GenderEnum),default=GenderEnum.UNKNOW)
    join_time = Column(db.DateTime,default=datetime.now)

    def __init__(self,*args,**kwargs):
        if 'password' in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop('password')
        super(FrontUser, self).__init__(*args,**kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,newpwd):
        self._password = generate_password_hash(newpwd)

    def check_password(self,raw_password):
        return check_password_hash(self._password,raw_password)