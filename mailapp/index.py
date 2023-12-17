import sys
sys.path.insert(0, '/Users/nguyenminhtu/Workspace/Freelance/mailserver')
from mailapp.admin import *
from flask import session, request, redirect, url_for, render_template, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from mailapp import app, login_manager
import utils

admin.init_app(app)

@login_manager.user_loader
def user_load(user_id):
    return utils.getUserByID(user_id=user_id)

@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        usr = utils.isAuthenticated(username, password)
        if usr:
            login_user(usr)
            session['logged_in'] = True
            session['role'] = False
            if usr.role_id == 1:
                session['role'] = True
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    if 'logged_in' in session:
        session.pop('logged_in', None)
        session.pop('user_id', None)
        session.pop('usr', None)
        session.pop('name', None)
        session.pop('role', None)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))
    
@app.route('/administration')
@login_required
def administration():
    if session['role']:
        return redirect('/admin')
    else:
        return redirect(url_for('index'))
    
@app.route('/home')
def home():
    if 'logged_in' in session:
        inbox = utils.getInbox(current_user.id)
        sentMail = utils.getSentMail(current_user.id)
        return render_template('index.html', receivedmails = inbox, sentMails = sentMail, 
                                totalInbox = len(inbox), totalSent = len(sentMail), secret_key = app.secret_key,
                                user = current_user.full_name, administration = session['role'], email = current_user.email_address)
    else:
        return redirect(url_for('login'))
    
@app.route('/change', methods=['GET', 'POST'])
@login_required
def change():
    if request.method == 'POST':
        if 'logged_in' in session:
                password = request.form['password'].strip()
                new_password = request.form['new-password'].strip()
                confirm = request.form['confirm'].strip()
                if utils.isAuthenticated(current_user.username, password) and new_password == confirm:
                    try:
                        utils.changePassword(current_user.username, confirm)
                        session.pop('logged_in', None)
                        return redirect(url_for('login'))
                    except:
                        return redirect(url_for('change'))
                else: return redirect(url_for('change'))

        return redirect(url_for('login'))

    return render_template('changePassword.html')

@app.route('/api/open-mail', methods = ['POST'])
def open_mail():
    data = request.json
    id = data.get('id')
    subject = data.get('subject')
    sender = data.get('sender')
    content = data.get('content')
    received_at = data.get('received_at')
    sender_name = utils.getUserByEmail(sender).full_name

    mails = session.get('mails')
    if not mails:
        mails = {}
    if id in mails:
        pass
    else:
        mails[id] = {
            'id': id,
            'subject': subject,
            'sender': sender,
            'sender_name': sender_name,
            'content': content,
            'received_at': received_at
        }
    session['mails'] = mails
    return jsonify(mails[id])  

@app.route('/api/send-mail', methods = ['POST'])
def send_mail():
    data = request.json
    email = data.get('email')
    title = data.get('title')
    content = data.get('message')
    app.logger.info('-------------------', email,title,content)
    try:
        receive_user_id = utils.getUserByEmail(email).id
        if utils.add_sent_mail(current_user.id, email, title, content):
            utils.add_received_mail(receive_user_id, current_user.email_address, title, content)
            return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    

@app.route('/get-secret-key')
def secret_key():
    secret_key = app.secret_key
    return jsonify({"secret_key": secret_key})


if __name__ == '__main__':

    app.run(debug=True, host='127.0.0.1', port=5000)