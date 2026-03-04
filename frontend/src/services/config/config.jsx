import { API_URL } from "../../config/environment";
import axios from "axios";

export const Config = axios.create({
    baseURL: API_URL,
    headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("freequeuesAccessToken")}`,
    },
    withCredentials: true,
});