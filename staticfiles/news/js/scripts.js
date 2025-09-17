// JavaScript for BBC-style functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('BBC Blog loaded successfully');
    
    // Mobile menu functionality
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const mainNav = document.getElementById('mainNav');
    const navOverlay = document.getElementById('navOverlay');
    const closeMenuBtn = document.querySelector('.close-menu');
    
    if (mobileMenuBtn && mainNav) {
        mobileMenuBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            mainNav.classList.toggle('active');
            if (navOverlay) navOverlay.classList.toggle('active');
            
            // Change icon based on menu state
            if (mainNav.classList.contains('active')) {
                this.innerHTML = '✕';
                this.setAttribute('aria-label', 'Close menu');
            } else {
                this.innerHTML = '☰';
                this.setAttribute('aria-label', 'Open menu');
            }
        });
    }

    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
        if (mainNav && mainNav.classList.contains('active') &&
            !mainNav.contains(event.target) &&
            event.target !== mobileMenuBtn) {
            mainNav.classList.remove('active');
            if (navOverlay) navOverlay.classList.remove('active');
            if (mobileMenuBtn) {
                mobileMenuBtn.innerHTML = '☰';
                mobileMenuBtn.setAttribute('aria-label', 'Open menu');
            }
        }
    });

    // Prevent clicks inside the nav from closing it
    if (mainNav) {
        mainNav.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }

    // Close menu via overlay
    if (navOverlay) {
        navOverlay.addEventListener('click', function() {
            mainNav.classList.remove('active');
            this.classList.remove('active');
            if (mobileMenuBtn) {
                mobileMenuBtn.innerHTML = '☰';
                mobileMenuBtn.setAttribute('aria-label', 'Open menu');
            }
        });
    }

    // Close menu via "X" button
    if (closeMenuBtn && mainNav) {
        closeMenuBtn.addEventListener('click', function() {
            mainNav.classList.remove('active');
            if (navOverlay) navOverlay.classList.remove('active');
            if (mobileMenuBtn) {
                mobileMenuBtn.innerHTML = '☰';
                mobileMenuBtn.setAttribute('aria-label', 'Open menu');
            }
        });
    }

    // Search form enhancement
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const searchInput = this.querySelector('input[name="q"]');
            if (!searchInput.value.trim()) {
                e.preventDefault();
                searchInput.focus();
            }
        });
    }

    // Responsive image handling
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('load', function() {
            this.classList.add('loaded');
        });
        img.addEventListener('error', function() {
            this.style.display = 'none';
            console.log('Image failed to load:', this.src);
        });
    });

    // Add touch support for mobile devices
    let touchStartX = 0;
    let touchEndX = 0;

    document.addEventListener('touchstart', function(e) {
        touchStartX = e.changedTouches[0].screenX;
    });

    document.addEventListener('touchend', function(e) {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    });

    function handleSwipe() {
        // Swipe left to close menu
        if (mainNav && mainNav.classList.contains('active') && touchEndX < touchStartX - 50) {
            mainNav.classList.remove('active');
            if (navOverlay) navOverlay.classList.remove('active');
            if (mobileMenuBtn) {
                mobileMenuBtn.innerHTML = '☰';
                mobileMenuBtn.setAttribute('aria-label', 'Open menu');
            }
        }
    }
});



// const track = document.getElementById('bannerTrack');

// // Duplicate banners for seamless infinite scroll
// track.innerHTML += track.innerHTML;

// // Optional: adjust speed dynamically
// let position = 0;
// const speed = 0.5; // smaller number = slower

// function animate() {
//     position -= speed;
//     if (Math.abs(position) >= track.scrollWidth / 2) position = 0;
//     track.style.transform = `translateX(${position}px)`;
//     requestAnimationFrame(animate);
// }

// animate();