    document.addEventListener('DOMContentLoaded', async () => {
        let preguntas = [];
        try {
            const res = await fetch('/api/Faq');
            if (!res.ok) throw new Error(`Error status: ${res.status}`);
            preguntas = await res.json();
        } catch (e) {
            console.error('Error al cargar preguntas frecuentes:', e);
            return;
        }

        const faqSection = document.querySelector('.faq-section');
        if (!faqSection) return;

        const accordion = document.createElement('div');
        accordion.classList.add('accordion');

        preguntas.forEach(pregunta => {
            const item = document.createElement('div');
            item.classList.add('accordion-item');

            item.innerHTML = `
        <div class="accordion-header" data-toggle="collapse">
            ${pregunta.titulo}
            <span class="accordion-icon"><i class="fa-solid fa-chevron-down"></i></span>
        </div>
        <div class="accordion-content">${pregunta.descripcion}</div>
        `;

            accordion.appendChild(item);
        });

        faqSection.innerHTML = '';
        faqSection.appendChild(accordion);

        initAccordion();
    });

    function initAccordion() {
        const headers = document.querySelectorAll('.accordion-header');
        headers.forEach(header => {
            header.addEventListener('click', function () {
                const isActive = this.classList.contains('active');
                document.querySelectorAll('.accordion-header').forEach(h => h.classList.remove('active'));
                document.querySelectorAll('.accordion-content').forEach(c => c.classList.remove('show'));
                if (!isActive) {
                    this.classList.add('active');
                    this.nextElementSibling.classList.add('show');
                }
            });
        });
    }
