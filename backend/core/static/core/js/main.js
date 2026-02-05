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

// Accessibility Features
const accessibilityToggle = document.getElementById('accessibilityToggle');
const accessibilityPanel = document.getElementById('accessibilityPanel');
const closeAccessibility = document.getElementById('closeAccessibility');
const largTextToggle = document.getElementById('largTextToggle');
const dyslexiaToggle = document.getElementById('dyslexiaToggle');
const dyslexiaOptions = document.getElementById('dyslexiaOptions');
const dyslexiaOverlay = document.getElementById('dyslexiaOverlay');
const dyslexiaColorBtns = document.querySelectorAll('.dyslexia-color');
const textToSpeechToggle = document.getElementById('textToSpeechToggle');
const ttsControls = document.getElementById('ttsControls');
const speakPageBtn = document.getElementById('speakPageBtn');
const stopSpeakBtn = document.getElementById('stopSpeakBtn');
const speechToTextToggle = document.getElementById('speechToTextToggle');
const sttControls = document.getElementById('sttControls');
const startListeningBtn = document.getElementById('startListeningBtn');
const sttResult = document.getElementById('sttResult');

if (accessibilityToggle && accessibilityPanel) {
	accessibilityToggle.addEventListener('click', () => {
		accessibilityPanel.classList.toggle('active');
		if (accessibilityPanel.classList.contains('active')) {
			setTimeout(() => {
				const firstFocusable = accessibilityPanel.querySelector('input, button, [tabindex]:not([tabindex="-1"])');
				if (firstFocusable) firstFocusable.focus();
			}, 100);
		}
	});
}

if (closeAccessibility && accessibilityPanel && accessibilityToggle) {
	closeAccessibility.addEventListener('click', () => {
		accessibilityPanel.classList.remove('active');
		accessibilityToggle.focus();
	});
}

document.addEventListener('keydown', (e) => {
	if (e.key === 'Escape' && accessibilityPanel && accessibilityPanel.classList.contains('active')) {
		accessibilityPanel.classList.remove('active');
		if (accessibilityToggle) accessibilityToggle.focus();
	}
	if (e.altKey && e.key === 'a' && accessibilityToggle) {
		e.preventDefault();
		accessibilityToggle.click();
	}
});

if (accessibilityPanel) {
	const focusableElements = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';
	accessibilityPanel.addEventListener('keydown', (e) => {
		if (e.key === 'Tab') {
			const focusables = Array.from(accessibilityPanel.querySelectorAll(focusableElements));
			if (!focusables.length) return;
			const firstFocusable = focusables[0];
			const lastFocusable = focusables[focusables.length - 1];

			if (e.shiftKey) {
				if (document.activeElement === firstFocusable) {
					e.preventDefault();
					lastFocusable.focus();
				}
			} else {
				if (document.activeElement === lastFocusable) {
					e.preventDefault();
					firstFocusable.focus();
				}
			}
		}
	});
}

if (largTextToggle) {
	largTextToggle.addEventListener('change', function() {
		if (this.checked) {
			document.body.classList.add('large-text');
			localStorage.setItem('largeText', 'true');
		} else {
			document.body.classList.remove('large-text');
			localStorage.setItem('largeText', 'false');
		}
	});
}

if (dyslexiaToggle && dyslexiaOptions && dyslexiaOverlay) {
	dyslexiaToggle.addEventListener('change', function() {
		dyslexiaOptions.style.display = this.checked ? 'block' : 'none';
		if (this.checked) {
			dyslexiaOverlay.style.display = 'block';
			localStorage.setItem('dyslexiaMode', 'true');
		} else {
			dyslexiaOverlay.style.display = 'none';
			localStorage.setItem('dyslexiaMode', 'false');
		}
	});
}

dyslexiaColorBtns.forEach(btn => {
	btn.addEventListener('click', function() {
		if (!dyslexiaOverlay) return;
		const color = this.dataset.color;
		dyslexiaOverlay.style.backgroundColor = color;
		localStorage.setItem('dyslexiaColor', color);
	});
});

let isTTSActive = false;

