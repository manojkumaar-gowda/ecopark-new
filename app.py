from flask import Flask,render_template,request, session
from datetime import datetime,timedelta
from sqlalchemy.sql.operators import exists
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy
import uuid
import random
import razorpay
import os
from werkzeug.wrappers import response
import requests
import pytz
app = Flask(__name__)
app.secret_key = "EcoPark"
app.permanent_session_lifetime = timedelta(days = 10000)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['UPLOAD_PATH'] =  os.path.join(os.path.dirname(__file__),'static')
db = SQLAlchemy(app)

class Ecopark_Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ecopark_id = db.Column(db.String(50), nullable=False, unique=True)
    vehicle_number = db.Column(db.String(10), nullable=False, unique=True)
    vehicle_model = db.Column(db.String(20), nullable=False)
    vehicle_owner = db.Column(db.String(20), nullable=False)
    mobile_number = db.Column(db.Integer,nullable=False,unique=True)
    email = db.Column(db.String(30), nullable=False)
    insurance_policy_number = db.Column(db.String(30), nullable=False)
    chasis_number = db.Column(db.String(30), nullable=False)
    engine_number = db.Column(db.String(30), nullable=False)
    vehicle_color = db.Column(db.String(30), nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False)
    account_approved = db.Column(db.Boolean,default=False)
    vehicle_park_status = db.Column(db.Boolean,default=False)
    wallet_balance = db.Column(db.Integer, default=150)
    parked_at = db.Column(db.Integer,default=0)
    parked_plan = db.Column(db.String(30),default='None')
    parked_on = db.Column(db.DateTime)
    parked_for = db.Column(db.Integer,default=0)
    exp_msg = db.Column(db.Boolean,default=True)
    def __repr__(self):
        return 'Client ID : ' + str(self.id)

class BackupEcoParks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    park_name = db.Column(db.String(20), nullable=False)
    park_address = db.Column(db.String(200), nullable=False)
    ultra_deluxe_vacancy = db.Column(db.Integer)
    semi_deluxe_vacancy = db.Column(db.Integer)
    basic_vacancy = db.Column(db.Integer)
    latitude =  db.Column(db.String(20), nullable=False)
    longitude =  db.Column(db.String(20), nullable=False)
    embeded_map = db.Column(db.String(2000), nullable=False)
    def __repr__(self):
        return 'Park_ID : ' + str(self.id)
    #db.session.add(BackupEcoParks(park_name="JP Nagar",park_address="Ecopark, 33rd Main Rd, MG Layout, JP Nagar Phase 6, J. P. Nagar, Bengaluru, Karnataka 560078",ultra_deluxe_vacancy = 50,semi_deluxe_vacancy=70,basic_vacancy=99,latitude="12.904054047384347",longitude="77.58047027186707",embeded_map="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d10533.673399184396!2d77.57842774048427!3d12.901232342121146!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bae150d7349a72b%3A0xf3d03ea1e1dd3d46!2sJ.%20P.%20Nagar%2C%20Bengaluru%2C%20Karnataka%20560078!5e0!3m2!1sen!2sin!4v1640092015597!5m2!1sen!2sin"))
    #db.session.add(BackupEcoParks(park_name="Banashankari",park_address="Ecopark, No 43/2, Outer Ring Road Near, Kathreguppe, Banashankari 3rd Stage, Banashankari, Bengaluru, Karnataka 560085",ultra_deluxe_vacancy = 60,semi_deluxe_vacancy=80,basic_vacancy=90,latitude="12.923003699864813",longitude="77.55370098591682",embeded_map="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d22317.194000610576!2d77.53623629205836!3d12.933482404397962!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bae3e2c22c358b7%3A0x157068107f36f2ef!2sBanashankari%2C%20Bengaluru%2C%20Karnataka!5e0!3m2!1sen!2sin!4v1640093043442!5m2!1sen!2sin"))
    #db.session.add(BackupEcoParks(park_name="HSR Layout",park_address="Ecopark, Service Rd, Sector 4, HSR Layout, Bengaluru, Karnataka 560102",ultra_deluxe_vacancy = 55,semi_deluxe_vacancy=75,basic_vacancy=90,latitude="12.915361135682208",longitude="77.63938522761872",embeded_map="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d7777.7703293933355!2d77.62991412548442!3d12.915101560483162!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bae1491bfdc6ecd%3A0xf232718439fbc879!2sHSR%20Layout%2C%20Bengaluru%2C%20Karnataka!5e0!3m2!1sen!2sin!4v1640092919578!5m2!1sen!2sin"))
    #db.session.add(BackupEcoParks(park_name="Electronic city",park_address="Ecopark, Electronics City Phase 1, Electronic City, Bengaluru, Karnataka 560100",ultra_deluxe_vacancy = 80,semi_deluxe_vacancy=90,basic_vacancy=99,latitude="12.848371629224271",longitude="77.66358293413437",embeded_map="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d62241.699731122746!2d77.6535976982812!3d12.836411294504565!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bae6c8a7750e1c3%3A0x4a5cfc0fce5af71d!2sElectronic%20City%2C%20Bengaluru%2C%20Karnataka!5e0!3m2!1sen!2sin!4v1640092783105!5m2!1sen!2sin"))

