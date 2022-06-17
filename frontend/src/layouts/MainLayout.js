import { Button, Layout } from "antd";
import React from "react";
import { Outlet, useNavigate } from "react-router-dom";
import "./MainLayout.css";

const { Header, Content } = Layout;

function MainLayout() {
    const navigate = useNavigate();

    return (
        <Layout>
            <Header>
                {/* <Button onClick={() => navigate("/login")}>Login</Button> */}
                {/* <NavLink to="/requests">Requests</NavLink> */}
                <Button>Connect Wallet</Button>
            </Header>
            <Content>
                <Outlet />
            </Content>
        </Layout>
    );
}

export default MainLayout;
