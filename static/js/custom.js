// Custom JavaScript for Dr. Mário Wolak Website

document.addEventListener('DOMContentLoaded', function () {

    // --- 1. EFEITOS DA NAVBAR E SCROLL SUAVE ---
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', function () {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const offsetTop = target.offsetTop - 80; // Ajuste para a altura da navbar fixa
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });

    // --- 2. LÓGICA DOS FLIP CARDS (CORRIGIDA E SIMPLIFICADA) ---
    const flipCards = document.querySelectorAll('.flip-card');
    flipCards.forEach(card => {
        // Função para virar o card
        const toggleFlip = () => {
            card.classList.toggle('flipped');
        };

        // Adiciona o evento de clique
        card.addEventListener('click', toggleFlip);

        // Adiciona acessibilidade para teclado (teclas Enter e Espaço)
        card.setAttribute('tabindex', '0'); // Permite que o elemento seja focado
        card.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault(); // Previne o scroll da página ao usar a barra de espaço
                toggleFlip();
            }
        });
    });

    // --- 3. LÓGICA DA GALERIA (CORRIGIDO) ---

    // Seleciona TODOS os elementos que podem ser a imagem principal
    const mainImages = document.querySelectorAll('.gallery-main-image');
    const galleryTitle = document.getElementById('gallery-title');
    const galleryDescription = document.getElementById('gallery-description');
    // Seleciona todas as miniaturas
    const thumbnails = document.querySelectorAll('.gallery-thumb');

    if (mainImages.length > 0 && thumbnails.length > 0) {
        thumbnails.forEach(thumb => {
            thumb.addEventListener('click', () => {
                // Atualiza a imagem principal, o título e a descrição
                // Itera sobre todas as imagens principais e atualiza o 'src' e o 'alt' de cada uma.
                // Apenas a que estiver visível na tela será mostrada ao usuário.
                mainImages.forEach(img => {
                    img.src = thumb.src;
                    img.alt = thumb.alt;
                });

                if (galleryTitle) galleryTitle.textContent = thumb.dataset.title;
                if (galleryDescription) galleryDescription.textContent = thumb.dataset.description;

                // Lógica mais robusta para atualizar a miniatura ativa:
                // 1. Remove a classe 'active' de TODAS as miniaturas.
                thumbnails.forEach(t => t.classList.remove('active'));
                // 2. Adiciona a classe 'active' apenas na miniatura que foi clicada.
                thumb.classList.add('active');
            });
        });
    }

    // --- 4. ANIMAÇÃO DE ENTRADA (SEM CONFLITOS) ---
    // Esta lógica cria um efeito de "fade in" para os cards sem usar a propriedade 'transform'
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                observer.unobserve(entry.target); // Anima apenas uma vez
            }
        });
    }, { threshold: 0.1 }); // A animação começa quando 10% do card está visível

    // Aplica o estado inicial e começa a observar os cards
    document.querySelectorAll('.flip-card').forEach(card => {
        card.style.opacity = '0'; // Começa invisível
        card.style.transition = 'opacity 0.8s ease'; // Define a suavidade da transição
        observer.observe(card);
    });

    // --- 5. LÓGICA DO FORMULÁRIO DE CONTATO (COM BACKEND DJANGO) ---
    const contactForm = document.querySelector('#forms form'); // Mantenha seu seletor

    if (contactForm) {
        // Pega o token CSRF do input que o Django gerou
        const csrftoken = contactForm.querySelector('[name=csrfmiddlewaretoken]').value;

        contactForm.addEventListener('submit', function (e) {
            e.preventDefault(); // Impede o envio tradicional do formulário
            const submitBtn = this.querySelector('button[type="submit"]');

            // Altera o estado do botão para "Enviando..."
            submitBtn.innerHTML = '<i class="bi bi-hourglass-split"></i> Enviando...';
            submitBtn.disabled = true;

            // Coleta os dados do formulário
            const formData = new FormData(this);

            // Envia os dados para a sua URL do Django
            fetch('/agendar-consulta/', { // A URL que você criou no urls.py
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken // Envia o token de segurança no cabeçalho
                },
                body: formData
            })
                .then(response => response.json()) // Converte a resposta do servidor para JSON
                .then(data => {
                    // Verifica a resposta do seu servidor Django
                    if (data.status === 'success') {
                        alert('Mensagem enviada com sucesso!');
                        this.reset(); // Limpa o formulário
                    } else {
                        // Mostra a mensagem de erro vinda do Django
                        alert('Ocorreu um erro: ' + data.message);
                        console.error('Erro do Backend:', data.message);
                    }
                })
                .catch(error => {
                    // Erro de rede ou na comunicação
                    alert('Ocorreu um erro de comunicação. Tente novamente.');
                    console.error('Erro no Fetch:', error);
                })
                .finally(() => {
                    // Este bloco sempre executa, seja com sucesso ou erro
                    // Restaura o botão
                    submitBtn.innerHTML = '<i class="bi bi-send"></i> Enviar Mensagem';
                    submitBtn.disabled = false;
                });
        });
    }

    // --- 6. FECHAR MENU MOBILE AO CLICAR ---
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    if (navbarCollapse) {
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (navbarCollapse.classList.contains('show')) {
                    new bootstrap.Collapse(navbarCollapse).hide();
                }
            });
        });
    }
});
