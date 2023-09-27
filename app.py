from flask import Flask, render_template, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = "my script key"

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"

db = SQLAlchemy(app)
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.datetime.now)
    
    def __repr__(self):
        return f'name : {self.name}/n email : {self.email}'
    

# create form class
class GetNameForm(FlaskForm):
    name = StringField("whats your Name ? ", validators=[DataRequired()])
    submit = SubmitField('Submit')

# create form class for db
class UserForm(FlaskForm):
    name = StringField("name: ", validators=[DataRequired()])
    email = StringField("email:", validators=[DataRequired()]) 
    submit = SubmitField('Submit')
    


@app.route('/')
def home():
    return render_template('home.html') 


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', username=name)

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("User added  Successfully !")
    our_users = Users.query.order_by(Users.date_added)
          
    return render_template('add_user.html',
                           form=form,
                           name=name,
                           our_users=our_users)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# update db record
@app.route('/update/<int:id>', methods=['Get', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        
        try :
            db.session.commit()
            flash("user updated successfully")
            return render_template('update_user.html',
                                form=form,
                                name_to_update=name_to_update)
        
        except :

            flash("there is an error !")
            return render_template('update_user.html',
                                form=form,
                                name_to_update=name_to_update)
            
    else:
            return render_template('update_user.html',
                                form=form,
                                name_to_update=name_to_update)           


@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = GetNameForm()
    
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully !")
    return render_template('name.html', form=form, name=name)
    
# with app.app_context():
#     db.create_all()
if __name__ == '__main__':
    
    app.run(debug=True, port=3030)



