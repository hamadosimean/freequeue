import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Input, Button } from "@/component/common";
import { authApi } from "@/services/api/authService";
import { useAuth } from "@/context/AuthContext";
import { useLang } from "@/context/LanguageContext";
import { AppRoutes } from "@/routes/routes";
import toast from "react-hot-toast";
import { LoadingSpinner } from "@/component/ui";
function Login() {
  const { t } = useLang();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!email || !password) {
      setError(`${t("fillAllFields")}`);
      toast.error(`${t("fillAllFields")}`);
      return;
    }

    setIsLoading(true);
    try {
      const response = await authApi.login({ email, password });
      if (response.data) {
        await login(response.data);
        setEmail("");
        setPassword("");
        setTimeout(() => navigate(AppRoutes.space), 3000);
      }
    } catch (err) {
      console.error("Login failed:", err);
      setError(err.response?.data?.detail || "Invalid email or password");
      toast.error(err.response?.data?.detail || "Invalid email or password");
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <LoadingSpinner label="loading" />;
  }

  return (
    <div className="flex items-center justify-center min-h-[80vh] px-4">
      <div className="w-full max-w-md p-8 space-y-6 bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-100 dark:border-gray-700 ring-2 ring-gray-300 dark:ring-gray-600">
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            {t("welcome")}
          </h1>
          <p className="text-gray-500 dark:text-gray-400">{t("signIn")}</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {error && (
            <div className="p-3 text-sm text-red-500 bg-red-50 dark:bg-red-900/20 rounded-lg border border-red-200 dark:border-red-800">
              {error}
            </div>
          )}

          <div className="space-y-4">
            <Input
              label={t("email")}
              type="email"
              placeholder="name@company.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <div className="space-y-1">
              <Input
                label={t("password")}
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <div className="flex justify-end">
                <Link
                  to={AppRoutes.forgetPassword}
                  className="text-sm font-medium text-blue-600 hover:text-blue-500"
                >
                  {t("forgotPass")}
                </Link>
              </div>
            </div>
          </div>

          <Button type="submit" fullWidth disabled={isLoading} className="py-3">
            {isLoading ? t("redirecting") : t("signIn")}
          </Button>
        </form>

        <div className="text-center">
          <p className="text-sm text-gray-600 dark:text-gray-400">
            {t("noAccount")}{" "}
            <Link
              to={AppRoutes.register}
              className="font-semibold text-blue-600 hover:text-blue-500"
            >
              {t("signUp")}
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Login;