class EcoParks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    park_name = db.Column(db.String(20), nullable=False)
    park_address = db.Column(db.String(200), nullable=False)
    ultra_deluxe_vacancy = db.Column(db.Integer)
    semi_deluxe_vacancy = db.Column(db.Integer)
    basic_vacancy = db.Column(db.Integer)
    latitude =  db.Column(db.String(20), nullable=False)
    longitude =  db.Column(db.String(20), nullable=False)
    embeded_map = db.Column(db.String(2000), nullable=False)
    def __repr__(self):
        return 'Park ID : ' + str(self.id)
    #db.session.add(EcoParks(park_name="JP Nagar",park_address="Ecopark, 33rd Main Rd, MG Layout, JP Nagar Phase 6, J. P. Nagar, Bengaluru, Karnataka 560078",ultra_deluxe_vacancy = 50,semi_deluxe_vacancy=70,basic_vacancy=99,latitude="12.904054047384347",longitude="77.58047027186707",embeded_map="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d10533.673399184396!2d77.57842774048427!3d12.901232342121146!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bae150d7349a72b%3A0xf3d03ea1e1dd3d46!2sJ.%20P.%20Nagar%2C%20Bengaluru%2C%20Karnataka%20560078!5e0!3m2!1sen!2sin!4v1640092015597!5m2!1sen!2sin"))
    #db.session.add(EcoParks(park_name="Banashankari",park_address="Ecopark, No 43/2, Outer Ring Road Near, Kathreguppe, Banashankari 3rd Stage, Banashankari, Bengaluru, Karnataka 560085",ultra_deluxe_vacancy = 60,semi_deluxe_vacancy=80,basic_vacancy=90,latitude="12.923003699864813",longitude="77.55370098591682",embeded_map="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d22317.194000610576!2d77.53623629205836!3d12.933482404397962!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bae3e2c22c358b7%3A0x157068107f36f2ef!2sBanashankari%2C%20Bengaluru%2C%20Karnataka!5e0!3m2!1sen!2sin!4v1640093043442!5m2!1sen!2sin"))
    #db.session.add(EcoParks(park_name="HSR Layout",park_address="Ecopark, Service Rd, Sector 4, HSR Layout, Bengaluru, Karnataka 560102",ultra_deluxe_vacancy = 55,semi_deluxe_vacancy=75,basic_vacancy=90,latitude="12.915361135682208",longitude="77.63938522761872",embeded_map="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d7777.7703293933355!2d77.62991412548442!3d12.915101560483162!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bae1491bfdc6ecd%3A0xf232718439fbc879!2sHSR%20Layout%2C%20Bengaluru%2C%20Karnataka!5e0!3m2!1sen!2sin!4v1640092919578!5m2!1sen!2sin"))
    #db.session.add(EcoParks(park_name="Electronic city",park_address="Ecopark, Electronics City Phase 1, Electronic City, Bengaluru, Karnataka 560100",ultra_deluxe_vacancy = 80,semi_deluxe_vacancy=90,basic_vacancy=99,latitude="12.848371629224271",longitude="77.66358293413437",embeded_map="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d62241.699731122746!2d77.6535976982812!3d12.836411294504565!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bae6c8a7750e1c3%3A0x4a5cfc0fce5af71d!2sElectronic%20City%2C%20Bengaluru%2C%20Karnataka!5e0!3m2!1sen!2sin!4v1640092783105!5m2!1sen!2sin"))
class WalletRecharge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(50), nullable=False, unique=True)
    client_id = db.Column(db.String(50), nullable=False)
    date_recharged = db.Column(db.DateTime, nullable=False)
    amount_recharged = db.Column(db.Integer)
    def __repr__(self):
        return 'Transaction ID : ' + str(self.transaction_id)

class ParkingHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(50))
    parked_at = db.Column(db.Integer)
    parked_plan = db.Column(db.String(30))
    parked_for = db.Column(db.Integer)
    parked_on = db.Column(db.DateTime)
    departed_on = db.Column(db.DateTime)
    dues = db.Column(db.Integer, default = 0)
    def __repr__(self):
        return 'Parking ID : ' + str(self.id)




#textMessage
def sendmessage(message,to):
    message = str(message)
    to = str(to)
    print(message)
    url = "https://www.fast2sms.com/dev/bulkV2"
    payload = "sender_id=TXTIND&message="+message+"&route=v3&numbers="+to
    headers = {
        'authorization': "YOUR FAST2SMS KEY",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        }
    #print("########################################################################################################")
    #response = requests.request("POST", url, data=payload, headers=headers)
    #print(response.text)
    return


@app.route('/uploadapp',methods=['GET','POST'])
def uploadapp():
    if request.method == "POST":
        file1 = request.files['app']
        file = os.path.join(app.config["UPLOAD_PATH"],"app_download")
        renamed_file = "ecopark" + ".apk"
        file1.save(os.path.join(file,renamed_file))
    return render_template('uploadapp.html')





#Admin
@app.route('/admin_login',methods=['GET',"POST"])
def admin_login():
    if "admin_logged_in" in session:
        return redirect('/admin_dashboard')
    if request.method == "POST":
        id = request.form["emp_id"]
        pwd = request.form["pswd"]
        if(id=="ecopark" and pwd=="123"):
            session.permanent = True
            session["admin_logged_in"] = True
            return redirect('/admin_dashboard')
        else:
            return render_template('admin_login.html',emp_id=id,pwd=pwd,message="Invalid credentials")
    return render_template('admin_login.html')

@app.route('/admin_dashboard',methods=['GET',"POST"])
def admin_dashboard():
    if "admin_logged_in" not in session:
        return redirect('/admin_login')
    new_req_obj = Ecopark_Client.query.filter(Ecopark_Client.account_approved == False).all()
    return render_template('admin_dashboard.html',new_req_obj = new_req_obj)

@app.route('/delete_application/<int:id>',methods=['GET','POST'])
def delete_application(id):
    if "admin_logged_in" not in session:
        return redirect('/admin_login')
    post = Ecopark_Client.query.get_or_404(id)
    to = post.mobile_number
    send_text = "Your application for EcoPark account got rejected. Please submit valid documents for account activation.\nThanks,\nEcopark Team"
    db.session.delete(post)
    db.session.commit()
    #send_message
    sendmessage(send_text,to)
    
    return redirect('/admin_dashboard')

@app.route('/manageWallet')
def manageWallet():
    if "admin_logged_in" not in session:
            return redirect('/admin_login')
    wallet_obj = WalletRecharge.query.all()
    return render_template('admin_wallet.html',wallet_obj = wallet_obj)

@app.route('/manageUsers')
def manageUsers():
    if "admin_logged_in" not in session:
            return redirect('/admin_login')
    user_obj = Ecopark_Client.query.all()
    return render_template('admin_users.html',user_obj = user_obj)
            
@app.route('/manageParkHistory')
def manageParkHistory():
    if "admin_logged_in" not in session:
            return redirect('/admin_login')
    park_obj = ParkingHistory.query.all()
    return render_template('admin_park_history.html',park_obj = park_obj)
            

@app.route('/arrival',methods=['GET',"POST"])
def admin_arrival():
    if "admin_logged_in" not in session:
        return redirect('/admin_login')
    parks = EcoParks.query.all()
    if request.method=="POST":
        vehicle_number = request.form['vehicle_number']
        vehicle_number = vehicle_number.upper()
        print(vehicle_number)
        exists = bool(db.session.query(Ecopark_Client).filter_by(vehicle_number=vehicle_number).first())
        user_obj = Ecopark_Client.query.filter(Ecopark_Client.vehicle_number == vehicle_number).first()
        if exists and user_obj.account_approved:
            park_obj = EcoParks.query.filter(EcoParks.id == user_obj.parked_at).first()
            if user_obj.vehicle_park_status:
                return render_template('admin_verify_arrival.html',user_obj=user_obj,park_obj=park_obj)
            else:
                size = 0
                park_obj = EcoParks.query.all()
                for x in park_obj:
                    size+=1
                return render_template('admin_nonbookedarrivals.html',user_obj = user_obj,vehicle_number = vehicle_number,park_obj=park_obj,size = size)
            
        else:
            
            return render_template('admin_arrival.html',message="Vehicle Number not registered",vehicle_number=vehicle_number,parks =parks)
    return render_template('admin_arrival.html',parks = parks)


