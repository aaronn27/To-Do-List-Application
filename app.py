from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database object
db = SQLAlchemy(app)

# Defining Todo model for the database
class Todo(db.Model):
    # Columns for sl no., title, description and date created
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Representation method for easier debugging
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Route for the homepage, handles both GET and POST requests
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        # If the request is POST, extract title and description from the form
        title = request.form['title']
        desc = request.form['desc']

        # Creating a new Todo object and add it to the database
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    #Query all items from the database and  pass them to the template
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

# Route to show all todo items (used for debugging purposes)
@app.route('/show')
def show():
    allTodo = Todo.query.all()
    print(allTodo)
    return

# Route to update an existing todo item
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        # If the request is POST, update the todo item with the new values
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    # For GET requests, retrieve the todo item and pass it to the template
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

# Route to delete a todo item
@app.route('/delete/<int:sno>')
def delete(sno):
    # Find the todo item by its serial number (sno) and delete it
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

# Run the Flask application in debug mode on port 8000
if __name__ == "__main__":
    app.run(debug=True, port=8000)