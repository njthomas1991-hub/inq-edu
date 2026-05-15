// Theme Toggle Functionality
const themeToggleCheckbox = document.getElementById('themeToggleCheckbox');
const themeIconPanel = document.getElementById('themeIconPanel');
const html = document.documentElement;

// Check for saved theme preference or default to light
const currentTheme = localStorage.getItem('theme') || 'light';
if (currentTheme === 'dark') {
	html.setAttribute('data-theme', 'dark');
	if (themeToggleCheckbox) themeToggleCheckbox.checked = true;
	updateThemeIcon('dark');
} else {
	html.removeAttribute('data-theme');
	if (themeToggleCheckbox) themeToggleCheckbox.checked = false;
	updateThemeIcon('light');
}

function updateThemeIcon(theme) {
	if (!themeIconPanel) return;
	if (theme === 'dark') {
		themeIconPanel.classList.remove('fa-moon');
		themeIconPanel.classList.add('fa-sun');
	} else {
		themeIconPanel.classList.remove('fa-sun');
		themeIconPanel.classList.add('fa-moon');
	}
}

if (themeToggleCheckbox) {
	themeToggleCheckbox.addEventListener('change', function() {
		if (this.checked) {
			html.setAttribute('data-theme', 'dark');
			localStorage.setItem('theme', 'dark');
			updateThemeIcon('dark');
		} else {
			html.removeAttribute('data-theme');
			localStorage.setItem('theme', 'light');
			updateThemeIcon('light');
		}
	});
}

