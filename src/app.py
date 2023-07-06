from flask import Flask, render_template, request, session, redirect, url_for, flash,make_response
from werkzeug.utils import secure_filename
from database import db, User,Cultivation, Profile, Admin, Insurance, Compensation, Land,Bank,Notification , Product,Subsidy
import os
from utils import is_image_file,predict
from PIL import Image
import datetime
import random


def add_notification(user_id,title, message):
    date = datetime.datetime.now()
    notification = Notification(user_id=user_id, notification_message=message, notification_date=date , title=title)
    db.session.add(notification)
    db.session.commit()

def crop_to_square(image):
    width, height = image.size
    size = min(width, height)
    left = (width - size) / 2
    top = (height - size) / 2
    right = (width + size) / 2
    bottom = (height + size) / 2
    square_image = image.crop((left, top, right, bottom))
    return square_image


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)
upload_folder = './uploads'


# check if uploads folder exists
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

PROFILE_FOLDER = os.path.join('uploads', 'profile')
if not os.path.exists(PROFILE_FOLDER):
    os.makedirs(PROFILE_FOLDER)
else:
    # clear the folder
    for filename in os.listdir(PROFILE_FOLDER):
        file_path = os.path.join(PROFILE_FOLDER, filename)
        # try:
        #     if os.path.isfile(file_path) or os.path.islink(file_path):
        #         os.unlink(file_path)
        # except Exception as e:
        #     print('Failed to delete %s. Reason: %s' % (file_path, e))


LAND_FOLDER = os.path.join('uploads', 'land')
if not os.path.exists(LAND_FOLDER):
    os.makedirs(LAND_FOLDER)
else:
    # clear the folder
    for filename in os.listdir(LAND_FOLDER):
        file_path = os.path.join(LAND_FOLDER, filename)
        # try:
        #     if os.path.isfile(file_path) or os.path.islink(file_path):
        #         os.unlink(file_path)
        # except Exception as e:
        #     print('Failed to delete %s. Reason: %s' % (file_path, e))

Product_FOLDER = os.path.join('uploads', 'product')
if not os.path.exists(Product_FOLDER):
    os.makedirs(Product_FOLDER)
else:
    # clear the folder
    for filename in os.listdir(Product_FOLDER):
        file_path = os.path.join(Product_FOLDER, filename)
        # try:
        #     if os.path.isfile(file_path) or os.path.islink(file_path):
        #         os.unlink(file_path)
        # except Exception as e:
        #     print('Failed to delete %s. Reason: %s' % (file_path, e))

def check_extension(filename):
    if not '.' in filename:
        return False
    ext = filename.rsplit('.', 1)[1]
    if ext.upper() in ['PNG', 'JPG', 'JPEG']:
        return True
    else:
        return False


def creat_admin():
    admin = Admin.query.filter_by(username='admin').first()
    if not admin:
        admin = Admin(username='admin', password='admin',email='admin@admin.com',phone='1234567890',panchayat='abc')
        db.session.add(admin)
        db.session.commit()



@app.route('/')
def home():
    
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        mobile = request.form['mobile']

        new_user = User(username=username, password=password, mobile=mobile)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    # check session
    if 'user_id' in session:
        details = Profile.query.filter_by(user_id=session['user_id']).first()
        # convert the details to dictionary
        details = details.__dict__
        # remove the id and _sa_instance_state from the dictionary
        details.pop('_sa_instance_state')
        details.pop('user_id')


        land_details = Land.query.filter_by(owner_id=session['user_id']).first()
        land_details = land_details.__dict__
        land_details.pop('owner_id')
        land_details.pop('_sa_instance_state')

        bank_details = Bank.query.filter_by(bank_id=session['user_id']).first()
        bank_details = bank_details.__dict__
        bank_details.pop('bank_id')
        bank_details.pop('_sa_instance_state')
        bank_details.pop('user_id')


        cul_details = Cultivation.query.filter_by(cultivation_id=session['user_id']).first()
        cul_details = cul_details.__dict__
        cul_details.pop('cultivation_id')
        cul_details.pop('_sa_instance_state')
        cul_details.pop('user_id')
        
        
        


        return render_template('profile.html',pfp=session['user_id'], cul_details=cul_details, details=details,bank_details=bank_details , land_details=land_details)

    return redirect(url_for('login'))

