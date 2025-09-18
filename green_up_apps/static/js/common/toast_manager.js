/**
 * Gère les notifications toast avec des messages, types, positions et durées d'animation personnalisables.
 * Utilise un patron de conception builder pour une configuration flexible.
 * @class
 */
class ToastManager {
    constructor() {
        // Initialiser le conteneur des toasts
        this.toastContainer = document.createElement('div');
        this.toastContainer.id = 'toast-container';
        this.toastContainer.className = 'fixed z-[10000009] flex flex-col gap-4';
        document.body.appendChild(this.toastContainer);

        // Injecter les styles CSS
        this.injectStyles();
    }

    /**
     * Injecte les styles CSS pour les animations et la mise en page des toasts.
     * @private
     */
    injectStyles() {
        const styles = `
            #toast-container {
                max-width: 20rem; /* max-w-xs */
                width: 20rem; /* max-w-xs */
                pointer-events: none; /* Empêche le conteneur de bloquer les clics */
            }
            #toast-container > * {
                pointer-events: auto; /* Autorise l'interaction avec les toasts */
            }
            /* Animations pour différentes positions */
            @keyframes slide-in-top {
                from { transform: translateY(-100%); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            @keyframes slide-out-top {
                from { transform: translateY(0); opacity: 1; }
                to { transform: translateY(-100%); opacity: 0; }
            }
            @keyframes slide-in-bottom {
                from { transform: translateY(100%); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            @keyframes slide-out-bottom {
                from { transform: translateY(0); opacity: 1; }
                to { transform: translateY(100%); opacity: 0; }
            }
            @keyframes slide-in-left {
                from { transform: translateX(-100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            @keyframes slide-out-left {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(-100%); opacity: 0; }
            }
            @keyframes slide-in-right {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            @keyframes slide-out-right {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }
            @keyframes progress {
                from { width: 100%; }
                to { width: 0%; }
            }
            .animate-slide-in-top {
                animation: slide-in-top var(--animation-duration, 0.3s) ease-out forwards;
            }
            .animate-slide-out-top {
                animation: slide-out-top var(--animation-duration, 0.3s) ease-in forwards;
            }
            .animate-slide-in-bottom {
                animation: slide-in-bottom var(--animation-duration, 0.3s) ease-out forwards;
            }
            .animate-slide-out-bottom {
                animation: slide-out-bottom var(--animation-duration, 0.3s) ease-in forwards;
            }
            .animate-slide-in-left {
                animation: slide-in-left var(--animation-duration, 0.3s) ease-out forwards;
            }
            .animate-slide-out-left {
                animation: slide-out-left var(--animation-duration, 0.3s) ease-in forwards;
            }
            .animate-slide-in-right {
                animation: slide-in-right var(--animation-duration, 0.3s) ease-out forwards;
            }
            .animate-slide-out-right {
                animation: slide-out-right var(--animation-duration, 0.3s) ease-in forwards;
            }
            .progress-bar {
                animation: progress var(--progress-duration, 4s) linear forwards;
            }
        `;
        const styleSheet = document.createElement('style');
        styleSheet.textContent = styles;
        document.head.appendChild(styleSheet);
    }

    /**
     * Définit la position du conteneur des toasts.
     * @param {string} position - La position ('top-left', 'top-right', 'bottom-left', 'bottom-right').
     * @private
     */
    setPosition(position) {
        // Supprimer les styles de position existants
        this.toastContainer.style.top = '';
        this.toastContainer.style.right = '';
        this.toastContainer.style.bottom = '';
        this.toastContainer.style.left = '';

        // Appliquer la nouvelle position
        switch (position) {
            case 'top-left':
                this.toastContainer.style.top = '1rem';
                this.toastContainer.style.left = '1rem';
                break;
            case 'top-right':
                this.toastContainer.style.top = '1rem';
                this.toastContainer.style.right = '1rem';
                break;
            case 'bottom-left':
                this.toastContainer.style.bottom = '1rem';
                this.toastContainer.style.left = '1rem';
                break;
            case 'bottom-right':
                this.toastContainer.style.bottom = '1rem';
                this.toastContainer.style.right = '1rem';
                break;
            default:
                this.toastContainer.style.top = '1rem';
                this.toastContainer.style.right = '1rem'; // Par défaut : top-right
        }
    }

    /**
     * Crée une nouvelle instance de ToastBuilder pour configurer un toast.
     * @returns {ToastBuilder} Une nouvelle instance de ToastBuilder.
     * @example
     * toastManager.buildToast()
     *     .setMessage('Opération réussie !')
     *     .setType('success')
     *     .setPosition('bottom-right')
     *     .setDuration(6000)
     *     .show();
     */
    buildToast() {
        return new ToastBuilder(this);
    }