@app.route('/admin_nonbookedarrivals',methods=['GET',"POST"])
def admin_nonbookedarrivals():
    if "admin_logged_in" not in session:
        return redirect('/admin_login')
    if request.method == "POST":
        place = request.form["place"]
        plan = request.form["plan"]
        stay = request.form["stay"]
        vehicle_number = request.form["vehicle_number"]
        cost = 0
        if plan == "Basic":
            leftout = EcoParks.query.get(place).basic_vacancy
        elif plan == "Semi deluxe":
            leftout = EcoParks.query.get(place).semi_deluxe_vacancy
        elif plan == "Ultra deluxe":
            leftout = EcoParks.query.get(place).ultra_deluxe_vacancy
        
        if plan == "Basic":
            cost = 15
        elif plan == "Semi deluxe":
            cost = 25
        elif plan == "Ultra deluxe":
            cost = 40
        total = round(cost * float(stay))
        user_obj = Ecopark_Client.query.filter(Ecopark_Client.vehicle_number == vehicle_number).first()
        if leftout<=0:
            return render_template('admin_nonbookedarrivals.html',user_obj=user_obj,vehicle_number = vehicle_number,message = "All slots full")
        if (user_obj.wallet_balance > total):
            Ecopark_Client.query.get(user_obj.id).wallet_balance = Ecopark_Client.query.get(user_obj.id).wallet_balance - total
        else:
            Ecopark_Client.query.get(user_obj.id).wallet_balance = 0

        time = float(stay)*60
        print(int(time))
        park_obj = EcoParks.query.filter(EcoParks.id == place).first()
        new_parking_obj = ParkingHistory(client_id = user_obj.ecopark_id, parked_at = int(place), parked_plan=plan,parked_for = int(time),dues=0,parked_on=datetime.now(),departed_on = datetime.now())
        Ecopark_Client.query.get(user_obj.id).vehicle_park_status = True
        Ecopark_Client.query.get(user_obj.id).parked_at = place
        Ecopark_Client.query.get(user_obj.id).parked_plan = plan
        Ecopark_Client.query.get(user_obj.id).parked_on = datetime.now()
        Ecopark_Client.query.get(user_obj.id).parked_for = int(time)
        if plan == 'Basic':
            park_obj.basic_vacancy = int(park_obj.basic_vacancy)-1
        elif plan == 'Semi deluxe':
            park_obj.semi_deluxe_vacancy = int(park_obj.semi_deluxe_vacancy)-1
        elif plan == 'Ultra deluxe':
            park_obj.ultra_deluxe_vacancy = int(park_obj.ultra_deluxe_vacancy)-1
        to = user_obj.mobile_number
        send_text = "INR "+str(total)+" spent on EcoPark Parking. "+"Remaining wallet Balance : INR "+str(user_obj.wallet_balance)
        #send_message
        sendmessage(send_text,to) 
        send_text = "Vehicle Parked at "+park_obj.park_name+" ecopark "+"on "+str(datetime.now())+"\nThanks,\nEcopark Team"
        #send_message
        sendmessage(send_text,to)    

        
        db.session.add(new_parking_obj)
        db.session.commit()
    return redirect('/arrival')