if (textToSpeechToggle && ttsControls) {
	textToSpeechToggle.addEventListener('change', function() {
		isTTSActive = this.checked;
		ttsControls.style.display = this.checked ? 'block' : 'none';
		localStorage.setItem('textToSpeech', this.checked ? 'true' : 'false');

		if (isTTSActive) {
			document.body.style.cursor = 'pointer';
			document.body.classList.add('tts-active');
		} else {
			document.body.style.cursor = 'default';
			document.body.classList.remove('tts-active');
			window.speechSynthesis.cancel();
		}
	});
}

document.addEventListener('click', function(e) {
	if (!isTTSActive) return;

	const skipElements = ['button', 'input', '#accessibilityPanel', '.accessibility-toggle', '.navbar'];
	const target = e.target;

	if (skipElements.some(selector => {
		if (selector.startsWith('#') || selector.startsWith('.')) {
			return target.closest(selector);
		}
		return target.tagName.toLowerCase() === selector;
	})) {
		return;
	}

	if (target.closest('a, button, input, [role="button"]')) {
		return;
	}

	e.preventDefault();

	let textToSpeak = '';
	const selectedText = window.getSelection().toString().trim();

	if (selectedText) {
		textToSpeak = selectedText;
	} else {
		let container = target;
		while (container && !textToSpeak.trim()) {
			if (container.innerText && container.innerText.trim().length > 0) {
				textToSpeak = container.innerText.trim();
				if (textToSpeak.length > 500) {
					container = container.parentElement;
					textToSpeak = '';
					continue;
				}
				break;
			}
			container = container.parentElement;
		}
	}

	if (textToSpeak && textToSpeak.length > 0) {
		const utterance = new SpeechSynthesisUtterance(textToSpeak);
		utterance.rate = ttsSpeed;
		utterance.pitch = 1.0;
		utterance.volume = 1.0;
		window.speechSynthesis.speak(utterance);
	}
}, true);

if (speakPageBtn) {
	speakPageBtn.addEventListener('click', () => {
		const mainContent = document.getElementById('main-content');
		const textToSpeak = mainContent ? mainContent.innerText : document.body.innerText;

		if (textToSpeak.trim()) {
			const utterance = new SpeechSynthesisUtterance(textToSpeak);
			utterance.rate = ttsSpeed;
			utterance.pitch = 1.0;
			utterance.volume = 1.0;
			window.speechSynthesis.speak(utterance);
		}
	});
}

if (stopSpeakBtn) {
	stopSpeakBtn.addEventListener('click', () => {
		window.speechSynthesis.cancel();
	});
}

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = SpeechRecognition ? new SpeechRecognition() : null;

if (speechToTextToggle && sttControls) {
	speechToTextToggle.addEventListener('change', function() {
		sttControls.style.display = this.checked ? 'block' : 'none';
		localStorage.setItem('speechToText', this.checked ? 'true' : 'false');
	});
}

if (startListeningBtn && recognition && sttResult) {
	startListeningBtn.addEventListener('click', () => {
		sttResult.style.display = 'block';
		sttResult.textContent = 'Listening...';
		recognition.start();
	});

	recognition.addEventListener('result', (event) => {
		let transcript = '';
		for (let i = event.resultIndex; i < event.results.length; i++) {
			transcript += event.results[i][0].transcript;
		}
		sttResult.textContent = 'You said: ' + transcript;
	});

	recognition.addEventListener('error', () => {
		sttResult.textContent = 'Error: Speech recognition failed';
	});
}

