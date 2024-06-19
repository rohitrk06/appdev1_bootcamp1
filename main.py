from flask import Flask,render_template, url_for,request,redirect
from application.database import db
from application.config import Config
from application.models import *
# from werkzeug.security import generate_password_hash


def create_app():
    app = Flask(__name__,template_folder='template')

    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()

        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin', description='Administrator')
            db.session.add(admin_role)
        store_manager = Role.query.filter_by(name='store_manager').first()
        if not store_manager:
            store_manager = Role(name='store_manager', description='Store Manager')
            db.session.add(store_manager)
        customer = Role.query.filter_by(name='customer').first()
        if not customer:
            customer = Role(name='customer', description='Customer')
            db.session.add(customer)
        admin = User.query.filter_by(username='admin').first()
        # print(admin)
        if not admin:
            admin = User(username='admin',
                            email='admin@gmail.com',
                            password='admin',
                            address = 'Kathmandu',
                            roles = [admin_role])
            
            db.session.add(admin)
        db.session.commit()
    
    return app

app = create_app()

from application.routes import *
from application.auth_routes import *


if __name__ == '__main__':
    app.run(debug=True)







# from flask import Flask
# from application.database import db
# from application.config import Config
# from application.models import *

# def create_app():
#     app = Flask(__name__)

#     app.config.from_object(Config)
   
#     db.init_app(app)
#     # app.app_context().push()

#     with app.app_context():
#         db.create_all()

#         db.session.commit()
#     return app

# app = create_app()

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

# if __name__ == '__main__':
#     app.run(debug=True)