@app.route('/departure',methods=['GET',"POST"])
def admin_departure():
    if "admin_logged_in" not in session:
        return redirect('/admin_login')
    if request.method == "POST":
        vehicle_number = request.form["vehicle_number"]
        vehicle_number = vehicle_number.upper()
        exists = bool(db.session.query(Ecopark_Client).filter_by(vehicle_number=vehicle_number).first())
        if not exists:
            return render_template('admin_departure.html',vehicle_number=vehicle_number,message="Vehicle Number not registered")
        user_obj = Ecopark_Client.query.filter(Ecopark_Client.vehicle_number == vehicle_number).first()
        difference = datetime.now() - user_obj.parked_on 
        taken_sec = difference.total_seconds()
        min = taken_sec/60
        print("***********")
        Ecopark_Client.query.get(user_obj.id).exp_msg = True
        if int(min) > user_obj.parked_for:
            fine = 0
            taken_more = int(min) - user_obj.parked_for
            taken_more = int(taken_more)
            print("Takenmore",taken_more)
            if(user_obj.parked_plan == "Basic"):
                if taken_more >= 1 and taken_more <=60:
                    fine = 30
                if taken_more > 60 and taken_more <=120:
                    fine = 60
                if taken_more > 120 and taken_more <=180:
                    fine = 90
                if taken_more > 180:
                    fine = 150
                if taken_more > 500:
                    fine = 1000
            elif(user_obj.parked_plan == "Semi deluxe"):
                if taken_more >= 1 and taken_more <=60:
                    fine = 50
                if taken_more > 60 and taken_more <=120:
                    fine = 100
                if taken_more > 120 and taken_more <=180:
                    fine = 150
                if taken_more > 180:
                    fine = 250
                if taken_more > 500:
                    fine = 2000
            elif(user_obj.parked_plan == "Ultra deluxe"):
                if taken_more >= 1 and taken_more <=60:
                    fine = 80
                if taken_more > 60 and taken_more <=120:
                    fine = 160
                if taken_more > 120 and taken_more <=180:
                    fine = 240
                if taken_more > 180:
                    fine = 400
                if taken_more > 500:
                    fine = 5000
            if(user_obj.wallet_balance >= fine):
                print("Taken from Wallet")
                print("Fine",fine)
                parked_at = Ecopark_Client.query.get(user_obj.id).parked_at
                parked_plan = Ecopark_Client.query.get(user_obj.id).parked_plan 
                if parked_plan == "Basic":
                    EcoParks.query.get(parked_at).basic_vacancy = EcoParks.query.get(parked_at).basic_vacancy + 1
                elif parked_plan == "Semi deluxe":
                    EcoParks.query.get(parked_at).semi_deluxe_vacancy = EcoParks.query.get(parked_at).semi_deluxe_vacancy + 1
                elif parked_plan == "Ultra deluxe":
                    EcoParks.query.get(parked_at).ultra_deluxe_vacancy = EcoParks.query.get(parked_at).ultra_deluxe_vacancy + 1
                Ecopark_Client.query.get(user_obj.id).wallet_balance = int(Ecopark_Client.query.get(user_obj.id).wallet_balance) - int(fine)

                topay = "NIL"
                Ecopark_Client.query.get(user_obj.id).vehicle_park_status = False
                Ecopark_Client.query.get(user_obj.id).parked_at = 0
                Ecopark_Client.query.get(user_obj.id).parked_plan = "None"
                Ecopark_Client.query.get(user_obj.id).parked_on = datetime.now()
                Ecopark_Client.query.get(user_obj.id).parked_for = 0
                park_history_obj = ParkingHistory.query.filter(ParkingHistory.client_id == user_obj.ecopark_id).all()
                park_history_id = park_history_obj[-1].id
                
                ParkingHistory.query.get(park_history_id).departed_on = datetime.now()
                ParkingHistory.query.get(park_history_id).dues = fine
                db.session.commit()
                to = user_obj.mobile_number
                send_text = "INR "+str(fine)+" was debited from your wallet for late departure.\nWallet Balance : INR "+ str(user_obj.wallet_balance)
                #send_message
                sendmessage(send_text,to) 
                send_text = "Thanks for using EcoPark services. Have a great jounery\nThanks,\nEcopark Team"
                #send_message
                sendmessage(send_text,to)               
                print("Wallet Balance",user_obj.wallet_balance)
                print("topay",topay)
                return render_template('admin_balance.html',topay = topay)
            else:
                
                parked_at = Ecopark_Client.query.get(user_obj.id).parked_at
                parked_plan = Ecopark_Client.query.get(user_obj.id).parked_plan 
                if parked_plan == "Basic":
                    EcoParks.query.get(parked_at).basic_vacancy = EcoParks.query.get(parked_at).basic_vacancy + 1
                elif parked_plan == "Semi deluxe":
                    EcoParks.query.get(parked_at).semi_deluxe_vacancy = EcoParks.query.get(parked_at).semi_deluxe_vacancy + 1
                elif parked_plan == "Ultra deluxe":
                    EcoParks.query.get(parked_at).ultra_deluxe_vacancy = EcoParks.query.get(parked_at).ultra_deluxe_vacancy + 1
                topay = fine - user_obj.wallet_balance
                Ecopark_Client.query.get(user_obj.id).wallet_balance = 0
                print("Fine",fine)
                print("Emptied Wallet and paid",topay)
                print("Wallet Balance",user_obj.wallet_balance)
                Ecopark_Client.query.get(user_obj.id).vehicle_park_status = False
                Ecopark_Client.query.get(user_obj.id).parked_at = 0
                Ecopark_Client.query.get(user_obj.id).parked_plan = "None"
                Ecopark_Client.query.get(user_obj.id).parked_on = datetime.now()
                Ecopark_Client.query.get(user_obj.id).parked_for = 0
                park_history_obj = ParkingHistory.query.filter(ParkingHistory.client_id == user_obj.ecopark_id).all()
                park_history_id = park_history_obj[-1].id
                ParkingHistory.query.get(park_history_id).departed_on = datetime.now()
                ParkingHistory.query.get(park_history_id).dues = fine
                db.session.commit()
                to = user_obj.mobile_number
                send_text = "INR "+str(fine)+" was debited for late departure.\nWallet Balance : INR 0. Please recharge immediately!" 
                #send_message
                sendmessage(send_text,to)
                send_text = "Thanks for using EcoPark services. Have a great jounery\nThanks,\nEcopark Team"
                #send_message
                sendmessage(send_text,to)
                print(ParkingHistory.query.get(park_history_id).departed_on)
   
                return render_template('admin_balance.html',topay = topay)
        else:
            print('No dues')
            
            to = user_obj.mobile_number
            send_text = "Thanks for using EcoPark services. Have a great jounery\nThanks,\nEcopark Team"
            #send_message
            sendmessage(send_text,to)
            parked_at = Ecopark_Client.query.get(user_obj.id).parked_at
            parked_plan = Ecopark_Client.query.get(user_obj.id).parked_plan 
            if parked_plan == "Basic":
                EcoParks.query.get(parked_at).basic_vacancy = EcoParks.query.get(parked_at).basic_vacancy + 1
            elif parked_plan == "Semi deluxe":
                EcoParks.query.get(parked_at).semi_deluxe_vacancy = EcoParks.query.get(parked_at).semi_deluxe_vacancy + 1
            elif parked_plan == "Ultra deluxe":
                EcoParks.query.get(parked_at).ultra_deluxe_vacancy = EcoParks.query.get(parked_at).ultra_deluxe_vacancy + 1
            Ecopark_Client.query.get(user_obj.id).vehicle_park_status = False
            Ecopark_Client.query.get(user_obj.id).parked_at = 0
            Ecopark_Client.query.get(user_obj.id).parked_plan = "None"
            Ecopark_Client.query.get(user_obj.id).parked_on = datetime.now()
            Ecopark_Client.query.get(user_obj.id).parked_for = 0
            park_history_obj = ParkingHistory.query.filter(ParkingHistory.client_id == user_obj.ecopark_id).all()
            park_history_id = park_history_obj[-1].id
            print(ParkingHistory.query.get(park_history_id).parked_on)
            ParkingHistory.query.get(park_history_id).departed_on = datetime.now()
            ParkingHistory.query.get(park_history_id).dues = 0
            
            db.session.commit()
            return render_template('admin_balance.html',topay = "NO DUES")
        
        

    return render_template('admin_departure.html')

@app.route('/admin_verify_arrival/<int:mobile_number>/<park_name>',methods=['GET',"POST"])
def admin_verify_arrival(mobile_number,park_name):
    if "admin_logged_in" not in session:
        return redirect('/admin_login')
    if request.method =="POST":
        
        send_text = "Vehicle Parked at "+str(park_name)+" ecopark "+"on "+str(datetime.now())+"\nThanks,\nEcopark Team"
        #send_message
        sendmessage(send_text,str(mobile_number))
        return redirect('/arrival')


@app.route('/deleteEcopark/<int:id>',methods=['GET',"POST"])
def deleteEcopark(id):
    if "admin_logged_in" not in session:
        return redirect('/admin_login')
    db.session.delete(EcoParks.query.get_or_404(id))
    db.session.commit()
    return redirect('/manageEcoParks')

@app.route('/editEcoParks',methods=['POST'])
def editEcoParks():
    if "admin_logged_in" not in session:
        return redirect('/admin_login')
    if request.method == "POST":
        park_address = request.form["park_address"]
        park_latitude = request.form["park_latitude"]
        park_longitude = request.form["park_longitude"]
        park_url = request.form["embeded_map_url"]
        udv = int(request.form["udv"])
        sdv = int(request.form["sdv"])
        bv = int(request.form["bv"])
        park_id = int(request.form["location"])
        EcoParks.query.get(park_id).park_address = park_address
        EcoParks.query.get(park_id).latitude = park_latitude
        EcoParks.query.get(park_id).longitude = park_longitude
        EcoParks.query.get(park_id).embeded_map = park_url
        EcoParks.query.get(park_id).ultra_deluxe_vacancy = udv
        EcoParks.query.get(park_id).semi_deluxe_vacancy = sdv
        EcoParks.query.get(park_id).basic_vacancy = bv
        db.session.commit()
        return redirect('/manageEcoParks')


