/**
 * @file shared.js
 * @brief Utilitários JavaScript compartilhados entre as páginas web de visualização.
 *
 * Responsável: Integrante P5 (ver docs/tarefas/P5_cheatsheet_slides_e_web.md).
 */

// Inicialização do tema claro/escuro
(function initTheme() {
  const savedTheme = localStorage.getItem('pd-theme') || 
    (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  document.documentElement.setAttribute('data-theme', savedTheme);
})();

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme') || 'light';
  const next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('pd-theme', next);
}

/**
 * Carrega o arquivo consolidado de resultados de benchmarks.
 * @returns {Promise<Object>} Dados dos benchmarks em JSON.
 */
async function loadBenchmarkResults() {
  try {
    const response = await fetch('data/results.json');
    if (!response.ok) {
      throw new Error(`Erro HTTP: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.warn('Resultados de benchmark ainda não gerados ou inacessíveis:', error);
    return {};
  }
}

// TODO(P5): Implementar animações, controles de playback (passo a passo) e renderizadores SVG/Canvas.
