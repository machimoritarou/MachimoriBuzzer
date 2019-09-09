from flask import Flask, request, redirect, jsonify, render_template, url_for
from mail import My_Mail
from DB import DB
from create_json import My_Json
from flask_login import login_user, logout_user, LoginManager, UserMixin, login_required
from flask_httpauth import HTTPBasicAuth

class User(UserMixin):
    pass

app = Flask(__name__)
app.secret_key = 'machimori'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/"

@login_manager.user_loader
def load_user(mail_address):
    db = DB()
    sql = 'select * from parent where parent_mail_address=\'{m_address}\';'.format(m_address=mail_address)
    data = db.select(sql)
    if mail_address not in data[0]:
        return
    user = User()
    user.id = mail_address
    return user

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        db = DB()
        mail_address = request.form['mail_address']
        password = request.form['password']
        sql = 'select * from parent where parent_mail_address=\'{m_address}\';'.format(m_address=mail_address)
        data = db.select(sql)
        for pas in data:
            if pas[6] == password:
                user = User()
                user.id = mail_address
                login_user(user)
                return redirect ('http://machimori.japanwest.cloudapp.azure.com/map?name={name}'.format(name=pas[4]))
        return redirect('/')
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('http://machimori.japanwest.cloudapp.azure.com/')

@app.route('/select_type')
def select_type():
    return render_template('select_type.html')

@app.route('/registration_parent')
def registration_parent():
    return render_template('registration_parent.html')

@app.route('/registration_parent_data',methods=['POST'])
def registration_parent_data():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        mail_addres = request.form['mail_addres']
        password = request.form['password']
        addres_number = request.form['zip11']
        addres = request.form['addr11']
        buzer_number = request.form['buzer_number']

        db = DB()
        data = (buzer_number,addres,0,0,first_name+last_name,mail_addres,password)
        sql = 'insert into parent values (%s,%s,%s,%s,%s,%s,%s)'
        db.insert_data(sql,data)
        return redirect('./')
                
@app.route('/registration_safehouse')
def registration_safehouse():
    return render_template('registration_safehouse.html')

@app.route('/registration_safehouse_data',methods=['POST'])
def registration_safehouse_data():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        mail_addres = request.form['mail_address']
        password = request.form['password']
        addres_number = request.form['zip11']
        addres = request.form['addr11']

        db = DB()
        data = (addres_number,0,0,first_name+last_name,mail_addres)
        sql = 'insert into safeguard values (%s,%s,%s,%s,%s)'
        db.insert_data(sql,data)
        return redirect('./')
    
@app.route('/map')
@login_required
def map():
    db = DB()
    sql = 'select * from occur;'
    occurdata = db.select(sql)
    sql = 'select * from safeguard'
    safeguarddata = db.select(sql) 
    create_json = My_Json()
    data = create_json.data_molding(0, occurdata, 1, safeguarddata)
    return render_template('map_display.html', data=data, name=request.args.get('name'))

@app.route('/add_occur_data', methods=['POST'])
def add_occur_data():
    if request.method == 'POST':
        data = request.form.getlist('case')
        print(data)
    return redirect('/map')

@app.route('/abnormal_mail')
def ab_send_mail():
    mail = My_Mail(app)
    mail.ab_send_mail(['ac6328mats@g.kumamoto-nct.ac.jp'])
    return "send"

@app.route('/buzzer_mail')
def bz_send_mail():
    mail = My_Mail(app)
    mail.bz_send_mail(['ac6328mats@g.kumamoto-nct.ac.jp'])
    return "send"

@app.route('/wio', methods=['GET','POST'])
def get_wiodata():
    mail = My_Mail(app)
    if request.method == 'POST':
        print('POSTで来た')
        mail.wio_get_mail(['ac6292tsur@g.kumamoto-nct.ac.jp', 'ac6328mats@g.kumamoto-nct.ac.jp', 'mi8117oish@g.kumamoto-nct.ac.jp'], 'POST', 0, 0)
    else :
        print('GETで来た')
        print(request.args.get('lat'))
        print(request.args.get('lon'))
        mail.wio_get_mail(['mi8117oish@g.kumamoto-nct.ac.jp','ac6328mats@g.kumamoto-nct.ac.jp', 'ac6292tsur@g.kumamoto-nct.ac.jp'], 'GET', request.args.get('lat'), request.args.get('lon'))
    return str(1)

@app.route('/auth/GZgUtindy45SywTrK4VPaczPPqOsbypG')
def mockmock():
    response = jsonify({'data': "GZgUtindy45SywTrK4VPaczPPqOsbypG"})
    return response

if __name__ == "__main__":
    app.run(debug=True)
