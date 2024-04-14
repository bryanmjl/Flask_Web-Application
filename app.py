'''Flask Web Application Business Logic'''

# Import Libraries
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from waitress import serve


# Flask and DB configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(300), nullable = False)                
    completed = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)    

    def __repr__(self):
        return '<Task %r>' % self.id


# Create DB before processing any other requests
@app.before_first_request
def create_tables():
    db.create_all()


# App with POST and GET methods
@app.route('/', methods = ['POST', 'GET']) 
def index():
    '''
    This is a app decorator for API with methods POST and GET
    :POST method: When user post a task to the website - Flask API posts to Database new content
    :GET method: Query Database and Return a web template
    '''

    # Request = POST
    if request.method == 'POST':
        task_content = request.form['content']  # From index.html under <input> tag
        new_task = Todo(content = task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue with adding task'

    # Request = GET       
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks= tasks)  # Add tasks = tasks so that this can appear on Webpage


# App with DELETE methods
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


# App with UPDATE methods
@app.route('/update/<int:id>', methods = ["GET", "POST"])
def update(id):

    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try: 
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task = task)


# Run Flask on WSGI Server (Waitress)
if __name__ == '__main__':
    serve(app, host='0.0.0.0', port= 8000)
