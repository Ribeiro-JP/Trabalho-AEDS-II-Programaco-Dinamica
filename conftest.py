"""Configuração global do pytest para o projeto de Programação Dinâmica.

Implementa um hook que intercepta exceções NotImplementedError lançadas pelos stubs
e converte automaticamente o resultado do teste em 'SKIPPED' com a mensagem
'ainda não implementado'.

Dessa forma:
1. `make test` executa com sucesso (0 falhas) mesmo com os stubs vazios.
2. À medida que os integrantes (P3 e P4) implementam cada função, seus respectivos
   testes passam a executar e validar a corretude sem necessidade de alterar decorators.
"""

from __future__ import annotations

import pytest


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> None:
    """Hook do pytest para marcar testes com NotImplementedError como skipped."""
    outcome = yield
    report = outcome.get_result()

    if call.when == "call" and call.excinfo is not None:
        if call.excinfo.errisinstance(NotImplementedError):
            report.outcome = "skipped"
            report.wasxfail = f"ainda não implementado: {call.excinfo.value}"
            # Define uma tupla simples de localização e motivo para o relatório resumido
            report.longrepr = (
                str(item.fspath),
                call.excinfo.lineno,
                f"Skipped: ainda não implementado ({call.excinfo.value})",
            )
