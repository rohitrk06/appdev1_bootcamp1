from application.database import db



class User(db.Model):
    username = db.Column(db.String(30),primary_key=True)
    email = db.Column(db.String(50),nullable=False,unique = True)
    password = db.Column(db.String(50),nullable=False)
    address = db.Column(db.String(100),nullable=True)

    #Relationships
    roles = db.relationship('Role',secondary='role_user',backref=db.backref('users',lazy=True))

    def __repr__(self):
        return f'<User {self.username}>'

class Role(db.Model):
    role_id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30),nullable=False)
    description = db.Column(db.String(100),nullable=True)

    def __repr__(self):
        return f'<Role {self.name}>'

class RoleUser(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(30),db.ForeignKey('user.username'))
    role_id = db.Column(db.Integer,db.ForeignKey('role.role_id'))


class Categories(db.Model):
    category_id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(40),nullable=False)
    description = db.Column(db.String(100),nullable=True)

    #Relationships
    products = db.relationship('Product',backref='category',lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'
    
class Product(db.Model):
    product_id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(40),nullable=False)
    description = db.Column(db.String(100),nullable=True)
    selling_price = db.Column(db.Float,nullable=False)
    stock = db.Column(db.Integer,nullable=False)
    manufacture_date = db.Column(db.Date,nullable=False)
    expiry_date = db.Column(db.Date,nullable=True)
    cost_price = db.Column(db.Float,nullable=False)
    image_url = db.Column(db.String(100),nullable=True)
    category_id = db.Column(db.Integer,db.ForeignKey('categories.category_id'))

    #Relationships


    def __repr__(self):
        return f'<Product {self.name}>'
    

class Cart(db.Model):
    card_id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(30),db.ForeignKey('user.username'))
    product_id = db.Column(db.Integer,db.ForeignKey('product.product_id'))
    quantity = db.Column(db.Integer,nullable=False)

class Requests(db.Model):
    request_id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(30),db.ForeignKey('user.username'))
    category_id = db.Column(db.Integer,db.ForeignKey('categories.category_id'), nullable= True)
    request_type = db.Column(db.String(20),nullable=False)
    request_date = db.Column(db.Date,nullable=False)
    status = db.Column(db.String(20),nullable=False)
    new_category_name = db.Column(db.String(40),nullable=True)
    new_category_description = db.Column(db.String(100),nullable=True)

    #Relationships
    catergory = db.relationship('Categories',backref='requests',lazy=True)

    def __repr__(self):
        return f'<Request {self.catergory_id} - {self.request_type}>'


class PurchaseHistory(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    order_id = db.Column(db.Integer,nullable=False)
    username = db.Column(db.String(30),db.ForeignKey('user.username'))
    product_id = db.Column(db.Integer,db.ForeignKey('product.product_id'))
    quantity = db.Column(db.Integer,nullable=False)
    purchase_date = db.Column(db.Date,nullable=False)
    total_price = db.Column(db.Float,nullable=False)

    #Relationships
    product = db.relationship('Product',backref='purchase_history',lazy=True)
