from app import app
from flask import render_template, redirect, url_for, flash
from app.forms import SignUpForm
from app.models import User


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=["GET", "POST"])
def signup():
    # Create an instance of the SignUpForm
    form = SignUpForm()
    # Check if a POST request AND data is valid
    if form.validate_on_submit():
        print('Form Submitted and Validated')
        # Get data from the form
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
        # Check to see if there is a user with username and/or email
        check_user = User.query.filter( (User.username == username) | (User.email == email) ).first()
        if check_user:
            flash(f"A user with that username and/or email already exists. Please try again.", 'danger')
            return redirect(url_for('signup'))
        # Create a new user with form data
        new_user = User(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        # Flash a success message
        flash(f'Thank you {new_user.username} for signing up!', 'success')
        # Redirect back to Home
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)
