import { Button } from "antd";
import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";

function TraineeHome() {
    const user = localStorage.getItem("web3_user");
    const navigate = useNavigate();

    useEffect(() => {
        if (JSON.parse(user).role === "staff") {
            navigate("/");
        }
    }, [navigate, user]);

    return (
        <div>
            <Button>Request Certificate</Button>
        </div>
    );
}

export default TraineeHome;
