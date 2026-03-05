import React, { useState } from "react";
import { useLang } from "@/context/LanguageContext";
import { useNavigate } from "react-router-dom";
import { authApi } from "@/services/api/authService";
import { Button, Input } from "@/component/common";
import toast from "react-hot-toast";
import { AppRoutes } from "@/routes/routes";
import { LoadingSpinner } from "@/component/ui";
function ResendActivationEmail() {
  const { t } = useLang();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);

  const handleResendActivationEmail = async () => {
    try {
      setLoading(true);
      const response = await authApi.resendActivationEmail({
        email,
      });
      if (response.status === 204 || response.status === 200 || response.data) {
        toast.success(t("passwordResent"));
        setEmail("");
        setTimeout(() => navigate(AppRoutes.activateMessage), 3000);
      }
    } catch (err) {
      console.error("Resend activation email failed:", err);
      toast.error(err.response?.data?.detail || "Email not sent");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingSpinner label="loading" />;
  }

  return (
    <div className="flex items-center justify-center min-h-[80vh] px-4 ">
      <div className="w-full max-w-md p-8 space-y-6 bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-100 dark:border-gray-700 ring-2 ring-gray-300 dark:ring-gray-600">
        <div className="text-center space-y-2">
          <p className="text-base md:text-xl font-bold text-gray-900 dark:text-gray-200">
            {t("resendActivationEmail")}
          </p>
        </div>
        <div className="space-y-4">
          <div className="space-y-2">
            <Input
              label={t("email")}
              id="email"
              type="email"
              placeholder={t("email")}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <Button onClick={handleResendActivationEmail} fullWidth>
            {t("resendActivationEmail")}
          </Button>
          <Button onClick={() => navigate(AppRoutes.login)} fullWidth>
            {t("goToLogin")}
          </Button>
        </div>
      </div>
    </div>
  );
}

export default ResendActivationEmail;
