from aitoolhub import create_app
from flask import send_from_directory

app = create_app('production')  # create app FIRST

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
