

"""
FlaskアプリケーションのRouteとView
"""

from datetime import datetime
from flask import render_template
from flaskr import app

@app.route('/')
@app.route('/home')
def home():
    """インデックスページの表示"""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )