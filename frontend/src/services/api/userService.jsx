import { Config } from "../config/config";

export const userApi = {
  userProfile: () => Config.get("auth/users/me/"),
  updateProfile: (payload) => Config.put("auth/users/me/", payload),
  partialUpdateProfile: (payload) => Config.patch("auth/users/me/", payload),
};
