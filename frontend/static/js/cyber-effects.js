document.addEventListener('DOMContentLoaded', function() {
    // Добавляем эффект мерцания для неоновых элементов
    const neonElements = document.querySelectorAll('.neon-text');
    neonElements.forEach(element => {
        setInterval(() => {
            element.style.textShadow = Math.random() > 0.95 
                ? '0 0 7px var(--neon-blue), 0 0 10px var(--neon-blue), 0 0 21px var(--neon-blue)'
                : '0 0 5px var(--neon-blue), 0 0 10px var(--neon-blue)';
        }, 50);
    });

    // Добавляем эффект глитча при наведении на кнопки
    const cyberButtons = document.querySelectorAll('.cyber-button');
    cyberButtons.forEach(button => {
        button.addEventListener('mouseover', function() {
            this.style.transform = `translate(${Math.random() * 2 - 1}px, ${Math.random() * 2 - 1}px)`;
        });
        button.addEventListener('mouseout', function() {
            this.style.transform = 'none';
        });
    });
}); 