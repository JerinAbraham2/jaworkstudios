#you can do this because website is a python package and when you put a init.py file it becomes a python package
from website import create_app
from flask import request, redirect
import os
from flask_sqlalchemy import SQLAlchemy

app = create_app()

if __name__ == '__app__':
    app.debug(debug=True)

#redirects http:// to https://
@app.before_request
def before_request():
    if 'DYNO' in os.environ:
        if request.url.startswith('http://'):
            url = request.url.replace('http://', 'https://', 1)
            code = 301
            return redirect(url, code=code)
#redirects http:// to https://















#web app: source /home/tobidendom/Documents/py/pyflask/env/bin/activate


#first time making new app or something pip3 install virtualenv (or just pip)
#once your in the virtual enviroment using the below source env/bin/activate
#then type in that pip3 (or just pip again) install flask (in linux you can do sudo apt install flask i think im not sure, i think you have to do pip and under env)
#same thing if you want sqlalchemy for that env, install in that env again using pip- install pip install flask-sqlalchemy


#the regular is below:
#run this: source env/bin/activate then flask run

    # cant have comments in the html if you have a base.html <!--you can use this for javascript as well <link rel="stylesheet" href="{{ url_for('static', filename='css/index.css') }}"> -->
    # <!-- the above is ginger {} text {{}} and it will take the thing and give the return as a string or something  -->
    # <!-- you cant have comments in the pages that inherit the base.html -->


#updating website git
#heroku login (or login heroku?)
#git add .
#git commit -m "comment here about what your changing"
#git push heroku master