@app.route('/profile/edit', methods=['GET', 'POST'])
def profile_edit():
    # check session
    if 'user_id' in session:
        profile = Profile.query.filter_by(user_id=session['user_id']).first() 

        if request.method ==  "POST":
            if profile:
                profile.name = request.form['name']
                profile.email = request.form['email']
                profile.phone = request.form['phone']
                profile.address = request.form['address']
                profile.city = request.form['city']
                profile.state = request.form['state']
                profile.pincode = request.form['pincode']
                profile.country = request.form['country']
                profile.gender = request.form['gender']
                profile.panchayat = request.form['panchayat']
                profile.dob = request.form['dob']
                db.session.commit()
                return redirect(url_for('profile'))

            # Commit the changes to the database
            db.session.commit()
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            district = request.form['district']
            pincode = request.form['pincode']
            country = request.form['country']
            gender =  request.form['gender']
            panchayat = request.form['panchayat']
            dob = request.form['dob']

            prof = Profile(name=name,
                           email=email,
                           phone=phone,
                           address=address,
                           district=district,
                           city=city,
                           country=country,
                           state=state,
                           pincode=pincode,
                           gender=gender,
                           dob=dob,  
                           panchayat=panchayat,
                           user_id= session['user_id'],
            )                         
            db.session.add(prof)
            db.session.commit()
            return redirect(url_for('picture_upload'))
       
        return render_template('profile_edit.html',p=profile)
    return redirect(url_for('login'))

@app.route('/picture/upload', methods=['GET', 'POST'])
def picture_upload():
    if 'user_id' in session:
        id = str(session['user_id']) + '.jpg'
        k = os.path.exists(os.path.join(PROFILE_FOLDER, id))
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('picture_upload.html')
        file = request.files['file']
        # check file name and file extension and type of file and size
        print(len(file.read()))
        file.seek(0)
        if is_image_file(file.read()) and check_extension(file.filename):
            # check file size
            if len(file.read()) > 1024 * 1024 * 5:
                return render_template('picture_upload.html?error=2')
            file.seek(0)
            filename = str(session['user_id']) + '_original.jpg'
            original_image_path = os.path.join(PROFILE_FOLDER, str(session['user_id']) + '_original.jpg')
            file.save(original_image_path)

            # Open the original image and perform cropping
            image = Image.open(original_image_path)
            square_image = crop_to_square(image)

            # Save the cropped square image
            square_image_path = os.path.join(PROFILE_FOLDER, str(session['user_id']) + '.jpg')
            square_image.save(square_image_path)

            # Delete the original image
            os.remove(original_image_path)


            if k:
                return redirect(url_for('profile'))
            return redirect(url_for('add_bank'))
        else:
            return redirect(url_for('picture_upload')+ '?error=1')
        
    return redirect(url_for('login'))

@app.route('/profile/picture.jpg')
def profile_picture():
    if 'user_id' in session:
        id = str(session['user_id']) + '.jpg'
        # check if the file exists
        if os.path.exists(os.path.join(PROFILE_FOLDER, id)):
            #read file and make a response with correct content-type
            with open(os.path.join(PROFILE_FOLDER, id), 'rb') as f:
                image = f.read()
            response = make_response(image)
            response.headers.set('Content-Type', 'image/jpg')
            return response
        else:
            return 'No profile picture found <a href="/picture/upload">Upload</a>'

    return redirect(url_for('login'))

