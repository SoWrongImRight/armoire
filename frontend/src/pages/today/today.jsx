import React, { useState, useEffect, useCallback } from "react";

const Today = () => {
  const [city, setCity] = useState("Orlando");
  const [data, setData] = useState(null);
  const [status, setStatus] = useState("");

  const load = useCallback(async (c) => {
    setStatus("Loading...");
    try {
      const res = await fetch(`/api/recommendations?city=${encodeURIComponent(c)}`);
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.detail || `Request failed (${res.status})`);
      }
      setData(await res.json());
      setStatus("");
    } catch (err) {
      setStatus(err.message);
    }
  }, []);

  useEffect(() => {
    load(city);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="today">
      <h1>Today's Outfit</h1>

      <div style={{ display: "flex", gap: "8px", marginBottom: "12px" }}>
        <input value={city} onChange={(e) => setCity(e.target.value)} placeholder="City" />
        <button onClick={() => load(city)}>Refresh</button>
      </div>

      {status && <p>{status}</p>}

      {data && data.configured === false && (
        <p>{data.message}</p>
      )}

      {data && data.configured && (
        <div>
          <p>
            <strong>{data.weather.city}</strong>: {Math.round(data.weather.temp_c)}°C,{" "}
            {data.weather.description}
          </p>
          {data.note && <p>{data.note}</p>}
          <h3>Suggested items</h3>
          {data.recommended.length === 0 ? (
            <p>No matching items in your wardrobe yet.</p>
          ) : (
            <div style={{ display: "flex", flexWrap: "wrap", gap: "12px" }}>
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

export default Today;
