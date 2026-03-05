import { authConfig } from "../config/authConfig";
import { Config } from "../config/config";
export const authApi = {
  register: (payload) => authConfig.post("auth/users/", payload),
  login: (payload) => authConfig.post("auth/jwt/create/", payload),
  activate: (payload) => authConfig.post("auth/users/activation/", payload),
  resendActivationEmail: (payload) =>
    authConfig.post("auth/users/resend_activation/", payload),
  resetPassword: (payload) =>
    authConfig.post("auth/users/reset_password/", payload),
  confirmedPasswordReset: (payload) =>
    authConfig.post("auth/users/reset_password_confirm/", payload),
  changePassword: (payload) => Config.post("auth/users/set_password/", payload),
  logout: (payload) => authConfig.post("accounts/logout", payload),
  refreshToken: (payload) => authConfig.post("auth/jwt/refresh/", payload),
};
