# fidelidade.py — desconto de fidelidade conforme o número de aluguéis no mês.


def desconto(total, alugueis_no_mes):
    if alugueis_no_mes >= 10:
        return total * 0.85
    elif alugueis_no_mes >= 5:
        return total * 0.90
    else:
        return total