import React, { useState, useEffect } from "react";
import "./App.css";
import TodoList from "./components/ToDoList";
import AddToDo from "./components/AddToDo";
import { getTodos, createTodo, updateTodo, deleteTodo } from "./services/api";

function App() {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch todos when component mounts
  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      setLoading(true);
      const data = await getTodos();
      setTodos(data);
      setError(null);
    } catch (err) {
      setError("Failed to fetch todos");
      console.error("Error fetching todos:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddTodo = async (text) => {
    try {
      const newTodo = await createTodo(text);
      setTodos([...todos, newTodo]);
      setError(null);
    } catch (err) {
      setError("Failed to add todo");
      console.error("Error adding todo:", err);
    }
  };

  const handleToggleTodo = async (id) => {
    try {
      const todo = todos.find((t) => t.id === id);
      const updatedTodo = await updateTodo(id, { completed: !todo.completed });
      setTodos(todos.map((t) => (t.id === id ? updatedTodo : t)));
      setError(null);
    } catch (err) {
      setError("Failed to update todo");
      console.error("Error updating todo:", err);
    }
  };

  const handleDeleteTodo = async (id) => {
    try {
      await deleteTodo(id);
      setTodos(todos.filter((t) => t.id !== id));
      setError(null);
    } catch (err) {
      setError("Failed to delete todo");
      console.error("Error deleting todo:", err);
    }
  };

  const handleEditTodo = async (id, newText) => {
    try {
      const updatedTodo = await updateTodo(id, { text: newText });
      setTodos(todos.map((t) => (t.id === id ? updatedTodo : t)));
      setError(null);
    } catch (err) {
      setError("Failed to update todo");
      console.error("Error updating todo:", err);
    }
  };

  if (loading) {
    return (
      <div className="app">
        <div className="loading">Loading...</div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>My Todo App</h1>
        <p>A simple todo app built with React & Flask</p>
      </header>

      {error && <div className="error">{error}</div>}

      <main className="app-main">
        <AddToDo onAddTodo={handleAddTodo} />
        <TodoList
          todos={todos}
          onToggleTodo={handleToggleTodo}
          onDeleteTodo={handleDeleteTodo}
          onEditTodo={handleEditTodo}
        />
      </main>
    </div>
  );
}

export default App;
