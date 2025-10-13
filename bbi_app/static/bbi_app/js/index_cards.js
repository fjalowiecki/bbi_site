document.addEventListener('DOMContentLoaded', function() {
    var cardsContainer = document.getElementById('project-cards-container');
    if (!cardsContainer) return;

    var projectCards = Array.from(cardsContainer.getElementsByClassName('project-card'));
    var paginationDotsContainer = document.getElementById('pagination-dots');

    if (projectCards.length === 0 || !paginationDotsContainer) {
        if (paginationDotsContainer) paginationDotsContainer.style.display = 'none';
        return;
    }

    var dots = Array.from(paginationDotsContainer.getElementsByClassName('pagination-dot'));
    var cardsPerPage = 4;
    var currentPage = 0;
    var autoSwitchInterval;
    var maxWidth = 0;
    
    // Oblicz maksymalną szerokość ze wszystkich widoków
    function calculateMaxWidth() {
        // Nie ustawiaj stałej szerokości na małych ekranach (mobile)
        var isMobile = window.innerWidth < 768;
        
        if (isMobile) {
            // Na mobile tylko pokaż pierwszą stronę
            showPage(0);
            return;
        }
        
        var calculatedMaxWidth = 0;
        
        // Sprawdź szerokość dla każdej strony
        for (var page = 0; page < dots.length; page++) {
            var startIndex = page * cardsPerPage;
            var endIndex = startIndex + cardsPerPage;
            
            // Pokaż tylko karty dla tej strony
            projectCards.forEach(function(card, index) {
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
            var currentWidth = cardsContainer.offsetWidth;
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
    setTimeout(function() {
        calculateMaxWidth();
        startAutoSwitch();
    }, 100);

    function showPage(pageNumber) {
        currentPage = pageNumber;
        var startIndex = pageNumber * cardsPerPage;
        var endIndex = startIndex + cardsPerPage;

        // Fade out wszystkie karty
        projectCards.forEach(function(card) {
            card.classList.add('opacity-0');
        });

        setTimeout(function() {
            projectCards.forEach(function(card, index) {
                if (index >= startIndex && index < endIndex) {
                    card.style.display = '';
                    card.style.visibility = 'visible';
                    card.style.position = 'relative';
                    requestAnimationFrame(function() {
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

        dots.forEach(function(dot, index) {
            dot.classList.remove('outline', 'outline-2', 'outline-[rgb(241,189,51)]');
            dot.setAttribute('aria-selected', 'false');
            if (index === pageNumber) {
                dot.classList.add('outline', 'outline-2', 'outline-[rgb(241,189,51)]');
                dot.setAttribute('aria-selected', 'true');
            }
        });
    }

    function startAutoSwitch() {
        clearInterval(autoSwitchInterval);
        autoSwitchInterval = setInterval(function() {
            var nextPage = (currentPage + 1) % dots.length;
            showPage(nextPage);
        }, 5000);
    }

    dots.forEach(function(dot) {
        dot.addEventListener('click', function(event) {
            event.preventDefault();
            var page = parseInt(dot.dataset.page);
            showPage(page);
            startAutoSwitch();
        });
    });

    // Obsługa swipe na mobile
    var touchStartX = 0;
    var touchEndX = 0;
    var minSwipeDistance = 50; // Minimalna odległość przesunięcia w pikselach

    cardsContainer.addEventListener('touchstart', function(e) {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    cardsContainer.addEventListener('touchend', function(e) {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    }, { passive: true });

    function handleSwipe() {
        var swipeDistance = touchEndX - touchStartX;
        
        if (Math.abs(swipeDistance) < minSwipeDistance) {
            return; // Zbyt krótkie przesunięcie - ignoruj
        }

        if (swipeDistance > 0) {
            // Swipe w prawo - poprzednia strona
            var prevPage = currentPage === 0 ? dots.length - 1 : currentPage - 1;
            showPage(prevPage);
        } else {
            // Swipe w lewo - następna strona
            var nextPage = (currentPage + 1) % dots.length;
            showPage(nextPage);
        }
        
        // Zrestartuj auto-switch po ręcznym przesunięciu
        startAutoSwitch();
    }

    // Obsługa zmiany rozmiaru okna
    var resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(function() {
            var isMobile = window.innerWidth < 768;
            
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