document.addEventListener('DOMContentLoaded', () => {
	const boxCount = 6;
	const container = document.getElementById('code-input');

	for (let i = 0; i < boxCount; i++) {
		const input = document.createElement('input');
		input.type = 'text';
		input.maxLength = 1;
		input.className = 'code-box form-control';
		container.appendChild(input);
	}

	const boxes = container.querySelectorAll('.code-box');
	const submitBtn = document.getElementById('submit-btn');
	const hiddenInput = document.getElementById('full-code');

	function updateFullCode() {
		const code = [...boxes].map(b => b.value.trim().toUpperCase()).join('');
		hiddenInput.value = code;
		submitBtn.disabled = !(code.length === boxes.length && /^[A-Z0-9]{6}$/.test(code));
	}

	boxes.forEach((box, idx) => {
		box.addEventListener('input', () => {
			box.value = box.value.toUpperCase().replace(/[^A-Z0-9]/g, '');
			if (box.value && idx < boxes.length - 1) {
				boxes[idx + 1].focus();
			}
			updateFullCode();
		});

		box.addEventListener('keydown', (e) => {
			if (e.key === 'Backspace' && box.value === '' && idx > 0) {
				boxes[idx - 1].focus();
			} else if (e.key.length === 1) {
				box.value = '';
			}
			setTimeout(updateFullCode, 0);
		});

		box.addEventListener('paste', (e) => {
			e.preventDefault();
			const pasteData = (e.clipboardData || window.clipboardData).getData('text');
			const code = pasteData.trim().toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, boxCount);

			[...code].forEach((char, i) => {
				boxes[i].value = char;
			});

			if (boxes[code.length - 1]) {
				boxes[code.length - 1].focus();
			}

			updateFullCode();
		});
	});

	boxes[0].focus();
	updateFullCode(); // Ensure everything starts clean
});
