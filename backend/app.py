# importing flask which helps us create a simple web server. 
# request lets us read data sent from the frontend. 
# jsonify helps us convert our data into a JSON format that the frontend can understand. 
from flask import Flask, request, jsonify
# flask_cors allows us to handle cross-origin requests, which is important for our frontend to access our API. 
from flask_cors import CORS
# flask_sqlalchemy helps us interact with our SQLite database. 
from flask_sqlalchemy import SQLAlchemy
# datetime helps us manage dates and times. 
from datetime import datetime
# os helps us work with the operating system, like finding the path to our database file. 
import os

# creating a Flask app. 
app = Flask(__name__)
# enabling CORS for React frontend. 
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])


# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "todos.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Todo Model
class Todo(db.Model):
    # Todo model for SQLAlchemy
    __tablename__ = 'todos'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        # Convert Todo object to dictionary for JSON serialization
        # We need to convert the object to a dictionary first - then Flask can use jsonify() to send it as JSON
        return {
            'id': self.id,
            'text': self.text,
            'completed': self.completed,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    # This is a built-in python method that helps us print the object in a readable format. 
    def __repr__(self):
        return f'<Todo {self.id}: {self.text[:50]}{"..." if len(self.text) > 50 else ""}>'

# Create database tables
with app.app_context():
    db.create_all()

# This endpoint returns all todos. 
@app.route('/api/todos', methods=['GET', 'OPTIONS'])
def get_todos():
    # Get all todos, optionally filtered by completion status
    try:
        # Optional query parameter to filter by completion status
        completed = request.args.get('completed')
        # If the completed query parameter is provided, we filter the todos by completion status. 
        if completed is not None:
            # Convert string to boolean
            is_completed = completed.lower() in ['true', '1', 'yes']
            # We filter the todos by completion status and order them by creation date in descending order. 
            todos = Todo.query.filter_by(completed=is_completed).order_by(Todo.created_at.desc()).all()
        else:
            # If no completion status is provided, we return all todos ordered by creation date in descending order. 
            todos = Todo.query.order_by(Todo.created_at.desc()).all()
        
        # Converts each todo to a dictionary and sends them back as JSON.
        return jsonify([todo.to_dict() for todo in todos])
    
    # If there is an error, we return a 500 error and a message. 
    except Exception as e:
        return jsonify({'error': 'Failed to fetch todos'}), 500

@app.route('/api/todos', methods=['POST', 'OPTIONS'])
def create_todo():
    # Create a new todo
    try:
        # Grabs the JSON data sent from the frontend. 
        data = request.get_json()

        # Checks that the  data exists and includes a text field (the todo task itself)
        if not data or 'text' not in data:
            return jsonify({'error': 'Todo text is required'}), 400
        
        # Rmoves any whitespace from the text field. 
        text = data['text'].strip()
        if not text:
            return jsonify({'error': 'Todo text cannot be empty'}), 400
        
        if len(text) > 500:
            return jsonify({'error': 'Todo text must be 500 characters or less'}), 400
        
        new_todo = Todo(text=text)
        db.session.add(new_todo)
        db.session.commit()
        
        # Converts the new todo to a dictionary and sends it back as JSON. 
        return jsonify(new_todo.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create todo'}), 500

# This endpoint returns a specific todo by ID. 
@app.route('/api/todos/<int:todo_id>', methods=['GET', 'OPTIONS'])
def get_todo(todo_id):
    # Get a specific todo by ID
    try:
        # Looks it up in the db, if it's not found, it returns a 404 error. 
        todo = Todo.query.get_or_404(todo_id)
        return jsonify(todo.to_dict())
    
    except Exception as e:
        return jsonify({'error': 'Todo not found'}), 404

@app.route('/api/todos/<int:todo_id>', methods=['PUT', 'OPTIONS'])
def update_todo(todo_id):
    # Update a todo (completion status or text) 
    try:
        todo = Todo.query.get_or_404(todo_id)
        data = request.get_json()
        # Checks that the data exists and is not empty. 
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update completion status
        if 'completed' in data:
            todo.completed = bool(data['completed'])
        
        # Update text if provided
        if 'text' in data:
            text = data['text'].strip()
            if not text:
                return jsonify({'error': 'Todo text cannot be empty'}), 400
            if len(text) > 500:
                return jsonify({'error': 'Todo text must be 500 characters or less'}), 400
            todo.text = text
        # Updates the last modified time and saves it to the db. 
        todo.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(todo.to_dict())
    
    except Exception as e:
        db.session.rollback()
        if 'not found' in str(e).lower():
            return jsonify({'error': 'Todo not found'}), 404
        return jsonify({'error': 'Failed to update todo'}), 500

# This endpoint deletes a todo by ID. 
@app.route('/api/todos/<int:todo_id>', methods=['DELETE', 'OPTIONS'])
def delete_todo(todo_id):
    # Delete a todo
    # Finds it, deletes it, and saves the changes to the db. 
    try:
        todo = Todo.query.get_or_404(todo_id)
        db.session.delete(todo)
        db.session.commit()
        
        return '', 204
    
    except Exception as e:
        db.session.rollback()
        if 'not found' in str(e).lower():
            return jsonify({'error': 'Todo not found'}), 404
        return jsonify({'error': 'Failed to delete todo'}), 500

@app.route('/api/todos/stats', methods=['GET', 'OPTIONS'])
def get_todo_stats():
    # Get statistics about todos
    try:
        total = Todo.query.count()
        completed = Todo.query.filter_by(completed=True).count()
        pending = total - completed
        
        return jsonify({
            'total': total,
            'completed': completed,
            'pending': pending,
            # Calculates the completion rate as a percentage. 
            'completion_rate': round((completed / total * 100) if total > 0 else 0, 1)
        })
    
    except Exception as e:
        return jsonify({'error': 'Failed to fetch stats'}), 500

# Used to if the server and db are working. 
# Useful for monitoring tools and debugging. 
@app.route('/api/health', methods=['GET', 'OPTIONS'])
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        db.session.execute(db.text('SELECT 1'))
        return jsonify({
            'status': 'healthy', 
            'message': 'Todo API is running',
            'database': 'connected'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'message': 'Database connection failed',
            'error': str(e)
        }), 500

# Error handlers
# If a route doesn't exist or a todo isn't found, return a 404 JSON error.
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404
# If something breaks inside the server, this catches the error, rolls back any DB changes, and returns a clean 500 error.
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

#Runs the app on port 5050 with debugging turned on (so you can see error messages while you code).
if __name__ == '__main__':
    app.run(debug=True, port=5050)