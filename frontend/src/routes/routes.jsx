import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// Import components
import Layout from "../layouts/layout";

// Import pages
import Home from "../pages/home/home";
import About from "../pages/about/about";
import Wardrobe from "../pages/wardrobe/wardrobe";
import Login from "../pages/login/login";

function AppRouter({ router = Router}) {
    const Router = router;

  return (
    <Router>
      <Routes>
        <Route element={<Layout />}>
            <Route path="/" element={<Home />} />
            <Route path="/wardrobe" element={<Wardrobe />} />
            <Route path="/login" element={<Login />} />
            <Route path="/about" element={<About />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default AppRouter;