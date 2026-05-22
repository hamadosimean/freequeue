import React from "react";
import Modal from "react-modal";
import { motion as Motion, AnimatePresence } from "motion/react";
import { IoClose } from "react-icons/io5";

// Set the app element for accessibility
if (typeof window !== "undefined") {
  Modal.setAppElement("#root");
}
 
const sizes = {
  sm: "max-w-md",
  md: "max-w-lg",
  lg: "max-w-2xl",
  xl: "max-w-4xl",
  full: "max-w-[95vw]",
};

export default function CustomModal({
  isOpen,
  onClose,
  children,
  title,
  size = "md",
  showCloseButton = true,
}) {
  return (
    <Modal
      isOpen={isOpen}
      onRequestClose={onClose}
      className="outline-none"
      overlayClassName="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
      contentLabel={title || "Modal"}
      closeTimeoutMS={300}
    >
      <AnimatePresence>
        {isOpen && (
          <Motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            transition={{ type: "spring", duration: 0.5, bounce: 0.3 }}
            className={`w-full ${sizes[size]} bg-white dark:bg-gray-800 rounded-2xl shadow-2xl border border-gray-100 dark:border-gray-700 overflow-hidden relative`}
          >
            {/* Header */}
            {(title || showCloseButton) && (
              <div className="px-6 py-4 border-b border-gray-100 dark:border-gray-700 flex items-center justify-between bg-gray-50/50 dark:bg-gray-800/50">
                {title && (
                  <h3 className="text-xl font-bold text-gray-900 dark:text-white">
                    {title}
                  </h3>
                )}
                {showCloseButton && (
                  <button
                    onClick={onClose}
                    className="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors text-gray-500 dark:text-gray-400"
                    aria-label="Close modal"
                  >
                    <IoClose size={24} />
                  </button>
                )}
              </div>
            )}

            {/* Content */}
            <div className="p-6">{children}</div>
          </Motion.div>
        )}
      </AnimatePresence>
    </Modal>
  );
}