@app.route('/add_land', methods=['GET', 'POST'])
def add_land():
    # check session
    if 'user_id' in session:
        if request.method ==  "POST":
            land_type = request.form['land_type']
            name = request.form['lname']
            kbhavan = request.form['kbhavan']
            area = request.form['area']
            taluk = request.form['taluk']
            village = request.form['village']
            block_number = request.form['block_number']
            survey_number = request.form['survey_number']
            subdivision_number = request.form['subdivision_number']
            district = request.form['district']
            ward_number = request.form['ward_number']

            user_id = session['user_id']
            land = Land(land_type=land_type,
                        land_name=name,
                        kbhavan=kbhavan,
                        land_area=area,
                        taluk=taluk,
                        village=village,
                        block_number=block_number,
                        survey_number=survey_number,
                        subdivision_number=subdivision_number,
                        district=district,
                        ward_number=ward_number,
                        owner_id=user_id)
            
            db.session.add(land)
            db.session.commit()
            return redirect(url_for('add_cultivation'))
        return render_template('landdetails.html')
    return redirect(url_for('login'))

@app.route('/add_cultivation', methods=['GET', 'POST'])
def add_cultivation():
    if 'user_id' in session:
        if request.method == "POST":
            survey_number = request.form['survey_number']
            crop_name = request.form['crop_name']
            crop_type = request.form['crop_type']
            crop_quantity = request.form['crop_quantity']
            planting_date = request.form['planting_date']
            harvesting_date = request.form['harvesting_date']
            expected_yield = request.form['expected_yield']
            irrigation_type = request.form['irrigation_type']
            land_type = request.form['land_type']
            user_id = session['user_id']
            cultivation = Cultivation(crop_name=crop_name,
                                      crop_type=crop_type,
                                      survey_number=survey_number,
                                      crop_quantity=crop_quantity,
                                      planting_date=planting_date,
                                      harvesting_date=harvesting_date,
                                      expected_yield=expected_yield,
                                      irrigation_type=irrigation_type,
                                      land_type=land_type,
                                      user_id=user_id)
            db.session.add(cultivation)
            db.session.commit()
            return redirect(url_for('profile'))
        return render_template('Cultivationdetails.html')
    return redirect(url_for('login'))

@app.route('/add_bank', methods=['GET', 'POST'])
def add_bank():
    if 'user_id' in session:
        bank = Bank.query.filter_by(user_id=session['user_id']).first() 
        if request.method == "POST":
            name = request.form['name']
            bank_name = request.form['bank_name']
            branch_name = request.form['branch_name']
            ifsc_code = request.form['ifsc_code']
            account_number = request.form['account_number']
            user_id = session['user_id']
            if bank:
                # Update the existing bank details
                bank.name = name
                bank.bank_name = bank_name
                bank.branch_name = branch_name
                bank.ifsc_code = ifsc_code
                bank.account_number = account_number
                db.session.commit()
                return redirect(url_for('profile'))
            else:
                # Create a new bank entry
                bank = Bank(bank_name=bank_name,
                            name=name,
                            branch_name=branch_name,
                            ifsc_code=ifsc_code,
                            account_number=account_number,
                            user_id=user_id)
                db.session.add(bank)
            
            db.session.commit()
            return redirect(url_for('add_land'))
        
        return render_template('bankdetail.html',b=bank)
    
    return redirect(url_for('login'))

@app.route('/services', methods=['GET', 'POST'])
def services():
    if 'user_id' in session:
        return render_template('service.html')
    return redirect(url_for('login'))

@app.route('/insurance/apply', methods=['GET', 'POST'])
def insurance_apply():
    if 'user_id' in session:
        user = Profile.query.filter_by(user_id=session['user_id']).first()
        cultivation = Cultivation.query.filter_by(user_id=session['user_id']).with_entities(Cultivation.crop_name).all()
        if request.method == "POST":
            print("here")
            scheme_type = request.form['scheme_type']            
            crop_name = request.form['crop_name']
            # check if crop in in cultivation
            c = any([crop.crop_name == crop_name for crop in cultivation])
            if not c:
                return render_template('insurance_apply.html', error="Crop not in cultivation")
            crop_type = request.form['crop_type']
            crop_count = request.form['crop_count']
            insurance_amount = request.form['insurance_amount']
            duration = request.form['duration']
            panchayat = user.panchayat
            user_id = session['user_id']
            insurance = Insurance(scheme_type=scheme_type,
                                  crop_type=crop_type,
                                  crop_name=crop_name,
                                  crop_count=crop_count,
                                  insurance_amount=insurance_amount,
                                  duration=duration,
                                  panchayat=panchayat,
                                  user_id=user_id
                                   )
            db.session.add(insurance)
            db.session.commit()
            return redirect(url_for('profile'))
        return render_template('insurance_apply.html')
    
    return redirect(url_for('login'))

