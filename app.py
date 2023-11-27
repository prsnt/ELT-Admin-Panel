import re
import secrets
import logging
import MySQLdb.cursors
from flask import Flask, render_template, request, session, app, redirect, url_for
from flask_admin import Admin, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.filters import FilterEqual
from flask_admin.form import Select2Widget
from flask_admin.model import InlineFormAdmin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.dialects import mysql
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from wtforms import SelectField, TextAreaField, StringField
from wtforms.validators import InputRequired, Length, URL

db = SQLAlchemy()
admin = Admin()
app = Flask(__name__)


@app.route('/')
@app.route('/admin/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = % s AND password = % s', (email, password,))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            message = 'Logged in successfully !'
            return render_template('admin.html', message=message)
        else:
            message = 'Please enter correct email / password !'
    return render_template('/admin/login.html', message=message)


# Make function for logout session
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))


# Make a register session for registration session
# and also connect to Mysql to code for access login
# and for completing our login
# session and making some flashing massage for error
@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:

        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email,))
        account = cursor.fetchone()
        if account:
            message = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address !'
        elif not userName or not password or not email:
            message = 'Please fill out the form !'
        else:
            cursor.execute(
                'INSERT INTO user VALUES (NULL, % s, % s, % s)',
                (userName, email, password,))
            mysql.connection.commit()
            message = 'You have successfully registered !'
    elif request.method == 'POST':
        message = 'Please fill out the form !'
    return render_template('/admin/register.html', message=message)


class FreePaidFilter(FilterEqual):
    def operation(self):
        return 'equals'

    def clean(self, value):
        return value


def create_app():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://prashant:Prsnt%40151993@localhost:3306/test_db'
    secret_key = secrets.token_hex(32)
    # Set the secret key
    app.config['SECRET_KEY'] = secret_key
    app.config['FLASK_ADMIN_FLUID_LAYOUT'] = True
    db = SQLAlchemy(app)
    admin = Admin(app, name='ADMIN PANEL', template_mode='bootstrap4')
    admin.add_view(ProductModelView(EltCleanExtraction, db.session, name='Products'))
    admin.add_view(CategoryModelView(Categories, db.session, name='Categories'))
    admin.add_view(TopicModelView(TopicArea, db.session, name='Topic Areas'))
    admin.add_view(DeveloperModelView(Developers, db.session, name='Developers'))
    admin.add_view(CountryModelView(CountryName, db.session, name='Countries'))
    admin.add_view(TypesELTModelView(ELTTypes, db.session, name='ELT Types'))
    admin.add_view(TasksModelView(Tasks, db.session, name='Tasks & Topics'))
    admin.add_view(LanguagesModelView(Languages, db.session, name="Languages"))
    admin.add_view(OSHTopicsModelView(OSHTopics, db.session, name="OSH Topics"))
    admin.add_view(HardwareModelView(Hardwares, db.session, name="Hardwares"))
    admin.add_view(OccupationModelView(Occupations, db.session, name="Occupations"))
    # Set SQLAlchemy logging level to DEBUG
    logging.getLogger('sqlalchemy').setLevel(logging.DEBUG)
    return app


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200))
    password = db.Column(db.String(200))
    role_id = db.Column(db.ForeignKey('role.role_id'))
    role = db.relationship('Role', backref=db.backref('users', lazy=True))


class Role(db.Model):
    role_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)


