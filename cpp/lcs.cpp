/**
 * @file lcs.cpp
 * @brief Implementação de referência em C++17 do algoritmo LCS (Cormen 15.4)
 *        para o experimento E4 (comparativo de desempenho Python x C++).
 *
 * Responsável: Integrante P4 (ver docs/tarefas/P4_estudo_de_caso_e_benchmarks.md).
 */

#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include <algorithm>

int main(int argc, char* argv[]) {
    // 1. Definição das strings de entrada (Valores padrão vs Argumentos de linha de comando)
    std::string a = "ABCBDAB";
    std::string b = "BDCABA";

    if (argc >= 3) {
        a = argv[1];
        b = argv[2];
    }

    std::cout << "[CPP - LCS] Iniciando experimento E4..." << std::endl;
    std::cout << "String A: \"" << a << "\" (len=" << a.length() << ")" << std::endl;
    std::cout << "String B: \"" << b << "\" (len=" << b.length() << ")\n" << std::endl;

    int m = a.length();
    int n = b.length();

    // Início da medição de tempo de CPU
    auto start_time = std::chrono::high_resolution_clock::now();

    // 2. Construção da Tabela DP (Bottom-Up)
    // Tabela de tamanho (m+1) x (n+1) inicializada com zeros
    std::vector<std::vector<int>> c(m + 1, std::vector<int>(n + 1, 0));

    for (int i = 1; i <= m; ++i) {
        for (int j = 1; j <= n; ++j) {
            if (a[i - 1] == b[j - 1]) {
                c[i][j] = c[i - 1][j - 1] + 1;
            } else {
                c[i][j] = std::max(c[i - 1][j], c[i][j - 1]);
            }
        }
    }

    // 3. Reconstrução (Traceback) de trás para frente
    std::string lcs_str = "";
    int i = m;
    int j = n;

    while (i > 0 && j > 0) {
        if (a[i - 1] == b[j - 1]) {
            lcs_str.push_back(a[i - 1]);
            i--;
            j--;
        } else if (c[i - 1][j] >= c[i][j - 1]) {
            i--;
        } else {
            j--;
        }
    }
    // Como coletamos do fim para o começo, invertemos a string resultante
    std::reverse(lcs_str.begin(), lcs_str.end());

    // Fim da medição de tempo
    auto end_time = std::chrono::high_resolution_clock::now();
    
    // Cálculo da duração do algoritmo
    auto elapsed_us = std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time).count();
    double elapsed_ms = elapsed_us / 1000.0;

    // 4. Saída formatada dos resultados para o Benchmark
    std::cout << "---------------- RESULTADOS ----------------" << std::endl;
    std::cout << "Comprimento da LCS : " << c[m][n] << std::endl;
    std::cout << "String da LCS      : \"" << lcs_str << "\"" << std::endl;
    std::cout << "Tempo de Execução  : " << elapsed_us << " us (" << elapsed_ms << " ms)" << std::endl;
    std::cout << "--------------------------------------------" << std::endl;

    return 0;
}
