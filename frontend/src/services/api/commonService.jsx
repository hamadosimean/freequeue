import { authConfig } from "../config/authConfig";

export const commonApi = {
  contact: (payload) => authConfig.post("contact/", payload),
};
