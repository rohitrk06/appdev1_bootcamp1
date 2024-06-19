from main import app
from flask import render_template, request, redirect, url_for, flash ,session
from application.database import db
from application.models import User, Role

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash("All Fields Required", 'danger')
            return redirect(url_for('login'))
        
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Invalid Email", 'danger')
            return redirect(url_for('login'))
        
        if user.password != password:
            flash("Invalid Password", 'danger')
            return redirect(url_for('login'))
        
        session['username'] = user.username
        session['email'] = user.email

        flash("Login Successful", 'success')
        return redirect(url_for('index'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    if request.method == 'POST':

        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        address = request.form.get('address')
        role = request.form.get('role')

        # Data validation
        if not username or not email or not password or not confirm_password or not role:
            flash("All Fields Required", 'danger')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash("Passwords do not match", 'danger')
            return redirect(url_for('register'))
        
        # if len(username)<3 and not username.isalnum():
        #     flash("Username must be alphanumeric and at least 3 characters long", 'danger')
        #     return redirect(url_for('register'))
        
        # if '@' not in email and '.' not in email:
        #     flash("Invalid Email", 'danger')
        #     return redirect(url_for('register'))
        
        if len(password)<8:
            flash("Password must be at least 8 characters long", 'danger')
            return redirect(url_for('register'))
        
        try:
            role = Role.query.filter_by(name=role).first()
            if not role:
                flash("Invalid Role", 'danger')
                return redirect(url_for('register'))
            user = User.query.filter_by(username=username).first()
            if user:
                flash("Username already exists", 'danger')
                return redirect(url_for('register'))
            user = User.query.filter_by(email=email).first()
            if user:
                flash("Email already exists", 'danger')
                return redirect(url_for('register'))
            user = User(username=username, email=email, password=password, address=address, roles=[role])
            db.session.add(user)
            db.session.commit()
            flash("User Registered Successfully", 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"User Registration Failed. Error: {e}", 'danger')
            return redirect(url_for('register'))

