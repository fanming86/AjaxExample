from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import time

Base = declarative_base()
engine = create_engine('mysql+mysqlconnector://root:1234@localhost/dutylist')
DBSession = sessionmaker(bind=engine)
db = DBSession()



class User(Base):
    __tablename__ = "du_user"
    user_id = Column( Integer,primary_key=True)
    username = Column(String(64), unique=True)
    phone = Column(String(64), unique=True)
    password = Column(String(64), unique=True)
    create_time = Column( unique=True)

    def __init__(self, username, phone, password, create_time):
        self.username = username
        self.phone = phone
        self.password = password
        self.create_time = create_time

    def __repr__(self):
        return self.username

phone = 111
username = 'zzz'
password = '123'
repassword = '1'

# if phone and password:
#     try:
#         user = db.query(User).filter(User.phone == phone).all()
#     except:
#         print 'phone not exist!'
#     else:
#         if user.password == password:
#             print 'login secusse!'
#         else:
#             print "password error!!!"
# else:
#     print 'phone or password is none!'
# data = User(username=username, phone=phone, password=password, create_time=time.time())
# print user.password
# db.add(data)
# db.commit()

if username and phone and password and repassword:
    user = db.query(User).filter(User.phone == phone).all()
    if user:
        print ('the thon has been register!')
    elif password != repassword:
        print('Password and Confirm Password not same')
    else:
        print('register success!')
else:
    print('field can not be empty')
db.close()

