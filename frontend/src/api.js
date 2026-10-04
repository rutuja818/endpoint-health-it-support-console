const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8001";

async function request(path, options = {}) {
  const response = await fetch(`${API}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {})
    },
    ...options
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed: ${response.status}`);
  }

  return response.json();
}

export const api = {
  summary: () => request("/api/dashboard/summary"),

  reports: () => request("/api/dashboard/reports"),

  endpoints: () => request("/api/endpoints"),

  endpoint: (id) => request(`/api/endpoints/${id}`),

  health: (id) => request(`/api/health/endpoint/${id}`),

  runHealthCheck: (id) =>
    request(`/api/health/endpoint/${id}/check`, {
      method: "POST"
    }),

  tickets: () => request("/api/tickets"),

  createTicket: (data) =>
    request("/api/tickets", {
      method: "POST",
      body: JSON.stringify(data)
    }),

  updateTicket: (id, data) =>
    request(`/api/tickets/${id}`, {
      method: "PUT",
      body: JSON.stringify(data)
    })
};