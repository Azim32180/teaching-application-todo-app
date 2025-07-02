import React, { useState } from "react";

const TodoItem = ({ todo, onToggle, onDelete, onEdit }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editText, setEditText] = useState(todo.text);
  const [error, setError] = useState("");

  const handleToggle = () => {
    onToggle(todo.id);
  };

  const handleDelete = () => {
    onDelete(todo.id);
  };

  const handleEditClick = () => {
    setIsEditing(true);
    setEditText(todo.text);
    setError("");
  };

  const handleEditChange = (e) => {
    setEditText(e.target.value);
    setError("");
  };

  const handleEditSave = () => {
    const trimmed = editText.trim();
    if (!trimmed) {
      setError("Todo text cannot be empty.");
      return;
    }
    onEdit(todo.id, trimmed);
    setIsEditing(false);
  };

  const handleEditCancel = () => {
    setIsEditing(false);
    setEditText(todo.text);
    setError("");
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString();
  };

  return (
    <li className={`todo-item ${todo.completed ? "completed" : ""}`}>
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={handleToggle}
        className="todo-checkbox"
      />
      {isEditing ? (
        <>
          <input
            type="text"
            value={editText}
            onChange={handleEditChange}
            className="todo-edit-input"
            autoFocus
          />
          <button onClick={handleEditSave} className="todo-save">
            Save
          </button>
          <button onClick={handleEditCancel} className="todo-cancel">
            Cancel
          </button>
          {error && (
            <span
              className="todo-error"
              style={{ color: "red", marginLeft: 8 }}
            >
              {error}
            </span>
          )}
        </>
      ) : (
        <>
          <span className={`todo-text ${todo.completed ? "completed" : ""}`}>
            {todo.text}
          </span>
          <span className="todo-date">{formatDate(todo.created_at)}</span>
          <button
            onClick={handleEditClick}
            className="todo-edit"
            aria-label="Edit todo"
          >
            Edit Todo
          </button>
          <button
            onClick={handleDelete}
            className="todo-delete"
            aria-label="Delete todo"
          >
            Delete
          </button>
        </>
      )}
    </li>
  );
};

export default TodoItem;
