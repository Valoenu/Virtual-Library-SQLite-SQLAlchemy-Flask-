from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)


# Database
class Base(DeclarativeBase):
    pass
    
app = database.config['SQLALCHEMY_DATABASE_URI'] = "sqllite:///allbooks.db"

#Extansion ~ You can name it db instead database (It will be much easier)
database = SQLAlchemy(model_class=Base)
database.init_app(app)


#Our Table

class Book(database.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rating: [float] = mapped_column(Float, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False) #String 250, Max number characters
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)

with app.app_context():
    database.create_all() # Requires application context


@append.route('/')
def home():
    results = database.session.execute(database.select(Book).order_by(Book.title))
    all = results.scallars().all() # Get elements from results 
    return render_template("index.html", library=books_library)


@app.route('/rating', methods = ["GET, POST"])
def edit():
    if request.method == "POST":
        updated_book = database.get_or_404(Book, id) # set book to update
        updated_book.rating = request.form['rating'] # Get ratings for boom
        database.session.commit() # Save changes
        redirect(url_for['home'])

    
    selected_book = database.get_or_404(Book, id)
    id_book = request.args.get('id')

    return render_template('rating.html', book=selected_book)


@app.route('/delete_page')
def delete():
    id_book = request.args.get('id')
    
    book_delete = database.get_or_404(Book, id_book) # Delete book by id

    database.session.delete(book_delete)
    database.session.commit() # Save changes
    
    return redirect(url_for ('home')) # Redirect back to home page
    


@app.route('/add', methods=["GET", "POST"])
def add(): # Use request.form to get item from .html
    if request.method == "POST":
        book_new = {
                "title": request.form["title"],
                "author": request.form["author"],
                "rating": request.form["rating"]
            }
        db.session.add(book_new)
        db.session.commit()
        
            #We are using redirect method from Flask (Redirect to homepage after form)
        return redirect(url_for('home'))

    return render_template("add.html")
    
    


if __name__ == "__main__":
    app.run(debug=True)

