#!/usr/bin/python
#****************************************************************#
# ScriptName: hello.py
# Author: www.zhangyunsheng.com@gmail.com
# Create Date: 2016-03-19 12:41
# Modify Date: 2016-03-19 16:35
# Copyright ? 2016 Renren Incorporated. All rights reserved.
#***************************************************************#

from flask import Flask
from flask import url_for
from flask import render_template
from flask import request
from flask import redirect
from flask import abort
from flask import session
import logging

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/user/<username>')
def show_user_profile(username):
    return 'User %s' %(username)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %d' % post_id

@app.route('/projects/')
def projects():
    return 'The projects page'

@app.route('/about')
def about():
    abort(404)
    return redirect(url_for('hello', name = "from about"))
    return 'The about page'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return session['username']
    else:
        return '''
            <form action="" method="post">
                <p><input type=text name=username>
                <p><input type=submit value=Login>
            </form>
        '''


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    #app.logger.debug('[DEBUG] access hello')
    #app.logger.warning('[WARN] access hello')
    #app.logger.error('[ERROR] access hello')
    logging.debug('access hello')
    logging.warning('access hello')
    return render_template('hello.html', name=name)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('hello.html', name = "404"), 404

if __name__ == '__main__':
    with app.test_request_context():
        print url_for('projects')
        print url_for('show_user_profile', username = 'zhang')

    #logging.basicConfig(level=logging.DEBUG,
    #        format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    #        datafmt = '%a, %d %b %Y %H:%M:%S',
    #        filename = '/home/work/data_processor/log/dp.log',
    #        filemode = 'w')

    app.run(host='0.0.0.0', port=8888, debug=True)


