import { LockOutlined, MailOutlined } from "@ant-design/icons";
import { Alert, Button, Col, Form, Input, Row } from "antd";
import React from "react";
import { useMutation } from "react-query";
import { useNavigate } from "react-router-dom";
import api from "../config/api";

function Login() {
    const navigate = useNavigate();

    const { mutate, isLoading, isError, error } = useMutation(
        (credentials) => api.post("/login", credentials),
        {
            onSuccess: async (response) => {
                const { data } = response;
                localStorage.setItem("web3_token", data.data.token);
                localStorage.setItem(
                    "web3_user",
                    JSON.stringify({
                        email: data.data.email,
                        role: data.data.role,
                        id: data.data.id,
                    })
                );

                if (data.data.role === "staff") {
                    navigate("/");
                } else {
                    navigate("/trainee");
                }
            },
        }
    );

    const handleSubmit = (values) => {
        mutate(values);
    };

    return (
        <Row
            type="flex"
            justify="center"
            align="middle"
            style={{ minHeight: "100vh" }}
        >
            <Col span={6}>
                <Form
                    onFinish={handleSubmit}
                    layout="vertical"
                    requiredMark={false}
                >
                    <Form.Item
                        label="Email"
                        name="email"
                        rules={[
                            {
                                required: true,
                                message: "Please input your email!",
                            },
                        ]}
                    >
                        <Input
                            prefix={
                                <MailOutlined className="site-form-item-icon" />
                            }
                            placeholder="Email"
                        />
                    </Form.Item>
                    <Form.Item
                        label="Password"
                        name="password"
                        rules={[
                            {
                                required: true,
                                message: "Please input your password!",
                            },
                        ]}
                    >
                        <Input.Password
                            prefix={
                                <LockOutlined className="site-form-item-icon" />
                            }
                            placeholder="Password"
                        />
                    </Form.Item>
                    <Button
                        htmlType="submit"
                        type="primary"
                        block
                        loading={isLoading}
                    >
                        Login
                    </Button>
                </Form>
                {isError ? (
                    <Alert
                        style={{ marginTop: "20px" }}
                        message={error}
                        type="error"
                    />
                ) : null}
            </Col>
        </Row>
    );
}

export default Login;
