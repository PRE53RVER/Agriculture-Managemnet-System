from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    mobile = db.Column(db.String(100))
    password = db.Column(db.String(100))

# profile table
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    address = db.Column(db.String(100))
    city = db.Column(db.String(100))
    district = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))    
    pincode = db.Column(db.String(100))
    gender = db.Column(db.String(100))
    dob = db.Column(db.String(100))
    panchayat = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('profiles', lazy=True))

# cultivation table
class Cultivation(db.Model):
    cultivation_id = db.Column(db.Integer, primary_key=True)
    survey_number = db.Column(db.String(100))
    crop_name = db.Column(db.String(100))
    crop_type = db.Column(db.String(100))
    crop_quantity = db.Column(db.String(100))
    planting_date = db.Column(db.String(100))
    harvesting_date = db.Column(db.String(100))
    expected_yield = db.Column(db.String(100))
    irrigation_type = db.Column(db.String(100))
    land_type = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# bank details table
class Bank(db.Model):
    bank_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    account_number = db.Column(db.String(100))
    ifsc_code = db.Column(db.String(100))
    bank_name = db.Column(db.String(100))
    branch_name = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
     
# admin table
class Admin(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    panchayat = db.Column(db.String(100))

# loan table
class Loan(db.Model):
    loan_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    panchayat = db.Column(db.String(100))
    loan_amount = db.Column(db.String(100))
    loan_type = db.Column(db.String(100))
    loan_status = db.Column(db.String(100), default='pending')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# insurance table
class Insurance(db.Model):
    insurance_id = db.Column(db.Integer, primary_key=True)
    scheme_type = db.Column(db.String(100))
    crop_type = db.Column(db.String(100))
    crop_name = db.Column(db.String(100))
    crop_count = db.Column(db.String(100))
    panchayat = db.Column(db.String(100))
    duration = db.Column(db.String(100))
    insurance_amount = db.Column(db.String(100))
    insurance_status = db.Column(db.String(100), default='pending')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# compenstation table
class Compensation(db.Model):
    compensation_id = db.Column(db.Integer, primary_key=True)
    survey_number = db.Column(db.String(100))
    crop_name = db.Column(db.String(100))
    land_name = db.Column(db.String(100))
    crop_count = db.Column(db.String(100))
    stage = db.Column(db.String(100))
    unit = db.Column(db.String(100))
    ward = db.Column(db.String(100))
    image = db.Column(db.String(100))
    status = db.Column(db.String(100), default='pending')
    panchayat = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# subsidy table
class Subsidy(db.Model):
    subsidy_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(100))
    panchayat = db.Column(db.String(100))
    status = db.Column(db.String(100), default='pending')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# land details table
class Land(db.Model):
    land_id = db.Column(db.Integer, primary_key=True)
    land_name = db.Column(db.String(100), unique=True)
    kbhavan = db.Column(db.String(100))
    taluk = db.Column(db.String(100))
    village = db.Column(db.String(100))
    district = db.Column(db.String(100))
    block_number = db.Column(db.String(100))
    survey_number = db.Column(db.String(100))
    subdivision_number = db.Column(db.String(100))
    ward_number = db.Column(db.String(100))
    panchayat = db.Column(db.String(100))
    land_area = db.Column(db.String(100))
    land_type = db.Column(db.String(100))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# table products
class Product(db.Model):

    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.String(100))
    image = db.Column(db.String(100))
    description = db.Column(db.String(100))
    type = db.Column(db.String(100))
   
# table cart
class Cart(db.Model):
    
        cart_id = db.Column(db.Integer, primary_key=True)
        product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# table order
class Order(db.Model):
        
        order_id = db.Column(db.Integer, primary_key=True)
        product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        order_date = db.Column(db.String(100))
        order_quantity = db.Column(db.String(100))
        order_status = db.Column(db.String(100), default='pending')


# table notification
class Notification(db.Model):
            
            notification_id = db.Column(db.Integer, primary_key=True)
            user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
            notification_date = db.Column(db.String(100))
            title = db.Column(db.String(100))
            notification_message = db.Column(db.String(100))
            notification_status = db.Column(db.String(100), default='unread')

    