@app.route('/insurance/list', methods=['GET', 'POST'])
def insurance_list():
    if 'user_id' in session:
        insurances = Insurance.query.filter_by(user_id=session['user_id']).all()

        return render_template('insurance_status.html', insurances=insurances)
    return redirect(url_for('login'))

@app.route('/compensation/apply', methods=['GET', 'POST'])
def compensation_apply():
    if 'user_id' in session:
        user = Profile.query.filter_by(user_id=session['user_id']).first()
        cultivation = Cultivation.query.filter_by(user_id=session['user_id']).with_entities(Cultivation.crop_name).all()
        if request.method == "POST":
            print("here")
            survey_number = request.form['surveyNumber']
            crop_name = request.form['cropName']
            land_name = request.form['landName']
            # check if crop in in cultivation
            c = any([crop.crop_name == crop_name for crop in cultivation])
            if not c:
                return render_template('compensation_apply.html', error="Crop not in cultivation")
            
            crop_count = request.form['cropQuantity']
            stage = request.form['cropStage']
            unit = request.form['unit']
            ward = request.form['ward']
            # check if crop image is there
            if request.files['image']:
                img = request.files['image']
                # upload to land folder with user_id and survey_number
                image_path = str(session['user_id']) + '_' + survey_number+str(random.randint(1, 10000)) + '.jpg'
                img.save(os.path.join(LAND_FOLDER, image_path))
            else:
                return render_template('compensation_apply.html', error="Crop image not uploaded")
            user_id = session['user_id']
            
            compensation = Compensation(survey_number=survey_number,
                                    crop_name=crop_name,
                                    land_name=land_name,
                                    crop_count=crop_count,
                                    stage=stage,
                                    unit=unit,
                                    ward=ward,
                                    image=image_path,
                                    user_id=user_id,
                                    panchayat=user.panchayat
                                    )
            db.session.add(compensation)
            db.session.commit()
            return redirect(url_for('profile'))
        return render_template('compensation_apply.html')
    
    return redirect(url_for('login'))

@app.route('/compensation/list', methods=['GET', 'POST'])
def compensation_list():
    if 'user_id' in session:
        compensations = Compensation.query.filter_by(user_id=session['user_id']).all()

        return render_template('compensation_status.html', compensations=compensations)
    return redirect(url_for('login'))


@app.route('/subsidy/list', methods=['GET', 'POST'])
def subsidy_list():
    if 'user_id' in session:
        subsidy = Subsidy.query.filter_by(user_id=session['user_id']).all()
        
        for i in subsidy:
            product = Product.query.filter_by(product_id=i.product_id).first()
            i.product_name = product.name
            i.product_price = product.price

        return render_template('subsidy_status.html', subsidy=subsidy)
    return redirect(url_for('login'))



@app.route('/image/<path:filename>')
def image(filename):
    if 'user_id' in session:
        # check file name
        if not filename.endswith('.jpg') and filename.count('/') > 0:
            return "image not found"
        # check file exists
        if not os.path.exists(os.path.join(LAND_FOLDER, filename)):
            return "image not found"
        # read image from file and make response with contentype as image
        image = open(os.path.join(LAND_FOLDER, filename), 'rb').read()
        response = make_response(image)
        response.headers.set('Content-Type', 'image/jpeg')
        return response

