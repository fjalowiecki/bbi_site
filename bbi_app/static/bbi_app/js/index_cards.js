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
    let maxWidth = 0;
    
    // Oblicz maksymalną szerokość ze wszystkich widoków
    function calculateMaxWidth() {
        // Nie ustawiaj stałej szerokości na małych ekranach (mobile)
        const isMobile = window.innerWidth < 768;
        
        if (isMobile) {
            // Na mobile tylko pokaż pierwszą stronę
            showPage(0);
            return;
        }
        
        let calculatedMaxWidth = 0;
        
        // Sprawdź szerokość dla każdej strony
        for (let page = 0; page < dots.length; page++) {
            const startIndex = page * cardsPerPage;
            const endIndex = startIndex + cardsPerPage;
            
            // Pokaż tylko karty dla tej strony
            projectCards.forEach((card, index) => {
                if (index >= startIndex && index < endIndex) {
                    card.style.display = '';
                    card.style.visibility = 'visible';
                    card.style.position = 'relative';
                } else {
                    card.style.display = 'none';
                }
            });
            
            // Wymuszenie przeliczenia layoutu
            cardsContainer.offsetHeight;
            
            // Zapisz szerokość
            const currentWidth = cardsContainer.offsetWidth;
            if (currentWidth > calculatedMaxWidth) {
                calculatedMaxWidth = currentWidth;
            }
        }
        
        // Ustaw stałą szerokość tylko na desktop
        if (calculatedMaxWidth > 0) {
            cardsContainer.style.width = calculatedMaxWidth + 'px';
            cardsContainer.style.minWidth = calculatedMaxWidth + 'px';
            cardsContainer.style.maxWidth = calculatedMaxWidth + 'px';
        }
        
        maxWidth = calculatedMaxWidth;
        
        // Przywróć widok pierwszej strony
        showPage(0);
    }
    
    // Oblicz maksymalną szerokość po załadowaniu
    setTimeout(() => {
        calculateMaxWidth();
        startAutoSwitch();
    }, 100);

    function showPage(pageNumber) {
        currentPage = pageNumber;
        const startIndex = pageNumber * cardsPerPage;
        const endIndex = startIndex + cardsPerPage;

        // Fade out wszystkie karty
        projectCards.forEach(card => {
            card.classList.add('opacity-0');
        });

        setTimeout(() => {
            projectCards.forEach((card, index) => {
                if (index >= startIndex && index < endIndex) {
                    card.style.display = '';
                    card.style.visibility = 'visible';
                    card.style.position = 'relative';
                    requestAnimationFrame(() => {
                        card.classList.remove('opacity-0');
                    });
                } else {
                    card.style.display = 'none';
                    card.style.visibility = 'hidden';
                    card.style.position = 'absolute';
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

    // Obsługa swipe na mobile
    let touchStartX = 0;
    let touchEndX = 0;
    const minSwipeDistance = 50; // Minimalna odległość przesunięcia w pikselach

    cardsContainer.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    cardsContainer.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    }, { passive: true });

    function handleSwipe() {
        const swipeDistance = touchEndX - touchStartX;
        
        if (Math.abs(swipeDistance) < minSwipeDistance) {
            return; // Zbyt krótkie przesunięcie - ignoruj
        }

        if (swipeDistance > 0) {
            // Swipe w prawo - poprzednia strona
            const prevPage = currentPage === 0 ? dots.length - 1 : currentPage - 1;
            showPage(prevPage);
        } else {
            // Swipe w lewo - następna strona
            const nextPage = (currentPage + 1) % dots.length;
            showPage(nextPage);
        }
        
        // Zrestartuj auto-switch po ręcznym przesunięciu
        startAutoSwitch();
    }

    // Obsługa zmiany rozmiaru okna
    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            const isMobile = window.innerWidth < 768;
            
            if (isMobile) {
                // Usuń stałą szerokość na mobile
                cardsContainer.style.width = '';
                cardsContainer.style.minWidth = '';
                cardsContainer.style.maxWidth = '';
            } else {
                // Przelicz szerokość na desktop
                calculateMaxWidth();
            }
        }, 250);
    });
});