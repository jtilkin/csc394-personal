import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./home";
import Employers from "./employers";
import Users from "./users";

function App() {
  return (
    <Router>
      <nav>
        <Link to="/">Home</Link> | <Link to="/employers">Employers</Link> | <Link to="/users">Users</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/employers" element={<Employers />} />
        <Route path="/users" element={<Users />} />
      </Routes>
    </Router>
  );
}

export default App;
