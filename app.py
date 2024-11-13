# imports
from flask import Flask

# application class
class App:
    # application starting function
    def run(self):
        self.flask.run(debug=True)

    # class initialization function
    def __init__(self):
        self.flask = Flask(__name__)

        ### flask callback functions ###

        # home flask function
        @self.flask.route('/')
        def home():
            return "<h1>Добро пожаловать на мой сайт!</h1>"

# creating application instance
app = App()

# application entry point
if __name__ == '__main__':
    app.run()