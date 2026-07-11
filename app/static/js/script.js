// ===== ПЕРЕКЛЮЧАТЕЛЬ ТЕМЫ =====
const themeToggle = document.getElementById('themeToggle');
const currentTheme = localStorage.getItem('theme') || 'dark';

document.documentElement.setAttribute('data-theme', currentTheme);
updateThemeIcon(currentTheme);

themeToggle.addEventListener('click', function() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);

    this.style.transform = 'rotate(360deg)';
    setTimeout(() => { this.style.transform = ''; }, 300);
});

function updateThemeIcon(theme) {
    const icon = themeToggle.querySelector('i');
    if (theme === 'dark') {
        icon.className = 'fas fa-sun';
    } else {
        icon.className = 'fas fa-moon';
    }
}

// ===== RIPPLE-ЭФФЕКТ =====
document.querySelector('.submit-btn').addEventListener('click', function(e) {
    const oldRipple = this.querySelector('.ripple');
    if (oldRipple) oldRipple.remove();

    const ripple = document.createElement('span');
    ripple.className = 'ripple';

    const rect = this.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = e.clientX - rect.left - size / 2;
    const y = e.clientY - rect.top - size / 2;

    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';

    this.appendChild(ripple);
    setTimeout(() => { ripple.remove(); }, 600);
});

// ===== ОТПРАВКА ФОРМЫ =====
document.getElementById('orderForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const form = this;
    const resultDiv = document.getElementById('result');
    resultDiv.classList.add('hidden');

    const btn = document.getElementById('submitBtn');
    btn.disabled = true;
    btn.querySelector('.btn-content').innerHTML = '<i class="fas fa-spinner"></i> ОТПРАВКА...';

    try {
        const formData = new FormData(form);
        const response = await fetch('/api/order', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            resultDiv.className = 'success';
            resultDiv.innerHTML = '✅ Заявка принята! Мы перезвоним вам в ближайшее время.';
            form.reset();
        } else {
            resultDiv.className = 'error';
            let errorMsg = 'Попробуйте еще раз';
            if (data.detail) {
                if (typeof data.detail === 'string') {
                    errorMsg = data.detail;
                } else if (Array.isArray(data.detail)) {
                    errorMsg = data.detail.map(d => d.msg || d).join(', ');
                }
            }
            resultDiv.innerHTML = '❌ Ошибка: ' + errorMsg;
        }
    } catch (error) {
        resultDiv.className = 'error';
        resultDiv.innerHTML = '❌ Ошибка соединения. Проверьте интернет.';
    } finally {
        resultDiv.classList.remove('hidden');
        btn.disabled = false;
        btn.querySelector('.btn-content').innerHTML = '<i class="fas fa-paper-plane"></i> ОТПРАВИТЬ ЗАЯВКУ';
    }
});