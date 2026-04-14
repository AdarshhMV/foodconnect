document.addEventListener('DOMContentLoaded', () => {
    document.body.classList.add('page-ready');
    window.setTimeout(() => {
        document.body.classList.add('loader-hidden');
    }, 220);

    const dismissToast = (toast) => {
        toast.classList.add('toast-dismiss');
        window.setTimeout(() => {
            toast.remove();
        }, 260);
    };

    document.querySelectorAll('.toast-message').forEach((toast, index) => {
        window.setTimeout(() => {
            toast.classList.add('toast-visible');
        }, 80 * (index + 1));

        const closeButton = toast.querySelector('.toast-message__close');
        if (closeButton) {
            closeButton.addEventListener('click', () => dismissToast(toast));
        }

        window.setTimeout(() => {
            if (document.body.contains(toast)) {
                dismissToast(toast);
            }
        }, 3600 + (index * 250));
    });

    document.querySelectorAll('button, .btn, a.custom-nav-link, .nav-action-btn').forEach((element) => {
        element.addEventListener('click', () => {
            element.classList.remove('is-clicked');
            window.requestAnimationFrame(() => {
                element.classList.add('is-clicked');
            });
        });
    });

    document.querySelectorAll('a[href]').forEach((link) => {
        const href = link.getAttribute('href');
        if (!href || href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:')) {
            return;
        }

        link.addEventListener('click', (event) => {
            if (
                event.defaultPrevented ||
                event.metaKey ||
                event.ctrlKey ||
                event.shiftKey ||
                event.altKey ||
                link.target === '_blank'
            ) {
                return;
            }

            const url = new URL(link.href, window.location.origin);
            if (url.origin !== window.location.origin) {
                return;
            }

            event.preventDefault();
            document.body.classList.add('page-exit');
            document.body.classList.remove('loader-hidden');
            window.setTimeout(() => {
                window.location.href = url.href;
            }, 180);
        });
    });

    document.querySelectorAll('form').forEach((form) => {
        form.addEventListener('submit', () => {
            document.body.classList.remove('loader-hidden');
        });
    });
});
