import { Button, Col, Form, Row, Upload } from "antd";
import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";

function Home() {
    const user = localStorage.getItem("web3_user");
    const navigate = useNavigate();

    useEffect(() => {
        if (JSON.parse(user).role !== "staff") {
            navigate("/trainee");
        }
    }, [navigate, user]);

    return (
        <>
            <Row
                type="flex"
                justify="center"
                align="middle"
                style={{ minHeight: "100vh" }}
            >
                <Col span={6}>
                    <Form layout="vertical" requiredMark={false}>
                        <Form.Item label="Certificate" name="certificate">
                            <Upload>
                                <Button>Click to upload</Button>
                            </Upload>
                        </Form.Item>
                        <Button type="primary">Mint</Button>
                    </Form>
                </Col>
            </Row>
        </>
    );
}

export default Home;
