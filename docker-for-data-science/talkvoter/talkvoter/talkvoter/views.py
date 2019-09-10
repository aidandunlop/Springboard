from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from .models import User
from .forms import LoginForm


def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=True)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


def logout():
    logout_user()
    return redirect(url_for('index'))


@login_required
def index():
    return render_template('index.html', title='Dashboard')
