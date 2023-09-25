from flask import Flask, render_template, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = "my script key"

# create form class
class GetNameForm(FlaskForm):
    name = StringField("whats your Name ? ", validators=[DataRequired()])
    submit = SubmitField('Submit')
    


@app.route('/')
def home():
    return render_template('home.html') 


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', username=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404




@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = GetNameForm()
    
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully !")
    return render_template('name.html', form=form, name=name)
    
    

if __name__ == '__main__':
    app.run(debug=True, port=3030)



