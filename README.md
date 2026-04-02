# HealthFlow CRM — Sprint 3: Recursão e Memoização

**Challenge FIAP 2025 — Hospital São Rafael**  
Disciplina: Dynamic Programming | Turma: 2ESPR

---

## Sobre o Projeto

O **HealthFlow** é um CRM inteligente desenvolvido para o Hospital São Rafael com o objetivo de centralizar o gerenciamento de leads, cadastros, agendamentos e atendimentos.

Neste sprint, o foco é aplicar técnicas de **programação dinâmica** — especificamente recursão e memoização — para resolver dois problemas reais do sistema:

1. Detecção de cadastros duplicados ao receber novos leads
2. Otimização do encaixe de consultas na agenda médica

---

## Estrutura do Repositório

```
├── Tarefas.py   # Código com as 3 tarefas implementadas
└── README.md
```

---

## Tarefas Implementadas

### Tarefa 1 — Verificação Recursiva de Duplicidade

Quando um novo lead chega via formulário (Instagram, Google, Facebook, TikTok), o sistema precisa verificar se ele já existe no banco antes de criar um novo cadastro.

A função `verificar_duplicidade()` percorre recursivamente a lista de cadastros existentes e compara os campos: **nome, telefone, e-mail e CPF**. Se qualquer um deles bater, o lead é bloqueado como duplicata.

**Por que recursão?**  
A lógica é naturalmente sequencial: olha o primeiro cadastro, se não for, passa para o próximo — até o fim da lista. A recursão modela esse comportamento de forma direta, sem precisar de um `for` explícito.

**Estrutura da função:**
```
caso base  → lista esgotada → retorna False (não é duplicata)
comparação → algum campo bate → retorna True (é duplicata)
recursão   → avança para o próximo índice
```

---

### Tarefa 2 — Memoização para Evitar Comparações Repetidas

Em um CRM com alto volume de leads chegando simultaneamente, é possível que o mesmo lead seja verificado mais de uma vez contra os mesmos cadastros. Isso gera reprocessamento desnecessário.

A função `verificar_duplicidade_memoizado()` aplica a mesma lógica da Tarefa 1, mas armazena cada resultado em um **dicionário de cache**. A chave é uma tupla com os dados do lead + o índice do cadastro comparado.

**Funcionamento do cache:**
```python
chave = (nome, telefone, email, cpf, indice)

if chave in cache:
    return cache[chave]   # resultado imediato, sem reprocessar

# ... faz a comparação ...
cache[chave] = resultado  # armazena para próximas chamadas
```

O teste no código demonstra isso com duas chamadas idênticas: a primeira processa e armazena, a segunda retorna instantaneamente do cache.

---

### Tarefa 3 — Otimização de Agenda com Subproblemas

O médico tem slots de tempo disponíveis ao longo do dia. Existem consultas com durações variadas aguardando encaixe. O objetivo é **maximizar o número de consultas encaixadas** sem sobreposição.

A função `melhor_encaixe()` testa recursivamente todas as combinações possíveis:
- Para cada consulta, tenta encaixá-la em cada slot disponível
- Se couber, consome aquela parte do slot e chama recursivamente para a próxima consulta
- Também testa a opção de **pular** a consulta atual (às vezes pular uma permite encaixar mais)
- O cache evita recalcular o mesmo estado (mesma consulta + mesmo estado dos slots) mais de uma vez

**Os slots são representados em minutos a partir das 08:00:**
```
(0, 30)    → 08:00 – 08:30
(45, 90)   → 08:45 – 09:30
(100, 160) → 09:40 – 10:40
(180, 210) → 11:00 – 11:30
```

---

## Como Executar

Necessário apenas Python 3.x, sem dependências externas.

```bash
python Tarefas.py
```

**Saída esperada:**
```
=======================================================
TAREFA 1 — Verificação Recursiva de Duplicidade
=======================================================
  Lead 'Carlos Silva': DUPLICATA — cadastro bloqueado
  Lead 'Jorge Costa': NOVO LEAD  — cadastro liberado

=======================================================
TAREFA 2 — Verificação com Memoização
=======================================================
  [1ª chamada — processando e armazenando no cache]
  Lead 'Carlos Silva': DUPLICATA — cadastro bloqueado
  Lead 'Jorge Costa': NOVO LEAD  — cadastro liberado

  [2ª chamada — resultado recuperado do cache, sem reprocessar]
  Lead 'Carlos Silva': DUPLICATA — cadastro bloqueado
  Lead 'Jorge Costa': NOVO LEAD  — cadastro liberado

=======================================================
TAREFA 3 — Otimização de Agenda com Memoização
=======================================================
  Slots disponíveis:
    08:00 – 08:30  (30 min livres)
    08:45 – 09:30  (45 min livres)
    09:40 – 10:40  (60 min livres)
    11:00 – 11:30  (30 min livres)

  Consultas pendentes (min): [20, 45, 25, 60, 15]
  Total de consultas: 5

  Resultado: 4 de 5 consultas encaixadas com sucesso
```

---

## Conceitos Aplicados

| Conceito | Onde foi aplicado |
|---|---|
| Recursão | Tarefas 1, 2 e 3 — percurso e tomada de decisão sem laço explícito |
| Caso base | Fim da lista (T1/T2) e todas consultas processadas (T3) |
| Memoização | Tarefas 2 e 3 — cache de resultados via dicionário |
| Programação dinâmica | Tarefa 3 — subproblemas sobrepostos com otimização |

---

## Integrantes

| Nome | RM |
|---|---|
| Enzo Luciano | 559557 |
| Alexandre Colvet Delfino | 560059 |
| Pedro Claudino Scarceli | 561023 |
| Samuel Baecker | 559269 |
| Luigi Thiengo | 560755 |

---

*Challenge FIAP — Agosto/2025 — Hospital São Rafael*
