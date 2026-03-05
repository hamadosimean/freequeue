import React, { useState, useEffect } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { motion as Motion } from "motion/react";
import { useLang } from "@/context/LanguageContext";
import { authApi } from "@/services/api/authService";
import { Button, Input } from "@/component/common";
import { ErrorDisplay } from "@/component/ui";
import { AppRoutes } from "@/routes/routes";
import toast from "react-hot-toast";

function ConfirmedPasswordReset() {
  const navigate = useNavigate();
  const { t } = useLang();
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token");
  const uid = searchParams.get("uid");

  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!token || !uid) {
      toast.error("Invalid or missing reset link.");
      navigate(AppRoutes.forgetPassword);
    }
  }, [token, uid, navigate]);

  const handleConfirmedPasswordReset = async (e) => {
    e.preventDefault();
    setError(null);

    // Basic Validation
    if (!newPassword || !confirmPassword) {
      setError(t("fillAllFields"));
      return;
    }

    if (newPassword !== confirmPassword) {
      setError(t("passwordsDoNotMatch"));
      return;
    }

    if (newPassword.length < 8) {
      setError(t("passwordTooShort"));
      return;
    }

    try {
      setLoading(true);
      const response = await authApi.confirmedPasswordReset({
        token: token,
        uid: uid,
        new_password: newPassword,
        re_new_password: confirmPassword,
      });

      if (response.status === 204 || response.status === 200 || response.data) {
        setNewPassword("");
        setConfirmPassword("");
        toast.success(t("passwordReset"));
        setTimeout(() => navigate(AppRoutes.login), 3000);
      }
    } catch (err) {
      console.error("Reset password failed:", err);
      const errorMessage =
        err.response?.data?.detail ||
        err.response?.data?.new_password?.[0] ||
        t("activationFailed");
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-[80vh] px-4">
      <Motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md p-8 space-y-6 bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-100 dark:border-gray-700 ring-2 ring-gray-300 dark:ring-gray-600"
      >
        <div className="text-center space-y-2">
          <h1 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-gray-100">
            {t("resetPassword")}
          </h1>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            {t("enterNewPassword")}
          </p>
        </div>

        <form onSubmit={handleConfirmedPasswordReset} className="space-y-4">
          {error && <ErrorDisplay error={error} />}

          <div className="space-y-4">
            <Input
              label={t("newPassword")}
              id="newPassword"
              type="password"
              placeholder="••••••••"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              required
            />
            <Input
              label={t("confirmPassword")}
              id="confirmPassword"
              type="password"
              placeholder="••••••••"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>

          <Button type="submit" fullWidth disabled={loading}>
            {loading ? t("verifying") : t("resetPassword")}
          </Button>
        </form>
      </Motion.div>
    </div>
  );
}

export default ConfirmedPasswordReset;
