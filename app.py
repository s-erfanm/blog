from flask import Flask, render_template

app = Flask(__name__)



@app.route('/')
def home():
    return "hello I'm a new here"




if __name__ == '__main__':
    app.run(debug=True, port=3030)