class EltCleanExtraction(db.Model):
    __tablename__ = 'elt_clean_extraction'

    # Define the columns of the table
    product_id = db.Column(db.Integer, primary_key=True)
    Name_of_OSH_related_ELT = db.Column(db.String(300))
    Description_of_technology = db.Column(db.String(5000))
    Website = db.Column(db.String(800))
    type_of_ELT = db.relationship("ELTTypes", secondary="product_elt", back_populates="products")
    categories = db.relationship("Categories", secondary="product_category", back_populates="products")
    topics = db.relationship("TopicArea", secondary="product_topic", back_populates="products")
    countries = db.relationship("CountryName", secondary="product_country", back_populates="products")
    developers = db.relationship("Developers", secondary="product_developer", back_populates="products")
    tasks_topics = db.relationship("Tasks", secondary="product_task", back_populates="products")
    languages = db.relationship("Languages", secondary="product_language", back_populates="products")
    osh_topics = db.relationship("OSHTopics", secondary="product_oshtopic", back_populates="products")
    hardwares = db.relationship("Hardwares", secondary="product_hardware", back_populates="products")
    occupations = db.relationship("Occupations", secondary="product_occupation", back_populates="products")
    date_of_release_and_version_number = db.Column(db.String(150))
    Certification_accreditation_for_completion = db.Column(db.String(200))
    ELT_in_Research_Articles = db.Column(db.String(400))
    Standards_used_in_Curriculum_development = db.Column(db.String(300))
    Duration_min = db.Column(db.String(100))
    Free_Paid = db.Column(db.String(20))


class Product_Categories(db.Model):
    __tablename__ = 'product_category'

    product_id = db.Column(db.Integer, db.ForeignKey('elt_clean_extraction.product_id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category_tbl.cat_id'), primary_key=True)

    def __str__(self):
        return self.categories


