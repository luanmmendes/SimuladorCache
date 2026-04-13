
T1 = int(input("Qual o tamanho da memória L1?"))
while T1 >5:
   print("tamanho máximo válido é 5.\n digite um válor valido")
   T1 = int(input())
T2 = int(input("Qual o tamanho da memória L2?"))
while (T2 > 10):
    print("Tamanho máximo valido é 10\n digite um valor valido:") 
    T2 = int(input())
T3 = int(input("Qual o tamanho da memória L3?"))
while T3>50:
    print("Tamanho máximo valido é 50\n Digite um valor Válido:")
    T3 = int(input())


class Cache1(): 
    def __init__(self,T1):
        self.acesso = 1
        self.T1 = T1
        self.Custo = 200
        self.arm = []
class Cache2():
    def __init__(self,T2):
        self.acesso = 3
        self.custo = 50
        self.T2 = T2
        self.arm = []
class Cache3():
    def __init__(self,T3):
        self.acesso = 6
        self.custo = 10
        self.T3 = T3
        self.arm = []
class Cache4():
    def __init__(self,):
        self.acesso = 16
        self.custo = 1
        self.arm = []
    #  self.tamanho fixo, mas o que define o tamanho? fixo em quanto?

CacheL1 = Cache1(T1)
CacheL2 = Cache2(T2)
CacheL3 = Cache3(T3)
RAM = Cache4()
print(CacheL1.T1,CacheL1.Custo,CacheL1.acesso)
print(CacheL2.T2,CacheL2.custo,CacheL2.acesso)
print(CacheL3.T3,CacheL3.custo,CacheL3.acesso)
#checa se tem uma string na memoria, busca em cada um dos locais, se der errado, vai na proxima, se der errado, na prox, isso ate chegar na ram