@app.route('/manageEcoParks',methods=['GET',"POST"])
def manageEcoParks():
    
    if "admin_logged_in" not in session:
        return redirect('/admin_login')
    if request.method == "POST":
        park_name = request.form["park_name"]
        park_address = request.form["park_address"]
        park_latitude = request.form["park_latitude"]
        park_longitude = request.form["park_longitude"]
        park_url = request.form["embeded_map_url"]
        udv = int(request.form["udv"])
        sdv = int(request.form["sdv"])
        bv = int(request.form["bv"])
        new_ecopark_obj = EcoParks(park_name = park_name,park_address = park_address,latitude = park_latitude ,longitude = park_longitude,embeded_map = park_url,ultra_deluxe_vacancy = udv,semi_deluxe_vacancy = sdv,basic_vacancy = bv)
        db.session.add(new_ecopark_obj)
        new_ecopark_obj = BackupEcoParks(park_name = park_name,park_address = park_address,latitude = park_latitude ,longitude = park_longitude,embeded_map = park_url,ultra_deluxe_vacancy = udv,semi_deluxe_vacancy = sdv,basic_vacancy = bv)
        db.session.add(new_ecopark_obj)
        db.session.commit()
    #parks_obj_obj
    parking_obj = {}
    parks_obj = EcoParks.query.all()
    for x in parks_obj:
        obj={}
        obj["ultra_deluxe_vacancy"] = x.ultra_deluxe_vacancy
        obj["semi_deluxe_vacancy"] = x.semi_deluxe_vacancy
        obj["basic_vacancy"] = x.basic_vacancy
        obj["latitude"] =  x.latitude 
        obj["longitude"] =  x.longitude 
        obj["embeded_map"] =  x.embeded_map 
        obj["park_address"] =  x.park_address
        obj["park_name"] =  x.park_name
        obj["park_id"] =  x.id
        parking_obj["Park"+str(x.id)] = obj
        
    print(parking_obj)
    park_obj = EcoParks.query.all()
    return render_template('manageEcoParks.html',park_obj = park_obj,parking_obj = parking_obj)



@app.route('/admin_logout',methods=['GET',"POST"])
def admin_logout():
    
    if "admin_logged_in"  in session:
        session.pop("admin_logged_in" , None)
    return redirect('/admin_dashboard')

@app.route('/approve/<int:id>',methods=['GET',"POST"])
def approve(id):
    if "admin_logged_in" not in session:
        return redirect('/admin_login')
    
    Ecopark_Client.query.get(id).account_approved = True
    post = Ecopark_Client.query.get(id)
    to = post.mobile_number
    send_text = "Your application for EcoPark account got approved. Now enjoy parking at the fastest and the safest parking lot in the world.\nThanks,\nEcopark Team"
    #send_message
    sendmessage(send_text,to)
    db.session.commit()
    return redirect('/admin_dashboard')
#Admin







@app.route('/terms_of_services',methods=['GET',"POST"])
def tos():
    
    if "recharge" in session:
        session.pop("recharge" , None)
    
    return render_template('terms_of_services.html')

@app.route('/privacy_policy',methods=['GET',"POST"])
def privacy_policy():
    if "recharge" in session:
        session.pop("recharge" , None)
    
    return render_template('privacy_policy.html')

@app.route('/team_members')
def team_members():
    return render_template('team_members.html')

@app.route('/basic',methods=["POST"])
def basic():
    if "user_id" not in session:
        return redirect('/login')
    if "park_selected" not in session:
        return redirect('/')
    if request.method == "POST":
        session["plan"] = "Basic"
        session["cost"] = "15"
        return redirect('/select_time')

@app.route('/semi_deluxe',methods=["POST"])
def semi_deluxe():
    if "user_id" not in session:
        return redirect('/login')
    if "park_selected" not in session:
        return redirect('/')
    if request.method == "POST":
        session["plan"] = "Semi deluxe"
        session["cost"] = "25"
        return redirect('/select_time')

@app.route('/ultra_deluxe',methods=["POST"])
def ultra_deluxe():
    if "user_id" not in session:
        return redirect('/login')
    if "park_selected" not in session:
        return redirect('/')
    if request.method == "POST":
        session["plan"] = "Ultra deluxe"
        session["cost"] = "40"
        return redirect('/select_time')



@app.route('/select_time',methods=["GET","POST"])
def select_time():
    if "user_id" not in session:
        return redirect('/login')
    if "park_selected" not in session:
        return redirect('/')
    if "plan" not in session:
        return redirect('/')
    if "cost" not in session:
        return redirect('/')
    print(session["plan"])
    print(session["cost"])
    #for empty parkslot
    park_obj = EcoParks.query.filter(EcoParks.id == int(session["park_selected"])).first()
    user_obj = Ecopark_Client.query.filter(Ecopark_Client.ecopark_id == session["user_id"]).first()
    low_balance = bool(user_obj.wallet_balance < 15)
    print(low_balance)
    park_obj = EcoParks.query.filter(EcoParks.id == int(session["park_selected"])).first()
    if session["plan"] == "Basic":
        if park_obj.basic_vacancy <= 0 :
            return render_template('plan.html',user_obj = user_obj,park_obj=park_obj,cost = session["cost"],plan = session["plan"],message = "Plan fully booked. Please select other plan")
    if session["plan"] == "Semi deluxe":
        if park_obj.semi_deluxe_vacancy <= 0 :
            return render_template('plan.html',user_obj = user_obj,park_obj=park_obj,cost = session["cost"],plan = session["plan"],message = "Plan fully booked. Please select other plan")
    if session["plan"] == "Ultra deluxe":
        if park_obj.ultra_deluxe_vacancy <= 0 :
            return render_template('plan.html',user_obj = user_obj,park_obj=park_obj,cost = session["cost"],plan = session["plan"],message = "Plan fully booked. Please select other plan")
    return render_template('select_time.html',user_obj = user_obj,park_obj=park_obj,cost = session["cost"],plan = session["plan"],low_balance = low_balance)

