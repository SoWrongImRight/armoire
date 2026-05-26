import React from "react";
import { Link } from "react-router-dom";

const Menu = () => {

    return (
        <div>
            <h1>Menu</h1>
            <ul>
                <li><Link to="/">Home</Link></li>
                <li><Link to="/wardrobe">Wardrobe</Link></li>
                <li><Link to="/login">Account</Link></li>
                <li><Link to="/about">About</Link></li>
                <li>Contact</li>
                <li>Services</li>
            </ul>
        </div>
    )
}

export default Menu;