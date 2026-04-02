
# HealthFlow CRM — Hospital São Rafael
# Sprint 3 — Recursão e Memoização | Dynamic Programming

# ============================================================
# DADOS DE EXEMPLO
# ============================================================

import os
os.system('cls')

cadastros = [
    {"nome": "Ana Lima",     "telefone": "11999990001", "email": "ana@email.com",    "cpf": "111.111.111-01"},
    {"nome": "Bruno Souza",  "telefone": "11999990002", "email": "bruno@email.com",  "cpf": "111.111.111-02"},
    {"nome": "Carla Mendes", "telefone": "11999990003", "email": "carla@email.com",  "cpf": "111.111.111-03"},
    {"nome": "Daniel Rocha", "telefone": "11999990004", "email": "daniel@email.com", "cpf": "111.111.111-04"},
    {"nome": "Eva Torres",   "telefone": "11999990005", "email": "eva@email.com",    "cpf": "111.111.111-05"},
]

lead_duplicado = {
    "nome": "Carlos Silva",
    "telefone": "11999990003",  # mesmo telefone que Carla Mendes
    "email": "carlos@email.com",
    "cpf": "999.999.999-99"
}

lead_novo = {
    "nome": "Jorge Costa",
    "telefone": "11999990099",
    "email": "jorge@email.com",
    "cpf": "999.999.999-88"
}


# ============================================================
# TAREFA 1 — Verificação recursiva de duplicidade
# ============================================================
# Percorre a lista de cadastros recursivamente.
# Retorna True se qualquer campo-chave do novo lead já existir.

def verificar_duplicidade(novo, lista, indice=0):
    # Caso base: fim da lista, nenhuma duplicata encontrada
    if indice == len(lista):
        return False

    atual = lista[indice]

    # Checa se qualquer campo identificador bate
    if (novo["nome"]     == atual["nome"]     or
        novo["telefone"] == atual["telefone"] or
        novo["email"]    == atual["email"]    or
        novo["cpf"]      == atual["cpf"]):
        return True

    # Avança para o próximo cadastro
    return verificar_duplicidade(novo, lista, indice + 1)


print("=" * 55)
print("TAREFA 1 — Verificação Recursiva de Duplicidade")
print("=" * 55)

for lead in [lead_duplicado, lead_novo]:
    duplicata = verificar_duplicidade(lead, cadastros)
    status = "DUPLICATA — cadastro bloqueado" if duplicata else "NOVO LEAD  — cadastro liberado"
    print(f"  Lead '{lead['nome']}': {status}")

print()


# ============================================================
# TAREFA 2 — Verificação com memoização
# ============================================================
# Mesma lógica da Tarefa 1, mas cada comparação (lead x índice)
# é armazenada no cache. Evita reprocessar pares já analisados.

cache_comparacoes = {}

def verificar_duplicidade_memoizado(novo, lista, indice=0):
    if indice == len(lista):
        return False

    # Chave única: dados do lead + posição na lista
    chave = (novo["nome"], novo["telefone"], novo["email"], novo["cpf"], indice)

    # Retorna resultado já calculado se existir no cache
    if chave in cache_comparacoes:
        return cache_comparacoes[chave]

    atual = lista[indice]

    if (novo["nome"]     == atual["nome"]     or
        novo["telefone"] == atual["telefone"] or
        novo["email"]    == atual["email"]    or
        novo["cpf"]      == atual["cpf"]):
        cache_comparacoes[chave] = True
        return True

    cache_comparacoes[chave] = False
    return verificar_duplicidade_memoizado(novo, lista, indice + 1)


print("=" * 55)
print("TAREFA 2 — Verificação com Memoização")
print("=" * 55)

print("  [1ª chamada — processando e armazenando no cache]")
for lead in [lead_duplicado, lead_novo]:
    duplicata = verificar_duplicidade_memoizado(lead, cadastros)
    status = "DUPLICATA — cadastro bloqueado" if duplicata else "NOVO LEAD  — cadastro liberado"
    print(f"  Lead '{lead['nome']}': {status}")

print()

print("  [2ª chamada — resultado recuperado do cache, sem reprocessar]")
for lead in [lead_duplicado, lead_novo]:
    duplicata = verificar_duplicidade_memoizado(lead, cadastros)
    status = "DUPLICATA — cadastro bloqueado" if duplicata else "NOVO LEAD  — cadastro liberado"
    print(f"  Lead '{lead['nome']}': {status}")

print()


# ============================================================
# TAREFA 3 — Otimização de agenda com memoização
# ============================================================
# Tenta encaixar o maior número de consultas nos slots do médico.
# A cada chamada: tenta encaixar a consulta atual em algum slot,
# ou pula ela. O cache evita recalcular combinações já testadas.

# Slots disponíveis (início e fim em minutos a partir das 08:00)
slots = [
    (0,   30),   # 08:00 – 08:30
    (45,  90),   # 08:45 – 09:30
    (100, 160),  # 09:40 – 10:40
    (180, 210),  # 11:00 – 11:30
]

# Consultas aguardando encaixe (duração em minutos)
consultas = [20, 45, 25, 60, 15]

cache_agenda = {}

def melhor_encaixe(consultas, slots, idx=0):
    # Caso base: todas as consultas foram processadas
    if idx == len(consultas):
        return 0

    chave = (idx, tuple(slots))

    if chave in cache_agenda:
        return cache_agenda[chave]

    duracao = consultas[idx]
    melhor = 0

    for i, (inicio, fim) in enumerate(slots):
        if fim - inicio >= duracao:
            # Encaixa a consulta: consome o slot e avança
            slots_atualizados = slots[:i] + [(inicio + duracao, fim)] + slots[i+1:]
            resultado = 1 + melhor_encaixe(consultas, slots_atualizados, idx + 1)
            if resultado > melhor:
                melhor = resultado

    # Testa também pular esta consulta
    pular = melhor_encaixe(consultas, slots, idx + 1)
    if pular > melhor:
        melhor = pular

    cache_agenda[chave] = melhor
    return melhor


print("=" * 55)
print("TAREFA 3 — Otimização de Agenda com Memoização")
print("=" * 55)

def minutos_para_hora(m):
    h = 8 + m // 60
    min_ = m % 60
    return f"{h:02d}:{min_:02d}"

print("  Slots disponíveis:")
for inicio, fim in slots:
    print(f"    {minutos_para_hora(inicio)} - {minutos_para_hora(fim)}  ({fim - inicio} min livres)")

print(f"\n  Consultas pendentes (min): {consultas}")
print(f"  Total de consultas: {len(consultas)}")

total = melhor_encaixe(consultas, slots)
print(f"\n  Resultado: {total} de {len(consultas)} consultas encaixadas com sucesso")
print()