@app.route('/booking',methods=["POST"])
def booking():
    if "user_id" not in session:
        return redirect('/login')
    if "park_selected" not in session:
        return redirect('/')
    if "plan" not in session:
        return redirect('/')
    if "cost" not in session:
        return redirect('/')
    
    if request.method =="POST":
        time = request.form["stay"]
        actual_cost = round(float(time)*int(session['cost']))
        time = int(float(time)*60)
        print(time)
        user_obj = Ecopark_Client.query.filter(Ecopark_Client.ecopark_id == session["user_id"]).first()
        park_obj = EcoParks.query.filter(EcoParks.id == int(session["park_selected"])).first()
        if session["plan"] == "Basic":
            if park_obj.basic_vacancy <= 0 :
                return render_template('plan.html',user_obj = user_obj,park_obj=park_obj,cost = session["cost"],plan = session["plan"],message = "Plan fully booked. Please select other plan")
        if session["plan"] == "Semi deluxe":
            if park_obj.semi_deluxe_vacancy <= 0 :
                return render_template('plan.html',user_obj = user_obj,park_obj=park_obj,cost = session["cost"],plan = session["plan"],message = "Plan fully booked. Please select other plan")
        if session["plan"] == "Ultra deluxe":
            if park_obj.ultra_deluxe_vacancy <= 0 :
                return render_template('plan.html',user_obj = user_obj,park_obj=park_obj,cost = session["cost"],plan = session["plan"],message = "Plan fully booked. Please select other plan")
        t = datetime.now()
        new_parking_obj = ParkingHistory(client_id = session["user_id"], parked_at = park_obj.id, parked_plan=session["plan"],parked_for = time,dues=0,parked_on=t,departed_on = t)
        Ecopark_Client.query.get(user_obj.id).vehicle_park_status = True
        Ecopark_Client.query.get(user_obj.id).wallet_balance =int(user_obj.wallet_balance) - int(actual_cost)
        Ecopark_Client.query.get(user_obj.id).parked_at = park_obj.id
        Ecopark_Client.query.get(user_obj.id).parked_plan = session['plan']
        Ecopark_Client.query.get(user_obj.id).parked_on = datetime.now()
        Ecopark_Client.query.get(user_obj.id).parked_for = int(time)
        if session['plan'] == 'Basic':
            park_obj.basic_vacancy = int(park_obj.basic_vacancy)-1
        elif session['plan'] == 'Semi deluxe':
            park_obj.semi_deluxe_vacancy = int(park_obj.semi_deluxe_vacancy)-1
        elif session['plan'] == 'Ultra deluxe':
            park_obj.ultra_deluxe_vacancy = int(park_obj.ultra_deluxe_vacancy)-1
            

        
        db.session.add(new_parking_obj)
        db.session.commit()
        print(user_obj.vehicle_park_status,user_obj.wallet_balance,user_obj.parked_at,user_obj.parked_plan,user_obj.parked_on,user_obj.parked_for)
        to = user_obj.mobile_number
        
        send_text = "Booking done on "+str(datetime.now())+" is valid for "+str(time)+" minutes. Please visit our app for further details.\nThanks,\nEcopark Team"
        #send_message
        sendmessage(send_text,to)
        send_text = "INR "+str(actual_cost)+" was debited for pre-booking of your parking lot. \nCurrent wallet Balance INR: "+str(user_obj.wallet_balance)+".\nThanks,\nEcopark Team"
        #send_message
        sendmessage(send_text,to)

        session['parked_at_id'] = park_obj.id
        return redirect('/booking_successful')
    
@app.route('/booking_successful')
def booking_successful():
    if "user_id" not in session:
        return redirect('/login')
    return render_template('booking_successful.html')


@app.route('/account_transactions')
def account_transactions():
    print(datetime.now())
    if "user_id" not in session:
        return redirect('/login')
    if "recharge" in session:
        session.pop("recharge" , None)
    if "plan" in session:
        session.pop("plan" , None)
    if "cost" in session:
        session.pop("cost" , None)
    if "park_selected" in session:
        session.pop("park_selected" , None)
    wallet_transactions = WalletRecharge.query.filter(WalletRecharge.client_id == session["user_id"]).all()
    parking_history = ParkingHistory.query.filter(ParkingHistory.client_id == session["user_id"]).all()
    park_obj = BackupEcoParks.query.all()
    print(park_obj)
    print(wallet_transactions)
    print(parking_history)
    user_obj = Ecopark_Client.query.filter(Ecopark_Client.ecopark_id == session["user_id"]).first()
    return render_template('account_transactions.html',user_obj = user_obj,wallet_transactions = wallet_transactions,parking_history=parking_history,park_obj = park_obj)

@app.route('/settings',methods=['GET',"POST"])
def settings():
    if "recharge" in session:
        session.pop("recharge" , None)
    if "user_id" not in session:
        return redirect('/login')
    if "plan" in session:
        session.pop("plan" , None)
    if "cost" in session:
        session.pop("cost" , None)
    if "park_selected" in session:
        session.pop("park_selected" , None)
    user_obj = Ecopark_Client.query.filter(Ecopark_Client.ecopark_id == session["user_id"]).first()
    if request.method=='POST':
        email = request.form['email']
        Ecopark_Client.query.get(user_obj.id).email = email
        db.session.commit()
        message = "Changes Saved"
        return render_template('settings.html',user_obj = user_obj,message = message)
    
    return render_template('settings.html',user_obj = user_obj)


@app.route('/',methods=['GET',"POST"])
def dashboard():
    if "recharge" in session:
        session.pop("recharge" , None)
    if "user_id" not in session:
        return redirect('/login')
    if "plan" in session:
        session.pop("plan" , None)
    if "cost" in session:
        session.pop("cost" , None)
    if "park_selected" in session:
        session.pop("park_selected" , None)
    if request.method == "POST":
        park_id = request.form['location']
        park_id = int(park_id)
        session['park_selected'] = park_id
        return redirect('/plan')
    session["send_reminder"] = "1"
    approved = Ecopark_Client.query.filter(Ecopark_Client.ecopark_id == session["user_id"]).first().account_approved
    if not approved:
        return redirect('/wait')
    user_obj = Ecopark_Client.query.filter(Ecopark_Client.ecopark_id == session["user_id"]).first()
    parks_obj = EcoParks.query.all()
    #parks_obj_obj
    park_obj = {}
    start = 1
    for x in parks_obj:
        obj={}
        obj["ultra_deluxe_vacancy"] = x.ultra_deluxe_vacancy
        obj["semi_deluxe_vacancy"] = x.semi_deluxe_vacancy
        obj["basic_vacancy"] = x.basic_vacancy
        obj["latitude"] =  x.latitude 
        obj["longitude"] =  x.longitude 
        obj["embeded_map"] =  x.embeded_map 
        obj["park_address"] =  x.park_address
        obj["park_name"] =  x.park_name
        park_obj["Park"+str(x.id)] = obj
        start+=1
    print(park_obj)
    if user_obj.vehicle_park_status:
        add = int(user_obj.parked_for)
        future_date = user_obj.parked_on + timedelta(minutes=add)
        print(future_date)
        x = datetime.now()
        print(x)
        time_delta = future_date - datetime.now() 
        total_seconds = time_delta.total_seconds()
        min, sec = divmod(total_seconds, 60)
        hour, min = divmod(min, 60)
        time_left = {'hours' : int(hour),'minutes':int(min),'seconds' :int(sec)}
        parked_obj = EcoParks.query.filter(EcoParks.id == user_obj.parked_at).first()
        if user_obj.parked_plan == "Basic":
            cost = 15
        elif user_obj.parked_plan == "Semi deluxe":
            cost = 25
        elif user_obj.parked_plan == "Ultra deluxe":
            cost = 40
        return render_template('dashboard.html',user_obj = user_obj,parks_obj = parks_obj,parked = parked_obj,cost = cost,plan = user_obj.parked_plan ,time_left = time_left,park_obj = park_obj)
    else:
        return render_template('dashboard.html',user_obj = user_obj,parks_obj = parks_obj,park_obj = park_obj,size = start-1)

