from flask import redirect, render_template, url_for, request as req,flash,session
from main import app
from flask import render_template
from application.models import *
from datetime import datetime

@app.route("/")
def index():
    if session.get('username',None):
        categories = Categories.query.all()
        return render_template('index.html',categories = categories)
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
        selling_price = float(req.form.get('selling_price'))
        stock = int(req.form.get('stock'))
        manufacture_date = datetime.strptime(req.form.get('mfg_date'), '%Y-%m-%d').date()
        expiry_date = datetime.strptime(req.form.get('expiry_date'), '%Y-%m-%d').date()
        cost_price = float(req.form.get('cost_price'))
        category_id = int(req.form.get('category'))

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
                          stock = stock,
                          manufacture_date = manufacture_date,
                          expiry_date = expiry_date,
                          cost_price = cost_price,
                          category_id = category.category_id,)
        try:    
            db.session.add(product)
            db.session.commit()
            flash('Product added successfully', 'success')
            return redirect(url_for('add_product'))
        except Exception as e:
            flash(f'Error adding product!! Error: {e}', 'danger')
            return redirect(url_for('add_product'))

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.filter_by(product_id=product_id).first()
    # print(product.description)

    if not product:
        flash('Product not found', 'danger')
        return redirect(url_for('index'))

    categories = Categories.query.all()
    if req.method == 'GET':
        return render_template('edit_product.html', product=product, categories=categories)
    
    if req.method == 'POST':
        name = req.form.get('product_name')
        description = req.form.get('description')
        selling_price = float(req.form.get('selling_price'))
        stock = int(req.form.get('stock'))
        manufacture_date = datetime.strptime(req.form.get('mfg_date'), '%Y-%m-%d').date()
        expiry_date = datetime.strptime(req.form.get('expiry_date'), '%Y-%m-%d').date()
        cost_price = float(req.form.get('cost_price'))
        category_id = int(req.form.get('category'))

        #data validation
        product = Product.query.filter_by(product_id=product_id).first()
        if name:
            product.name = name
        if description:
            product.description = description
        if selling_price:
            product.selling_price = selling_price
        if stock:
            product.stock = stock
        if manufacture_date:
            product.manufacture_date = manufacture_date
        if expiry_date:
            product.expiry_date = expiry_date
        if cost_price:
            product.cost_price = cost_price
        if category_id:
            category = Categories.query.filter_by(category_id=category_id).first()
            if not category:
                flash('Invalid Category', 'danger')
                return redirect(url_for('edit_product', product_id=product_id))
            product.category_id = category.category_id
        
        if selling_price < cost_price:
            flash('Alert you are selling product in Loss', 'danger')
            return redirect(url_for('add_product'))
    
        if expiry_date < manufacture_date:
            flash('Expiry date should be greater than manufacture date', 'danger')
            return redirect(url_for('add_product'))
        
        if session['role'] == 'admin':
            flash('Unauthorized Access', 'danger')
            return redirect(url_for('index'))

        try:
            db.session.commit()
            flash('Product updated successfully', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error updating product!! Error: {e}', 'danger')
            return redirect(url_for('edit_product', product_id=product_id))
        
@app.route('/delete_product/<int:product_id>', methods=['GET', 'POST'])
def delete_product(product_id):
    product = Product.query.filter_by(product_id = product_id).first()
    if not product:
        flash('Product not found', 'danger')
        return redirect(url_for('index'))
    
    if req.method == 'GET':
        return render_template('delete_product.html', product=product)
    
    if req.method == 'POST':
        if session['role'] == 'store_manager':
            try:
                db.session.delete(product)
                db.session.commit()
                flash('Product deleted successfully', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                flash(f'Error deleting product!! Error: {e}', 'danger')
                return redirect(url_for('delete_product', product_id=product_id))
        else:
            flash('Unauthorized Access', 'danger')
            return redirect(url_for('index'))
        

@app.route('/edit_category/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    category = Categories.query.filter_by(category_id=category_id).first()
    if not category:
        flash('Category not found', 'danger')
        return redirect(url_for('index'))
    
    if req.method=='GET':
        print(category)
        return render_template('edit_category.html', category=category)
    
    if req.method == 'POST':
        name = req.form.get('category_name')
        description = req.form.get('description')
        
        if session['role']=='admin':
            try:
                existing_category = Categories.query.filter_by(name=name).first()
                if existing_category and category_id != existing_category.category_id:
                    flash('Category already exists', 'danger')
                    return redirect(url_for('edit_category', category_id=category_id))
                
                if name:
                    category.name = name
                if description:
                    category.description = description

                db.session.commit()
                flash('Category updated Successfully', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                flash(f'Error adding category!! Error: {e}', 'danger')
                return redirect(url_for('edit_category', category_id=category_id))
        
        elif session['role'] == 'store_manager':
            request = Requests.query.filter_by(username=session['username'], request_type='edit_category', status='pending',new_category_name=name).first()
            
            if request:
                flash('Request already raised by the store manager', 'danger')
                return redirect(url_for('edit_category', category_id=category_id))
            
            request = Requests(username=session['username'],
                                request_type='edit_category',
                                request_date=datetime.now(),
                                status = 'pending',
                                category_id = category_id,
                                new_category_name = name,
                                new_category_description = description)  
            try:
                db.session.add(request)
                db.session.commit()
                flash('Request raised successfully', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                flash(f'Error raising request!! Error: {e}', 'danger')
                return redirect(url_for('edit_category', category_id=category_id))
            
        else:
            flash('Unauthorized Access', 'danger')
            return redirect(url_for('index'))
        

@app.route('/delete_category/<int:category_id>', methods=['GET', 'POST'])
def delete_category(category_id):
    category = Categories.query.filter_by(category_id = category_id).first()
    if not category:
        flash('Category not found', 'danger')
        return redirect(url_for('index'))
    
    if req.method == 'GET':
        return render_template('delete_category.html', category=category)
    
    if req.method == 'POST':
        if session['role'] == 'store_manager':
            request = Requests.query.filter_by(username=session['username'], request_type='delete_category', status='pending',category_id=category_id).first()
            
            if request:
                flash('Request already raised by the store manager', 'danger')
                return redirect(url_for('edit_category', category_id=category_id))
            
            request = Requests(username=session['username'],
                                request_type='delete_category',
                                request_date=datetime.now(),
                                status = 'pending',
                                category_id = category_id)  
            try:
                db.session.add(request)
                db.session.commit()
                flash('Request raised successfully', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                flash(f'Error raising request!! Error: {e}', 'danger')
                return redirect(url_for('edit_category', category_id=category_id))
            
        elif session['role'] == 'admin':
            try:
                db.session.delete(category)
                db.session.commit()
                flash('Category deleted successfully', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                flash(f'Error deleting category!! Error: {e}', 'danger')
                return redirect(url_for('delete_category', category_id=category_id))
        else:
            flash('Unauthorized Access', 'danger')
            return redirect(url_for('index'))


@app.route('/store_manager_requests')
def store_manager_requests():
    if session['role'] == 'admin':
        requests = Requests.query.filter_by(status='pending').all()
        return render_template('requests.html', requests=requests)
    elif session['role'] == 'store_manager':
        requests = Requests.query.filter_by(username=session['username']).all()
        return render_template('requests.html', requests=requests)
    else:
        flash('Unauthorized Access', 'danger')
        return redirect(url_for('index'))
    
@app.route('/approve_request/<int:request_id>', methods=['GET', 'POST'])
def approve_request(request_id):
    request= Requests.query.filter_by(request_id=request_id).first()

    if not request:
        flash('Request not found', 'danger')
        return redirect(url_for('index'))
    
    if session['role']=='admin':
        if request.request_type == 'add_category':
            category = Categories.query.filter_by(name=request.new_category_name).first()
            if category:
                request.status = 'rejected'
                db.session.commit()
                flash('Category already exists - Request Rejected', 'danger')
                return redirect(url_for('store_manager_requests'))
            
            category = Categories(name=request.new_category_name, description=request.new_category_description)
            try:
                db.session.add(category)
                db.session.commit()
                request.status = 'approved'
                db.session.commit()
                flash('Category added successfully', 'success')
                return redirect(url_for('store_manager_requests'))
            except Exception as e:
                flash(f'Error adding category!! Error: {e}', 'danger')
                return redirect(url_for('store_manager_requests'))
        
        if request.request_type == 'edit_category':
            category = Categories.query.filter_by(name=request.new_category_name).first()
            if category:
                request.status = 'rejected'
                db.session.commit()
                flash('Category with same name already exits - Request Rejected', 'danger')
                return redirect(url_for('store_manager_requests'))
            
            category = Categories.query.filter_by(category_id=request.category_id).first()
            if not category:
                request.status = 'rejected'
                db.session.commit()
                flash('Category not found - Request Rejected', 'danger')
                return redirect(url_for('store_manager_requests'))
            
            category.name = request.new_category_name
            category.description = request.new_category_description
            try:
                db.session.commit()
                request.status = 'approved'
                db.session.commit()
                flash('Category updated successfully', 'success')
                return redirect(url_for('store_manager_requests'))
            except Exception as e:
                flash(f'Error updating category!! Error: {e}', 'danger')
                return redirect(url_for('store_manager_requests'))
            
        if request.request_type == 'delete_category':
            category = Categories.query.filter_by(category_id=request.category_id).first()
            if not category:
                request.status = 'rejected'
                db.session.commit()
                flash('Category not found - Request Rejected', 'danger')
                return redirect(url_for('store_manager_requests'))
            
            try:
                db.session.delete(category)
                # db.session.commit()
                request.status = 'approved'
                db.session.commit()
                flash('Category deleted successfully', 'success')
                return redirect(url_for('store_manager_requests'))
            except Exception as e:
                flash(f'Error deleting category!! Error: {e}', 'danger')
                return redirect(url_for('store_manager_requests'))
            
@app.route('/reject_request/<int:request_id>', methods=['GET', 'POST'])
def reject_request(request_id):
    request= Requests.query.filter_by(request_id=request_id).first()

    if not request:
        flash('Request not found', 'danger')
        return redirect(url_for('index'))
    
    if session['role']=='admin':
        request.status = 'rejected'
        db.session.commit()
        flash('Request rejected successfully', 'success')
        return redirect(url_for('store_manager_requests'))
    
@app.route('/add_to_cart/<int:product_id>', methods=['GET', 'POST'])
def add_to_cart(product_id):    
    product = Product.query.filter_by(product_id=product_id).first()
    if not product:
        flash('Product not found', 'danger')
        return redirect(url_for('index'))
    
    # if req.method == 'GET':
    #     return render_template('add_to_cart.html', product=product)
    
    if req.method == 'POST':
        quantity = req.form.get('quantity')
        if not quantity:
            flash('Quantity is required', 'danger')
            return redirect(url_for('add_to_cart', product_id=product_id))
        try:
            quantity = int(quantity)
        except:
            flash('Quantity should be a number', 'danger')
            return redirect(url_for('add_to_cart', product_id=product_id))
        if quantity <= 0:
            flash('Quantity should be greater than 0', 'danger')
            return redirect(url_for('add_to_cart', product_id=product_id))
        
        if quantity > product.stock:
            flash('Insufficient stock', 'danger')
            return redirect(url_for('add_to_cart', product_id=product_id))
        
        cart = Cart.query.filter_by(username=session['username'], product_id=product_id).first()
        if cart:
            cart.quantity += quantity
            product.stock -= quantity
        else:
            cart = Cart(username=session['username'], product_id=product_id, quantity=quantity)
            product.stock -= quantity
        
        try:
            db.session.add(cart)
            db.session.commit()
            flash('Product added to cart successfully', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error adding product to cart!! Error: {e}', 'danger')
            return redirect(url_for('add_to_cart', product_id=product_id))

            

        

