#coding:utf-8


from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from app import db
import os.path

db.create_all()
# 当数据库不存在的时候创建新的数据库 
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
# 否则直接更新
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))



'''
此脚本为数据库创建脚本，直接运行即可
在运行上述命令之后你会在当前工作路径下发现一个新的 app.db 文件。这是一个空的 sqlite 数据库，创建一开始就支持迁移。同样你还将有一个 db_repository 文件夹，里面还有一些文件，这是 SQLAlchemy-migrate 存储它的数据文件的地方。请注意，我们不会再生成新的存储库，前提是如果它已经存在。这将方便我们重新创建数据库，同时保留现有的存储库，如果我们需要的话我们只需要迁移数据库而不需要重新创建一个新的数据库。

'''