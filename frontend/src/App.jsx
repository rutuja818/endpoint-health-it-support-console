import React, { useState, useEffect, useMemo } from "react";
import { api } from "./api";

const nav = ["Dashboard", "Endpoints", "Tickets", "Troubleshooting", "Reports"];

function Badge({ value }) {
  return (
    <span className={`badge ${String(value).toLowerCase().replaceAll(" ", "-")}`}>
      {value}
    </span>
  );
}

function Layout({ page, setPage, children }) {
  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">EH</div>
          <div>
            <strong>Endpoint Health</strong>
            <small>IT Support Console</small>
          </div>
        </div>

        <nav>
          {nav.map(item => (
            <button
              key={item}
              className={page === item ? "nav-item active" : "nav-item"}
              onClick={() => setPage(item)}
            >
              {item}
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          <span className="status-dot" />
          Local monitoring
        </div>
      </aside>

      <main className="main">
        <header className="topbar">
          <div>
            <h1>{page}</h1>
            <p>Endpoint monitoring and IT support operations</p>
          </div>

          <div className="user-chip">
            <div className="avatar">IT</div>
            <span>IT Technician</span>
          </div>
        </header>

        {children}
      </main>
    </div>
  );
}

function Dashboard({ setPage }) {
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api.summary()
      .then(setSummary)
      .catch(e => setError(e.message));
  }, []);

  if (error) {
    return (
      <div className="error-box">
        {error}
        <br />
        <small>Start the FastAPI backend and database.</small>
      </div>
    );
  }

  if (!summary) {
    return <div className="loading">Loading dashboard...</div>;
  }

  const cards = [
    ["Total Endpoints", summary.total_endpoints, "devices"],
    ["Healthy", summary.healthy, "healthy"],
    ["Warning", summary.warning, "warning"],
    ["Critical", summary.critical, "critical"],
    ["Open Tickets", summary.open_tickets, "tickets"],
    ["High Priority", summary.high_priority, "priority"]
  ];

  return (
    <>
      <section className="cards">
        {cards.map(([title, value, cls]) => (
          <div className="metric" key={title}>
            <span>{title}</span>
            <strong className={cls}>{value}</strong>
          </div>
        ))}
      </section>

      <section className="grid two">
        <div className="panel">
          <div className="panel-head">
            <div>
              <h2>Endpoint Health</h2>
              <p>Current device status distribution</p>
            </div>

            <button
              className="link-button"
              onClick={() => setPage("Endpoints")}
            >
              View all
            </button>
          </div>

          <div className="health-bars">
            <Bar
              label="Healthy"
              value={summary.healthy}
              total={summary.total_endpoints}
            />

            <Bar
              label="Warning"
              value={summary.warning}
              total={summary.total_endpoints}
            />

            <Bar
              label="Critical"
              value={summary.critical}
              total={summary.total_endpoints}
            />

            <Bar
              label="Offline"
              value={summary.offline}
              total={summary.total_endpoints}
            />
          </div>
        </div>

        <div className="panel">
          <div className="panel-head">
            <div>
              <h2>Support Operations</h2>
              <p>Current incident workload</p>
            </div>

            <button
              className="link-button"
              onClick={() => setPage("Tickets")}
            >
              Tickets
            </button>
          </div>

          <div className="operation-list">
            <div>
              <span>All tickets</span>
              <strong>{summary.tickets}</strong>
            </div>

            <div>
              <span>Open / in progress</span>
              <strong>{summary.open_tickets}</strong>
            </div>

            <div>
              <span>High / critical</span>
              <strong>{summary.high_priority}</strong>
            </div>
          </div>
        </div>
      </section>

      <section className="panel">
        <div className="panel-head">
          <div>
            <h2>Endpoint Management Workflow</h2>
            <p>
              Collection → health check → incident → troubleshooting →
              resolution
            </p>
          </div>
        </div>

        <div className="workflow">
          {[
            "Endpoint Agent",
            "Health Monitoring",
            "IT Incident",
            "Troubleshooting",
            "Resolution"
          ].map((x, i) => (
            <div className="workflow-step" key={x}>
              <b>{i + 1}</b>
              <span>{x}</span>
            </div>
          ))}
        </div>
      </section>
    </>
  );
}

