import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// Import pages
import Home from "../pages/home/home";

function AppRouter({ router = Router}) {
    const Router = router;

  return (
    <Router>
      <Routes>
        <Route>
            <Route path="/" element={<Home />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default AppRouter;