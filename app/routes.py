from app import app
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SignUpForm, LogInForm, AddressForm
from app.models import User, Address


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/addresses', methods=['GET'])
@login_required
def addresses():
    addies = Address.query.all()
    return render_template('addresses.html', addies=addies)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    
    form = SignUpForm()
    
    if form.validate_on_submit():
        print('Form Submitted and Validated')
        
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(f"""
        First Name: {first_name},
        Last Name: {last_name},
        Email: {email},
        Username: {username},
        Password: {password}
        """)
        
        check_user = User.query.filter( (User.username == username) | (User.email == email) ).first()
        if check_user:
            flash(f"A user with that username and/or email already exists. Please try again.", 'danger')
            return redirect(url_for('signup'))
        
        new_user = User(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        
        flash(f'Thank you {new_user.username} for signing up!', 'success')
        
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()

    if form.validate_on_submit():
        
        username = form.username.data
        password = form.password.data
        print(username, password)
        
        user = User.query.filter_by(username = username).first()
        
        if user is not None and user.check_password(password):
            
            login_user(user)
            flash(f"Welcome back {user.username}! You are now logged in!", "success")
            return redirect(url_for('index'))
        else:
            flash("Incorrect username and/or password", "danger")
            redirect(url_for('login'))
        
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out", "warning")
    return redirect(url_for('index'))



@app.route('/add_address', methods=['GET', 'POST'])
@login_required
def add_address():
    form = AddressForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone_number = form.phone_number.data
        address = form.address.data
        print(first_name, last_name, address, phone_number, current_user)
        
        new_address = Address(first_name=first_name, last_name=last_name, phone_number=phone_number, address=address, user_id=current_user.id)
        flash(f"The address for {new_address.first_name} {new_address.last_name} has been created!", "success")
        return redirect(url_for('index'))

    return render_template('create.html', form=form)


@app.route('/addresses/<address_id>')
def get_adress(address_id):
    addies = Address.query.get(address_id)
    if not addies:
        flash(f"An entry with id {address_id} does not exist", "danger")
        return redirect(url_for('index'))
    return render_template('addresses.html', addies=addies)


@app.route('/addresses/<address_id>/edit', methods=["GET", "POST"])
@login_required
def edit_address(address_id):
    addies = Address.query.get(address_id)
    if not addies:
        flash(f"An entry with id {address_id} does not exist", "danger")
        return redirect(url_for('index'))
    # Make sure the post author is the current user
    if addies.user_id != current_user.id:
        flash("You do not have permission to edit this post", "danger")
        return redirect(url_for('index'))
    form = AddressForm()
    if form.validate_on_submit():
        # Get the form data
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone_number = form.phone_number.data
        address = form.address.data
        # update the post using the .update method
        addies.update(first_name=first_name, last_name=last_name, phone_number=phone_number, address=address)
        flash(f"The address for {addies.first_name} {addies.last_name} has been updated", "success")
        return redirect(url_for('addresses', address_id=address_id))
    if request.method == 'GET':
        form.first_name.data = addies.first_name
        form.last_name.data = addies.last_name
        form.phone_number.data = addies.phone_number
        form.address.data = addies.address
    return render_template('edit_address.html', addies=addies, form=form)

@app.route('/addresses/<address_id>/delete')
@login_required
def delete_address(address_id):
    addies = Address.query.get(address_id)
    if not addies:
        flash(f"An address with id {address_id} does not exist", "danger")
        return redirect(url_for('index'))
    # Make sure the post author is the current user
    if addies.user_id != current_user.id:
        flash("You do not have permission to delete this post", "danger")
        return redirect(url_for('addresses'))
    addies.delete()
    flash(f"{addies.first_name} {addies.last_name} has been deleted", "info")
    return redirect(url_for('addresses'))
