# Simulador de Hierarquia de Memória

Simulador em Python para uma hierarquia inclusiva com cache L1, L2, L3 e RAM.
O programa recebe uma string de acessos, divide a entrada em blocos de 2 caracteres
e calcula métricas de desempenho para as políticas FIFO, LRU e LFU.

## Arquivos

- `trabalho.py`: simulador principal.
- `RELATORIO.md`: descrição da implementação, testes e análise dos resultados.

## Execução do simulador

Formato:

```bash
python trabalho.py <string_entrada> <X1> <X2> <X3> <FIFO|LRU|LFU>
```

Exemplo:

```bash
python trabalho.py abcdabcd 2 4 8 LRU
```

Parâmetros:

- `string_entrada`: sequência de caracteres alfabéticos. Cada par de caracteres representa um bloco.
- `X1`: tamanho máximo da L1, entre 1 e 5.
- `X2`: tamanho máximo da L2, entre 1 e 10.
- `X3`: tamanho máximo da L3, entre 1 e 50.
- política: `FIFO`, `LRU` ou `LFU`.

A configuração deve respeitar `X1 <= X2 <= X3`.

## Fórmulas

- Custo total: `200*X1 + 50*X2 + 10*X3`
- Taxa de acerto L1: `acertos_l1 / total_acessos * 100`
- Taxa de acerto L2: `acertos_l2 / total_acessos * 100`
- Taxa de acerto L3: `acertos_l3 / total_acessos * 100`
- Taxa global de faltas: `acessos_ram / total_acessos * 100`
- Tempo médio: `tempo_total / total_acessos`
