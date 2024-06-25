from flask import redirect, render_template, url_for, request as req,flash,session
from main import app
from flask import render_template
from application.models import *
from datetime import datetime

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if req.method == 'GET':
        return render_template('add_category.html') 
    
    if req.method == 'POST':
        name = req.form.get('category_name')
        description = req.form.get('description')
        
        if not name:
            flash('Category Name is required', 'danger')
            return redirect(url_for('add_category'))
        
        category = Categories.query.filter_by(name=name).first()

        if category:
            flash('Category already exists', 'danger')
            return redirect(url_for('add_category'))
        
        if session['role']=='admin':
            try:
                category = Categories(name=name, description=description)
                db.session.add(category)
                db.session.commit()
                flash('Category added successfully', 'success')
                return redirect(url_for('add_category'))
            except Exception as e:
                flash(f'Error adding category!! Error: {e}', 'danger')
                return redirect(url_for('add_category'))
        
        elif session['role'] == 'store_manager':
            request = Requests.query.filter_by(username=session['username'], request_type='add_category', status='pending',new_category_name=name).first()
            
            if request:
                flash('Request already raised by the store manager', 'danger')
                return redirect(url_for('add_category'))
            
            request = Requests(username=session['username'],
                                request_type='add_category',
                                request_date=datetime.now(),
                                status = 'pending',
                                new_category_name = name,
                                new_category_description = description)  
            try:
                db.session.add(request)
                db.session.commit()
                flash('Request raised successfully', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                flash(f'Error raising request!! Error: {e}', 'danger')
                return redirect(url_for('add_category'))
            
        else:
            flash('Unauthorized Access', 'danger')
            return redirect(url_for('index'))
        
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if req.method =='GET':
        categories = Categories.query.all()
        return render_template('add_product.html', categories=categories)
    
    if req.method == 'POST':
        name = req.form.get('product_name')
        description = req.form.get('description')
        selling_price = req.form.get('selling_price')
        stock = req.form.get('stock')
        manufacture_date = req.form.get('mfg_date')
        expiry_date = req.form.get('expiry_date')
        cost_price = req.form.get('cost_price')
        category_id = req.form.get('category')

    #data validation

    if not name or not selling_price or not stock or not manufacture_date or not cost_price:
        flash('All fields are required', 'danger')
        return redirect(url_for('add_product'))
    
    category = Categories.query.filter_by(category_id=category_id).first()
    if not category:
        flash('Invalid Category', 'danger')
        return redirect(url_for('add_product'))
    
    if selling_price < cost_price:
        flash('Alert you are selling product in Loss', 'danger')
        return redirect(url_for('add_product'))
    
    if expiry_date < manufacture_date:
        flash('Expiry date should be greater than manufacture date', 'danger')
        return redirect(url_for('add_product'))
    
    if session['role'] == 'admin':
        flash('Unauthorized Access', 'danger')
        return redirect(url_for('index'))
    
    if session['role'] == 'store_manager':
        product = Product(name = name,
                          description = description,
                          selling_price = selling_price,
                          stock = int(stock),
                          manufacture_date = datetime.strptime(manufacture_date, "%Y-%m-%d").date(),
                          expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d").date(),
                          cost_price = int(cost_price),
                          category_id = category.category_id)
        try:   
            db.session.add(product)
            db.session.commit()
            flash('Product added successfully', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error adding product!! Error: {e}', 'danger')
            # db.session.rollback()
            return redirect(url_for('add_product'))