function loadAccessibilityPreferences() {
	if (largTextToggle && localStorage.getItem('largeText') === 'true') {
		largTextToggle.checked = true;
		document.body.classList.add('large-text');
	}
	if (dyslexiaToggle && dyslexiaOverlay && dyslexiaOptions && localStorage.getItem('dyslexiaMode') === 'true') {
		dyslexiaToggle.checked = true;
		dyslexiaOverlay.style.display = 'block';
		dyslexiaOptions.style.display = 'block';
		const savedColor = localStorage.getItem('dyslexiaColor') || '#fff5cc';
		dyslexiaOverlay.style.backgroundColor = savedColor;
	}
	if (textToSpeechToggle && ttsControls && localStorage.getItem('textToSpeech') === 'true') {
		textToSpeechToggle.checked = true;
		ttsControls.style.display = 'block';
		isTTSActive = true;
		document.body.classList.add('tts-active');
	}
	if (speechToTextToggle && sttControls && localStorage.getItem('speechToText') === 'true') {
		speechToTextToggle.checked = true;
		sttControls.style.display = 'block';
	}
	if (localStorage.getItem('highContrast') === 'true') {
		const highContrast = document.getElementById('highContrastToggle');
		if (highContrast) highContrast.checked = true;
		document.body.classList.add('high-contrast');
	}
	if (localStorage.getItem('reducedMotion') === 'true') {
		const reducedMotion = document.getElementById('reducedMotionToggle');
		if (reducedMotion) reducedMotion.checked = true;
		document.body.classList.add('reduced-motion');
	}
	if (localStorage.getItem('readingGuide') === 'true') {
		const readingGuideToggle = document.getElementById('readingGuideToggle');
		const readingGuide = document.getElementById('readingGuide');
		const readingGuideColors = document.getElementById('readingGuideColors');
		if (readingGuideToggle) readingGuideToggle.checked = true;
		if (readingGuide) readingGuide.style.display = 'block';
		if (readingGuideColors) readingGuideColors.style.display = 'block';
	}
	const savedReadingGuideColor = localStorage.getItem('readingGuideColor') || 'cream';
	const readingGuide = document.getElementById('readingGuide');
	if (readingGuide) {
		readingGuide.classList.add('color-' + savedReadingGuideColor);
	}
	document.querySelector(`#readingGuideColors .color-btn[title="${savedReadingGuideColor.charAt(0).toUpperCase() + savedReadingGuideColor.slice(1)}"]`)?.classList.add('active');
	if (localStorage.getItem('focusMode') === 'true') {
		const focusModeToggle = document.getElementById('focusModeToggle');
		if (focusModeToggle) focusModeToggle.checked = true;
		document.body.classList.add('focus-mode');
	}
	if (localStorage.getItem('underlineLinks') === 'true') {
		const underlineLinksToggle = document.getElementById('underlineLinksToggle');
		if (underlineLinksToggle) underlineLinksToggle.checked = true;
		document.body.classList.add('underline-links');
	}
	const savedLetterSpacing = localStorage.getItem('letterSpacing');
	if (savedLetterSpacing) {
		const letterSpacingSlider = document.getElementById('letterSpacingSlider');
		if (letterSpacingSlider) letterSpacingSlider.value = savedLetterSpacing;
		document.documentElement.style.setProperty('--custom-letter-spacing', savedLetterSpacing + 'px');
		document.body.classList.add('custom-spacing');
	}
	const savedWordSpacing = localStorage.getItem('wordSpacing');
	if (savedWordSpacing) {
		const wordSpacingSlider = document.getElementById('wordSpacingSlider');
		if (wordSpacingSlider) wordSpacingSlider.value = savedWordSpacing;
		document.documentElement.style.setProperty('--custom-word-spacing', savedWordSpacing + 'px');
		document.body.classList.add('custom-spacing');
	}
	const savedTTSSpeed = localStorage.getItem('ttsSpeed');
	if (savedTTSSpeed) {
		const ttsSpeedSlider = document.getElementById('ttsSpeedSlider');
		const ttsSpeedValue = document.getElementById('ttsSpeedValue');
		if (ttsSpeedSlider) ttsSpeedSlider.value = savedTTSSpeed;
		if (ttsSpeedValue) ttsSpeedValue.textContent = savedTTSSpeed;
	}
	const savedColorFilter = localStorage.getItem('colorBlindnessFilter');
	if (savedColorFilter && savedColorFilter !== 'none') {
		const colorBlindnessFilter = document.getElementById('colorBlindnessFilter');
		if (colorBlindnessFilter) colorBlindnessFilter.value = savedColorFilter;
		document.body.classList.add('filter-' + savedColorFilter);
	}
	if (localStorage.getItem('widgitSymbols') === 'true') {
		const widgitSymbolsToggle = document.getElementById('widgitSymbolsToggle');
		if (widgitSymbolsToggle) widgitSymbolsToggle.checked = true;
		document.body.classList.add('widgit-active');
	}
}

