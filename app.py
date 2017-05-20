from flask import Flask, render_template, redirect, url_for, request, flash
from forms import UserForm, MessageForm
from flask_modus import Modus
from flask_sqlalchemy import SQLAlchemy
import os
from IPython import embed
import jinja2

app = Flask(__name__)
modus = Modus(app)

if os.environ.get('ENV') == 'production:
    app.config.from_object('config.ProductionConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.jinja_env.undefined = jinja2.StrictUndefined
app.jinja_env.auto_reload = True

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    email = db.Column(db.Text)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    messages = db.relationship('Message', backref='user', lazy='dynamic')

    def __init__(self, username, email, first_name, last_name):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
    
    def __repr__(self):
        return "Username: {}, email: {}, first name: {}, last name: {}".format(self.username, self.email, self.first_name, self.last_name)

@app.route('/users')
def index():
    return render_template('/users/index.html', users=User.query.all())

@app.route('/users/new', methods=['GET', 'POST'])
def new():
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        db.session.add(User(request.form['username'], request.form['email'], request.form['first_name'], request.form['last_name']))
        db.session.commit()
        flash("Thanks for signing up!")
        return redirect(url_for('index'))
    return render_template('/users/new.html', form=form)

@app.route('/users/<int:id>', methods=["GET", "PATCH", "DELETE"])
def show(id):
    update_user = User.query.get(id)
    if request.method == b"PATCH":
        update_user.username = request.form['username']
        update_user.email = request.form['email']
        update_user.first_name = request.form['first_name']
        update_user.last_name = request.form['last_name']
        db.session.add(update_user)
        db.session.commit()
        flash("User info updated!")
        return redirect(url_for('index'))
    
    if request.method == b"DELETE":
        db.session.delete(update_user)
        db.session.commit()
        flash("User deleted!")
        return redirect(url_for('index'))
    
    user = User.query.filter_by(id=id).first_or_404()
    return render_template('/users/show.html', user=user)

@app.route('/users/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        db.session.add(User(request.form['username'], request.form['email'], request.form['first_name'], request.form['last_name']))
        db.session.commit()
        flash("Edited user!")
        return redirect(url_for('index'))
    return render_template('/users/edit.html', id=id, form=form)



class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.VARCHAR(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, text, user_id):
        self.text = text
        self.user_id = user_id
    
    def __repr__(self):
        return "{} wrote text: {}, user_id: {}".format(self.users.username, self.text, self.user_id)

@app.route('/users/<int:id>/messages')
def m_index(id):
    check_user = User.query.filter_by(id=id).first_or_404()
    return render_template('/messages/index.html', id=check_user.id, messages=check_user.messages)

@app.route('/users/<int:id>/messages/new', methods=["GET", "POST"])
def m_new(id):
    check_user = User.query.filter_by(id=id).first_or_404()
    mform = MessageForm(request.form)
    if request.method == 'POST' and mform.validate():
        db.session.add(Message(request.form['text'], request.form['user_id']))
        db.session.commit()
        flash("New message posted!")
        return redirect(url_for('m_index', id=check_user.id, messages=check_user.messages))
    return render_template('/messages/new.html', id=check_user.id, form=mform)

@app.route('/users/<int:id>/messages/<int:mid>', methods=["GET", "PATCH", "DELETE"])
def m_show(id, mid):
    check_user = User.query.filter_by(id=id).first_or_404()
    check_message = Message.query.filter_by(id=mid).first_or_404()
    if request.method == b"PATCH":
        check_message.text = request.form['text']
        check_message.user_id = request.form['user_id']
        db.session.add(check_message)
        db.session.commit()
        flash("Message edited!")
        return redirect(url_for('m_index', id=check_user.id))
    
    if request.method == b"DELETE":
        db.session.delete(check_message)
        db.session.commit()
        flash("Message deleted!")
        return redirect(url_for('m_index', id=check_user.id))

    return render_template('/messages/show.html', id=check_user.id, message=check_message)

@app.route('/users/<int:id>/messages/<int:mid>/edit', methods=['GET', 'POST'])
def m_edit(id, mid):
    check_user = User.query.filter_by(id=id).first_or_404()
    check_message = Message.query.filter_by(id=mid).first_or_404()
    
    mform = MessageForm(request.form)
    if request.method == 'POST' and mform.validate():
        db.session.add(Message(request.form['text'], request.form['user_id']))
        db.session.commit()
        flash("Edited message!")
        return redirect(url_for('m_index'))
    return render_template('/messages/edit.html', id=check_user.id, message=check_message, form=mform)

if __name__ == '__main__':
    app.run(port=3000, debug=True)