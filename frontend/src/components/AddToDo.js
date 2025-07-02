import React, { useState } from "react";

const AddTodo = ({ onAddTodo }) => {
  const [text, setText] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!text.trim()) return;

    setIsSubmitting(true);
    try {
      await onAddTodo(text.trim());
      setText("");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="add-todo">
      <form onSubmit={handleSubmit} className="add-todo-form">
        <input
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Add a new todo..."
          className="add-todo-input"
          disabled={isSubmitting}
        />
        <button
          type="submit"
          className="add-todo-button"
          disabled={isSubmitting || !text.trim()}
        >
          {isSubmitting ? "Adding..." : "Add Todo"}
        </button>
      </form>
    </div>
  );
};

export default AddTodo;
