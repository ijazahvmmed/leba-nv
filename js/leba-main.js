
// Initialize GSAP ScrollTrigger
gsap.registerPlugin(ScrollTrigger);

// Initialize Three.js Background (Subtle Grid)
function initThreeJS() {
    const canvas = document.createElement('canvas');
    canvas.id = 'bg-canvas';
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.zIndex = '-1';
    canvas.style.pointerEvents = 'none';
    document.body.appendChild(canvas);

    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 5;

    // Create Particles
    const geometry = new THREE.BufferGeometry();
    const particlesCount = 500;
    const posArray = new Float32Array(particlesCount * 3);

    for (let i = 0; i < particlesCount * 3; i++) {
        posArray[i] = (Math.random() - 0.5) * 15;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
    const material = new THREE.PointsMaterial({
        size: 0.005,
        color: 0x222222, // Dark grey for subtle effect
    });

    const particlesMesh = new THREE.Points(geometry, material);
    scene.add(particlesMesh);

    // Mouse Interaction
    let mouseX = 0;
    let mouseY = 0;

    document.addEventListener('mousemove', (event) => {
        mouseX = event.clientX;
        mouseY = event.clientY;
    });

    const clock = new THREE.Clock();

    function animate() {
        const elapsedTime = clock.getElapsedTime();

        particlesMesh.rotation.y = elapsedTime * 0.05;
        particlesMesh.rotation.x = mouseY * 0.0001;
        particlesMesh.rotation.y += mouseX * 0.0001;

        renderer.render(scene, camera);
        requestAnimationFrame(animate);
    }

    animate();

    // Handle Resize
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
}

function initSmoothScroll() {
    // Dynamically load Lenis if appropriate, or user can add <script src="https://unpkg.com/@studio-freight/lenis@1.0.42/dist/lenis.min.js"></script>
    if (typeof Lenis === 'undefined') {
        const script = document.createElement('script');
        script.src = 'https://unpkg.com/@studio-freight/lenis@1.0.42/dist/lenis.min.js';
        script.onload = startLenis;
        document.head.appendChild(script);
    } else {
        startLenis();
    }

    function startLenis() {
        const lenis = new Lenis({
            duration: 1.2,
            easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
            direction: 'vertical',
            gestureDirection: 'vertical',
            smooth: true,
            mouseMultiplier: 1,
            smoothTouch: false,
            touchMultiplier: 2,
        });

        function raf(time) {
            lenis.raf(time);
            requestAnimationFrame(raf);
        }

        requestAnimationFrame(raf);

        // Integrate with GSAP ScrollTrigger
        if (typeof ScrollTrigger !== 'undefined') {
            lenis.on('scroll', ScrollTrigger.update);
            gsap.ticker.add((time) => {
                lenis.raf(time * 1000);
            });
            gsap.ticker.lagSmoothing(0);
        }
    }
}

function initAnimations() {
    if (typeof gsap === 'undefined') return;

    // Load Sequence
    const tl = gsap.timeline();

    // Site Header Drop (Smooth & Slow)
    tl.from('.site-header', {
        y: -100,
        opacity: 0,
        duration: 1.2,
        ease: 'power4.out',
        delay: 0.2
    });

    // Panel Reveals (The "Whispery" Flow)
    // We target both specific review panels and general panels if they don't have the class yet, 
    // but primarily likely .reveal-panel which we should ensure exists in HTML or add dynamically.
    // Given the HTML structure, we might need to target sections generically if classes are missing, 
    // but better to stick to the 'reveal-panel' hook which was used before.

    const panels = document.querySelectorAll('.reveal-panel, section.panel');
    panels.forEach(panel => {
        gsap.fromTo(panel,
            {
                y: 100,
                opacity: 0,
                scale: 0.98
            },
            {
                scrollTrigger: {
                    trigger: panel,
                    start: "top 85%", // Smooth entry point
                    toggleActions: "play none none reverse"
                },
                y: 0,
                opacity: 1,
                scale: 1,
                duration: 1.4, // Slower duration for "whispery" feel
                ease: 'power3.out'
            }
        );
    });

    // Text Reveals with Blur (The Signature Effect)
    // We target headings and paragraphs inside panels to give them that specific flow
    // independent of the panel reveal for extra smoothness.
    const textElements = document.querySelectorAll('.main-wrapper h1, .main-wrapper h2, .main-wrapper p:not(.nav-links a)');

    textElements.forEach(text => {
        gsap.fromTo(text,
            {
                filter: 'blur(15px)', // Soft blur
                y: 40,
                opacity: 0
            },
            {
                scrollTrigger: {
                    trigger: text,
                    start: "top 92%",
                    toggleActions: "play none none reverse"
                },
                filter: 'blur(0px)',
                y: 0,
                opacity: 1,
                duration: 1.8, // Long, luxurious duration
                ease: 'expo.out' // "Whispery" settling
            }
        );
    });

    // Image Reveals (Parallax-ish drift)
    const images = document.querySelectorAll('.card-img-container img, .panel img');
    images.forEach(img => {
        gsap.fromTo(img,
            { scale: 1.1, opacity: 0.5 },
            {
                scrollTrigger: { trigger: img, start: "top 90%" },
                scale: 1,
                opacity: 1,
                duration: 1.5,
                ease: "power2.out"
            }
        );
    });
}

function initMobileMenu() {
    const hamburger = document.querySelector('.hamburger');
    const overlay = document.querySelector('.mobile-nav-overlay');

    if (hamburger && overlay) {
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('active');
            overlay.classList.toggle('active');
        });
    }
}

// Simple Lightbox Implementation
function initLightbox() {
    // 1. Create Lightbox DOM Elements
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox-overlay';
    lightbox.innerHTML = `
        <div class='lightbox-close'>&times;</div>
        <img class='lightbox-content' src='' alt='Preview'>
    `;
    document.body.appendChild(lightbox);

    const lightboxImg = lightbox.querySelector('.lightbox-content');
    const closeBtn = lightbox.querySelector('.lightbox-close');

    // 2. Select all links that point to images
    const imageLinks = document.querySelectorAll('a[href$=".jpg"], a[href$=".jpeg"], a[href$=".png"], a[href$=".webp"]');

    imageLinks.forEach(link => {
        // Exclude logo
        if (link.closest('.nav-logo')) return;

        link.addEventListener('click', (e) => {
            e.preventDefault();
            const src = link.getAttribute('href');
            lightboxImg.src = src;
            lightbox.classList.add('active');
        });
    });

    // 3. Close Logic
    lightbox.addEventListener('click', (e) => {
        if (e.target !== lightboxImg) {
            lightbox.classList.remove('active');
        }
    });
}

window.addEventListener('load', () => {
    initThreeJS();
    initSmoothScroll();
    initAnimations();
    initMobileMenu();
    initLightbox();
});