class Product_Topicarea(db.Model):
    __tablename__ = 'product_topic'

    product_id = db.Column(db.Integer, db.ForeignKey('elt_clean_extraction.product_id'), primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topicarea_tbl.topic_id'), primary_key=True)

    def __str__(self):
        return self.topics


class Product_Country(db.Model):
    __tablename__ = 'product_country'

    product_id = db.Column(db.Integer, db.ForeignKey('elt_clean_extraction.product_id'), primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country_tbl.country_id'), primary_key=True)

    def __str__(self):
        return self.countries


class Product_ELT(db.Model):
    __tablename__ = 'product_elt'

    product_id = db.Column(db.Integer, db.ForeignKey('elt_clean_extraction.product_id'), primary_key=True)
    elt_id = db.Column(db.Integer, db.ForeignKey('elt_types_tbl.elt_type_id'), primary_key=True)

    def __str__(self):
        return self.type_of_ELT


class Product_developer(db.Model):
    __tablename__ = 'product_developer'

    product_id = db.Column(db.Integer, db.ForeignKey('elt_clean_extraction.product_id'), primary_key=True)
    developer_id = db.Column(db.Integer, db.ForeignKey('developer_tbl.developer_id'), primary_key=True)

    def __str__(self):
        return self.developers


class Product_tasks(db.Model):
    __tablename__ = 'product_task'

    product_id = db.Column(db.Integer, db.ForeignKey('elt_clean_extraction.product_id'), primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks_tbl.task_id'), primary_key=True)

    def __str__(self):
        return self.tasks_topics


class Product_language(db.Model):
    __tablename__ = 'product_language'

    product_id = db.Column(db.Integer, db.ForeignKey('elt_clean_extraction.product_id'), primary_key=True)
    language_id = db.Column(db.Integer, db.ForeignKey('language_tbl.language_id'), primary_key=True)

    def __str__(self):
        return self.languages


class Product_osh_topics(db.Model):
    __tablename__ = 'product_oshtopic'

    product_id = db.Column(db.Integer, db.ForeignKey('elt_clean_extraction.product_id'), primary_key=True)
    osh_topic_id = db.Column(db.Integer, db.ForeignKey('osh_topics_tbl.osh_topic_id'), primary_key=True)

    def __str__(self):
        return self.osh_topics


class Product_Hardware(db.Model):
    __tablename__ = 'product_hardware'

    product_id = db.Column(db.Integer, db.ForeignKey('elt_clean_extraction.product_id'), primary_key=True)
    hardware_id = db.Column(db.Integer, db.ForeignKey('hardwares_tbl.hardware_id'), primary_key=True)

    def __str__(self):
        return self.hardwares


class Product_Occupation(db.Model):
    __tablename__ = 'product_occupation'

    product_id = db.Column(db.Integer, db.ForeignKey('elt_clean_extraction.product_id'), primary_key=True)
    occupation_id = db.Column(db.Integer, db.ForeignKey('occupation_tbl.occupation_id'), primary_key=True)

    def __str__(self):
        return self.occupations


class Occupations(db.Model):
    __tablename__ = 'occupation_tbl'

    occupation_id = db.Column(db.Integer, primary_key=True)
    occupation_name = db.Column(db.String(300))
    products = db.relationship("EltCleanExtraction", secondary="product_occupation", back_populates="occupations")

    def __str__(self):
        return self.occupation_name


class Hardwares(db.Model):
    __tablename__ = 'hardwares_tbl'

    hardware_id = db.Column(db.Integer, primary_key=True)
    hardware_name = db.Column(db.String(200))
    products = db.relationship("EltCleanExtraction", secondary="product_hardware", back_populates="hardwares")

    def __str__(self):
        return self.hardware_name


class Languages(db.Model):
    __tablename__ = 'language_tbl'

    language_id = db.Column(db.Integer, primary_key=True)
    language_name = db.Column(db.String(200))
    products = db.relationship("EltCleanExtraction", secondary="product_language", back_populates="languages")

    def __str__(self):
        return self.language_name


class OSHTopics(db.Model):
    __tablename__ = 'osh_topics_tbl'

    osh_topic_id = db.Column(db.Integer, primary_key=True)
    osh_topic_name = db.Column(db.String(500))
    products = db.relationship("EltCleanExtraction", secondary="product_oshtopic", back_populates="osh_topics")

    def __str__(self):
        return self.osh_topic_name


class ELTTypes(db.Model):
    __tablename__ = 'elt_types_tbl'

    elt_type_id = db.Column(db.Integer, primary_key=True)
    elt_type_name = db.Column(db.String(300))
    products = db.relationship("EltCleanExtraction", secondary="product_elt", back_populates="type_of_ELT")

    def __str__(self):
        return self.elt_type_name


class Tasks(db.Model):
    __tablename__ = 'tasks_tbl'

    # Define the columns of the table
    task_id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(150))
    products = db.relationship("EltCleanExtraction", secondary="product_task", back_populates="tasks_topics")

    def __str__(self):
        return self.task_name


class Developers(db.Model):
    __tablename__ = 'developer_tbl'

    # Define the columns of the table
    developer_id = db.Column(db.Integer, primary_key=True)
    developer_name = db.Column(db.String(150))
    products = db.relationship("EltCleanExtraction", secondary="product_developer", back_populates="developers")

    def __str__(self):
        return self.developer_name


class Categories(db.Model):
    __tablename__ = 'category_tbl'

    # Define the columns of the table
    cat_id = db.Column(db.Integer, primary_key=True)
    cat_name = db.Column(db.String(150))
    products = db.relationship("EltCleanExtraction", secondary="product_category", back_populates="categories")

    def __str__(self):
        return self.cat_name


class TopicArea(db.Model):
    __tablename__ = 'topicarea_tbl'

    # Define the columns of the table
    topic_id = db.Column(db.Integer, primary_key=True)
    topic_area = db.Column(db.String(400))
    products = db.relationship("EltCleanExtraction", secondary="product_topic", back_populates="topics")

    def __str__(self):
        return self.topic_area


class CountryName(db.Model):
    __tablename__ = 'country_tbl'

    country_id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(200))
    products = db.relationship("EltCleanExtraction", secondary="product_country", back_populates="countries")

    def __str__(self):
        return self.country_name


class HomeView(AdminIndexView):
    @expose("/")
    def index(self):
        return self.render('admin/eltcleanextraction.html')


# Create a ModelView for the Product model
class ProductModelView(ModelView):
    column_display_pk = True  # Show the primary key in the list view
    column_list = ['product_id', 'Name_of_OSH_related_ELT', 'Description_of_technology', 'Website',
                   'categories', 'developers', 'type_of_ELT', 'tasks_topics',
                   'topics', 'countries', 'Free_Paid']
    form_columns = ['Name_of_OSH_related_ELT',
                    'Description_of_technology',
                    'Website',
                    'categories',
                    'developers',
                    'type_of_ELT',
                    'languages',
                    'hardwares',
                    'occupations',
                    'osh_topics',
                    'tasks_topics',
                    'topics',
                    'countries',
                    'date_of_release_and_version_number',
                    'Certification_accreditation_for_completion',
                    'ELT_in_Research_Articles',
                    'Standards_used_in_Curriculum_development',
                    'Duration_min',
                    'Free_Paid'
                    ]  # Specify which columns to display in the form
    form_extra_fields = {
        'Name_of_OSH_related_ELT': StringField('Name of OSH related ELT',
                                               validators=[InputRequired(), Length(max=300)]),
        'Description_of_technology': TextAreaField('Description of Technology',
                                                   validators=[InputRequired(), Length(max=5000)]),
        'Website': StringField('Website', validators=[InputRequired(), URL(), Length(max=800)]),

        'date_of_release_and_version_number': StringField('Date of release and version number',
                                                          validators=[Length(max=150)]),
        'Certification_accreditation_for_completion': StringField('Certification accreditation for completion',
                                                                  validators=[Length(max=200)]),
        'ELT_in_Research_Articles': StringField('ELT in research articles', validators=[Length(max=400)]),
        'Standards_used_in_Curriculum_development': StringField('Standards used in Curriculum development',
                                                                validators=[Length(max=300)]),
        'Duration_min': StringField('Duration (Mins)', validators=[Length(max=100)]),
    }
    column_searchable_list = ['Name_of_OSH_related_ELT']
    column_filters = ['categories', 'topics', 'countries', 'developers',
                      FreePaidFilter(column=EltCleanExtraction.Free_Paid, name='Free Or Paid',
                                     options=(('free', 'Free'), ('paid', 'Paid')))]

    column_sortable_list = ['product_id', 'Name_of_OSH_related_ELT', 'Free_Paid']

    column_formatters = {'Description_of_technology': lambda v, c, m, p: m.Description_of_technology[:100] if m.Description_of_technology else ''}

    free_paid_choices = [
        ('free', 'Free'),
        ('paid', 'Paid')
    ]

    form_overrides = {
        'Description_of_technology': TextAreaField,
        'Free_Paid': SelectField
    }

    form_args = {
        'Free_Paid': {
            'widget': Select2Widget(multiple=False),
            'choices': free_paid_choices
        },
        'developers': {
            'label': 'Developers',
            'validators': [Length(max=300)],
        },
        'type_of_ELT': {
            'label': 'Type of ELT',
            'validators': [Length(max=200)],
        },
        'languages': {
            'label': 'Languages',
            'validators': [Length(max=300)],
        },
        'hardwares': {
            'label': 'Hardware options for ELT',
            'validators': [Length(max=500)],
        },
        'occupations': {
            'label': 'Skill trade occupations',
            'validators': [Length(max=400)],
        },
        'osh_topics': {
            'label': 'OSH Topics',
            'validators': [Length(max=400)],
        },
        'tasks_topics': {
            'label': 'Tasks and Topics',
            'validators': [Length(max=1000)],
        },
        'topics': {
            'label': 'Key topic areas',
            'validators': [InputRequired(), Length(max=300)],
        },
        'countries': {
            'label': 'Country head quarters',
            'validators': [Length(max=150)],
        },
    }

    def on_form_prefill(self, form, id):
        # record = EltCleanExtraction.Free_Paidquery.get(id)
        # print("PRT"+EltCleanExtraction.Free_Paid)
        if EltCleanExtraction.Free_Paid:
            form.Free_Paid.data = EltCleanExtraction.Free_Paid


# Create a ModelView for the Product model
class CategoryModelView(ModelView):
    column_display_pk = True  # Show the primary key in the list view
    column_list = ['cat_id', 'cat_name']
    form_columns = ['cat_name']  # Specify which columns to display in the form

    form_extra_fields = {
        'cat_name': StringField('Category Name', validators=[InputRequired(), Length(max=150)]),
    }


# Create a ModelView for the Product model
class TopicModelView(ModelView):
    column_display_pk = True  # Show the primary key in the list view
    column_list = ['topic_id', 'topic_area']
    form_columns = ['topic_area']  # Specify which columns to display in the form
    column_searchable_list = ['topic_area']
    form_extra_fields = {
        'topic_area': StringField('Topic Area', validators=[InputRequired(), Length(max=400)]),
    }


# Create a ModelView for the Product model
class DeveloperModelView(ModelView):
    column_display_pk = True  # Show the primary key in the list view
    column_list = ['developer_id', 'developer_name']
    form_columns = ['developer_name']  # Specify which columns to display in the form
    column_searchable_list = ['developer_name']
    form_extra_fields = {
        'developer_name': StringField('Developer Name', validators=[InputRequired(), Length(max=150)]),
    }


# Create a ModelView for the Product model
class CountryModelView(ModelView):
    column_display_pk = True  # Show the primary key in the list view
    column_list = ['country_id', 'country_name']
    form_columns = ['country_name']  # Specify which columns to display in the form
    column_searchable_list = ['country_name']
    form_extra_fields = {
        'country_name': StringField('Country Name', validators=[InputRequired(), Length(max=200)]),
    }


# Create a ModelView for the Product model
class TypesELTModelView(ModelView):
    column_display_pk = True  # Show the primary key in the list view
    column_list = ['elt_type_id', 'elt_type_name']
    form_columns = ['elt_type_name']  # Specify which columns to display in the form
    column_searchable_list = ['elt_type_name']
    form_extra_fields = {
        'elt_type_name': StringField('ELT type name', validators=[InputRequired(), Length(max=200)]),
    }


# Create a ModelView for the Product model
class TasksModelView(ModelView):
    column_display_pk = True  # Show the primary key in the list view
    column_list = ['task_id', 'task_name']
    form_columns = ['task_name']  # Specify which columns to display in the form
    column_searchable_list = ['task_name']
    form_extra_fields = {
        'task_name': StringField('Task Name', validators=[InputRequired(), Length(max=200)]),
    }


# Create a ModelView for the Product model
class LanguagesModelView(ModelView):
    column_display_pk = True  # Show the primary key in the list view
    column_list = ['language_id', 'language_name']
    form_columns = ['language_name']  # Specify which columns to display in the form
    column_searchable_list = ['language_name']
    form_extra_fields = {
        'language_name': StringField('Language', validators=[InputRequired(), Length(max=200)]),
    }


# Create a ModelView for the Product model
class OSHTopicsModelView(ModelView):
    column_display_pk = True  # Show the primary key in the list view
    column_list = ['osh_topic_id', 'osh_topic_name']
    form_columns = ['osh_topic_name']  # Specify which columns to display in the form
    column_searchable_list = ['osh_topic_name']
    form_extra_fields = {
        'osh_topic_name': StringField('OSH Topic Name', validators=[InputRequired(), Length(max=200)]),
    }


# Create a ModelView for the Product model
class HardwareModelView(ModelView):
    column_display_pk = True  # Show the primary key in the list view
    column_list = ['hardware_id', 'hardware_name']
    form_columns = ['hardware_name']  # Specify which columns to display in the form
    column_searchable_list = ['hardware_name']
    form_extra_fields = {
        'hardware_name': StringField('Hardware Name', validators=[InputRequired(), Length(max=200)]),
    }


# Create a ModelView for the Product model
class OccupationModelView(ModelView):
    column_display_pk = True  # Show the primary key in the list view
    column_list = ['occupation_id', 'occupation_name']
    form_columns = ['occupation_name']  # Specify which columns to display in the form
    column_searchable_list = ['occupation_name']
    form_extra_fields = {
        'occupation_name': StringField('Occupation', validators=[InputRequired(), Length(max=200)]),
    }


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
