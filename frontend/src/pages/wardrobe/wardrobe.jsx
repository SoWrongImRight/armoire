import React, { useState, useEffect, useCallback } from "react";

const Wardrobe = () => {
  const [images, setImages] = useState([]);
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  const loadImages = useCallback(async () => {
    try {
      const res = await fetch("/api/images");
      if (!res.ok) throw new Error(`Could not load images (${res.status})`);
      const data = await res.json();
      setImages(data.images || []);
    } catch (err) {
      setStatus(err.message);
    }
  }, []);

  useEffect(() => {
    loadImages();
  }, [loadImages]);

  const handleUpload = async (event) => {
    event.preventDefault();
    if (!file) {
      setStatus("Choose an image first.");
      return;
    }
    setLoading(true);
    setStatus("Uploading...");
    try {
      const form = new FormData();
      form.append("file", file);
      const res = await fetch("/api/images", { method: "POST", body: form });
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.detail || `Upload failed (${res.status})`);
      }
      setStatus("Uploaded.");
      setFile(null);
      event.target.reset();
      await loadImages();
    } catch (err) {
      setStatus(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="wardrobe">
      <h1>Wardrobe</h1>
      <p>Upload an item photo. Images are stored in S3-compatible object storage.</p>

      <form onSubmit={handleUpload}>
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <button type="submit" disabled={loading}>
          {loading ? "Uploading..." : "Upload"}
        </button>
      </form>

      {status && <p>{status}</p>}

      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "12px",
          marginTop: "16px",
        }}
      >
        {images.map((img) => (
          <figure key={img.key} style={{ margin: 0, width: "160px" }}>
            <img
              src={img.url}
              alt={img.key}
              style={{
                width: "160px",
                height: "160px",
                objectFit: "cover",
                borderRadius: "8px",
              }}
            />
            <figcaption style={{ fontSize: "11px", wordBreak: "break-all" }}>
              {img.key}
            </figcaption>
          </figure>
        ))}
      </div>

      {images.length === 0 && <p>No images yet.</p>}
    </div>
  );
};

export default Wardrobe;
