from flask import Flask,render_template,redirect,request,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db =  SQLAlchemy(app)


class Todo(db.Model):
    Sno = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(500),nullable=False)
    dateCreated = db.Column(db.DateTime,default=datetime.utcnow)
    done = db.Column(db.Boolean,default=False,nullable=False)

    def __repr__(self) -> str:
        return f"{self.title} : {self.desc}"

@app.route("/", methods=['GET','POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template("index.html",alltodo=allTodo)

@app.route('/delete/<int:Sno>')
def delete(Sno):
    todo=Todo.query.filter_by(Sno=Sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:sno>')
def update(sno):
    todo = Todo.query.filter_by(Sno=sno).first()
    todo.done = True
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)