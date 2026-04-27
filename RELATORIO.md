# Relatorio do Simulador de Hierarquia de Memoria

## 1. Implementacao

O trabalho foi implementado em Python no arquivo `trabalho.py`.
A hierarquia simulada possui quatro niveis:

| Nivel | Tempo de acesso | Custo por bloco | Tamanho maximo |
|---|---:|---:|---:|
| L1 | 1 | 200 | 5 |
| L2 | 3 | 50 | 10 |
| L3 | 6 | 10 | 50 |
| RAM | 16 | 1 | automatico |

A RAM e inicializada automaticamente com todos os blocos distintos presentes na entrada.
A entrada e processada da esquerda para a direita, em blocos consecutivos de dois caracteres.
Caracteres nao alfabeticos sao descartados e, quando a quantidade de caracteres validos e impar,
o ultimo caractere e ignorado.

A hierarquia e inclusiva: quando um bloco e encontrado em L2, ele e promovido para L1; quando e
encontrado em L3, e promovido para L2 e L1; quando e encontrado apenas na RAM, e carregado em
L3, L2 e L1.

Cada cache aplica a politica de substituicao localmente. As politicas implementadas sao:

- `FIFO`: remove o bloco inserido ha mais tempo.
- `LRU`: remove o bloco menos recentemente usado.
- `LFU`: remove o bloco com menor frequencia de uso. Em caso de empate, usa FIFO pela ordem de insercao.

## 2. Metricas Calculadas

O simulador exibe as metricas obrigatorias:

- configuracao utilizada: `X1`, `X2`, `X3` e politica;
- custo total;
- numero total de acessos;
- acertos em L1, L2 e L3;
- acessos a RAM;
- taxa de acerto de L1, L2 e L3;
- taxa global de faltas;
- tempo total acumulado;
- tempo medio de acesso.

Formulas usadas:

- Custo total: `200*X1 + 50*X2 + 10*X3`
- Taxa de acerto de cada cache: `acertos_no_nivel / total_acessos * 100`
- Taxa global de faltas: `acessos_ram / total_acessos * 100`
- Tempo medio: `tempo_total / total_acessos`

## 3. Entradas de Teste

O arquivo `benchmark_padroes_memoria.txt` contem 10 padroes de acesso. Cada padrao possui
3 strings de 200 caracteres, correspondendo a 100 acessos por string. Portanto, cada padrao
foi avaliado com 300 acessos e o conjunto completo com 3000 acessos.

Os padroes cobrem comportamentos como:

- alta localidade temporal;
- acesso sequencial com grande variedade;
- alternancia entre fases;
- blocos quentes com intrusoes frias;
- padrao quase aleatorio;
- repeticao ciclica moderada;
- rajadas de localidade;
- concentracao progressiva;
- alternancia entre bloco quente e variavel;
- retorno tardio com distancia de reuso longa.

## 4. Execucao por Arquivo

O programa aceita uma string diretamente pela linha de comando ou um arquivo completo:

```bash
python trabalho.py abcdabcd 2 4 8 LRU
python trabalho.py --arquivo benchmark_padroes_memoria.txt 1 10 40 LFU
```

No modo `--arquivo`, cada linha `# PADRAO` inicia um novo grupo. O simulador imprime o
resultado de cada padrao e depois simula todos os acessos juntos para gerar o resultado geral.

## 5. Experimentos

Como o limite de custo informado para a arquitetura foi `1100`, as configuracoes com custo
maior que esse valor sao rejeitadas pelo programa.

Resumo agregado sobre os 3000 acessos do benchmark:

| Configuracao | X1 | X2 | X3 | Politica | Custo | Tempo medio | L1 | L2 | L3 | Faltas |
|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|
| baixo_custo | 1 | 2 | 5 | FIFO | 350 | 19.95 | 0.03% | 2.53% | 34.27% | 63.17% |
| baixo_custo | 1 | 2 | 5 | LRU | 350 | 19.68 | 0.03% | 4.93% | 32.63% | 62.40% |
| baixo_custo | 1 | 2 | 5 | LFU | 350 | 19.77 | 0.03% | 6.63% | 29.77% | 63.57% |
| orcamento_equilibrado | 3 | 6 | 20 | FIFO | 1100 | 15.25 | 3.47% | 34.70% | 14.07% | 47.77% |
| orcamento_equilibrado | 3 | 6 | 20 | LRU | 1100 | 15.12 | 5.03% | 35.07% | 11.93% | 47.97% |
| orcamento_equilibrado | 3 | 6 | 20 | LFU | 1100 | 13.34 | 11.37% | 28.37% | 22.33% | 37.93% |
| melhor_benchmark | 1 | 10 | 40 | FIFO | 1100 | 13.26 | 0.03% | 47.13% | 14.77% | 38.07% |
| melhor_benchmark | 1 | 10 | 40 | LRU | 1100 | 13.18 | 0.03% | 47.60% | 14.60% | 37.77% |
| melhor_benchmark | 1 | 10 | 40 | LFU | 1100 | 12.69 | 0.03% | 44.13% | 22.47% | 33.37% |

## 6. Analise Critica

A melhor configuracao encontrada para o benchmark agregado, respeitando o custo maximo de
`1100`, foi:

```text
X1=1, X2=10, X3=40, politica LFU
```

Essa configuracao usa pouca L1, mas amplia L2 e L3 dentro do orcamento. Para o conjunto de
padroes fornecido, essa escolha reduziu as faltas globais para `33.37%` e obteve tempo medio
`12.69`, melhor que a configuracao `X1=3, X2=6, X3=20` com o mesmo custo.

O resultado mostra que maximizar L1 nem sempre e a melhor decisao sob custo limitado. Como L1
custa 200 por bloco, reduzir L1 libera orcamento para armazenar mais blocos em L2 e L3. No
benchmark fornecido existem padroes com working set maior e retorno tardio, o que favorece
caches inferiores maiores.

Entre as politicas, LFU foi superior na melhor configuracao porque preservou blocos repetidos
ao longo do benchmark completo. LRU ficou proximo, mas teve mais acessos a RAM no agregado.

## 7. Conclusao

O simulador atende aos requisitos do enunciado e aos detalhes adicionais: permite configurar os
tamanhos das caches, escolher a politica de substituicao, avaliar uma string isolada, avaliar
todos os padroes do arquivo de benchmark, exibir resultado por padrao e exibir o resultado geral.

A arquitetura recomendada para a avaliacao pelo benchmark completo e:

```text
X1=1, X2=10, X3=40, politica LFU, custo=1100
```
