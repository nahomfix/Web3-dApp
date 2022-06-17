import { Route, Routes } from "react-router-dom";
import "./App.css";
import MainLayout from "./layouts/MainLayout";
import Home from "./pages/Home";
import Login from "./pages/Login";

function App() {
    return (
        <>
            <Routes>
                <Route path="/" element={<MainLayout />}>
                    <Route index element={<Home />} />
                </Route>
                <Route path="/login" element={<Login />} />
            </Routes>
        </>
    );
}

export default App;