@app.route('/plan',methods=['GET',"POST"])
def plan():
    if "user_id" not in session:
        return redirect('/login')
    if "park_selected" not in session:
        return redirect('/')
    user_obj = Ecopark_Client.query.filter(Ecopark_Client.ecopark_id == session["user_id"]).first()
    park_obj = EcoParks.query.filter(EcoParks.id == int(session["park_selected"])).first()
    return render_template('plan.html',user_obj = user_obj,park_obj = park_obj)

@app.route('/expired')
def expired():
    if "user_id" not in session:
        return redirect('/login')
    
    user_obj = Ecopark_Client.query.filter(Ecopark_Client.ecopark_id == session["user_id"]).first()
    if not user_obj.vehicle_park_status:
        return redirect('/') 
    if user_obj.exp_msg:
        session.pop("send_reminder" , None)
        to = user_obj.mobile_number
        send_text = "Your Parking stay just got expired. Please visit the respective ecopark for further process"
        #send_message
        print("Message sent")
        Ecopark_Client.query.get(user_obj.id).exp_msg = False
        db.session.commit()
        sendmessage(send_text,to)
    parked_obj = EcoParks.query.filter(EcoParks.id == user_obj.parked_at).first()
       
    return render_template('expired.html',user_obj = user_obj,parked = parked_obj)


@app.route('/wallet',methods=['GET',"POST"])
def wallet():
    if "user_id" not in session:
        return redirect('/login')
    if "recharge" in session:
        session.pop("recharge" , None)
    if "plan" in session:
        session.pop("plan" , None)
    if "cost" in session:
        session.pop("cost" , None)
    if "park_selected" in session:
        session.pop("park_selected" , None)
    approved = Ecopark_Client.query.filter(Ecopark_Client.ecopark_id == session["user_id"]).first().account_approved
    if not approved:
        return redirect('/wait')
    wallet_balance = Ecopark_Client.query.filter(Ecopark_Client.ecopark_id == session["user_id"]).first().wallet_balance
    if request.method == "POST":
        add_balance = request.form['add_balance']
        session['recharge'] = add_balance
        return redirect('/pay')
        
    user_obj = Ecopark_Client.query.filter(Ecopark_Client.ecopark_id == session["user_id"]).first()
    return render_template('wallet.html',wallet_balance = wallet_balance,user_obj = user_obj)

@app.route('/pay',methods=["GET","POST"])
def pay():
    if "user_id" not in session:
        return redirect('/login')
    if "recharge" not in session:
        return redirect('/wallet')
    client = razorpay.Client(auth= (" YOUR RAZORPAY CRED"," YOUR RAZORPAY CRED"))
    amount = session["recharge"]
    amount = amount+"00"
    payment = client.order.create({'amount' : int(amount),'currency' : 'INR' , 'payment_capture': '1'})
    user_obj = Ecopark_Client.query.filter(Ecopark_Client.ecopark_id == session["user_id"]).first()
    return render_template('pay.html',amount=amount,id=str(random.randint(1000,9999)),user_obj = user_obj)

@app.route('/success',methods=["POST"])
def success():
    if "user_id" not in session:
        return redirect('/login')
    if "recharge" not in session:
        return redirect('/wallet')
    user_obj = Ecopark_Client.query.filter(Ecopark_Client.ecopark_id == session["user_id"]).first()
    Ecopark_Client.query.get(user_obj.id).wallet_balance = user_obj.wallet_balance + int(session["recharge"])
    transaction_id = str(uuid.uuid4())
    client_id = session["user_id"]
    amount_recharged = session["recharge"]

    db.session.add(WalletRecharge(transaction_id = transaction_id,client_id = client_id,amount_recharged = amount_recharged,date_recharged=datetime.now()))
    db.session.commit()
    to = user_obj.mobile_number
    send_text = "Wallet Recharge of INR "+str(amount_recharged)+" was successful.\nTransaction id: "+str(transaction_id)+"\nCurrent Wallet Balance: INR "+str(user_obj.wallet_balance)
    #send_message
    sendmessage(send_text,to)
    return redirect('/payment_successful')

@app.route('/extend',methods=["GET","POST"])
def extend():
    if "user_id" not in session:
        return redirect('/login')
    if request.method=='POST':
        time = request.form["stay"]
        cost = 0
        user_obj = Ecopark_Client.query.filter(Ecopark_Client.ecopark_id == session["user_id"]).first()
        
        if user_obj.parked_plan == "Basic":
            cost = 15
        elif user_obj.parked_plan == "Semi deluxe":
            cost = 25
        elif user_obj.parked_plan == "Ultra deluxe":
            cost = 40
        actual_cost = round(float(time)*int(cost))
        time = int(float(time)*60)
        Ecopark_Client.query.get(user_obj.id).wallet_balance =int(user_obj.wallet_balance) - int(actual_cost)
        Ecopark_Client.query.get(user_obj.id).parked_for = int(user_obj.parked_for) + int(time)
        
        db.session.commit()
        to = user_obj.mobile_number
        send_text = "INR "+str(actual_cost)+" was debited for extended parking.\nCurrent wallet Balance: INR "+str(user_obj.wallet_balance)+".\nThanks,\nEcopark Team"
        #send_message
        sendmessage(send_text,to)

        
        send_text = "Parking extended for "+str(time)+" minutes. Please visit our app for further details.\nThanks,\nEcopark Team"
        #send_message
        sendmessage(send_text,to)

        return redirect('/booking_successful')
        

@app.route('/payment_successful',methods=["GET","POST"])
def payment_successful():
    if "user_id" not in session:
        return redirect('/login')
    if "recharge" not in session:
        return redirect('/wallet')
    session.pop("recharge" , None)
    return render_template('payment_successful.html')


@app.route('/login',methods=['GET',"POST"])
def login():
    if "recharge" in session:
        session.pop("recharge" , None)
    if "user_id" in session:
        return redirect('/')
        
    if request.method=='POST':
        vehicle_number = request.form['vehicle_number']
        vehicle_number = vehicle_number.upper()
        exists = bool(db.session.query(Ecopark_Client).filter_by(vehicle_number=vehicle_number).first())
        print(exists)
        if exists:
            session["vehicle_number"] = vehicle_number
            session["redirect_to"] = "dashboard"
            otp = random.randint(1000,9999)
            session["otp"] = otp
            user_obj = Ecopark_Client.query.filter(Ecopark_Client.vehicle_number == vehicle_number).first()
            to = str(user_obj.mobile_number)
            send_text = "Your OTP for account verification is "+str(otp)
            #send_message
            sendmessage(send_text,to)
            print(session["otp"])
            print(session["vehicle_number"])
            return redirect('/account_verification')
        else:    
            return render_template('login.html',message = "Account not found. Please SignUp",vehicle_number=vehicle_number)
    return render_template('login.html')


