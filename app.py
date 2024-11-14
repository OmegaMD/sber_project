# imports
from flask import Flask, render_template

# application class
class App:
    # application starting function
    def run(self):
        self.flask.run(debug=True)

    # class initialization function
    def __init__(self):
        ### local class variables ###

        # flask
        self.flask = Flask(__name__)

        ### flask callback functions ###

        # home flask function
        @self.flask.route('/')
        def home():
            return render_template('index.html')

        # going to login flask function
        @self.flask.route('/login', methods=['GET'])
        def login():
            return render_template('login.html')



# creating application instance
app = App()

# application entry point
if __name__ == '__main__':
    app.run()