# test_locadora.py — a rede de segurança da locadora.
from locadora import Locadora


def test_devolver_no_prazo():
    loc = Locadora()
    loc.alugar("BK1", "bike", 8, 2)
    assert loc.devolver("BK1", 10) == 9.0             # 2h, sem atraso
    assert "BK1" not in loc.ativos


def test_piso_de_uma_hora():
    loc = Locadora()
    loc.alugar("BK2", "patinete", 8, 1)
    assert loc.devolver("BK2", 8) == 7.0              # 0h -> piso 1 -> 4 + 3*1


def test_multa_por_atraso():
    loc = Locadora()
    loc.alugar("BK3", "bike", 8, 2)
    assert loc.devolver("BK3", 12) == 19.0            # usa 4h (13) + atraso 2h (6)


def test_avisos_saem_na_devolucao(capsys):
    loc = Locadora()
    loc.alugar("BK4", "bike", 8, 2)
    loc.devolver("BK4", 10)
    saida = capsys.readouterr().out
    assert "[MANUTENCAO]" in saida
    assert "[PAINEL]" in saida
    assert "[FINANCEIRO]" in saida


def test_bike_de_carga():
    loc = Locadora()
    loc.alugar("BK5", "bike_carga", 8, 2)
    assert loc.devolver("BK5", 10) == 20.0            # 2h -> 10 + 5*2


def test_observador_novo_recebe_evento():
    class ObservadorEspiao:
        def __init__(self):
            self.evento_recebido = None

        def notificar(self, evento):
            self.evento_recebido = evento

    loc = Locadora()
    espiao = ObservadorEspiao()
    loc.observadores.append(espiao)

    loc.alugar("BK6", "bike", 8, 2)
    loc.devolver("BK6", 10)

    assert espiao.evento_recebido is not None
    assert espiao.evento_recebido.codigo == "BK6"
    assert espiao.evento_recebido.total == 9.0


def test_devolver_com_spy_de_cobranca():
    class CobrancaSpy:
        def __init__(self):
            self.chamadas = []

        def cobrar(self, codigo, valor):
            self.chamadas.append((codigo, valor))

    spy = CobrancaSpy()
    loc = Locadora(servico_cobranca=spy)
    loc.alugar("BK7", "bike", 8, 2)
    total = loc.devolver("BK7", 10)

    assert total == 9.0
    assert spy.chamadas == [("BK7", 9.0)]


def test_multa_nao_ultrapassa_teto():
    loc = Locadora()
    loc.alugar("BK8", "bike", 0, 1)
    total = loc.devolver("BK8", 100)          # atraso enorme
    preco_base = 5.0 + 2.0 * 100              # horas_uso = 100
    assert total == preco_base + 30.0         # multa travada em 30
