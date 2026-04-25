# Simulador de Hierarquia de Memoria

Projeto feito por: **Luan da Cruz Mendes** e **Marco Túlio Tavares Oliveira**

Simulador em Python para uma hierarquia inclusiva com cache L1, L2, L3 e RAM.
O programa recebe uma string de acessos, divide a entrada em blocos de 2 caracteres
e calcula metricas de desempenho para as politicas FIFO, LRU e LFU.
Tambem permite avaliar todos os padroes de um arquivo de benchmark.

## Arquivos

- `trabalho.py`: simulador principal.
- `benchmark_padroes_memoria.txt`: padroes usados nos testes.
- `RELATORIO.md`: descricao da implementacao, testes e analise dos resultados.

## Execucao do simulador

Formato:

```bash
python trabalho.py <string_entrada> <X1> <X2> <X3> <FIFO|LRU|LFU>
python trabalho.py --arquivo <caminho_arquivo> <X1> <X2> <X3> <FIFO|LRU|LFU>
```

Exemplos:

```bash
python trabalho.py abcdabcd 2 4 8 LRU
python trabalho.py --arquivo benchmark_padroes_memoria.txt 1 10 40 LFU
```

Parametros:

- `string_entrada`: sequencia de caracteres alfabeticos. Cada par de caracteres representa um bloco.
- `caminho_arquivo`: arquivo com padroes de acesso. Linhas iniciadas por `# PADRAO` separam os padroes.
- `X1`: tamanho maximo da L1, entre 1 e 5.
- `X2`: tamanho maximo da L2, entre 1 e 10.
- `X3`: tamanho maximo da L3, entre 1 e 50.
- politica: `FIFO`, `LRU` ou `LFU`.

A configuracao deve respeitar `X1 <= X2 <= X3`.
O custo `200*X1 + 50*X2 + 10*X3` deve ser menor ou igual a `1100`.

No modo `--arquivo`, o programa imprime as metricas de cada padrao e, no final,
as metricas do conjunto completo.

## Formulas

- Custo total: `200*X1 + 50*X2 + 10*X3`
- Taxa de acerto L1: `acertos_l1 / total_acessos * 100`
- Taxa de acerto L2: `acertos_l2 / total_acessos * 100`
- Taxa de acerto L3: `acertos_l3 / total_acessos * 100`
- Taxa global de faltas: `acessos_ram / total_acessos * 100`
- Tempo medio: `tempo_total / total_acessos`