    /**
     * Affiche un toast avec la configuration spécifiée.
     * @private
     * @param {Object} config - La configuration du toast.
     * @param {string} config.message - Le message à afficher.
     * @param {string} [config.type='info'] - Le type de toast ('success', 'danger', 'warning', 'info').
     * @param {string} [config.position='top-right'] - La position ('top-left', 'top-right', 'bottom-left', 'bottom-right').
     * @param {number} [config.duration=4000] - La durée de la barre de progression et de la fermeture automatique en millisecondes.
     */
    showToast({ message, type = 'info', position = 'top-right', duration = 4000 }) {
        const toastStyles = {
            success: {
                id: 'toast-success',
                iconBg: 'text-green-500 bg-green-100',
                icon: `<svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z"/>
                </svg>`,
                textColor: 'text-gray-500',
                bg: 'bg-white',
                progressColor: 'bg-green-500',
                title: window.django?.gettext ? window.django.gettext('Succès') : 'Succès'
            },
            danger: {
                id: 'toast-danger',
                iconBg: 'text-red-500 bg-red-100',
                icon: `<svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 11.793a1 1 0 1 1-1.414 1.414L10 11.414l-2.293 2.293a1 1 0 0 1-1.414-1.414L8.586 10 6.293 7.707a1 1 0 0 1 1.414-1.414L10 8.586l2.293-2.293a1 1 0 0 1 1.414 1.414L11.414 10l2.293 2.293Z"/>
                </svg>`,
                textColor: 'text-gray-500',
                bg: 'bg-white',
                progressColor: 'bg-red-500',
                title: window.django?.gettext ? window.django.gettext('Erreur') : 'Erreur'
            },
            warning: {
                id: 'toast-warning',
                iconBg: 'text-orange-500 bg-orange-100',
                icon: `<svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM10 15a1 1 0 1 1 0-2 1 1 0 0 1 0 2Zm1-4a1 1 0 0 1-2 0V6a1 1 0 0 1 2 0v5Z"/>
                </svg>`,
                textColor: 'text-gray-500',
                bg: 'bg-white',
                progressColor: 'bg-orange-500',
                title: window.django?.gettext ? window.django.gettext('Avertissement') : 'Avertissement'
            },
            info: {
                id: 'toast-info',
                iconBg: 'text-blue-500 bg-blue-100',
                icon: `<svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
                    <path fill-rule="evenodd" d="M2 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10S2 17.523 2 12Zm9.408-5.5a1 1 0 1 0 0 2h.01a1 1 0 1 0 0-2h-.01ZM10 10a1 1 0 1 0 0 2h1v3h-1a1 1 0 1 0 0 2h4a1 1 0 1 0 0-2h-1v-4a1 1 0 0 0-1-1h-2Z" clip-rule="evenodd"/>
                </svg>`,
                textColor: 'text-gray-500',
                bg: 'bg-white',
                progressColor: 'bg-blue-500',
                title: window.django?.gettext ? window.django.gettext('Information') : 'Information'
            }
        };

        const style = toastStyles[type] || toastStyles.info;

        // Déterminer l'animation en fonction de la position
        let slideInAnimation, slideOutAnimation;
        switch (position) {
            case 'top-left':
                slideInAnimation = 'animate-slide-in-left';
                slideOutAnimation = 'animate-slide-out-left';
                break;
            case 'top-right':
                slideInAnimation = 'animate-slide-in-right';
                slideOutAnimation = 'animate-slide-out-right';
                break;
            case 'bottom-left':
                slideInAnimation = 'animate-slide-in-left';
                slideOutAnimation = 'animate-slide-out-left';
                break;
            case 'bottom-right':
                slideInAnimation = 'animate-slide-in-right';
                slideOutAnimation = 'animate-slide-out-right';
                break;
            default:
                slideInAnimation = 'animate-slide-in-right';
                slideOutAnimation = 'animate-slide-out-right';
        }

        // Créer l'élément du toast
        const toast = document.createElement('div');
        toast.id = style.id;
        toast.className = `flex items-center w-full max-w-xs p-4 mb-4 ${style.textColor} ${style.bg} rounded-lg shadow-sm ${slideInAnimation} relative border border-gray-200`;
        toast.setAttribute('role', 'alert');

        // Définir les durées d'animation personnalisées
        const animationDuration = Math.min(duration / 10, 500); // Limiter l'animation de glissement à 0,5s
        toast.style.setProperty('--animation-duration', `${animationDuration}ms`);
        toast.style.setProperty('--progress-duration', `${duration}ms`);

        toast.innerHTML = `
            <div class="flex flex-row justify-between w-full items-center">
                <div class="flex flex-row items-center">
                    <div class="inline-flex items-center justify-center shrink-0 w-8 h-8 ${style.iconBg} rounded-lg">
                        ${style.icon}
                        <span class="sr-only">${style.title} icon</span>
                    </div>
                    <div class="ms-3 text-sm font-normal">${message}</div>
                </div>
                <button type="button" class="-mx-1.5 -my-1.5 ms-1.5 bg-white text-gray-400 hover:text-gray-900 rounded-lg focus:ring-2 focus:ring-gray-300 p-1.5 hover:bg-gray-100 inline-flex items-center justify-center h-8 w-8" data-dismiss-target="#${style.id}" aria-label="${window.django?.gettext ? window.django.gettext('Fermer') : 'Fermer'}">
                    <span class="sr-only">${window.django?.gettext ? window.django.gettext('Fermer') : 'Fermer'}</span>
                    <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
                    </svg>
                </button>
            </div>
            <div class="absolute bottom-0 left-0 h-1 ${style.progressColor} progress-bar rounded-br-lg rounded-bl-lg"></div>
        `;

        this.toastContainer.appendChild(toast);
        this.setPosition(position);

        // Gestionnaire du bouton de fermeture
        const closeBtn = toast.querySelector('button[data-dismiss-target]');
        closeBtn.addEventListener('click', () => {
            toast.classList.remove(slideInAnimation);
            toast.classList.add(slideOutAnimation);
            setTimeout(() => toast.remove(), animationDuration);
        });

        // Fermeture automatique après la durée spécifiée
        setTimeout(() => {
            if (toast.parentElement) {
                toast.classList.remove(slideInAnimation);
                toast.classList.add(slideOutAnimation);
                setTimeout(() => toast.remove(), animationDuration);
            }
        }, duration);
    }

