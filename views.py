from flask import render_template, request, redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, login_user, logout_user, login_required, current_user, LoginManager
from app import app, User

login_manager = LoginManager(app)
login_manager.login_view = 'login'


class UserLogin(UserMixin):
    pass


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Register a new user and add them to the database
        pass
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Authenticate the user and log them in
        pass
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Create a ModelView for the Product model
class ProductModelView(ModelView):
    column_display_pk = True  # Show the primary key in the list view
    column_list = ['product_id', 'Name_of_OSH_related_ELT', 'Website']
    form_columns = ['Name_of_OSH_related_ELT', 'Website']  # Specify which columns to display in the form


# Create a ModelView for the Product model
class CategoryModelView(ModelView):
    column_display_pk = True  # Show the primary key in the list view
    column_list = ['cat_id', 'cat_name']
    form_columns = ['cat_id', 'cat_name']  # Specify which columns to display in the form
