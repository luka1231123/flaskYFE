from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stats.db'
db=SQLAlchemy(app)


class stat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    filename = db.Column(db.String(500), nullable=False)
    content = db.Column(db.String(100000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    is_yt = db.Column(db.Boolean, nullable=False)
    def __repr__(self):
        return '<Content %r>' % self.id

@app.route("/")
def index():
    stats = stat.query.order_by(stat.date_created).filter_by(is_yt=False).all()
    entries_length = len(stats)
    return render_template('index.html.j2', stats=stats, entries_length=entries_length)




@app.route("/interviews")
def interviews():
    stats = stat.query.order_by(stat.date_created).filter_by(is_yt=True).all()
    entries_length = len(stats)
    return render_template('interviews.html.j2', stats=stats, entries_length=entries_length)

@app.route("/admin", methods=['POST', 'GET'])
def admin():
    if request.method=='POST':
        checkbox = request.form.get('checkbox')
        is_yt2 = bool(checkbox == 'on')
        password = request.form.get('password')
        filename = request.form.get('filename')
        title = request.form.get('title')
        body = request.form.get('body-text')

        if password is None or password != "n378asD":
            return "<a href='/admin'>Incorrect password</a>"
        
        if any(field is None for field in [filename, title, body]):
            return 'Missing required fields'

        new_stat = stat(is_yt=is_yt2, filename=filename, title=title, content=body)
        try:
            db.session.add(new_stat)
            db.session.commit()
        except Exception as e:
            return 'There was an issue with the database: {}'.format(str(e))
        
        return redirect("/")

    else:
        return render_template('admin.html.j2')

@app.route("/statia/<id>")
def statia(id):
    entry = stat.query.get(id)
    return render_template('stat.html.j2', entry=entry)


if __name__ == "__main__":
    app.run(debug=True)