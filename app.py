from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stats.db'
db=SQLAlchemy(app)

class stat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    content = db.Column(db.String(100000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Content %r>' % self.id




@app.route("/")
def index():
    stats = stat.query.order_by(stat.date_created).all()
    entries_length = len(stats)
    return render_template('index.html.j2', stats=stats, entries_length=entries_length)

@app.route("/interviews")
def interviews():
    stats = stat.query.order_by(stat.date_created).all()
    entries_length = len(stats)
    return render_template('interviews.html.j2', stats=stats, entries_length=entries_length)

@app.route("/admin", methods=['POST', 'GET'])
def admin():
    if request.method=='POST':
        password = request.form.get('password')
        title = request.form.get('title')
        body = request.form.get('body-text')
        if password=="n378asD":
            new_stat = stat()
            new_stat.content=body
            new_stat.title=title
            try:
                db.session.add(new_stat)
                db.session.commit()
            except:
                return 'There was an issue with the database'
            return redirect("/")
        else:
            return "<a href='/admin'>incorrect password </a>" 

    else:
        return render_template('admin.html.j2')

@app.route("/statia/<id>")
def statia(id):
    entry = stat.query.get(id)
    return render_template('stat.html.j2', entry=entry)


if __name__ == "__main__":
    app.run(debug=True)