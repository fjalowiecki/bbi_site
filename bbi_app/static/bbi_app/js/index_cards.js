document.addEventListener('DOMContentLoaded', () => {
    const cardsContainer = document.getElementById('project-cards-container');
    if (!cardsContainer) return;

    const projectCards = Array.from(cardsContainer.getElementsByClassName('project-card'));
    const paginationDotsContainer = document.getElementById('pagination-dots');

    if (projectCards.length === 0 || !paginationDotsContainer) {
        if (paginationDotsContainer) paginationDotsContainer.style.display = 'none';
        return;
    }

    const dots = Array.from(paginationDotsContainer.getElementsByClassName('pagination-dot'));
    const cardsPerPage = 4;
    let currentPage = 0;
    let autoSwitchInterval;

    function showPage(pageNumber) {
        currentPage = pageNumber;
        const startIndex = pageNumber * cardsPerPage;
        const endIndex = startIndex + cardsPerPage;

        projectCards.forEach(card => {
            if (!card.classList.contains('hidden')) {
                card.classList.add('opacity-0');
            }
        });

        setTimeout(() => {
            projectCards.forEach((card, index) => {
                if (index >= startIndex && index < endIndex) {
                    card.classList.remove('hidden');
                    requestAnimationFrame(() => {
                        card.classList.remove('opacity-0');
                    });
                } else {
                    card.classList.add('hidden');
                    card.classList.add('opacity-0');
                }
            });
        }, 250);

        dots.forEach((dot, index) => {
            dot.classList.remove('outline', 'outline-2', 'outline-[rgb(241,189,51)]');
            if (index === pageNumber) {
                dot.classList.add('outline', 'outline-2', 'outline-[rgb(241,189,51)]');
            }
        });
    }

    function startAutoSwitch() {
        clearInterval(autoSwitchInterval);
        autoSwitchInterval = setInterval(() => {
            let nextPage = (currentPage + 1) % dots.length;
            showPage(nextPage);
        }, 5000);
    }

    dots.forEach(dot => {
        dot.addEventListener('click', (event) => {
            event.preventDefault();
            const page = parseInt(dot.dataset.page);
            showPage(page);
            startAutoSwitch();
        });
    });

    if (dots.length > 0) {
        showPage(0);
        startAutoSwitch();
    }
});