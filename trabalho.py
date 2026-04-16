import sys
import re
from collections import OrderedDict


class EstruturaCache:
    def __init__(self):
        self.acesso = 0
        self.custo = 0
        self.tamanho = 0
        self.tamanhoMaximo = 0
        self.list = []
        self.ordem_insercao = []  # Usado pelo LFU para desempate FIFO
        self.frequencia = {}

    def busca(self, bloco, algoritmo=None):
        if bloco in self.list:
            # LRU: move o bloco para o final (mais recente)
            if algoritmo == "LRU":
                self.list.remove(bloco)
                self.list.append(bloco)
            # LFU: incrementa a frequência de uso
            if algoritmo == "LFU":
                self.frequencia[bloco] = self.frequencia.get(bloco, 0) + 1
            return True
        else:
            return False

    def insere(self, bloco, algoritmo):
        # Evita duplicatas na cache
        if bloco in self.list:
            return
        if algoritmo == "FIFO":
            self.fifo_substituir(bloco)
        elif algoritmo == "LRU":
            self.lru_substituir(bloco)
        elif algoritmo == "LFU":
            self.lfu_substituir(bloco)

    def fifo_substituir(self, novo_bloco):
        if len(self.list) < self.tamanhoMaximo:
            self.list.append(novo_bloco)
            self.tamanho += 1
        else:
            self.list.pop(0)  # Remove o primeiro (mais antigo)
            self.list.append(novo_bloco)

    def lru_substituir(self, novo_bloco):
        if len(self.list) < self.tamanhoMaximo:
            self.list.append(novo_bloco)
            self.tamanho += 1
        else:
            self.list.pop(0)  # Remove o menos recentemente usado (primeiro da lista)
            self.list.append(novo_bloco)

    def lfu_substituir(self, novo_bloco):
        if len(self.list) < self.tamanhoMaximo:
            self.list.append(novo_bloco)
            self.tamanho += 1
            self.frequencia[novo_bloco] = 1
            self.ordem_insercao.append(novo_bloco)
        else:
            # Encontra a menor frequência
            menor_freq = min(self.frequencia[b] for b in self.list)
            # Entre os blocos com menor frequência, usa FIFO (mais antigo na ordem de inserção)
            candidatos = [
                b
                for b in self.ordem_insercao
                if b in self.list and self.frequencia.get(b, 0) == menor_freq
            ]
            bloco_remover = candidatos[0]
            self.list.remove(bloco_remover)
            self.ordem_insercao.remove(bloco_remover)
            del self.frequencia[bloco_remover]
            self.list.append(novo_bloco)
            self.frequencia[novo_bloco] = 1
            self.ordem_insercao.append(novo_bloco)


class L1(EstruturaCache):
    def __init__(self):
        super().__init__()
        self.acesso = 1
        self.custo = 200
        self.tamanhoMaximo = 5


class L2(EstruturaCache):
    def __init__(self):
        super().__init__()
        self.acesso = 3
        self.custo = 150
        self.tamanhoMaximo = 10


class L3(EstruturaCache):
    def __init__(self):
        super().__init__()
        self.acesso = 6
        self.custo = 10
        self.tamanhoMaximo = 50


class RAM(EstruturaCache):
    def __init__(self, blocos_distintos):
        super().__init__()
        self.acesso = 16
        self.custo = 1
        self.tamanho = len(blocos_distintos)
        self.tamanhoMaximo = len(blocos_distintos)
        self.list = list(blocos_distintos)


#  PADRÕES DE ACESSO PREDEFINIDOS

# Padrão 1: Alta localidade temporal (poucos blocos repetidos muitas vezes)
# Blocos: "ab", "cd" se repetem muitas vezes → alta taxa de hit
PADRAO_ALTA_LOCALIDADE = (
    "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
    "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
    "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
)

# Padrão 2: Quase aleatório (muitos blocos distintos, pouca repetição)
# Muitos blocos diferentes → cache não consegue reter
PADRAO_QUASE_ALEATORIO = (
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMN"
    "OPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzAB"
    "CDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnop"
)

# Padrão 3: Com fases distintas (começa repetitivo, depois aleatório)
# Fase 1: repete "ab", "cd" | Fase 2: muitos blocos novos
PADRAO_COM_FASES = (
    "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
    "efghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQR"
    "STUVWXYZabcdefghijklmnopqrstuvwxyzABCDEF"
)


def tratamentoStringEntrada(stringEntrada):
    # Regex que permite apenas letras maiúsculas e minúsculas
    textoTratado = re.sub("[^a-zA-Z]", "", stringEntrada)

    # Verifica se o tamanho é impar e remove o ultimo caractere
    if len(textoTratado) % 2 != 0:
        textoTratado = textoTratado[:-1]

    # Divide a string em blocos de 2 caracteres
    blocos = []
    for i in range(0, len(textoTratado), 2):
        blocos.append(textoTratado[i : i + 2])

    return blocos


def validar_configuracao(x1, x2, x3, algoritmo):
    if not all(isinstance(x, int) for x in (x1, x2, x3)):
        return False, "X1, X2 e X3 devem ser inteiros."

    if not all(x > 0 for x in (x1, x2, x3)):
        return False, "X1, X2 e X3 devem ser maiores que zero."

    if x1 > 5:
        return False, "X1 deve ser menor ou igual a 5."

    if x2 > 10:
        return False, "X2 deve ser menor ou igual a 10."

    if x3 > 50:
        return False, "X3 deve ser menor ou igual a 50."

    if not (x1 <= x2 <= x3):
        return False, "A configuração deve respeitar X1 <= X2 <= X3."

    if algoritmo not in ["FIFO", "LRU", "LFU"]:
        return False, "Algoritmo inválido. Use: FIFO, LRU ou LFU."

    return True, "Configuração válida."


