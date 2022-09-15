from flask import Flask,request,render_template,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.String(), nullable=False)
    date_created = db.Column("date_created",db.DateTime, default= datetime.utcnow)

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<username %r>' % self.id

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/', methods = ["POST", "GET"])
def index():
    title = "User Data API"
    return render_template("users.html", title= title)

@app.route('/users', methods = ["POST", "GET"])
def users():
    title = "My User List"
    if request.method == "POST":
        user_name = request.form["nm"]
        new_user =  Users(username=user_name)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/users')
        except Exception as e:
            print('Failed to upload to ftp: '+ str(e))
            return "There was a problem adding the user"

    else:
        users = Users.query.order_by(Users.date_created)
        return render_template("users.html", title= title, users=users)

@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    user_to_update = Users.query.get_or_404(id)

    if request.method == "POST":
        user_to_update.username = request.form["nm"]
        try:
            db.session.commit()
            return redirect('/users')
        except:
            return "There was a problem updating user..."
    else:
        return render_template('update.html', user_to_update=user_to_update)

if __name__== "__main__":
    app.run(port=5000,debug= True)