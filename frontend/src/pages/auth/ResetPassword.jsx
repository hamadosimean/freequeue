import React, { useState } from "react";
import { useLang } from "@/context/LanguageContext";
import { Input, Button } from "@/component/common";
import { authApi } from "@/services/api/authService";
import toast, { Toaster } from "react-hot-toast";
import { AppRoutes } from "@/routes/routes";
import { ErrorDisplay, LoadingSpinner } from "@/component/ui";
import { useNavigate } from "react-router-dom";
function ResetPassword() {
  const { t } = useLang();
  const navigate = useNavigate();
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmNewPassword, setConfirmNewPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (newPassword !== confirmNewPassword) {
      setError(t("passwordsDoNotMatch"));
      return;
    }

    try {
      setIsLoading(true);
      const response = await authApi.changePassword({
        current_password: currentPassword,
        new_password: newPassword,
        re_new_password: confirmNewPassword,
      });
      if (response.status === 204 || response.status === 200 || response.data) {
        toast.success(t("passwordReset"));
        setCurrentPassword("");
        setNewPassword("");
        setConfirmNewPassword("");
        setTimeout(() => navigate(AppRoutes.login), 3000);
      }
    } catch (err) {
      console.error("Reset password failed:", err);
      const data = err.response?.data;
      let errorMessage = t("activationFailed");

      if (data) {
        if (data.detail) {
          errorMessage = data.detail;
        } else if (data.current_password) {
          errorMessage = data.current_password[0];
        } else if (data.new_password) {
          errorMessage = data.new_password[0];
        } else if (data.non_field_errors) {
          errorMessage = data.non_field_errors[0];
        }
      }

      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <LoadingSpinner label={t("loading")} />;
  }
  return (
    <div>
      <Toaster />
      <div className="flex items-center justify-center min-h-[80vh] px-4">
        <div className="w-full max-w-md p-8 space-y-6 bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-100 dark:border-gray-700 ring-2 ring-gray-300 dark:ring-gray-600">
          <div className="text-center space-y-2">
            <h1 className="text-xl font-bold text-gray-900 dark:text-white">
              {t("changePassword")}
            </h1>
            <p className="text-gray-500 dark:text-gray-400">
              {t("enterNewPassword")}
            </p>
          </div>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && <ErrorDisplay error={error} />}
            <Input
              label={t("currentPassword")}
              type="password"
              placeholder="••••••••"
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
              required
            />
            <Input
              label={t("newPassword")}
              type="password"
              placeholder="••••••••"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              required
            />
            <Input
              label={t("confirmNewPassword")}
              type="password"
              placeholder="••••••••"
              value={confirmNewPassword}
              onChange={(e) => setConfirmNewPassword(e.target.value)}
              required
            />
            <Button
              type="submit"
              fullWidth
              disabled={isLoading}
              className="py-3"
            >
              {isLoading ? t("redirecting") : t("resetPassword")}
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default ResetPassword;
