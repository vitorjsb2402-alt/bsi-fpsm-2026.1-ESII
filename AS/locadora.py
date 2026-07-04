# locadora.py — sistema da locadora de veículos (bikes, patinetes...).
#
# Um veículo é alugado (alugar) e depois devolvido (devolver). Na devolução,
# cobra-se o aluguel + a multa de atraso (com teto de R$ 30), e os
# interessados são avisados via Observer.

from dataclasses import dataclass

from precos import preco_aluguel
from cobranca import ServicoCobranca

MULTA_MAXIMA = 30.0


@dataclass
class Evento:
    codigo: str
    tipo: str
    total: float


class ObservadorManutencao:
    def notificar(self, evento):
        print("[MANUTENCAO] revisar {} {}".format(evento.tipo, evento.codigo))


class ObservadorPainel:
    def notificar(self, evento):
        print("[PAINEL] {} disponível de novo".format(evento.codigo))


class ObservadorFinanceiro:
    def notificar(self, evento):
        print("[FINANCEIRO] recebido R$ {:.2f} de {}".format(evento.total, evento.codigo))


class Locadora:
    def __init__(self, servico_cobranca=None):
        self.ativos = {}
        self.servico_cobranca = servico_cobranca or ServicoCobranca()
        self.observadores = [
            ObservadorManutencao(),
            ObservadorPainel(),
            ObservadorFinanceiro(),
        ]

    def alugar(self, codigo, tipo, hora_inicio, horas_previstas):
        self.ativos[codigo] = (tipo, hora_inicio, horas_previstas)

    def _calcular_total(self, codigo, hora_fim):
        tipo = self.ativos[codigo][0]
        hora_inicio = self.ativos[codigo][1]
        horas_previstas = self.ativos[codigo][2]

        horas_uso = hora_fim - hora_inicio
        if horas_uso < 1:
            horas_uso = 1
        preco_base = preco_aluguel(tipo, horas_uso)

        horas_atraso = hora_fim - (hora_inicio + horas_previstas)
        if horas_atraso <= 0:
            multa = 0.0
        else:
            multa = 3.0 * horas_atraso
            if multa > MULTA_MAXIMA:
                multa = MULTA_MAXIMA

        return preco_base + multa

    def devolver(self, codigo, hora_fim):
        tipo = self.ativos[codigo][0]
        total = self._calcular_total(codigo, hora_fim)
        self.servico_cobranca.cobrar(codigo, total)

        evento = Evento(codigo=codigo, tipo=tipo, total=total)
        for observador in self.observadores:
            observador.notificar(evento)

        del self.ativos[codigo]
        return total

    def simular(self, codigo, hora_fim):
        return self._calcular_total(codigo, hora_fim)