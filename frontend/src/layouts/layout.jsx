import React from "react";
import { Outlet } from "react-router-dom";

// Import components
import Menu from "../components/menu/menu";
import Footer from "../components/footer/footer";


const Layout = () => {

    return (
        <div>
            <h1>Layout</h1>
            <Menu />
            <Outlet />
            <Footer />
        </div>
    )
}

export default Layout;