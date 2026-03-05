import React, { useEffect, useState } from "react";
import { useLang } from "@/context/LanguageContext";
import { useSearchParams, useNavigate } from "react-router-dom";
import { authApi } from "@/services/api/authService";
import { Button } from "@/component/common";
import { FaCheckCircle, FaTimesCircle } from "react-icons/fa";
import { LoadingSpinner } from "@/component/ui";
import { AppRoutes } from "@/routes/routes";
function Activate() {
  const navigate = useNavigate();
  const { t } = useLang();
  const [searchParams] = useSearchParams();
  const uid = searchParams.get("uid");
  const token = searchParams.get("token");
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("verifying");

  const handleActivate = async () => {
    if (!uid || !token) {
      setStatus("error");
      return;
    }

    try {
      setStatus("verifying");
      setLoading(true);
      const response = await authApi.activate({
        uid,
        token,
      });
      if (response.status === 204 || response.status === 200 || response.data) {
        setStatus("success");
        setTimeout(() => navigate(AppRoutes.login), 3000);
      }
    } catch (err) {
      console.error("Activation failed:", err);
      setStatus("error");
    } finally {
      setLoading(false);
    }
  };
  useEffect(() => {
    async function activate() {
      await handleActivate();
    }
    activate();
  }, [uid, token]);

  if (loading) {
    return <LoadingSpinner label="loading" />;
  }

  return (
    <div className="flex items-center justify-center min-h-[80vh] px-4">
      <div className="w-full max-w-md p-8 space-y-6 bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-100 dark:border-gray-700 text-center ring-gray-300 dark:ring-gray-600">
        {status === "success" && (
          <div className="space-y-4">
            <div className="bg-green-100 dark:bg-green-900/20 p-3 rounded-full w-16 h-16 flex items-center justify-center mx-auto">
              <FaCheckCircle className="w-8 h-8 text-green-600" />
            </div>
            <h2 className="text-base md:text-xl font-bold text-gray-900 dark:text-white">
              {t("activationSuccess")}
            </h2>
            <p className="text-gray-500 dark:text-gray-400">
              {t("redirecting")}...
            </p>
            <Button onClick={() => navigate(AppRoutes.login)} fullWidth>
              {t("goToLogin")}
            </Button>
          </div>
        )}

        {status === "error" && (
          <div className="space-y-4">
            <div className="p-3 rounded-full w-16 h-16 flex items-center justify-center mx-auto">
              <FaTimesCircle className="w-8 h-8 text-red-600" />
            </div>
            <h2 className="text-base md:text-xl font-bold text-gray-900 dark:text-white">
              {t("activationFailed")}
            </h2>
            <div className="space-y-2">
              <Button onClick={handleActivate} variant="outline" fullWidth>
                {t("retry")}
              </Button>
              <Button
                onClick={() => navigate(AppRoutes.resendActivationEmail)}
                fullWidth
              >
                {t("resendActivationEmail")}
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Activate;
