from flask import Flask, render_template,request,sessions
import json
from flask.globals import session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
import pymysql
pymysql.install_as_MySQLdb()

local_server=True
with open('config.json','r') as c:
    params=json.load(c)["params"]

app=Flask(__name__,template_folder='template')
app.secret_key = 'super-secret key' #for admin and password login in flask
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-password']
)
mail=Mail(app)

if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)

class Contacts(db.Model):
    sr_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),  nullable=False)
    email = db.Column(db.String(20),  nullable=False)
    phone_num = db.Column(db.String(15),  nullable=False)
    message = db.Column(db.String(120),  nullable=False)
    date = db.Column(db.String(12),nullable=True)

class Posts(db.Model):
    sr_no = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25),  nullable=False)
    slug = db.Column(db.String(20),  nullable=False)
    content= db.Column(db.String(30),  nullable=False)
    date = db.Column(db.String(12),nullable=True)
    img_file = db.Column(db.String(12),nullable=True)
    tag_line = db.Column(db.String(25),nullable=True)



@app.route("/")
def home():
    posts=Posts.query.filter_by().all()[0:params['no_of_posts']]
    return render_template('index.html',params=params,posts=posts)

@app.route("/about")
def about():
    
    return render_template('about.html',params=params)

@app.route("/dashboard",methods=['GET','POST'])
def dashboard():
    if 'user' in session and session['user']==params['admin_user']: #if already logged in
        posts=Posts.query.all()#it will show all posts
        return render_template('dashboard.html',params=params,posts=posts)

    if request.method=="POST":
        username =request.form.get('uname')
        userpass =request.form.get('pass')
        if username==params['admin_user'] and userpass==params['admin_password']:
            #set the session variable
            session['user']=username  #saying to flask app that this user is ogged in
            posts=Posts.query.all() #it will show all posts
            return render_template('dashboard.html',params=params,posts=posts)
   
    return render_template('sign_in.html',params=params )

@app.route("/contact",methods=['GET','POST'])
def contact():
    if request.method=='POST':
        #add entry to database
        name=request.form.get('name') 
        email=request.form.get('email') 
        phone=request.form.get('phone') 
        message=request.form.get('message') 
        
        entry=Contacts(name=name,email=email,phone_num=phone,date=datetime.now(),message=message) #lhs is up thay is of class
        db.session.add(entry)
        db.session.commit()

        mail.send_message('new mwssage from blog', 
        sender=email,
        recipients=[params['gmail-user']],
        body=message + "\n" + phone )

    return render_template('contact.html',params=params)


@app.route("/post",methods=['GET','POST'])
def post():
    return render_template('post.html',params=params,post=post)

@app.route("/post/<string:post_slug>",methods=['GET'])# variable post_slug has to be passed in function too :rule of flak
def post_route(post_slug):
    post=Posts.query.filter_by(slug=post_slug).first()

    return render_template('post.html',params=params,post=post)


app.run(debug=True)