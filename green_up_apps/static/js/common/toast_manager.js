/**
 * ToastManager with design inspired by showNotification function
 * Uses a builder pattern for flexible configuration.
 * @class
 */
class ToastManager {
    constructor() {
        // Initialize toast container
        this.toastContainer = document.createElement('div');
        this.toastContainer.id = 'toast-container2';
        this.toastContainer.style.position = 'fixed';
        this.toastContainer.style.zIndex = '10000';
        this.toastContainer.style.display = 'flex';
        this.toastContainer.style.flexDirection = 'column';
        this.toastContainer.style.gap = '12px';
        this.toastContainer.style.maxWidth = '320px';
        this.toastContainer.style.width = '100%';
        this.toastContainer.style.pointerEvents = 'none';
        document.body.appendChild(this.toastContainer);

        // Set default position (top-right, as in showNotification)
        this.setPosition('top-right');

        // Current config
        this.currentPosition = 'top-right';
        this.currentDuration = 5000; // Default duration: 5 seconds, as in showNotification

        // Inject CSS styles
        this.injectStyles();
    }

    /**
     * Injects CSS styles for toast design and animations, inspired by showNotification.
     * @private
     */
    injectStyles() {
        const styles = `
            #toast-container2 > * {
                pointer-events: auto;
            }

            /* Toast element styles, inspired by showNotification */
            .toast {
                padding: 16px;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                color: #fff;
                position: relative;
                overflow: hidden;
                transition: transform 0.3s ease, opacity 0.3s ease;
            }

            .toast-success {
                background-color: #16a34a; /* bg-green-600 */
            }

            .toast-error {
                background-color: #dc2626; /* bg-red-600 */
            }

            .toast-warning {
                background-color: #d97706; /* bg-yellow-600 */
            }

            .toast-info {
                background-color: #2563eb; /* bg-blue-600 */
            }

            .toast-icon {
                margin-right: 8px;
                font-size: 18px;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;
            }

            .toast-content {
                flex-grow: 1;
                font-size: 14px;
            }

            .toast-close {
                background: none;
                border: none;
                font-size: 16px;
                cursor: pointer;
                color: #fff;
                padding: 4px;
                border-radius: 50%;
                width: 24px;
                height: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;
            }

            .toast-close:hover {
                color: #e5e7eb; /* text-gray-200 */
            }

            /* Animation keyframes, inspired by showNotification */
            @keyframes slideInRight {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }

            @keyframes slideOutRight {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }

            @keyframes slideInLeft {
                from { transform: translateX(-100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }

            @keyframes slideOutLeft {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(-100%); opacity: 0; }
            }

            @keyframes slideInTop {
                from { transform: translateY(-100%); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }

            @keyframes slideOutTop {
                from { transform: translateY(0); opacity: 1; }
                to { transform: translateY(-100%); opacity: 0; }
            }

            @keyframes slideInBottom {
                from { transform: translateY(100%); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }

            @keyframes slideOutBottom {
                from { transform: translateY(0); opacity: 1; }
                to { transform: translateY(100%); opacity: 0; }
            }

            /* Animation classes */
            .animate-slide-in-right {
                animation: slideInRight 0.3s ease-out forwards;
            }

            .animate-slide-out-right {
                animation: slideOutRight 0.3s ease-in forwards;
            }

            .animate-slide-in-left {
                animation: slideInLeft 0.3s ease-out forwards;
            }

            .animate-slide-out-left {
                animation: slideOutLeft 0.3s ease-in forwards;
            }

            .animate-slide-in-top {
                animation: slideInTop 0.3s ease-out forwards;
            }

            .animate-slide-out-top {
                animation: slideOutTop 0.3s ease-in forwards;
            }

            .animate-slide-in-bottom {
                animation: slideInBottom 0.3s ease-out forwards;
            }

            .animate-slide-out-bottom {
                animation: slideOutBottom 0.3s ease-in forwards;
            }

            /* Responsive adjustments */
            @media (max-width: 768px) {
                #toast-container2 {
                    max-width: 90%;
                }
            }
        `;

        const styleSheet = document.createElement('style');
        styleSheet.textContent = styles;
        document.head.appendChild(styleSheet);

        // Add Font Awesome if not already present
        if (!document.querySelector('link[href*="font-awesome"]')) {
            const fontAwesomeLink = document.createElement('link');
            fontAwesomeLink.rel = 'stylesheet';
            fontAwesomeLink.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css';
            document.head.appendChild(fontAwesomeLink);
        }
    }

    /**
     * Sets the position of the toast container.
     * @param {string} position - The position ('top-left', 'top-right', 'bottom-left', 'bottom-right').
     * @private
     */
    setPosition(position) {
        this.toastContainer.classList.remove('top-right', 'top-left', 'bottom-right', 'bottom-left');
        this.toastContainer.classList.add(position);

        switch (position) {
            case 'top-left':
                this.toastContainer.style.top = '16px';
                this.toastContainer.style.left = '16px';
                this.toastContainer.style.bottom = '';
                this.toastContainer.style.right = '';
                break;
            case 'top-right':
                this.toastContainer.style.top = '16px';
                this.toastContainer.style.right = '16px';
                this.toastContainer.style.bottom = '';
                this.toastContainer.style.left = '';
                break;
            case 'bottom-left':
                this.toastContainer.style.bottom = '16px';
                this.toastContainer.style.left = '16px';
                this.toastContainer.style.top = '';
                this.toastContainer.style.right = '';
                break;
            case 'bottom-right':
                this.toastContainer.style.bottom = '16px';
                this.toastContainer.style.right = '16px';
                this.toastContainer.style.top = '';
                this.toastContainer.style.left = '';
                break;
        }

        this.currentPosition = position;
    }

