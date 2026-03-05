import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Input, Button } from "@/component/common";
import { authApi } from "@/services/api/authService";
import { useLang } from "@/context/LanguageContext";
import { AppRoutes } from "@/routes/routes";
import toast from "react-hot-toast";
import { ErrorDisplay, LoadingSpinner } from "@/component/ui";
function Register() {
  const { t } = useLang();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [phone, setPhone] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const handlePasswordConfirmation = (e) => {
    e.preventDefault();
    setConfirmPassword(e.target.value);
    if (password.toString().length === confirmPassword.toString().length) {
      if (password.toString() != confirmPassword.toString()) {
        setError(`${t("passwordsDoNotMatch")}`);
        return;
      } else {
        setError("");
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (
      !email ||
      !password ||
      !confirmPassword ||
      !firstName ||
      !lastName ||
      !phone
    ) {
      setError(`${t("fillAllFields")}`);
      toast.error(`${t("fillAllFields")}`);
      return;
    }

    setIsLoading(true);
    try {
      const response = await authApi.register({
        first_name: firstName,
        last_name: lastName,
        email: email,
        phone_number: phone,
        password: password,
        re_password: confirmPassword,
      });
      if (response.data) {
        setEmail("");
        setPassword("");
        setConfirmPassword("");
        setFirstName("");
        setLastName("");
        setPhone("");

        navigate(AppRoutes.activateMessage);
      }
    } catch (err) {
      console.error("Registration failed:", err);
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
        toast.error(err.response.data.detail);
      } else {
        setError("An unexpected error occurred. Please try again.");
        toast.error("An unexpected error occurred. Please try again.");
      }
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
            {t("createAccount")}
          </h1>
          <p className="text-gray-500 dark:text-gray-400">{t("signUp")}</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {error && <ErrorDisplay error={error} />}

          <div className="space-y-4">
            <Input
              label={t("firstName")}
              type="text"
              placeholder="Ayoub"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              required
            />
            <Input
              label={t("lastName")}
              type="text"
              placeholder="Ouedraogo"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              required
            />
            <Input
              label={t("email")}
              type="email"
              placeholder="name@company.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <Input
              label={t("phone")}
              type="text"
              placeholder="+226 70 00 00 00"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
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
              <Input
                label={t("confirmPassword")}
                type="password"
                placeholder="••••••••"
                value={confirmPassword}
                onChange={handlePasswordConfirmation}
                required
              />
            </div>
          </div>

          <Button type="submit" fullWidth disabled={isLoading} className="py-3">
            {isLoading ? t("redirecting") : t("signUp")}
          </Button>
        </form>

        <div className="text-center">
          <p className="text-sm text-gray-600 dark:text-gray-400">
            {t("alreadyHaveAccount")}{" "}
            <Link
              to={AppRoutes.login}
              className="font-semibold text-blue-600 hover:text-blue-500"
            >
              {t("signIn")}
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Register;
