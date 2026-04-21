# Relatório do Simulador de Hierarquia de Memória

## 1. Implementação

O trabalho foi implementado em Python no arquivo `trabalho.py`.
A hierarquia simulada possui quatro níveis:

| Nível | Tempo de acesso | Custo por bloco | Tamanho máximo |
|---|---:|---:|---:|
| L1 | 1 | 200 | 5 |
| L2 | 3 | 50 | 10 |
| L3 | 6 | 10 | 50 |
| RAM | 16 | 1 | automático |

A RAM é inicializada automaticamente com todos os blocos distintos presentes na entrada.
A entrada é processada da esquerda para a direita, em blocos consecutivos de dois caracteres.
Caracteres não alfabéticos são descartados e, quando a quantidade de caracteres válidos é ímpar,
o último caractere é ignorado.

A hierarquia é inclusiva: quando um bloco é encontrado em L2, ele é promovido para L1; quando é
encontrado em L3, é promovido para L2 e L1; quando é encontrado apenas na RAM, é carregado em
L3, L2 e L1.

Cada cache aplica a política de substituição localmente. As políticas implementadas são:

- `FIFO`: remove o bloco inserido há mais tempo.
- `LRU`: remove o bloco menos recentemente usado.
- `LFU`: remove o bloco com menor frequência de uso. Em caso de empate, usa FIFO pela ordem de inserção.

## 2. Métricas Calculadas

O simulador exibe as métricas obrigatórias:

- configuração utilizada: `X1`, `X2`, `X3` e política;
- custo total;
- número total de acessos;
- acertos em L1, L2 e L3;
- acessos à RAM;
- taxa de acerto de L1, L2 e L3;
- taxa global de faltas;
- tempo total acumulado;
- tempo médio de acesso.

Fórmulas usadas:

- Custo total: `200*X1 + 50*X2 + 10*X3`
- Taxa de acerto de cada cache: `acertos_no_nivel / total_acessos * 100`
- Taxa global de faltas: `acessos_ram / total_acessos * 100`
- Tempo médio: `tempo_total / total_acessos`

## 3. Entradas de Teste

O arquivo `benchmark_padroes_memoria.txt` contém 10 padrões de acesso. Cada padrão possui
3 strings de 200 caracteres, correspondendo a 100 acessos por string. Portanto, cada padrão
foi avaliado com 300 acessos e o conjunto completo com 3000 acessos.

Os padrões cobrem comportamentos como:

- alta localidade temporal;
- acesso sequencial com grande variedade;
- alternância entre fases;
- blocos quentes com intrusões frias;
- padrão quase aleatório;
- repetição cíclica moderada;
- rajadas de localidade;
- concentração progressiva;
- alternância entre bloco quente e variável;
- retorno tardio com distância de reuso longa.

## 4. Experimentos

Foram comparadas três configurações principais:

| Configuração | X1 | X2 | X3 | Custo |
|---|---:|---:|---:|---:|
| baixo_custo | 1 | 2 | 5 | 350 |
| medio_custo | 3 | 6 | 20 | 1100 |
| alto_desempenho | 5 | 10 | 50 | 2000 |

Resumo agregado sobre os 3000 acessos do benchmark:

| Configuração | Política | Custo | Tempo médio | L1 | L2 | L3 | Faltas |
|---|---|---:|---:|---:|---:|---:|---:|
| baixo_custo | FIFO | 350 | 20.13 | 0.00% | 2.50% | 33.27% | 64.23% |
| baixo_custo | LRU | 350 | 19.86 | 0.00% | 4.90% | 31.67% | 63.43% |
| baixo_custo | LFU | 350 | 20.21 | 0.00% | 4.90% | 29.43% | 65.67% |
| medio_custo | FIFO | 1100 | 16.20 | 3.30% | 33.80% | 9.60% | 53.30% |
| medio_custo | LRU | 1100 | 16.02 | 4.90% | 34.00% | 8.00% | 53.10% |
| medio_custo | LFU | 1100 | 16.57 | 4.90% | 30.00% | 10.00% | 55.10% |
| alto_desempenho | FIFO | 2000 | 13.47 | 35.67% | 9.83% | 9.07% | 45.43% |
| alto_desempenho | LRU | 2000 | 13.42 | 36.57% | 9.33% | 8.67% | 45.43% |
| alto_desempenho | LFU | 2000 | 13.70 | 34.33% | 8.03% | 12.20% | 45.43% |

## 5. Busca Competitiva sob Restrição de Custo

Como o enunciado deixa a faixa de custo-alvo a critério do professor, foi adotado custo máximo
de 1500 para a busca competitiva. Foram testadas as configurações válidas
com `1 <= X1 <= 5`, `X1 <= X2 <= 10` e `X2 <= X3 <= 50`, usando as três políticas.

As cinco melhores configurações encontradas foram:

| X1 | X2 | X3 | Política | Custo | Tempo médio |
|---:|---:|---:|---|---:|---:|
| 5 | 5 | 25 | LRU | 1500 | 14.01 |
| 5 | 5 | 25 | FIFO | 1500 | 14.10 |
| 5 | 5 | 25 | LFU | 1500 | 14.30 |
| 2 | 10 | 40 | LRU | 1300 | 14.37 |
| 2 | 10 | 41 | LRU | 1310 | 14.37 |

## 6. Análise Crítica

A configuração de alto desempenho reduziu o tempo médio de acesso em relação às configurações
menores, mas também aumentou bastante o custo. A configuração `alto_desempenho` com LRU teve
tempo médio de 13.42 e custo 2000. Já a melhor configuração sob custo até 1500 foi `X1=5`,
`X2=5`, `X3=25` com LRU, tempo médio de 14.01. Isso representa desempenho próximo ao máximo
testado, mas com custo 25% menor.

Nos resultados agregados, LRU foi a política mais consistente. Ela obteve o menor tempo médio
nas três configurações principais. FIFO ficou próximo em alguns casos, mas tende a perder quando
o padrão se beneficia de reutilização recente. LFU foi útil para preservar blocos frequentes, mas
teve resultado pior no agregado porque alguns padrões mudam de fase; nesses casos, frequências
antigas podem manter blocos que já não são tão úteis.

O aumento de L1 teve impacto importante no tempo médio porque acertos em L1 custam apenas 1.
Entretanto, aumentar L1 é caro. Por isso, a busca competitiva favoreceu `X1=5`, mas reduziu L2 e
L3 em relação à configuração máxima, equilibrando custo e desempenho.

## 7. Conclusão

O simulador atende aos requisitos principais do enunciado: permite configurar os tamanhos das
caches, escolher a política de substituição, processar strings de entrada, simular uma hierarquia
inclusiva, calcular as métricas obrigatórias e validar as restrições de configuração.

Pelos experimentos, a configuração recomendada sob custo máximo 1500 é:

```text
X1=5, X2=5, X3=25, política LRU
```

Essa configuração apresentou o melhor tempo médio dentro da restrição adotada e ficou próxima
do desempenho da configuração máxima, com custo menor.