document.addEventListener('DOMContentLoaded', () => {

    /* ========================================
       AUTH PASSWORD TOGGLE
    ======================================== */

    const passwordToggleButtons =
        document.querySelectorAll(
            '.password-toggle'
        );

    passwordToggleButtons.forEach(
        (toggleButton) => {

            const wrapper =
                toggleButton.closest(
                    '.password-wrapper'
                );

            if (!wrapper) {
                return;
            }

            const passwordInput =
                wrapper.querySelector(
                    'input'
                );

            if (!passwordInput) {
                return;
            }

            toggleButton.addEventListener(
                'click',
                () => {

                    const isPassword =
                        passwordInput.type ===
                        'password';

                    passwordInput.type =
                        isPassword ? 'text' : 'password';

                    const icon =
                        toggleButton.querySelector(
                            'i'
                        );

                    if (icon) {
                        icon.className = isPassword
                            ? 'fa-solid fa-eye-slash'
                            : 'fa-solid fa-eye';
                    }

                }
            );

        }
    );

    /* ========================================
       ACCESSIBILITY PANEL
    ======================================== */

    const accessibilityToggle =
        document.getElementById(
            'accessibilityToggle'
        );

    const accessibilityPanel =
        document.getElementById(
            'accessibilityPanel'
        );

    const closeAccessibility =
        document.getElementById(
            'closeAccessibility'
        );

    function openAccessibilityPanel() {

        accessibilityPanel.classList.add(
            'active'
        );

        accessibilityToggle.setAttribute(
            'aria-expanded',
            'true'
        );

    }

    function closeAccessibilityPanel() {

        accessibilityToggle.focus();

        accessibilityPanel.classList.remove(
            'active'
        );

        accessibilityToggle.setAttribute(
            'aria-expanded',
            'false'
        );

    }

    if (
        accessibilityToggle &&
        accessibilityPanel
    ) {

        accessibilityToggle.addEventListener(
            'click',
            () => {

                const isOpen =
                    accessibilityPanel.classList.contains(
                        'active'
                    );

                if (isOpen) {

                    closeAccessibilityPanel();

                } else {

                    openAccessibilityPanel();

                }

            }
        );

    }

    if (closeAccessibility) {

        closeAccessibility.addEventListener(
            'click',
            closeAccessibilityPanel
        );

    }

    /* ========================================
       LARGE TEXT
    ======================================== */

    const largeTextToggle =
        document.getElementById(
            'largeTextToggle'
        );

    if (largeTextToggle) {

        if (
            localStorage.getItem(
                'largeText'
            ) === 'true'
        ) {

            document.body.classList.add(
                'large-text'
            );

            largeTextToggle.checked = true;

        }

        largeTextToggle.addEventListener(
            'change',
            function () {

                if (this.checked) {

                    document.body.classList.add(
                        'large-text'
                    );

                    localStorage.setItem(
                        'largeText',
                        'true'
                    );

                } else {

                    document.body.classList.remove(
                        'large-text'
                    );

                    localStorage.setItem(
                        'largeText',
                        'false'
                    );

                }

            }
        );

    }

    /* ========================================
       DARK MODE
    ======================================== */

    const darkModeToggle =
        document.getElementById(
            'darkModeToggle'
        );

    if (darkModeToggle) {

        if (
            localStorage.getItem(
                'theme'
            ) === 'dark'
        ) {

            document.documentElement.setAttribute(
                'data-theme',
                'dark'
            );

            darkModeToggle.checked = true;

        }

        darkModeToggle.addEventListener(
            'change',
            function () {

                if (this.checked) {

                    document.documentElement.setAttribute(
                        'data-theme',
                        'dark'
                    );

                    localStorage.setItem(
                        'theme',
                        'dark'
                    );

                } else {

                    document.documentElement.removeAttribute(
                        'data-theme'
                    );

                    localStorage.setItem(
                        'theme',
                        'light'
                    );

                }

            }
        );

    }

    /* ========================================
       REDUCED MOTION
    ======================================== */

    const reducedMotionToggle =
        document.getElementById(
            'reducedMotionToggle'
        );

    if (reducedMotionToggle) {

        reducedMotionToggle.addEventListener(
            'change',
            function () {

                const videos =
                    document.querySelectorAll(
                        'video'
                    );

                if (this.checked) {

                    videos.forEach(video => {

                        video.pause();

                    });

                    localStorage.setItem(
                        'reducedMotion',
                        'true'
                    );

                } else {

                    videos.forEach(video => {

                        video.play();

                    });

                    localStorage.setItem(
                        'reducedMotion',
                        'false'
                    );

                }

            }
        );

    }

    /* ========================================
       READING GUIDE
    ======================================== */

    const readingGuideToggle =
        document.getElementById(
            'readingGuideToggle'
        );

    const readingGuide =
        document.getElementById(
            'readingGuide'
        );

    if (
        readingGuideToggle &&
        readingGuide
    ) {

        readingGuideToggle.addEventListener(
            'change',
            function () {

                if (this.checked) {

                    readingGuide.style.display =
                        'block';

                } else {

                    readingGuide.style.display =
                        'none';

                }

            }
        );

        document.addEventListener(
            'mousemove',
            (e) => {

                if (
                    readingGuide.style.display
                    === 'block'
                ) {

                    readingGuide.style.top =
                        (e.clientY - 20) + 'px';

                }

            }
        );

    }

    /* ========================================
       UNDERLINE LINKS
    ======================================== */

    const underlineLinksToggle =
        document.getElementById(
            'underlineLinksToggle'
        );

    if (underlineLinksToggle) {

        if (
            localStorage.getItem(
                'underlineLinks'
            ) === 'true'
        ) {

            document.body.classList.add(
                'underline-links'
            );

            underlineLinksToggle.checked = true;

        }

        underlineLinksToggle.addEventListener(
            'change',
            function () {

                if (this.checked) {

                    document.body.classList.add(
                        'underline-links'
                    );

                    localStorage.setItem(
                        'underlineLinks',
                        'true'
                    );

                } else {

                    document.body.classList.remove(
                        'underline-links'
                    );

                    localStorage.setItem(
                        'underlineLinks',
                        'false'
                    );

                }

            }
        );

    }

});