    /**
     * Ferme tous les toasts actuellement affichés.
     * @example
     * toastManager.closeAllToasts();
     */
    closeAllToasts() {
        const toasts = this.toastContainer.querySelectorAll('div');
        toasts.forEach(toast => {
            const slideInAnimation = Array.from(toast.classList).find(cls => cls.startsWith('animate-slide-in'));
            let slideOutAnimation = 'animate-slide-out-right'; // Par défaut
            if (slideInAnimation) {
                const direction = slideInAnimation.replace('animate-slide-in-', '');
                slideOutAnimation = `animate-slide-out-${direction}`;
            }

            // Obtenir la durée de l'animation du toast (par défaut 300ms si non défini)
            const animationDuration = parseFloat(toast.style.getPropertyValue('--animation-duration')) || 300;

            toast.classList.remove(slideInAnimation);
            toast.classList.add(slideOutAnimation);
            setTimeout(() => {
                if (toast.parentElement) {
                    toast.remove();
                }
            }, animationDuration);
        });
    }
}

/**
 * Classe builder pour configurer et afficher les toasts de manière fluide.
 * @class
 */
class ToastBuilder {
    /**
     * @param {ToastManager} manager - L'instance de ToastManager.
     */
    constructor(manager) {
        this.manager = manager;
        this.config = {
            message: '',
            type: 'info',
            position: 'top-right',
            duration: 4000 // Durée par défaut : 4 secondes
        };
    }

    /**
     * Définit le message du toast.
     * @param {string} message - Le message à afficher.
     * @returns {ToastBuilder} Cette instance du builder.
     */
    setMessage(message) {
        this.config.message = message;
        return this;
    }

    /**
     * Définit le type de toast.
     * @param {string} type - Le type de toast ('success', 'danger', 'warning', 'info').
     * @returns {ToastBuilder} Cette instance du builder.
     */
    setType(type) {
        this.config.type = type;
        return this;
    }

    /**
     * Définit la position du toast.
     * @param {string} position - La position ('top-left', 'top-right', 'bottom-left', 'bottom-right').
     * @returns {ToastBuilder} Cette instance du builder.
     */
    setPosition(position) {
        this.config.position = position;
        return this;
    }

    /**
     * Définit la durée de la barre de progression et de la fermeture automatique du toast.
     * @param {number} duration - La durée en millisecondes.
     * @returns {ToastBuilder} Cette instance du builder.
     */
    setDuration(duration) {
        this.config.duration = duration;
        return this;
    }

    /**
     * Affiche le toast configuré.
     * @example
     * toastManager.buildToast()
     *     .setMessage('Opération réussie !')
     *     .setType('success')
     *     .setPosition('bottom-right')
     *     .setDuration(6000)
     *     .show();
     */
    show() {
        if (!this.config.message) {
            throw new Error(window.django?.gettext ? window.django.gettext('Le message du toast est requis') : 'Le message du toast est requis');
        }
        this.manager.showToast(this.config);
    }
}

// Exporter une instance singleton
const toastManager = new ToastManager();
window.toastManager = toastManager;