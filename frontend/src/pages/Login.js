import { LockOutlined, MailOutlined } from "@ant-design/icons";
import { Button, Col, Form, Input, Row } from "antd";
import React from "react";

function Login() {
    const handleSubmit = (values) => {
        console.log(values);
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
                    <Button htmlType="submit" type="primary" block>
                        Login
                    </Button>
                </Form>
            </Col>
        </Row>
    );
}

export default Login;
