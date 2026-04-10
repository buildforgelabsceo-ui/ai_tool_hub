# app.py
from aitoolhub import create_app

app = create_app('production')  # change to production

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)