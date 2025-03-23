import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import WelcomePage from './pages/WelcomePage'
import HomePage from './pages/HomePage';


const App = () => {
  return (
    <Router >
    <Routes>
      <Route path="/" element={<WelcomePage />} />
      <Route path="/home" element={<HomePage />} />

    </Routes>
    </Router >
  
  )
}

export default App
