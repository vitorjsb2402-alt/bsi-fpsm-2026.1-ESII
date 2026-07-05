# precos.py — quanto custa alugar cada tipo de veículo.
#
# O preço é uma base fixa mais um valor por hora, que muda conforme o tipo.
# Cada tipo tem sua própria estratégia de cálculo (Strategy), escolhida
# por uma fábrica (criar_tarifa).


class TarifaBike:
    def calcular(self, horas):
        return 5.0 + 2.0 * horas


class TarifaPatinete:
    def calcular(self, horas):
        return 4.0 + 3.0 * horas


class TarifaEletrica:
    def calcular(self, horas):
        return 8.0 + 4.0 * horas


class TarifaBikeCarga:
    def calcular(self, horas):
        return 10.0 + 5.0 * horas


def criar_tarifa(tipo):
    tarifas = {
        "bike": TarifaBike,
        "patinete": TarifaPatinete,
        "eletrica": TarifaEletrica,
        "bike_carga": TarifaBikeCarga,
    }
    if tipo not in tarifas:
        raise ValueError("tipo de veículo desconhecido: {!r}".format(tipo))
    return tarifas[tipo]()


def preco_aluguel(tipo, horas):
    return criar_tarifa(tipo).calcular(horas)
