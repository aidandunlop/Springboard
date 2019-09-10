from flask_admin.contrib.sqla import ModelView
from flask import request, redirect, url_for
from flask_login import current_user
from wtforms import PasswordField


class AuthModelView(ModelView):

    form_excluded_columns = ('password_hash')
    #  Form will now use all the other fields in the model

    #  Add our own password form field - call it password2
    form_extra_fields = {
        'password': PasswordField('Password')
    }

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

    def on_model_change(self, form, User, is_created):
        if form.password.data is not None:
            User.set_password(form.password.data)
