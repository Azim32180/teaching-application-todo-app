const API_BASE_URL = "http://localhost:5050/api";

// Helper function to handle API responses
const handleResponse = async (response) => {
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.message || `HTTP error! status: ${response.status}`);
  }

  // Handle empty responses (like DELETE)
  if (response.status === 204) {
    return null;
  }

  return response.json();
};

export const getTodos = async () => {
  const response = await fetch(`${API_BASE_URL}/todos`);
  return handleResponse(response);
};

export const createTodo = async (text) => {
  const response = await fetch(`${API_BASE_URL}/todos`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  });
  return handleResponse(response);
};

export const updateTodo = async (id, updates) => {
  const response = await fetch(`${API_BASE_URL}/todos/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(updates),
  });
  return handleResponse(response);
};

export const deleteTodo = async (id) => {
  const response = await fetch(`${API_BASE_URL}/todos/${id}`, {
    method: "DELETE",
  });
  return handleResponse(response);
};

export const getTodoStats = async () => {
  const response = await fetch(`${API_BASE_URL}/todos/stats`);
  return handleResponse(response);
};

export const getTodo = async (id) => {
  const response = await fetch(`${API_BASE_URL}/todos/${id}`);
  return handleResponse(response);
};