@app.route('/show_notification', methods=['GET', 'POST'])
def show_notification():
    if 'user_id' in session:
        
        notifications = Notification.query.filter_by(user_id=session['user_id']).all()
        print(len(notifications))
        return render_template('show_notification.html', notifications=notifications)
    return redirect(url_for('login'))

@app.route('/soil_test', methods=['GET', 'POST'])
def soil_test():
    if 'user_id' in session:
        if request.method=="POST" and request.files['image']:
            img_test = request.files['image']
            res = predict(img_test)
            return render_template('soil_test.html',result=res)
        return render_template('soil_test.html')
    return redirect(url_for('login'))

@app.route('/products', methods=['GET', 'POST'])
def product():
    if 'user_id' in session:
        products = Product.query.all()
        subsidy=Subsidy.query.filter_by(user_id=session["user_id"]).with_entities(Subsidy.product_id).all()
        subsidy = [int(i[0]) for i in subsidy]
        print(subsidy)
        applyed = []
        for i in products:
            print(i.product_id in subsidy,i.product_id)
            if i.product_id in subsidy:
                continue
            else:
                applyed.append(i)

        return render_template('products.html',products=applyed)
    return redirect(url_for('login'))

@app.route('/product/<int:product_id>/apply_subsidy', methods=['GET', 'POST'])
def apply_subsidy(product_id):
    if 'user_id' in session:
        if request.method=="POST":
            user = Profile.query.filter_by(user_id=session['user_id']).first()
            subsidy = Subsidy(product_id=product_id, user_id=session['user_id'],panchayat=user.panchayat)
            db.session.add(subsidy)
            db.session.commit()
            add_notification(session["user_id"],"Applied-Subsidy",f"The subsidy for the product with product id {product_id} has been send")
            return redirect(url_for('product'))
        return render_template('products.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['user_id'] = user.id
            # check if profile is complete or not
            profile = Profile.query.filter_by(user_id=user.id).first()
            if profile:
                return redirect(url_for('profile'))
            else:
                return redirect(url_for('profile_edit'))

        return 'Invalid username or password'

    return render_template('login.html')

@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']

        user = User.query.filter_by(username=username).first()

        if user:
            # Code to send a password reset email goes here
            return 'Password reset email sent.'

        return 'User not found.'

    return render_template('forgotpassword.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('profile.html')

    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # check session
    if 'user_id' in session:
        details = Admin.query.filter_by(admin_id=session['user_id']).first()
        return render_template('admin/admin.html', details=details)

    return redirect(url_for('login'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        admin = Admin.query.filter_by(username=username).first()

        if admin and admin.password == password:
            session['user_id'] = admin.admin_id
            session['admin'] = True
            return redirect(url_for('admin'))

        return 'Invalid username or password'

    return render_template('admin/login.html')


@app.route('/admin/users', methods=['GET', 'POST'])
def admin_users():
    # view all users
    if 'user_id' in session and session["admin"]:
        # get all users of the same panchayat as admin
        admin = Admin.query.filter_by(admin_id=session['user_id']).first()
        details = Profile.query.filter_by(panchayat=admin.panchayat).all()
        return render_template('admin/user.html', employees=details)

@app.route('/admin/insurance', methods=['GET', 'POST'])
def admin_insurance():
    # view all insurance applications
    if 'user_id' in session and session["admin"]:
        admin = Admin.query.filter_by(admin_id=session['user_id']).first()
        details = Insurance.query.filter_by(insurance_status="pending", panchayat=admin.panchayat).all()
        # add username to details from profile table
        for detail in details:
            user = Profile.query.filter_by(user_id=detail.user_id).first()
            detail.username = user.name
        return render_template('admin/insure.html', indetails=details)

@app.route('/admin/insurance/approve/<id>', methods=['POST'])
def admin_insurance_approve(id):
    # check admin session
    if 'user_id' in session and session['admin'] == True:
        if request.method == "POST":
            insurance = Insurance.query.filter_by(insurance_id=id).first()
            insurance.insurance_status = "Approved"
            db.session.commit()
            # send notification to user
            user = Profile.query.filter_by(user_id=insurance.user_id).first()
            print(user.user_id)
            add_notification(user.user_id, f"Insurance Approved", f"Your insurance application with insurance id {insurance.insurance_id}  has been approved.")
            return redirect(url_for('admin_insurance'))
    return redirect(url_for('admin_login'))

@app.route('/admin/insurance/reject/<id>', methods=['POST'])
def admin_insurance_reject(id):
    # check admin session
    if 'user_id' in session and session['admin'] == True:
        if request.method == "POST":
            insurance = Insurance.query.filter_by(insurance_id=id).first()
            insurance.insurance_status = "Rejected"
            db.session.commit()
            user = Profile.query.filter_by(user_id=insurance.user_id).first()
            add_notification(user.user_id,f"Insurance Rejected", f"Your insurance application with insurance id {insurance.insurance_id}  has been rejected.")
            return redirect(url_for('admin_insurance'))
    return redirect(url_for('admin_login'))

@app.route('/admin/compensation', methods=['GET', 'POST'])
def admin_compensation():
    # view all compensation applications
    if 'user_id' in session and session["admin"]:
        admin = Admin.query.filter_by(admin_id=session['user_id']).first()
        details = Compensation.query.filter_by(status="pending", panchayat=admin.panchayat).all()
        # add username to details from profile table
        for detail in details:
            user = Profile.query.filter_by(user_id=detail.user_id).first()
            detail.username = user.name
        return render_template('admin/compensation.html', indetails=details)

@app.route('/admin/compensation/approve/<id>', methods=['POST'])
def admin_compensation_approve(id):
    # check admin session
    if 'user_id' in session and session['admin'] == True:
        if request.method == "POST":
            compensation = Compensation.query.filter_by(compensation_id=id).first()
            compensation.status = "Approved"
            db.session.commit()
            # send notification to user
            user = Profile.query.filter_by(user_id=compensation.user_id).first()
            add_notification(user.user_id,f"Compensation Approved", f"Your compensation application with compensation id {compensation.compensation_id}  has been approved.")
            return redirect(url_for('admin_compensation'))
    return redirect(url_for('admin_login'))

@app.route('/admin/compensation/reject/<id>', methods=['POST'])
def admin_compensation_reject(id):
    # check admin session
    if 'user_id' in session and session['admin'] == True:
        if request.method == "POST":
            compensation = Compensation.query.filter_by(compensation_id=id).first()
            compensation.status = "Rejected"
            db.session.commit()
            # send notification to user
            user = Profile.query.filter_by(user_id=compensation.user_id).first()
            add_notification(user.user_id, f"Compensation Rejected", f"Your compensation application with compensation id {compensation.compensation_id}  has been rejected.")
            return redirect(url_for('admin_compensation'))
    return redirect(url_for('admin_login'))

@app.route('/admin/add_notifications', methods=['GET', 'POST'])
def add_notifications():
    if 'user_id' in session and session["admin"]:
        if request.method == 'POST':
            # check for broadcast
            if request.form['user_id'] == "all":
                users = Profile.query.all()
                for user in users:
                    add_notification(user.user_id, request.form['title'], request.form['message'])
                return redirect(url_for('add_notifications'))
            title = request.form['title']
            message = request.form['message']
            user_id = request.form['user_id']
            add_notification(user_id, title, message)
            return redirect(url_for('add_notifications'))
        return render_template('admin/add_notifications.html')

@app.route('/admin/add_product', methods=['GET', 'POST'])
def add_product():
    if 'user_id' in session and session["admin"]:
        if request.method == 'POST':
            name = request.form['name']
            price = request.form['price']
            description = request.form['description']
            image = request.files['image']
            type = request.form['type']
            print("hello",flush=True)
            if type not in ["seed", "fertilizer", "machine"]:
                return redirect(url_for('add_product'),error="Invalid product type")
            filename = Product_FOLDER+secure_filename(image.filename)
            image.save(filename)
            print(filename)
            new_product = Product(name=name, price=price, description=description, image=filename , type=type)
            db.session.add(new_product)
            db.session.commit()
            return redirect(url_for('admin'))
        return render_template('admin/add_product.html')
    
@app.route('/admin/products', methods=['GET', 'POST'])
def admin_products():
    if 'user_id' in session and session["admin"]:
        products = Product.query.all()
        return render_template('admin/products.html', products=products)
    return redirect(url_for('admin_login'))

@app.route('/admin/delete_product/<id>', methods=['GET', 'POST'])
def delete_product(id):
    if 'user_id' in session and session["admin"]:
        product = Product.query.filter_by(product_id=id).first()
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('admin_products'))


@app.route('/admin/add', methods=['GET', 'POST'])
def add_admin():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        panchayat = request.form['panchayat']
        mobile = request.form['phone']

        new_user = Admin(username=username,panchayat=panchayat, email=email , password=password, phone=mobile)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('add_admin'))

    return render_template('admin/addadmin.html')

@app.route('/reset')
def reset():
    if 'user_id' in session and session["admin"]:
            with app.app_context():
                Subsidy.__table__.drop(db.engine)  # Drop all existing tables
                Subsidy.__table__.create(db.engine)  # Recreate all tables
                return "deleted"

@app.route('/image/product/<path:filename>')
def image_product(filename):
    if 'user_id' in session:
        # check file name
        if not filename.endswith('.jpg') and filename.count('/') > 0:
            return "image not found"
        # check file exists
        if not os.path.exists(filename):
            return "image not found"
        # read image from file and make response with contentype as image
        image = open(filename, 'rb').read()
        response = make_response(image)
        response.headers.set('Content-Type', 'image/jpeg')
        return response
    return redirect(url_for("login"))



@app.route('/admin/subsidy', methods=['GET', 'POST'])
def admin_subsidy():
    # view all compensation applications
    if 'user_id' in session and session["admin"]:
        admin = Admin.query.filter_by(admin_id=session['user_id']).first()
        details = Subsidy.query.filter_by(status="pending", panchayat=admin.panchayat).all()
        # add username to details from profile table
        for detail in details:
            product = Product.query.filter_by(product_id=detail.product_id).first()
            detail.product_name = product.name
            detail.product_price = product.price
            user = Profile.query.filter_by(user_id=detail.user_id).first()
            detail.username = user.name
        return render_template('admin/subsidy.html', indetails=details)
    
@app.route('/admin/subsidy/approve/<id>', methods=['POST'])
def admin_subsidy_approve(id):
    # check admin session
    if 'user_id' in session and session['admin'] == True:
        if request.method == "POST":
            subsidy = Subsidy.query.filter_by(subsidy_id=id).first()
            subsidy.status = "Approved"
            db.session.commit()
            # send notification to user
            user = Profile.query.filter_by(user_id=subsidy.user_id).first()
            add_notification(user.user_id,f"Subsidy Approved", f"Your Subsidy application with Subsidy id {subsidy.subsidy_id}  has been approved.")
            return redirect(url_for('admin_subsidy'))
    return redirect(url_for('admin_login'))

@app.route('/admin/subsidy/reject/<id>', methods=['POST'])
def admin_subsidy_reject(id):
    # check admin session
    if 'user_id' in session and session['admin'] == True:
        if request.method == "POST":
            subsidy = Subsidy.query.filter_by(subsidy_id=id).first()
            subsidy.status = "Rejected"
            db.session.commit()
            # send notification to user
            user = Profile.query.filter_by(user_id=subsidy.user_id).first()
            add_notification(user.user_id, f"Subsidy Rejected", f"Your subsidy application with subsidy id {subsidy.subsidy_id}  has been rejected.")
            return redirect(url_for('admin_subsidy'))
    return redirect(url_for('admin_login'))




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        creat_admin()
    app.run(host="0.0.0.0")
