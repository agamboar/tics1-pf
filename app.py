from flask import Flask, render_template

def create_app():
    app = Flask(__name__)
    return app





if __name__ == '__main__':
    app.run(debug=True)