/**
 * PD LAB — Laboratório Interativo de Programação Dinâmica
 * Módulos JavaScript Compartilhados (shared.js)
 * 
 * Contém exclusivamente utilitários globais:
 * - ThemeManager: gerenciamento e persistência de tema claro/escuro
 * - Navigation: controle de rotas ativas e acessibilidade do menu
 * - Storage: wrapper defensivo para localStorage
 * - AnimationUtils: utilitários de animação e controlador de passos
 * - DOMUtils: helpers funcionais para manipulação de DOM
 */

(function (window, document) {
  'use strict';

  // Namespace global PDLab
  const PDLab = window.PDLab || {};

  /* -------------------------------------------------------------------------
   * 1. STORAGE: Armazenamento seguro com tratamento de cotas e exceções
   * ------------------------------------------------------------------------- */
  const Storage = {
    prefix: 'pdlab_',

    isAvailable() {
      try {
        const testKey = '__pdlab_test__';
        window.localStorage.setItem(testKey, testKey);
        window.localStorage.removeItem(testKey);
        return true;
      } catch (e) {
        return false;
      }
    },

    get(key, defaultValue = null) {
      if (!this.isAvailable()) return defaultValue;
      try {
        const item = window.localStorage.getItem(this.prefix + key);
        if (item === null) return defaultValue;
        return JSON.parse(item);
      } catch (e) {
        console.warn(`[PDLab.Storage] Erro ao recuperar chave "${key}":`, e);
        return defaultValue;
      }
    },

    set(key, value) {
      if (!this.isAvailable()) return false;
      try {
        window.localStorage.setItem(this.prefix + key, JSON.stringify(value));
        return true;
      } catch (e) {
        console.warn(`[PDLab.Storage] Erro ao gravar chave "${key}":`, e);
        return false;
      }
    },

    remove(key) {
      if (!this.isAvailable()) return;
      try {
        window.localStorage.removeItem(this.prefix + key);
      } catch (e) {
        console.warn(`[PDLab.Storage] Erro ao remover chave "${key}":`, e);
      }
    }
  };

  /* -------------------------------------------------------------------------
   * 2. THEME MANAGER: Alternância e sincronização de tema claro/escuro
   * ------------------------------------------------------------------------- */
  const ThemeManager = {
    STORAGE_KEY: 'theme',
    THEME_LIGHT: 'light',
    THEME_DARK: 'dark',

    init() {
      const savedTheme = Storage.get(this.STORAGE_KEY, null);
      const systemPrefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
      const initialTheme = savedTheme || (systemPrefersDark ? this.THEME_DARK : this.THEME_LIGHT);

      this.applyTheme(initialTheme, false);
      this.bindEvents();
    },

    getTheme() {
      return document.documentElement.getAttribute('data-theme') || this.THEME_LIGHT;
    },

    applyTheme(theme, save = true) {
      const targetTheme = theme === this.THEME_DARK ? this.THEME_DARK : this.THEME_LIGHT;
      document.documentElement.setAttribute('data-theme', targetTheme);

      if (save) {
        Storage.set(this.STORAGE_KEY, targetTheme);
      }

      this.updateButtonUI(targetTheme);

      // Dispara evento customizado para os simuladores (redesenho de SVG/Canvas)
      window.dispatchEvent(new CustomEvent('pdlab:themechange', {
        detail: { theme: targetTheme }
      }));
    },

    toggle() {
      const current = this.getTheme();
      const next = current === this.THEME_DARK ? this.THEME_LIGHT : this.THEME_DARK;
      this.applyTheme(next, true);
      return next;
    },

    updateButtonUI(theme) {
      const toggleBtns = document.querySelectorAll('[data-action="toggle-theme"], .theme-toggle-btn');
      toggleBtns.forEach((btn) => {
        const isDark = theme === this.THEME_DARK;
        // ☀ no escuro para alternar para o claro, ☾ no claro para alternar para o escuro
        const icon = isDark ? '☀' : '☾';
        const label = isDark ? 'Mudar para tema claro' : 'Mudar para tema escuro';
        
        btn.textContent = icon;
        btn.setAttribute('aria-label', label);
        btn.setAttribute('title', label);
      });
    },

    bindEvents() {
      // Delegação de evento de clique para os botões de tema
      document.addEventListener('click', (e) => {
        const toggleBtn = e.target.closest('[data-action="toggle-theme"], .theme-toggle-btn');
        if (toggleBtn) {
          e.preventDefault();
          this.toggle();
        }
      });

      // Sincroniza caso o sistema operacional mude o tema e o usuário não tenha preferência salva
      if (window.matchMedia) {
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
          const hasUserChoice = Storage.get(this.STORAGE_KEY, null);
          if (!hasUserChoice) {
            this.applyTheme(e.matches ? this.THEME_DARK : this.THEME_LIGHT, false);
          }
        });
      }
    }
  };

  /* -------------------------------------------------------------------------
   * 3. NAVIGATION: Marcação de rota ativa e suporte acessível ao menu
   * ------------------------------------------------------------------------- */
  const Navigation = {
    init() {
      this.highlightActiveRoute();
      this.bindDropdowns();
      this.bindMobileNav();
    },

    highlightActiveRoute() {
      const currentPath = window.location.pathname.split('/').pop() || 'index.html';
      const navLinks = document.querySelectorAll('.nav-link, .dropdown-item a');

      navLinks.forEach((link) => {
        const href = link.getAttribute('href');
        if (!href) return;

        const targetFile = href.split('/').pop();
        const isCurrent = targetFile === currentPath || 
          ((currentPath === '' || currentPath === 'index.html') && (targetFile === 'index.html' || targetFile === './'));

        if (isCurrent) {
          link.classList.add('active');
          link.setAttribute('aria-current', 'page');

          // Se for item de dropdown, destaca também o botão pai do dropdown
          const parentDropdown = link.closest('.nav-dropdown');
          if (parentDropdown) {
            const toggle = parentDropdown.querySelector('.nav-dropdown-toggle');
            if (toggle) {
              toggle.classList.add('active');
            }
          }
        } else {
          link.classList.remove('active');
          link.removeAttribute('aria-current');
        }
      });
    },

    bindDropdowns() {
      const dropdowns = document.querySelectorAll('.nav-dropdown');

      dropdowns.forEach((dropdown) => {
        const toggle = dropdown.querySelector('.nav-dropdown-toggle');
        if (!toggle) return;

        toggle.addEventListener('click', (e) => {
          e.preventDefault();
          const isOpen = dropdown.classList.contains('open');
          this.closeAllDropdowns();
          if (!isOpen) {
            dropdown.classList.add('open');
            toggle.setAttribute('aria-expanded', 'true');
          }
        });
      });

      // Fecha dropdown ao clicar fora
      document.addEventListener('click', (e) => {
        if (!e.target.closest('.nav-dropdown')) {
          this.closeAllDropdowns();
        }
      });

      // Fecha dropdowns com a tecla Escape
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
          this.closeAllDropdowns();
          this.closeMobileNav();
        }
      });
    },

    closeAllDropdowns() {
      document.querySelectorAll('.nav-dropdown').forEach((dropdown) => {
        dropdown.classList.remove('open');
        const toggle = dropdown.querySelector('.nav-dropdown-toggle');
        if (toggle) toggle.setAttribute('aria-expanded', 'false');
      });
    },

    bindMobileNav() {
      const toggle = document.querySelector('.mobile-nav-toggle');
      const siteNav = document.querySelector('.site-nav');
      if (!toggle || !siteNav) return;

      toggle.addEventListener('click', () => {
        const isOpen = siteNav.classList.toggle('is-open');
        toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      });
    },

    closeMobileNav() {
      const siteNav = document.querySelector('.site-nav');
      const toggle = document.querySelector('.mobile-nav-toggle');
      if (siteNav && siteNav.classList.contains('is-open')) {
        siteNav.classList.remove('is-open');
        if (toggle) toggle.setAttribute('aria-expanded', 'false');
      }
    }
  };

  /* -------------------------------------------------------------------------
   * 4. ANIMATION UTILS: Temporização assíncrona e controlador de passos
   * ------------------------------------------------------------------------- */
  const AnimationUtils = {
    sleep(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    },

    /**
     * StepController: Controlador de passos para simuladores de PD.
     * Permite execução passo-a-passo, autoplay, pause e velocidade configurável.
     */
    createStepController({
      onStep = () => {},
      onComplete = () => {},
      onReset = () => {},
      getTotalSteps = () => 0,
      baseDelayMs = 500
    } = {}) {
      let currentStep = 0;
      let isPlaying = false;
      let timerId = null;
      let speedMultiplier = 1.0;

      const controller = {
        get currentStep() { return currentStep; },
        get isPlaying() { return isPlaying; },
        get speedMultiplier() { return speedMultiplier; },

        setSpeed(multiplier) {
          speedMultiplier = Math.max(0.2, Math.min(5.0, Number(multiplier) || 1.0));
        },

        getCurrentDelay() {
          return Math.max(50, Math.round(baseDelayMs / speedMultiplier));
        },

        nextStep() {
          const total = getTotalSteps();
          if (currentStep < total) {
            currentStep += 1;
            onStep(currentStep, total);
            if (currentStep >= total) {
              controller.pause();
              onComplete();
            }
            return true;
          }
          controller.pause();
          return false;
        },

        prevStep() {
          if (currentStep > 0) {
            currentStep -= 1;
            onStep(currentStep, getTotalSteps());
            return true;
          }
          return false;
        },

        reset() {
          controller.pause();
          currentStep = 0;
          onReset();
        },

        play() {
          if (isPlaying) return;
          const total = getTotalSteps();
          if (currentStep >= total) {
            controller.reset();
          }
          isPlaying = true;

          const tick = () => {
            if (!isPlaying) return;
            const advanced = controller.nextStep();
            if (advanced && isPlaying) {
              timerId = setTimeout(tick, controller.getCurrentDelay());
            }
          };

          timerId = setTimeout(tick, controller.getCurrentDelay());
        },

        pause() {
          isPlaying = false;
          if (timerId !== null) {
            clearTimeout(timerId);
            timerId = null;
          }
        },

        togglePlay() {
          if (isPlaying) controller.pause();
          else controller.play();
        }
      };

      return controller;
    }
  };

  /* -------------------------------------------------------------------------
   * 5. DOM UTILS: Seleção rápida e criação segura de elementos
   * ------------------------------------------------------------------------- */
  const DOMUtils = {
    $(selector, parent = document) {
      return parent.querySelector(selector);
    },

    $$(selector, parent = document) {
      return Array.from(parent.querySelectorAll(selector));
    },

    create(tag, attributes = {}, ...children) {
      const el = document.createElement(tag);
      for (const [key, value] of Object.entries(attributes)) {
        if (key === 'className') {
          el.className = value;
        } else if (key === 'dataset') {
          for (const [dataKey, dataVal] of Object.entries(value)) {
            el.dataset[dataKey] = dataVal;
          }
        } else if (key.startsWith('on') && typeof value === 'function') {
          el.addEventListener(key.slice(2).toLowerCase(), value);
        } else if (value !== false && value !== null && value !== undefined) {
          el.setAttribute(key, value === true ? '' : value);
        }
      }

      for (const child of children) {
        if (typeof child === 'string' || typeof child === 'number') {
          el.appendChild(document.createTextNode(String(child)));
        } else if (child instanceof Node) {
          el.appendChild(child);
        }
      }

      return el;
    }
  };

  // Exportação no namespace PDLab
  PDLab.Storage = Storage;
  PDLab.ThemeManager = ThemeManager;
  PDLab.Navigation = Navigation;
  PDLab.AnimationUtils = AnimationUtils;
  PDLab.DOMUtils = DOMUtils;

  window.PDLab = PDLab;

  // Inicialização no carregamento do DOM
  document.addEventListener('DOMContentLoaded', () => {
    ThemeManager.init();
    Navigation.init();
  });

})(window, document);
