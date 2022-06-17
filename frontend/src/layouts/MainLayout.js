import { Button, Layout } from "antd";
import React from "react";
import { Outlet, useNavigate } from "react-router-dom";
import "./MainLayout.css";

const { Header, Content } = Layout;

function MainLayout() {
    const navigate = useNavigate();

    const logout = () => {
        localStorage.removeItem("web3_token");
        localStorage.removeItem("web3_user");

        navigate("/login");
    };

    return (
        <Layout>
            <Header className="navigation">
                {/* <NavLink to="/requests">Requests</NavLink> */}
                <Button type="primary">Connect Wallet</Button>
                <Button onClick={logout}>Logout</Button>
            </Header>
            <Content>
                <Outlet />
            </Content>
        </Layout>
    );
}

export default MainLayout;
