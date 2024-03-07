import React from 'react';
import logo from '../assets/icons/logo.png'; // Adjust the path as necessary

function Navbar() {
  return (
    <nav className="navbar">
      <ul className="nav-links left">
        <li><a href="index.html">Home</a></li>
        <li><a href="">About</a></li>
        <li><a href="">Games</a></li>
      </ul>

      <div className="nav-logo">
        <img src={logo} alt="Logo" />
      </div>

      <ul className="nav-links right">
        <li><a href="">Contact</a></li>
        <li><a href="">Register</a></li>
        <li><a href="">Login</a></li>
      </ul>
    </nav>
  );
}

export default Navbar;
