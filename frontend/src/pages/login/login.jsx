import React, { useState, useEffect, useCallback } from "react";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [me, setMe] = useState(null);
  const [status, setStatus] = useState("");

  const loadMe = useCallback(async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      setMe(null);
      return;
    }
    const res = await fetch("/api/auth/me", {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (res.ok) {
      setMe(await res.json());
    } else {
      localStorage.removeItem("token");
      setMe(null);
    }
  }, []);

  useEffect(() => {
    loadMe();
  }, [loadMe]);

  const register = async () => {
    setStatus("Registering...");
    try {
      const res = await fetch("/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.detail || `Register failed (${res.status})`);
      }
      setStatus("Registered. You can now log in.");
    } catch (err) {
      setStatus(err.message);
    }
  };

  const login = async () => {
    setStatus("Logging in...");
    try {
      const form = new URLSearchParams();
      form.append("username", email);
      form.append("password", password);
      const res = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: form,
      });
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.detail || `Login failed (${res.status})`);
      }
      const data = await res.json();
      localStorage.setItem("token", data.access_token);
      setStatus("Logged in.");
      await loadMe();
    } catch (err) {
      setStatus(err.message);
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setMe(null);
    setStatus("Logged out.");
  };

  return (
    <div className="login">
      <h1>Account</h1>
      {me ? (
        <div>
          <p>Logged in as <strong>{me.email}</strong></p>
          <button onClick={logout}>Log out</button>
        </div>
      ) : (
        <div style={{ display: "grid", gap: "6px", maxWidth: "320px" }}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <div style={{ display: "flex", gap: "8px" }}>
            <button onClick={login}>Log in</button>
            <button onClick={register}>Register</button>
          </div>
        </div>
      )}
      {status && <p>{status}</p>}
    </div>
  );
};

export default Login;
