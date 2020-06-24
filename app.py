from routes import app
from config import SECRET
if __name__ == '__main__':
    # Running app in debug mode
    app.secret_key = SECRET
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
