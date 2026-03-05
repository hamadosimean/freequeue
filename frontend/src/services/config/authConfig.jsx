import { API_URL } from "../../config/environment";
import axios from "axios";

export const authConfig = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});
