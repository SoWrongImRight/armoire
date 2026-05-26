import React, { useState, useEffect, useCallback, useRef } from "react";

const CATEGORIES = ["top", "bottom", "outerwear", "shoes", "accessory"];
const SEASONS = ["spring", "summer", "fall", "winter", "all"];

const EMPTY_FORM = {
  name: "",
  category: "top",
  brand: "",
  season: "all",
  fit: "",
  size: "",
  color: "",
};

const Wardrobe = () => {
  const [items, setItems] = useState([]);
  const [summary, setSummary] = useState(null);
  const [form, setForm] = useState(EMPTY_FORM);
  const [file, setFile] = useState(null);
  const [filter, setFilter] = useState("");
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  const load = useCallback(async () => {
    try {
      const qs = filter ? `?category=${encodeURIComponent(filter)}` : "";
      const [itemsRes, summaryRes] = await Promise.all([
        fetch(`/api/items${qs}`),
        fetch("/api/items/summary"),
      ]);
      if (!itemsRes.ok) throw new Error(`Could not load items (${itemsRes.status})`);
      setItems(await itemsRes.json());
      if (summaryRes.ok) setSummary(await summaryRes.json());
    } catch (err) {
      setStatus(err.message);
    }
  }, [filter]);

  useEffect(() => {
    load();
  }, [load]);

  // Live updates: refresh when any client changes the wardrobe.
  const loadRef = useRef(load);
  useEffect(() => {
    loadRef.current = load;
  }, [load]);
  useEffect(() => {
    const proto = window.location.protocol === "https:" ? "wss" : "ws";
    const ws = new WebSocket(`${proto}://${window.location.host}/ws`);
    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        if (msg.type === "items_changed") loadRef.current();
      } catch (err) {
        /* ignore malformed messages */
      }
    };
    return () => ws.close();
  }, []);

  const onField = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const uploadImage = async () => {
    if (!file) return null;
    const data = new FormData();
    data.append("file", file);
    const res = await fetch("/api/images", { method: "POST", body: data });
    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      throw new Error(body.detail || `Image upload failed (${res.status})`);
    }
    return (await res.json()).key;
  };

  const addItem = async (e) => {
    e.preventDefault();
    if (!form.name.trim()) {
      setStatus("Name is required.");
      return;
    }
    setLoading(true);
    setStatus("Saving...");
    try {
      const imageKey = await uploadImage();
      const payload = { ...form };
      Object.keys(payload).forEach((k) => {
        if (payload[k] === "") delete payload[k];
      });
      if (imageKey) payload.image_key = imageKey;

      const res = await fetch("/api/items", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.detail || `Save failed (${res.status})`);
      }
      setStatus("Saved.");
      setForm(EMPTY_FORM);
      setFile(null);
      e.target.reset();
      await load();
    } catch (err) {
      setStatus(err.message);
    } finally {
      setLoading(false);
    }
  };

  const removeItem = async (id) => {
    try {
      const res = await fetch(`/api/items/${id}`, { method: "DELETE" });
      if (!res.ok && res.status !== 204) throw new Error(`Delete failed (${res.status})`);
      await load();
    } catch (err) {
      setStatus(err.message);
    }
  };

  return (
    <div className="wardrobe">
      <h1>Wardrobe</h1>

      {summary && (
        <p>
          <strong>{summary.total}</strong> items
          {Object.entries(summary.by_category).length > 0 && " — "}
          {Object.entries(summary.by_category)
            .map(([cat, n]) => `${cat}: ${n}`)
            .join(", ")}
        </p>
      )}

      <form onSubmit={addItem} style={{ display: "grid", gap: "6px", maxWidth: "420px" }}>
        <input name="name" placeholder="Name *" value={form.name} onChange={onField} />
        <select name="category" value={form.category} onChange={onField}>
          {CATEGORIES.map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
        <input name="brand" placeholder="Brand" value={form.brand} onChange={onField} />
        <select name="season" value={form.season} onChange={onField}>
          {SEASONS.map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
        <input name="fit" placeholder="Fit" value={form.fit} onChange={onField} />
        <input name="size" placeholder="Size" value={form.size} onChange={onField} />
        <input name="color" placeholder="Color" value={form.color} onChange={onField} />
        <input type="file" accept="image/*" onChange={(e) => setFile(e.target.files[0])} />
        <button type="submit" disabled={loading}>
          {loading ? "Saving..." : "Add item"}
        </button>
      </form>

      {status && <p>{status}</p>}

      <div style={{ margin: "16px 0" }}>
        <label>
          Filter by category:{" "}
          <select value={filter} onChange={(e) => setFilter(e.target.value)}>
            <option value="">all</option>
            {CATEGORIES.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </label>
      </div>

      <div style={{ display: "flex", flexWrap: "wrap", gap: "12px" }}>
        {items.map((item) => (
          <figure
            key={item.id}
            style={{
              margin: 0,
              width: "180px",
              border: "1px solid #ddd",
              borderRadius: "8px",
              padding: "8px",
            }}
          >
            {item.image_url ? (
              <img
                src={item.image_url}
                alt={item.name}
                style={{ width: "100%", height: "160px", objectFit: "cover", borderRadius: "6px" }}
              />
            ) : (
              <div
                style={{
                  width: "100%",
                  height: "160px",
                  background: "#f2f2f2",
                  borderRadius: "6px",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  color: "#999",
                }}
              >
                no image
              </div>
            )}
            <figcaption style={{ fontSize: "13px", marginTop: "6px" }}>
              <strong>{item.name}</strong>
              <br />
              {item.category}
              {item.brand ? ` · ${item.brand}` : ""}
              {item.season ? ` · ${item.season}` : ""}
              {item.size ? ` · ${item.size}` : ""}
            </figcaption>
            <button onClick={() => removeItem(item.id)} style={{ marginTop: "6px" }}>
              Delete
            </button>
          </figure>
        ))}
      </div>

      {items.length === 0 && <p>No items yet.</p>}
    </div>
  );
};

export default Wardrobe;
