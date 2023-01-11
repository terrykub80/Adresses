from app import app
from flask import render_template, redirect, url_for, flash
from app.forms import SignUpForm


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
        print(first_name, last_name, email, username, password)
        # TODO Check to see if there is a user with username and/or email

        # TODO Create a new user with form data

        # Flash a success message
        flash(f"Thank you {first_name} {last_name} for signing up!", 'success')
        # Redirect back to Home
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)
