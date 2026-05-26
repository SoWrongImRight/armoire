import React, { useState } from "react";

const Stylist = () => {
  const [city, setCity] = useState("Orlando");
  const [data, setData] = useState(null);
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  const suggest = async () => {
    setLoading(true);
    setStatus("Asking the stylist...");
    setData(null);
    try {
      const res = await fetch(`/api/ai/outfit?city=${encodeURIComponent(city)}`);
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.detail || `Request failed (${res.status})`);
      }
      setData(await res.json());
      setStatus("");
    } catch (err) {
      setStatus(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="stylist">
      <h1>AI Stylist</h1>
      <p>Get an outfit suggestion from your wardrobe, powered by Claude.</p>

      <div style={{ display: "flex", gap: "8px", marginBottom: "12px" }}>
        <input value={city} onChange={(e) => setCity(e.target.value)} placeholder="City (optional)" />
        <button onClick={suggest} disabled={loading}>
          {loading ? "Thinking..." : "Suggest an outfit"}
        </button>
      </div>

      {status && <p>{status}</p>}

      {data && data.configured === false && <p>{data.message}</p>}

      {data && data.configured && (
        <div>
          {data.rationale && (
            <blockquote style={{ borderLeft: "3px solid #ccc", paddingLeft: "12px", color: "#444" }}>
              {data.rationale}
            </blockquote>
          )}
          {data.recommended.length === 0 ? (
            <p>No items were recommended. Add some items to your wardrobe first.</p>
          ) : (
            <div style={{ display: "flex", flexWrap: "wrap", gap: "12px", marginTop: "12px" }}>
              {data.recommended.map((item) => (
                <figure key={item.id} style={{ margin: 0, width: "150px" }}>
                  {item.image_url ? (
                    <img
                      src={item.image_url}
                      alt={item.name}
                      style={{ width: "150px", height: "150px", objectFit: "cover", borderRadius: "6px" }}
                    />
                  ) : (
                    <div
                      style={{
                        width: "150px",
                        height: "150px",
                        background: "#f2f2f2",
                        borderRadius: "6px",
                      }}
                    />
                  )}
                  <figcaption style={{ fontSize: "13px" }}>
                    {item.name} ({item.category})
                  </figcaption>
                </figure>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Stylist;