function Bar({ label, value, total }) {
  const width = total ? Math.round((value / total) * 100) : 0;

  return (
    <div className="bar-row">
      <div className="bar-label">
        <span>{label}</span>
        <strong>{value}</strong>
      </div>

      <div className="bar-track">
        <div
          className={`bar-fill ${label.toLowerCase()}`}
          style={{ width: `${width}%` }}
        />
      </div>
    </div>
  );
}

function Endpoints() {
  const [data, setData] = useState([]);
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState("All");
  const [selected, setSelected] = useState(null);
  const [health, setHealth] = useState([]);

  const [checking, setChecking] = useState(false);
  const [checkMessage, setCheckMessage] = useState("");
  const [checkError, setCheckError] = useState("");

  useEffect(() => {
    api.endpoints()
      .then(setData)
      .catch(console.error);
  }, []);

  async function openEndpoint(endpoint) {
    setSelected(endpoint);
    setCheckMessage("");
    setCheckError("");

    try {
      setHealth(await api.health(endpoint.id));
    } catch {
      setHealth([]);
    }
  }

  async function runHealthCheck() {
    if (!selected) return;

    setChecking(true);
    setCheckMessage("");
    setCheckError("");

    try {
      await api.runHealthCheck(selected.id);

      const updatedEndpoints = await api.endpoints();
      setData(updatedEndpoints);

      const updatedEndpoint = updatedEndpoints.find(
        endpoint => endpoint.id === selected.id
      );

      if (updatedEndpoint) {
        setSelected(updatedEndpoint);
      }

      const updatedHealth = await api.health(selected.id);
      setHealth(updatedHealth);

      setCheckMessage("Health check completed successfully.");
    } catch (error) {
      console.error(error);
      setCheckError(error.message || "Health check failed.");
    } finally {
      setChecking(false);
    }
  }

  const filtered = useMemo(
    () =>
      data.filter(e => {
        const matchesText = e.hostname
          .toLowerCase()
          .includes(query.toLowerCase());

        const matchesStatus =
          status === "All" || e.status === status.toLowerCase();

        return matchesText && matchesStatus;
      }),
    [data, query, status]
  );

  return (
    <>
      <div className="toolbar">
        <input
          placeholder="Search hostname..."
          value={query}
          onChange={e => setQuery(e.target.value)}
        />

        <select
          value={status}
          onChange={e => setStatus(e.target.value)}
        >
          <option>All</option>
          <option>Healthy</option>
          <option>Warning</option>
          <option>Critical</option>
          <option>Offline</option>
        </select>
      </div>

      <div className="panel">
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Hostname</th>
                <th>OS</th>
                <th>IP</th>
                <th>CPU</th>
                <th>Memory</th>
                <th>Disk</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>
              {filtered.map(e => (
                <tr
                  key={e.id}
                  onClick={() => openEndpoint(e)}
                  className="clickable"
                >
                  <td>
                    <strong>{e.hostname}</strong>
                  </td>

                  <td>{e.os}</td>
                  <td>{e.ip_address}</td>
                  <td>{e.cpu_usage}%</td>
                  <td>{e.memory_usage}%</td>
                  <td>{e.disk_usage}%</td>

                  <td>
                    <Badge value={e.status} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {selected && (
        <div
          className="modal-backdrop"
          onClick={() => setSelected(null)}
        >
          <div
            className="modal"
            onClick={e => e.stopPropagation()}
          >
            <div className="modal-head">
              <div>
                <h2>{selected.hostname}</h2>
                <p>
                  {selected.os} · {selected.os_version}
                </p>
              </div>

              <button
                className="icon-button"
                onClick={() => setSelected(null)}
              >
                ×
              </button>
            </div>

            <div className="detail-grid">
              <Info
                label="CPU"
                value={`${selected.cpu_usage}%`}
              />

              <Info
                label="Memory"
                value={`${selected.memory_usage}%`}
              />

              <Info
                label="Disk"
                value={`${selected.disk_usage}%`}
              />

              <Info
                label="IP Address"
                value={selected.ip_address}
              />

              <Info
                label="Architecture"
                value={selected.architecture}
              />

              <Info
                label="Processor"
                value={selected.processor}
              />
            </div>

            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "12px",
                marginTop: "20px",
                marginBottom: "18px"
              }}
            >
              <button
                className="primary"
                onClick={runHealthCheck}
                disabled={checking}
              >
                {checking ? "Running..." : "Run Health Check"}
              </button>

              {checkMessage && (
                <span className="muted">
                  {checkMessage}
                </span>
              )}

              {checkError && (
                <span className="error-text">
                  {checkError}
                </span>
              )}
            </div>

            <h3>Recent Health Checks</h3>

            <div className="mini-list">
              {health.slice(0, 5).map(h => (
                <div key={h.id}>
                  <span>
                    {new Date(h.checked_at).toLocaleString()}
                  </span>

                  <Badge value={h.overall_status} />
                </div>
              ))}

              {!health.length && (
                <span className="muted">
                  No health checks recorded.
                </span>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
}

function Info({ label, value }) {
  return (
    <div className="info">
      <span>{label}</span>
      <strong>{value ?? "—"}</strong>
    </div>
  );
}

function Tickets() {
  const [tickets, setTickets] = useState([]);
  const [endpoints, setEndpoints] = useState([]);
  const [showForm, setShowForm] = useState(false);

  const [form, setForm] = useState({
    title: "",
    description: "",
    category: "Network",
    priority: "Medium",
    endpoint_id: ""
  });

  async function load() {
    const [t, e] = await Promise.all([
      api.tickets(),
      api.endpoints()
    ]);

    setTickets(t);
    setEndpoints(e);
  }

  useEffect(() => {
    load().catch(console.error);
  }, []);

  async function submit(e) {
    e.preventDefault();

    await api.createTicket({
      ...form,
      endpoint_id: form.endpoint_id
        ? Number(form.endpoint_id)
        : null
    });

    setForm({
      title: "",
      description: "",
      category: "Network",
      priority: "Medium",
      endpoint_id: ""
    });

    setShowForm(false);
    load();
  }

  async function resolve(id) {
    await api.updateTicket(id, {
      status: "Resolved"
    });

    load();
  }

  return (
    <>
      <div className="toolbar">
        <button
          className="primary"
          onClick={() => setShowForm(true)}
        >
          + New Ticket
        </button>
      </div>

      {showForm && (
        <div className="panel form-panel">
          <h2>Create support ticket</h2>

          <form onSubmit={submit}>
            <div className="form-grid">
              <label>
                Issue title
                <input
                  required
                  value={form.title}
                  onChange={e =>
                    setForm({
                      ...form,
                      title: e.target.value
                    })
                  }
                />
              </label>

              <label>
                Endpoint
                <select
                  value={form.endpoint_id}
                  onChange={e =>
                    setForm({
                      ...form,
                      endpoint_id: e.target.value
                    })
                  }
                >
                  <option value="">Unassigned</option>

                  {endpoints.map(x => (
                    <option key={x.id} value={x.id}>
                      {x.hostname}
                    </option>
                  ))}
                </select>
              </label>

              <label>
                Category
                <select
                  value={form.category}
                  onChange={e =>
                    setForm({
                      ...form,
                      category: e.target.value
                    })
                  }
                >
                  {[
                    "Network",
                    "Hardware",
                    "Software",
                    "Operating System",
                    "Application",
                    "Security",
                    "Performance",
                    "Other"
                  ].map(x => (
                    <option key={x}>{x}</option>
                  ))}
                </select>
              </label>

              <label>
                Priority
                <select
                  value={form.priority}
                  onChange={e =>
                    setForm({
                      ...form,
                      priority: e.target.value
                    })
                  }
                >
                  {[
                    "Low",
                    "Medium",
                    "High",
                    "Critical"
                  ].map(x => (
                    <option key={x}>{x}</option>
                  ))}
                </select>
              </label>
            </div>

            <label>
              Description
              <textarea
                required
                value={form.description}
                onChange={e =>
                  setForm({
                    ...form,
                    description: e.target.value
                  })
                }
              />
            </label>

            <div className="form-actions">
              <button
                type="button"
                className="secondary"
                onClick={() => setShowForm(false)}
              >
                Cancel
              </button>

              <button className="primary">
                Create Ticket
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="panel">
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Ticket</th>
                <th>Issue</th>
                <th>Category</th>
                <th>Priority</th>
                <th>Status</th>
                <th>Created</th>
                <th></th>
              </tr>
            </thead>

            <tbody>
              {tickets.map(t => (
                <tr key={t.id}>
                  <td>
                    <strong>{t.ticket_number}</strong>
                  </td>

                  <td>{t.title}</td>
                  <td>{t.category}</td>

                  <td>
                    <Badge value={t.priority} />
                  </td>

                  <td>
                    <Badge value={t.status} />
                  </td>

                  <td>
                    {new Date(
                      t.created_at
                    ).toLocaleDateString()}
                  </td>

                  <td>
                    {!["Resolved", "Closed"].includes(t.status) && (
                      <button
                        className="small-button"
                        onClick={() => resolve(t.id)}
                      >
                        Resolve
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}

function Troubleshooting() {
  const workflows = [
    [
      "Internet not working",
      [
        "Check IP configuration",
        "Check gateway connectivity",
        "Test DNS resolution",
        "Test external connectivity"
      ]
    ],

    [
      "Low disk space",
      [
        "Review disk usage",
        "Identify large files",
        "Remove approved temporary data",
        "Recheck free space"
      ]
    ],

    [
      "High CPU usage",
      [
        "Identify top processes",
        "Check application behavior",
        "Review recent changes",
        "Document resolution"
      ]
    ],

    [
      "Application not responding",
      [
        "Check process state",
        "Review application logs",
        "Restart only if appropriate",
        "Record result"
      ]
    ]
  ];

  return (
    <div className="grid two">
      {workflows.map(([title, steps]) => (
        <div className="panel" key={title}>
          <h2>{title}</h2>

          <ol className="steps">
            {steps.map(s => (
              <li key={s}>{s}</li>
            ))}
          </ol>
        </div>
      ))}

      <div className="panel wide">
        <h2>Endpoint Compliance Simulation</h2>

        <p className="muted">
          This is a project simulation, not a real MDM control plane.
        </p>

        <div className="compliance">
          <Info
            label="OS Update"
            value="Update Required"
          />

          <Info
            label="Firewall"
            value="Enabled"
          />

          <Info
            label="Encryption"
            value="Unknown"
          />

          <Info
            label="Password Policy"
            value="Compliant"
          />
        </div>
      </div>
    </div>
  );
}

function Reports() {
  const [data, setData] = useState(null);

  useEffect(() => {
    api.reports()
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) {
    return <div className="loading">Loading reports...</div>;
  }

  return (
    <div className="grid two">
      <div className="panel">
        <h2>Operating System Distribution</h2>

        {Object.entries(data.os_distribution).map(([k, v]) => (
          <Bar
            key={k}
            label={k}
            value={v}
            total={Object.values(
              data.os_distribution
            ).reduce((a, b) => a + b, 0)}
          />
        ))}
      </div>

      <div className="panel">
        <h2>Ticket Status</h2>

        {Object.entries(data.ticket_status).map(([k, v]) => (
          <Bar
            key={k}
            label={k}
            value={v}
            total={Object.values(
              data.ticket_status
            ).reduce((a, b) => a + b, 0)}
          />
        ))}
      </div>
    </div>
  );
}

export default function App() {
  const [page, setPage] = useState("Dashboard");

  return (
    <Layout page={page} setPage={setPage}>
      {page === "Dashboard" && (
        <Dashboard setPage={setPage} />
      )}

      {page === "Endpoints" && <Endpoints />}

      {page === "Tickets" && <Tickets />}

      {page === "Troubleshooting" && (
        <Troubleshooting />
      )}

      {page === "Reports" && <Reports />}
    </Layout>
  );
}