    /**
     * Creates a new ToastBuilder instance to configure a toast.
     * @returns {ToastBuilder} A new ToastBuilder instance.
     */
    buildToast() {
        return new ToastBuilder(this);
    }

    /**
     * Shows a toast with the specified configuration.
     * @private
     * @param {Object} config - The toast configuration.
     */
    showToast(config) {
        const { message, type = 'info', position = 'top-right', duration = 5000 } = config;

        // Sanitize message to prevent XSS
        const sanitizedMessage = message.replace(/</g, '&lt;').replace(/>/g, '&gt;');

        if (position !== this.currentPosition) {
            this.setPosition(position);
        }

        const toastStyles = {
            success: { class: 'toast-success', icon: '<i class="fas fa-check-circle"></i>' },
            error: { class: 'toast-error', icon: '<i class="fas fa-times-circle"></i>' },
            warning: { class: 'toast-warning', icon: '<i class="fas fa-exclamation-triangle"></i>' },
            info: { class: 'toast-info', icon: '<i class="fas fa-info-circle"></i>' }
        };

        const style = toastStyles[type] || toastStyles.info;

        // Determine initial and final transform based on position
        let initialTransform, slideInAnimation, slideOutAnimation;
        switch (position) {
            case 'top-left':
            case 'bottom-left':
                initialTransform = 'translateX(-100%)';
                slideInAnimation = 'animate-slide-in-left';
                slideOutAnimation = 'animate-slide-out-left';
                break;
            case 'top-right':
            case 'bottom-right':
                initialTransform = 'translateX(100%)';
                slideInAnimation = 'animate-slide-in-right';
                slideOutAnimation = 'animate-slide-out-right';
                break;
            case 'top-center':
                initialTransform = 'translateY(-100%)';
                slideInAnimation = 'animate-slide-in-top';
                slideOutAnimation = 'animate-slide-out-top';
                break;
            case 'bottom-center':
                initialTransform = 'translateY(100%)';
                slideInAnimation = 'animate-slide-in-bottom';
                slideOutAnimation = 'animate-slide-out-bottom';
                break;
            default:
                initialTransform = 'translateX(100%)';
                slideInAnimation = 'animate-slide-in-right';
                slideOutAnimation = 'animate-slide-out-right';
        }

        // Create toast element
        const toast = document.createElement('div');
        toast.className = `toast ${style.class}`;
        toast.style.transform = initialTransform;
        toast.style.opacity = '0';

        toast.innerHTML = `
            <div class="flex items-center space-x-2">
                <div class="toast-icon">${style.icon}</div>
                <div class="toast-content">${sanitizedMessage}</div>
                <button class="toast-close">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;

        this.toastContainer.appendChild(toast);

        // Force reflow to ensure animation triggers
        toast.offsetHeight; // Trigger reflow

        // Animate in
        requestAnimationFrame(() => {
            toast.classList.add(slideInAnimation);
            toast.style.transform = null; // Remove inline transform to let CSS animation take over
            toast.style.opacity = '1';
        });

        // Close button handler
        const closeBtn = toast.querySelector('.toast-close');
        closeBtn.addEventListener('click', () => {
            toast.classList.remove(slideInAnimation);
            toast.classList.add(slideOutAnimation);
            setTimeout(() => {
                if (toast.parentElement) {
                    toast.remove();
                }
            }, 300);
        });

        // Auto-close after specified duration
        setTimeout(() => {
            if (toast.parentElement) {
                toast.classList.remove(slideInAnimation);
                toast.classList.add(slideOutAnimation);
                setTimeout(() => {
                    if (toast.parentElement) {
                        toast.remove();
                    }
                }, 300);
            }
        }, duration);
    }

    /**
     * Closes all currently displayed toasts.
     */
    closeAllToasts() {
        const toasts = this.toastContainer.querySelectorAll('.toast');
        toasts.forEach(toast => {
            const slideInAnimation = Array.from(toast.classList).find(cls => cls.startsWith('animate-slide-in'));
            let slideOutAnimation = 'animate-slide-out-right';

            if (slideInAnimation) {
                const direction = slideInAnimation.replace('animate-slide-in-', '');
                slideOutAnimation = `animate-slide-out-${direction}`;
            }

            toast.classList.remove(slideInAnimation);
            toast.classList.add(slideOutAnimation);
            setTimeout(() => {
                if (toast.parentElement) {
                    toast.remove();
                }
            }, 300);
        });
    }
}

/**
 * Builder class for configuring and displaying toasts fluently.
 * @class
 */
class ToastBuilder {
    constructor(manager) {
        this.manager = manager;
        this.config = {
            message: '',
            type: 'info',
            position: 'top-right',
            duration: 5000
        };
    }

    setMessage(message) {
        this.config.message = message;
        return this;
    }

    setType(type) {
        this.config.type = type;
        return this;
    }

    setPosition(position) {
        this.config.position = position;
        return this;
    }

    setDuration(duration) {
        this.config.duration = duration;
        return this;
    }

    show() {
        if (!this.config.message) {
            throw new Error('Toast message is required');
        }
        this.manager.showToast(this.config);
    }
}

// Export a singleton instance
const ToastManager = new ToastManager();
window.ToastManager = ToastManager;