class Simulador:
    def __init__(self, blocos, x1, x2, x3, algoritmo):
        self.blocos = blocos
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3
        self.algoritmo = algoritmo

        # Cria os níveis de cache
        self.l1 = L1()
        self.l1.tamanhoMaximo = x1
        self.l2 = L2()
        self.l2.tamanhoMaximo = x2
        self.l3 = L3()
        self.l3.tamanhoMaximo = x3

        # RAM com blocos distintos da entrada
        blocos_distintos = set(blocos)
        self.ram = RAM(blocos_distintos)

        # Contadores de métricas
        self.acertos_l1 = 0
        self.acertos_l2 = 0
        self.acertos_l3 = 0
        self.acessos_ram = 0
        self.tempo_total = 0
        self.total_acessos = len(blocos)

    def simular(self):
        for bloco in self.blocos:
            if self.l1.busca(bloco, self.algoritmo):
                self.tempo_total += self.l1.acesso
                self.acertos_l1 += 1
            elif self.l2.busca(bloco, self.algoritmo):
                self.tempo_total += self.l1.acesso + self.l2.acesso
                self.acertos_l2 += 1
                self.l1.insere(bloco, self.algoritmo)
            elif self.l3.busca(bloco, self.algoritmo):
                self.tempo_total += self.l1.acesso + self.l2.acesso + self.l3.acesso
                self.acertos_l3 += 1
                self.l1.insere(bloco, self.algoritmo)
                self.l2.insere(bloco, self.algoritmo)
            else:
                self.tempo_total += (
                    self.l1.acesso + self.l2.acesso + self.l3.acesso + self.ram.acesso
                )
                self.acessos_ram += 1
                self.l1.insere(bloco, self.algoritmo)
                self.l2.insere(bloco, self.algoritmo)
                self.l3.insere(bloco, self.algoritmo)

    def calcular_metricas(self):
        # Custo total da configuração: 200*X1 + 150*X2 + 10*X3
        custo_total = (
            (self.l1.custo * self.x1)
            + (self.l2.custo * self.x2)
            + (self.l3.custo * self.x3)
        )

        # Taxas de acerto
        taxa_l1 = (
            (self.acertos_l1 / self.total_acessos * 100)
            if self.total_acessos > 0
            else 0
        )
        taxa_l2 = (
            (self.acertos_l2 / self.total_acessos * 100)
            if self.total_acessos > 0
            else 0
        )
        taxa_l3 = (
            (self.acertos_l3 / self.total_acessos * 100)
            if self.total_acessos > 0
            else 0
        )

        # Taxa global de faltas (acessos que foram para RAM)
        taxa_faltas = (
            (self.acessos_ram / self.total_acessos * 100)
            if self.total_acessos > 0
            else 0
        )

        # Tempo médio de acesso
        tempo_medio = (
            (self.tempo_total / self.total_acessos) if self.total_acessos > 0 else 0
        )

        return {
            "custo_total": custo_total,
            "taxa_l1": taxa_l1,
            "taxa_l2": taxa_l2,
            "taxa_l3": taxa_l3,
            "taxa_faltas": taxa_faltas,
            "tempo_medio": tempo_medio,
        }

    def exibir_relatorio(self):
        metricas = self.calcular_metricas()

        print("=" * 50)
        print("         RELATÓRIO DA SIMULAÇÃO")
        print("=" * 50)
        print(f"  1. Configuração: X1={self.x1}, X2={self.x2}, X3={self.x3}")
        print(f"     Política de substituição: {self.algoritmo}")
        print(f"  2. Custo total da configuração: {metricas['custo_total']}")
        print(f"  3. Número total de acessos: {self.total_acessos}")
        print("-" * 50)
        print(f"  4. Acertos na L1: {self.acertos_l1}")
        print(f"  5. Acertos na L2: {self.acertos_l2}")
        print(f"  6. Acertos na L3: {self.acertos_l3}")
        print(f"  7. Acessos à RAM: {self.acessos_ram}")
        print("-" * 50)
        print(f"  8. Taxa de acerto L1: {metricas['taxa_l1']:.2f}%")
        print(f"  9. Taxa de acerto L2: {metricas['taxa_l2']:.2f}%")
        print(f" 10. Taxa de acerto L3: {metricas['taxa_l3']:.2f}%")
        print(f" 11. Taxa global de faltas: {metricas['taxa_faltas']:.2f}%")
        print("-" * 50)
        print(f" 12. Tempo total de acesso: {self.tempo_total}")
        print(f" 13. Tempo médio de acesso: {metricas['tempo_medio']:.2f}")
        print("=" * 50)


if __name__ == "__main__":
    # Separa os argumentos da linha de comando
    stringEntrada = sys.argv[1]
    x1, x2, x3 = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    algoritmo = sys.argv[5]

    # Confere parametros e algoritmo
    valido, mensagem = validar_configuracao(x1, x2, x3, algoritmo)
    if not valido:
        print(mensagem)
        sys.exit(1)

    # Trata a string de entrada
    blocos = tratamentoStringEntrada(stringEntrada)

    # Hierarquia de memória inclusiva
    simulador = Simulador(blocos, x1, x2, x3, algoritmo)
    simulador.simular()
    simulador.exibir_relatorio()
