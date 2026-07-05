# test_fidelidade.py — testes do desconto de fidelidade (TDD).
from fidelidade import desconto


def test_sem_desconto_abaixo_de_5():
    assert desconto(100, 4) == 100


def test_desconto_10_por_cento_no_limite_inferior():
    assert desconto(100, 5) == 90


def test_desconto_10_por_cento_no_limite_superior():
    assert desconto(100, 9) == 90


def test_desconto_15_por_cento_a_partir_de_10():
    assert desconto(200, 10) == 170
