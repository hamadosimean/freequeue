import React, { useState } from "react";
import { useLang } from "@/context/LanguageContext";
import { commonApi } from "@/services";
import toast, { Toaster } from "react-hot-toast";
import LoadingSpinner from "@/component/ui/LoadingSpinner";
function Contact() {
  const { t } = useLang();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
    company: "",
    subject: "",
    message: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      const response = await commonApi.contact(formData);
      if (response.status === 201 || response.status === 200) {
        toast.success("Message sent successfully!");
      }
      setFormData({
        name: "",
        email: "",
        phone: "",
        company: "",
        subject: "",
        message: "",
      });
    } catch (error) {
      toast.error("Failed to send message");
      setError(error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingSpinner loading="sending message..." />;
  }
  return (
    <section className="container mx-auto px-4 py-16 dark:bg-gray-900  ">
      <Toaster />
      {/* Page title */}
      <div className="max-w-3xl mx-auto text-center mb-12">
        <h1 className="text-4xl md:text-5xl font-extrabold text-gray-900 dark:text-white mb-4">
          {t("contactTitle") || "Contact Us"}
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          {t("contactIntro") ||
            "Have a question or feedback? Reach out to us using the form below or email us directly at contact.techarea@gmail.com."}
        </p>
      </div>

      {/* Contact form */}
      <form
        className="max-w-3xl mx-auto bg-white dark:bg-gray-900 p-8 rounded-xl shadow-sm dark:shadow-md space-y-6 ring-2 ring-gray-300 dark:ring-gray-700"
        onSubmit={handleSubmit}
      >
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <label
              className="block text-gray-700 dark:text-gray-300 font-medium mb-2"
              htmlFor="name"
            >
              {t("contactName") || "Full Name"}
            </label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none transition"
            />
          </div>

          <div>
            <label
              className="block text-gray-700 dark:text-gray-300 font-medium mb-2"
              htmlFor="email"
            >
              {t("contactEmail") || "Email"}
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none transition"
            />
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <label
              className="block text-gray-700 dark:text-gray-300 font-medium mb-2"
              htmlFor="phone"
            >
              {t("contactPhone") || "Phone (optional)"}
            </label>
            <input
              type="text"
              id="phone"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none transition"
            />
          </div>

          <div>
            <label
              className="block text-gray-700 dark:text-gray-300 font-medium mb-2"
              htmlFor="company"
            >
              {t("contactCompany") || "Company (optional)"}
            </label>
            <input
              type="text"
              id="company"
              name="company"
              value={formData.company}
              onChange={handleChange}
              className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none transition"
            />
          </div>
        </div>

        <div>
          <label
            className="block text-gray-700 dark:text-gray-300 font-medium mb-2"
            htmlFor="subject"
          >
            {t("contactSubject") || "Subject"}
          </label>
          <input
            type="text"
            id="subject"
            name="subject"
            value={formData.subject}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none transition"
          />
        </div>

        <div>
          <label
            className="block text-gray-700 dark:text-gray-300 font-medium mb-2"
            htmlFor="message"
          >
            {t("contactMessage") || "Message"}
          </label>
          <textarea
            id="message"
            name="message"
            rows="6"
            value={formData.message}
            onChange={handleChange}
            required
            className="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none transition resize-none"
          ></textarea>
        </div>

        <button
          type="submit"
          className="w-full md:w-auto bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-3 rounded-lg transition"
        >
          {t("send") || "Send Message"}
        </button>
      </form>

      {/* Direct email */}
      <div className="max-w-3xl mx-auto text-center mt-12">
        <p className="text-gray-600 dark:text-gray-400">
          {t("contactDirectEmail") || "Or email us directly at"}{" "}
          <a
            href="mailto:contact.techarea@gmail.com"
            className="text-blue-600 dark:text-blue-400 underline"
          >
            contact.techarea@gmail.com
          </a>
        </p>
      </div>
    </section>
  );
}

export default Contact;