@app.route('/logout',methods=['GET',"POST"])
def logout():
    if "recharge" in session:
        session.pop("recharge" , None)
    session.pop("user_id" , None)
    return render_template('login.html',message = "Successfully Logged out")

@app.route('/resend_otp',methods=["POST"])
def resend_otp():
    if "recharge" in session:
        session.pop("recharge" , None)
    if "user_id" in session:
        return redirect('/wait')
    if "redirect_to" in session:
        if "otp" not in session and "vehicle_number" not in session:
            return redirect('/login')
    if "otp" not in session and "mobile_number" not in session:
            return redirect('/login')
    otp = random.randint(1000,9999)
    session["otp"] = otp
    print(session["otp"])
    if "redirect_to" in session:
        user_obj = Ecopark_Client.query.filter(Ecopark_Client.vehicle_number == session["vehicle_number"]).first()
        to = str(user_obj.mobile_number)
    else:
        to = str(session["phone_number"])
    send_text = "Your OTP for account verification is "+str(otp)
    #send_message
    sendmessage(send_text,to)
    return redirect('/account_verification')

@app.route('/signup',methods=['GET',"POST"])
def signup():
    if "recharge" in session:
        session.pop("recharge" , None)
    if "user_id" in session:
        return redirect('/')
    if request.method=='POST':
        phone_number = request.form['phone_number']
        exists = bool(db.session.query(Ecopark_Client).filter_by(mobile_number=phone_number).first())
        if not exists:
            session["phone_number"] = phone_number
            otp = random.randint(1000,9999)
            session["otp"] = otp
            print(session["otp"])
            print(session["phone_number"])
            to = str(phone_number)
            send_text = "Your OTP for account verification is "+str(otp)
            #send_message
            sendmessage(send_text,to)
            return redirect('/account_verification')
        else:
            error_statement = "Mobile Number already exists"
            return render_template('signup.html',error_statement = error_statement,phone_number = phone_number)
    return render_template('signup.html')



@app.route('/wait')
def wait():
    if "recharge" in session:
        session.pop("recharge" , None)
    if "user_id" not in session:
        return redirect('/login')
    print(session["user_id"])
    approved = Ecopark_Client.query.filter(Ecopark_Client.ecopark_id == session["user_id"]).first().account_approved
    print(approved)
    if approved:
        return redirect('/')
    return render_template('wait.html')


@app.route('/account_verification',methods=['GET',"POST"])
def otp():
    if "recharge" in session:
        session.pop("recharge" , None)
    if "user_id" in session:
        return redirect('/wait')
    if "redirect_to" in session:
        if "otp" not in session and "vehicle_number" not in session:
            return redirect('/login')
    if "otp" not in session and "mobile_number" not in session:
            return redirect('/login')

    otp = str(session["otp"])
    if request.method =='POST':
        otp_part1 = str(request.form['otp_part1'])
        otp_part2 = str(request.form['otp_part2'])
        otp_part3 = str(request.form['otp_part3'])
        otp_part4 = str(request.form['otp_part4'])
        if otp_part1+otp_part2+otp_part3+otp_part4 == otp:
            session.pop("otp" , None)
            if "redirect_to" in session:
                session.pop("redirect_to" , None)
                ecopark_id = Ecopark_Client.query.filter(Ecopark_Client.vehicle_number ==session['vehicle_number']).first().ecopark_id
                session.pop("vehicle_number" , None)
                session.permanent = True
                session["user_id"] = ecopark_id
                return redirect('/')
            else:
                return redirect('/registration')
        else:
            error_statement = 'Invalid OTP'
            return render_template('account_verification.html',error_statement = error_statement)
    return render_template('account_verification.html')




@app.route('/registration',methods=['GET',"POST"])
def registration():
    if "recharge" in session:
        session.pop("recharge" , None)
    if "user_id" in session:
        return redirect('/wait')
    if "phone_number" not in session:
        return redirect('/signup')
    if request.method =='POST':
        ecopark_id = str(uuid.uuid4())
        vehicle_number = str(request.form['vehicle_number'])
        vehicle_number = vehicle_number.upper()
        vehicle_model = str(request.form['vehicle_model'])
        vehicle_owner = str(request.form['vehicle_owner'])
        email = str(request.form['email'])
        insurance_policy_number = str(request.form['insurance_policy_number'])
        chasis_number = str(request.form['chasis_number'])
        engine_number = str(request.form['engine_number'])
        vehicle_color = str(request.form['vehicle_color'])
        new_form = Ecopark_Client(ecopark_id = ecopark_id , vehicle_number = vehicle_number, vehicle_model = vehicle_model,vehicle_owner = vehicle_owner,mobile_number = session["phone_number"],email = email,insurance_policy_number = insurance_policy_number,chasis_number = chasis_number,engine_number = engine_number,vehicle_color = vehicle_color,date_joined=datetime.now(),parked_on=datetime.now())
        try:
            db.session.add(new_form)
            db.session.commit()
            file1 = request.files['v_image']
            file2 = request.files['rc_image']
            file3 = request.files['id_image']
            user_proof = os.path.join(app.config["UPLOAD_PATH"],"user_proof")
            vehicle_rc = os.path.join(app.config["UPLOAD_PATH"],"vehicle_rc")
            vehicle_image = os.path.join(app.config["UPLOAD_PATH"],"vehicle_image")
            renamed_file = ecopark_id + ".pdf"
            file3.save(os.path.join(user_proof,renamed_file))
            file2.save(os.path.join(vehicle_rc,renamed_file))
            file1.save(os.path.join(vehicle_image,renamed_file))
            session.pop("phone_number" , None)
            session.permanent = True
            session["user_id"] = ecopark_id
            return redirect('/wait')        
        except:
            return render_template('registration.html',phone_number = session["phone_number"],ecopark_id = ecopark_id,vehicle_number=vehicle_number,vehicle_model=vehicle_model,vehicle_owner=vehicle_owner,email=email,insurance_policy_number = insurance_policy_number,chasis_number = chasis_number,engine_number = engine_number,vehicle_color = vehicle_color,message = "Some of the information are already taken by another user. Please enter valid details")        
    return render_template('registration.html',phone_number = session["phone_number"])



@app.errorhandler(404)
def not_found(e):
    if "recharge" in session:
        session.pop("recharge" , None)
    return render_template('err.html')
if __name__ == "__main__":
    app.run(debug=True)
