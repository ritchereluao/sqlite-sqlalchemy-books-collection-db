from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Book Title: {self.title}"


db.create_all()


@app.route('/')
def home():
    # books = db.session.query(Books).all()
    books = Books.query.all()
    return render_template("index.html", all_books=books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["book_name"]
        author = request.form["book_author"]
        rating = request.form["book_rating"]

        new_book = Books(title=title, author=author, rating=rating)
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template("add.html")


@app.route("/edit/<int:book_id>", methods=["GET", "POST"])
def edit(book_id):
    book_info = Books.query.filter_by(id=book_id).first()

    if request.method == "POST":
        book_to_update = Books.query.filter_by(id=book_id).first()
        book_to_update.rating = request.form["new_rating"]
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("edit_rating.html", book_info=book_info)


@app.route("/del")
def delete():
    book_id = request.args.get("id")

    book_to_delete = Books.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
