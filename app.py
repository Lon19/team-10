from flask import Flask, render_template
#app = Flask(__name__)
app = Flask(__name__, template_folder="build/", static_folder="build/static")

@app.route('/')
def hello_world():
  return render_template('index.html')

if __name__ == '__main__':
  app.run(debug=True)

