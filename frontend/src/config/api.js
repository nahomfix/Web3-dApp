import axios from "axios";

const api = axios.create({
    baseURL: process.env.REACT_APP_API,
});

const token = localStorage.getItem("web3_token");

api.interceptors.request.use(
    async function (config) {
        config.headers = {
            ...config.headers,
            "x-access-token": token ?? "",
        };
        return config;
    },
    function (error) {
        return Promise.reject(error);
    }
);

api.interceptors.response.use(
    function (response) {
        return response;
    },
    function (error) {
        if (error.response) {
            console.log(error.response.data.data);
            return Promise.reject(error.response.data.data);
        } else if (error.request) {
            console.log(error.message);
            return Promise.reject(error.message);
        } else {
            console.log(error.message);
            return Promise.reject(error.message);
        }

        // return Promise.reject(error);
    }
);

export default api;
