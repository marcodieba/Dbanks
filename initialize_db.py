# -*- Mode: Python; coding: utf-8 -*-
from app import db
from app.models import Users, AdminUser
from werkzeug import generate_password_hash

# Drop all tables from db file
#db.drop_all()
db.create_all()

# db.session.add(Users("marco","marco@marco.com", '123'))
# db.session.add(Users("ciara","ciara@ciara.com",'123'))
# db.session.add(Users("cc","c@c.com","321"))
# db.session.add(AdminUser(login="test", password=generate_password_hash("test")))



# for d in dados:
#     db.session.add(d)
db.session.commit()

# Create all tables on db file,
# copying the structure from the definition on the Models
