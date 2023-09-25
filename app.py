from flask import Flask, render_template, url_for

app = Flask(__name__)



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', username=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404













if __name__ == '__main__':
    app.run(debug=True, port=3030)



