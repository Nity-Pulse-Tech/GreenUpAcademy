/**
 * Notification manager that integrates with ToastManager for displaying notifications.
 */
class NotificationManager {
    constructor() {
        // Ensure toastManager is available
        if (!window.toastManager) {
            console.error('ToastManager is not initialized. Ensure toast_manager.js is loaded.');
        }
    }

    /**
     * Displays a success notification.
     * @param {string} message - The message to display.
     * @param {string} [position='top-right'] - The position of the toast.
     * @param {number} [duration=4000] - Duration in milliseconds.
     */
    showSuccess(message, position = 'top-right', duration = 4000) {
        if (window.toastManager) {
            window.toastManager.buildToast()
                .setMessage(message)
                .setType('success')
                .setPosition(position)
                .setDuration(duration)
                .show();
        } else {
            console.error('Cannot show success toast: toastManager is not available.');
        }
    }

    /**
     * Displays an error notification.
     * @param {string} message - The message to display.
     * @param {string} [position='top-right'] - The position of the toast.
     * @param {number} [duration=4000] - Duration in milliseconds.
     */
    showError(message, position = 'top-right', duration = 4000) {
        if (window.toastManager) {
            window.toastManager.buildToast()
                .setMessage(message)
                .setType('danger')
                .setPosition(position)
                .setDuration(duration)
                .show();
        } else {
            console.error('Cannot show error toast: toastManager is not available.');
        }
    }

    /**
     * Displays a warning notification.
     * @param {string} message - The message to display.
     * @param {string} [position='top-right'] - The position of the toast.
     * @param {number} [duration=4000] - Duration in milliseconds.
     */
    showWarning(message, position = 'top-right', duration = 4000) {
        if (window.toastManager) {
            window.toastManager.buildToast()
                .setMessage(message)
                .setType('warning')
                .setPosition(position)
                .setDuration(duration)
                .show();
        } else {
            console.error('Cannot show warning toast: toastManager is not available.');
        }
    }

    /**
     * Displays an info notification.
     * @param {string} message - The message to display.
     * @param {string} [position='top-right'] - The position of the toast.
     * @param {number} [duration=4000] - Duration in milliseconds.
     */
    showInfo(message, position = 'top-right', duration = 4000) {
        if (window.toastManager) {
            window.toastManager.buildToast()
                .setMessage(message)
                .setType('info')
                .setPosition(position)
                .setDuration(duration)
                .show();
        } else {
            console.error('Cannot show info toast: toastManager is not available.');
        }
    }
}

// Export a singleton instance
const notificationManager = new NotificationManager();
window.notificationManager = notificationManager;