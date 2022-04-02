from flask import Flask, render_template

app = Flask(__name__,template_folder='template')  #if u want to name the templates folder something else other than TEMPLATES 

@app.route("/ash")
def hello():
    return render_template('index.html')

@app.route("/about")
def ashraf():
    king="shahrukh khan"
    return render_template('about.html', name3=king)  # this name3 can be accessed from html file

# @app.route("/ashraf1")
# def hello_world2():
#     return "Hello, khan1!"
app.run(debug=True)