const highContrastToggle = document.getElementById('highContrastToggle');
if (highContrastToggle) {
	highContrastToggle.addEventListener('change', function() {
		if (this.checked) {
			document.body.classList.add('high-contrast');
			localStorage.setItem('highContrast', 'true');
			announceToScreenReader('High contrast mode enabled');
		} else {
			document.body.classList.remove('high-contrast');
			localStorage.setItem('highContrast', 'false');
			announceToScreenReader('High contrast mode disabled');
		}
	});
}

const reducedMotionToggle = document.getElementById('reducedMotionToggle');
if (reducedMotionToggle) {
	reducedMotionToggle.addEventListener('change', function() {
		if (this.checked) {
			document.body.classList.add('reduced-motion');
			localStorage.setItem('reducedMotion', 'true');
			announceToScreenReader('Reduced motion enabled');
		} else {
			document.body.classList.remove('reduced-motion');
			localStorage.setItem('reducedMotion', 'false');
			announceToScreenReader('Reduced motion disabled');
		}
	});
}

const readingGuideToggle = document.getElementById('readingGuideToggle');
const readingGuide = document.getElementById('readingGuide');
const readingGuideColors = document.getElementById('readingGuideColors');
let currentReadingGuideColor = 'cream';

if (readingGuideToggle && readingGuide) {
	readingGuideToggle.addEventListener('change', function() {
		if (this.checked) {
			readingGuide.style.display = 'block';
			if (readingGuideColors) readingGuideColors.style.display = 'block';
			localStorage.setItem('readingGuide', 'true');
			announceToScreenReader('Reading guide enabled');
		} else {
			readingGuide.style.display = 'none';
			if (readingGuideColors) readingGuideColors.style.display = 'none';
			localStorage.setItem('readingGuide', 'false');
			announceToScreenReader('Reading guide disabled');
		}
	});
}

document.querySelectorAll('#readingGuideColors .color-btn').forEach(btn => {
	btn.addEventListener('click', (e) => {
		e.preventDefault();
		const colorName = btn.title.toLowerCase();
		if (readingGuide) {
			readingGuide.classList.remove('color-cream', 'color-blue', 'color-pink', 'color-green');
			readingGuide.classList.add('color-' + colorName);
		}
		currentReadingGuideColor = colorName;
		document.querySelectorAll('#readingGuideColors .color-btn').forEach(b => b.classList.remove('active'));
		btn.classList.add('active');
		localStorage.setItem('readingGuideColor', colorName);
		announceToScreenReader('Reading guide color changed to ' + colorName);
	});
});

document.addEventListener('mousemove', (e) => {
	if (readingGuide && readingGuide.style.display === 'block') {
		readingGuide.style.top = (e.clientY - 20) + 'px';
	}
});

const ttsSpeedSlider = document.getElementById('ttsSpeedSlider');
const ttsSpeedValue = document.getElementById('ttsSpeedValue');
let ttsSpeed = 1.0;

if (ttsSpeedSlider && ttsSpeedValue) {
	ttsSpeedSlider.addEventListener('input', function() {
		ttsSpeed = parseFloat(this.value);
		ttsSpeedValue.textContent = ttsSpeed.toFixed(1);
		localStorage.setItem('ttsSpeed', ttsSpeed);
	});
}

function speakText(text) {
	const utterance = new SpeechSynthesisUtterance(text);
	utterance.rate = ttsSpeed;
	utterance.pitch = 1.0;
	utterance.volume = 1.0;
	window.speechSynthesis.speak(utterance);
}

const focusModeToggle = document.getElementById('focusModeToggle');
if (focusModeToggle) {
	focusModeToggle.addEventListener('change', function() {
		if (this.checked) {
			document.body.classList.add('focus-mode');
			localStorage.setItem('focusMode', 'true');
			announceToScreenReader('Focus mode enabled');
			enableFocusMode();
		} else {
			document.body.classList.remove('focus-mode');
			localStorage.setItem('focusMode', 'false');
			announceToScreenReader('Focus mode disabled');
			disableFocusMode();
		}
	});
}

function enableFocusMode() {
	document.addEventListener('mouseover', highlightFocusedElement);
}

