import { Route, Routes } from "react-router-dom";
import "./App.css";
import ProtectedRoute from "./hoc/ProtectedRoute";
import MainLayout from "./layouts/MainLayout";
import Home from "./pages/Home";
import Login from "./pages/Login";
import TraineeHome from "./pages/TraineeHome";

function App() {
    return (
        <>
            <Routes>
                <Route
                    path="/"
                    element={
                        <ProtectedRoute>
                            <MainLayout />
                        </ProtectedRoute>
                    }
                >
                    <Route index element={<Home />} />
                    <Route path="trainee" element={<TraineeHome />} />
                </Route>
                <Route path="/login" element={<Login />} />
            </Routes>
        </>
    );
}

export default App;
