from flask import Flask
#create a new app instance
app = Flask(__name__)

#create flask routes
@app.route('/')
def hello_world():
    return 'Hello world'

@app.route('/skill_drill')
def skill_drill(x):
    x = 2
    y = x + 3
    return y 