function disableFocusMode() {
	document.removeEventListener('mouseover', highlightFocusedElement);
	document.querySelectorAll('.focus-active').forEach(el => {
		el.classList.remove('focus-active');
	});
}

function highlightFocusedElement(e) {
	document.querySelectorAll('.focus-active').forEach(el => {
		el.classList.remove('focus-active');
	});
	const target = e.target.closest('p, h1, h2, h3, h4, h5, h6, section, article, div.card, li');
	if (target) {
		target.classList.add('focus-active');
	}
}

const underlineLinksToggle = document.getElementById('underlineLinksToggle');
if (underlineLinksToggle) {
	underlineLinksToggle.addEventListener('change', function() {
		if (this.checked) {
			document.body.classList.add('underline-links');
			localStorage.setItem('underlineLinks', 'true');
			announceToScreenReader('All links underlined');
		} else {
			document.body.classList.remove('underline-links');
			localStorage.setItem('underlineLinks', 'false');
			announceToScreenReader('Link underlines removed');
		}
	});
}

const letterSpacingSlider = document.getElementById('letterSpacingSlider');
const letterSpacingValue = document.getElementById('letterSpacingValue');
if (letterSpacingSlider && letterSpacingValue) {
	letterSpacingSlider.addEventListener('input', function() {
		const value = this.value;
		letterSpacingValue.textContent = value;
		document.documentElement.style.setProperty('--custom-letter-spacing', value + 'px');
		document.body.classList.add('custom-spacing');
		localStorage.setItem('letterSpacing', value);
	});
}

const wordSpacingSlider = document.getElementById('wordSpacingSlider');
const wordSpacingValue = document.getElementById('wordSpacingValue');
if (wordSpacingSlider && wordSpacingValue) {
	wordSpacingSlider.addEventListener('input', function() {
		const value = this.value;
		wordSpacingValue.textContent = value;
		document.documentElement.style.setProperty('--custom-word-spacing', value + 'px');
		document.body.classList.add('custom-spacing');
		localStorage.setItem('wordSpacing', value);
	});
}

const colorBlindnessFilter = document.getElementById('colorBlindnessFilter');
if (colorBlindnessFilter) {
	colorBlindnessFilter.addEventListener('change', function() {
		document.body.classList.remove('filter-protanopia', 'filter-deuteranopia', 'filter-tritanopia', 'filter-achromatopsia');
		if (this.value !== 'none') {
			document.body.classList.add('filter-' + this.value);
			localStorage.setItem('colorBlindnessFilter', this.value);
			announceToScreenReader(this.options[this.selectedIndex].text + ' filter enabled');
		} else {
			localStorage.setItem('colorBlindnessFilter', 'none');
			announceToScreenReader('Color filter disabled');
		}
	});
}

const pauseAllMediaBtn = document.getElementById('pauseAllMediaBtn');
if (pauseAllMediaBtn) {
	pauseAllMediaBtn.addEventListener('click', function() {
		document.querySelectorAll('video').forEach(video => {
			video.pause();
		});
		document.querySelectorAll('audio').forEach(audio => {
			audio.pause();
		});
		if (!document.body.classList.contains('reduced-motion')) {
			document.body.classList.add('reduced-motion');
			setTimeout(() => {
				document.body.classList.remove('reduced-motion');
			}, 100);
		}
		announceToScreenReader('All media paused');
	});
}

function announceToScreenReader(message) {
	const ariaLiveRegion = document.getElementById('ariaLiveRegion');
	if (!ariaLiveRegion) return;
	ariaLiveRegion.textContent = message;
	setTimeout(() => {
		ariaLiveRegion.textContent = '';
	}, 1000);
}

const widgitToggle = document.getElementById('widgitToggle');
if (widgitToggle) {
	widgitToggle.addEventListener('change', function() {
		if (this.checked) {
			document.body.classList.add('widgit-active');
			localStorage.setItem('widgitSymbols', 'true');
			announceToScreenReader('Widgit symbols enabled');
		} else {
			document.body.classList.remove('widgit-active');
			localStorage.setItem('widgitSymbols', 'false');
			announceToScreenReader('Widgit symbols disabled');
		}
	});
}

loadAccessibilityPreferences();
