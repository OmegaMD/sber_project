# imports
from flask import Flask, render_template, request, redirect, url_for

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

        @self.flask.route('/submit_login', methods=['POST'])
        def submit_login():
            print(f"login:    { str(request.form.get('login_input')) }")
            print(f"password: { str(request.form.get('password_input')) }")
            return render_template('map.html')


# creating application instance
app = App()

# application entry point
if __name__ == '__main__':
    app.run()