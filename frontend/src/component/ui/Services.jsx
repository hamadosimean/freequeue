import React from "react";
import { useLang } from "@/context/LanguageContext";
import {
  FiActivity,
  FiCreditCard,
  FiHome,
  FiFileText,
  FiUsers,
  FiMapPin,
} from "react-icons/fi";

function Services() {
  const { t } = useLang();

  const services = [
    {
      icon: <FiActivity />,
      title: t("serviceHealthcareTitle"),
      text: t("serviceHealthcareText"),
    },
    {
      icon: <FiCreditCard />,
      title: t("serviceBankingTitle"),
      text: t("serviceBankingText"),
    },
    {
      icon: <FiHome />,
      title: t("serviceGovernmentTitle"),
      text: t("serviceGovernmentText"),
    },
    {
      icon: <FiFileText />,
      title: t("serviceAdministrationTitle"),
      text: t("serviceAdministrationText"),
    },
    {
      icon: <FiUsers />,
      title: t("serviceCustomerSupportTitle"),
      text: t("serviceCustomerSupportText"),
    },
    {
      icon: <FiMapPin />,
      title: t("serviceWalkInTitle"),
      text: t("serviceWalkInText"),
    },
  ];

  return (
    <section className="container mx-auto px-4 py-20">
      {/* Title */}
      <div className="max-w-3xl mx-auto text-center mb-16">
        <h2 className="text-xl md:text-4xl font-extrabold text-gray-900">
          {t("servicesTitle")}
        </h2>

        <p className="text-lg text-gray-600 dark:text-gray-400">
          {t("servicesSubtitle")}
        </p>
      </div>

      {/* Services grid */}
      <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-10 max-w-6xl mx-auto">
        {services.map((service, index) => (
          <div
            key={index}
            className="p-8 rounded-xl bg-gray-100 dark:bg-gray-800 hover:shadow-lg transition"
          >
            <div className="text-4xl text-blue-600 mb-4">{service.icon}</div>

            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">
              {service.title}
            </h3>

            <p className="text-gray-600 dark:text-gray-400">{service.text}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

export default Services;
