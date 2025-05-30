import './App.css';
import Home from './components/home';
import Navbar from './components/navbar';
import History from './components/history';
import Login from './components/login';
import Register from './components/register';
import { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom";

// Component with access to location
function AppContent() {
  const location = useLocation();
  const [show, setShow] = useState(false);
  const hideNavbarPaths = ['/login', '/register'];

  useEffect(() => {
    let timer;

    if (location.pathname === '/') {
      timer = setTimeout(() => {
        setShow(true);
      }, 2000);
    } else {
      setShow(true); // instantly show on other pages (or keep false if you want to hide always)
    }

    return () => clearTimeout(timer);
  }, [location.pathname]);

  return (
    <>
      {show && !hideNavbarPaths.includes(location.pathname) && <Navbar />}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/history" element={<History />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </>
  );
}

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;
