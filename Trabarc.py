import random
import os

acesso_contador = 0  # Contador global para o algoritmo LRU
algoritmo_substituicao = "FIFO"

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

class Bloco:
    def __init__(self, index, n1, n2, n3, n4, n5):
        self.index = index
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.n4 = n4
        self.n5 = n5

class Cache:
    def __init__(self, index, bloco, FIFO, LRU, LFU):
        self.index = index
        self.bloco = bloco
        self.FIFO = FIFO
        self.LRU = LRU
        self.LFU = LFU
        self.modificado = False

def inicializar_memoria_principal():
    """Realiza a simulação da memória principal (RAM)"""
    memoria_principal = []
    valores = list(range(1, 1251))  # Lista de números de 1 a 1251
    random.shuffle(valores)  # Embaralha os números para distribuição aleatória

    indice = 0
    for i in range(250):  # 250 blocos
        bloco = Bloco(index=i, n1=valores[indice], n2=valores[indice + 1], 
                      n3=valores[indice + 2], n4=valores[indice + 3], n5=valores[indice + 4])
        memoria_principal.append(bloco)
        indice += 5  # Avança para o próximo conjunto de 5 números
    return memoria_principal

def encontrar_bloco_por_dado(dado, memoria_principal):
    """Função utilizada para buscar na memoria ram o bloco com o valor especificado"""
    for bloco in memoria_principal:
        if dado in [bloco.n1, bloco.n2, bloco.n3, bloco.n4, bloco.n5]:
            return bloco
    return None

def acessar_memoria(dado, cache, memoria_principal, algoritmo, novo_valor=None):
    """Realiza os acessos à memoria, verificando se o dado está na Cache ou RAM, e aplica as modificações conforme sinalizado"""
    global acesso_contador

    bloco_encontrado = None
    for c in cache:
        if dado in [c.bloco.n1, c.bloco.n2, c.bloco.n3, c.bloco.n4, c.bloco.n5]:
            bloco_encontrado = c
            break

    if bloco_encontrado:
        # Cache hit
        print(f"Cache Hit: Dado {dado} encontrado na cache no bloco {bloco_encontrado.index}.")
        
        # Identificar qual valor foi acessado e modificar
        if novo_valor is not None:
            print(f"Modificando valor {dado} no bloco {bloco_encontrado.index} na cache.")
            if bloco_encontrado.bloco.n1 == dado:
                bloco_encontrado.bloco.n1 = novo_valor
            elif bloco_encontrado.bloco.n2 == dado:
                bloco_encontrado.bloco.n2 = novo_valor
            elif bloco_encontrado.bloco.n3 == dado:
                bloco_encontrado.bloco.n3 = novo_valor
            elif bloco_encontrado.bloco.n4 == dado:
                bloco_encontrado.bloco.n4 = novo_valor
            elif bloco_encontrado.bloco.n5 == dado:
                bloco_encontrado.bloco.n5 = novo_valor
            
            bloco_encontrado.modificado = True  # Marca como modificado para Write-Back

            # Write-Back: Atualiza a memória principal se necessário
            if bloco_encontrado.modificado:
                memoria_principal[bloco_encontrado.index] = bloco_encontrado.bloco
                print(f"Write-Back: Atualizando RAM com o bloco {bloco_encontrado.index} modificado.")

        # Atualizar contadores de acordo com o algoritmo
        if algoritmo == "LRU":
            acesso_contador += 1
            bloco_encontrado.LRU = acesso_contador
        elif algoritmo == "LFU":
            bloco_encontrado.LFU += 1

        return bloco_encontrado.bloco
    else:
        # Cache miss
        print(f"Cache Miss: Dado {dado} não encontrado na cache.")
        bloco_memoria = encontrar_bloco_por_dado(dado, memoria_principal)
        if bloco_memoria:
            substituir_na_cache(dado, bloco_memoria, cache, algoritmo, memoria_principal)
            return bloco_memoria
        else:
            print(f"Erro: Dado {dado} não encontrado na memória principal.")
            return None

def substituir_na_cache(dado, bloco_memoria, cache, algoritmo, memoria_principal, novo_valor=None):
    """Esta função substitui blocos na cache com base no algoritmo de substituição selecionado"""
    if len(cache) >= 5:
        if algoritmo == "FIFO":
            substituir_fifo(cache, memoria_principal)
        elif algoritmo == "LRU":
            substituir_lru(cache, memoria_principal)
        elif algoritmo == "LFU":
            substituir_lfu(cache, memoria_principal)

    global acesso_contador
    novo_cache = Cache(index=bloco_memoria.index, bloco=bloco_memoria, 
                       FIFO=len(cache) + 1, LRU=acesso_contador, LFU=1)
    
    if novo_valor is not None and bloco_memoria.n1 == dado:  # Aplica o valor modificado ao carregar o bloco
        print(f"Modificando valor no bloco {bloco_memoria.index} ao carregar para cache.")
        novo_cache.bloco.n1 = novo_valor
        novo_cache.modificado = True

    cache.append(novo_cache)
    print(f"Bloco {bloco_memoria.index} inserido na cache contendo o dado {dado}.")

def substituir_fifo(cache, memoria_principal):
    """Substitui o bloco mais antigo na cache e realiza o Write-Back se necessário"""
    menor_fifo = cache[0]
    for c in cache:
        if c.FIFO < menor_fifo.FIFO:
            menor_fifo = c

    if menor_fifo.modificado:
        memoria_principal[menor_fifo.index] = menor_fifo.bloco  # Atualiza a RAM
        print(f"Write-Back: Atualizando RAM com o bloco {menor_fifo.index}")

    cache.remove(menor_fifo)
    print(f"Substituindo bloco {menor_fifo.index} (FIFO) na cache.")

def substituir_lru(cache, memoria_principal):
    """Substitui o bloco menos recente usado na CACHE e realiza Write-Back se necessário"""
    menor_lru = cache[0]
    for c in cache:
        if c.LRU < menor_lru.LRU:
            menor_lru = c

    if menor_lru.modificado:
        memoria_principal[menor_lru.index] = menor_lru.bloco  # Atualiza a RAM
        print(f"Write-Back: Atualizando RAM com o bloco {menor_lru.index}")

    cache.remove(menor_lru)
    print(f"Substituindo bloco {menor_lru.index} (LRU) na cache.")

def substituir_lfu(cache, memoria_principal):
    """Substitui o bloco menos frequente usado na CACHE e realiza Write-Back se necessário"""
    menor_lfu = cache[0]
    for c in cache:
        if c.LFU < menor_lfu.LFU:
            menor_lfu = c

    if menor_lfu.modificado:
        memoria_principal[menor_lfu.index] = menor_lfu.bloco  # Atualiza a RAM
        print(f"Write-Back: Atualizando RAM com o bloco {menor_lfu.index}")

    cache.remove(menor_lfu)
    print(f"Substituindo bloco {menor_lfu.index} (LFU) na cache.")

'''def gerar_acessos_aleatorios(cache, memoria_principal, algoritmo, quantidade):
    """Simula os acessos aleatorios na memória"""
    for _ in range(quantidade):
        dado = random.randint(1, 1500)
        operacao = random.choice(["leitura", "modificacao"])

        if operacao == "leitura":
            acessar_memoria(dado, cache, memoria_principal, algoritmo)
        else:
            novo_valor = random.randint(1000, 2000)
            acessar_memoria(dado, cache, memoria_principal, algoritmo, novo_valor)'''

def reiniciar_simulacao(cache, memoria_principal):
    """Função utilizada quando necessário reinicializar a simulação"""
    global acesso_contador
    acesso_contador = 0
    cache.clear()
    memoria_principal.clear()
    memoria_principal.extend(inicializar_memoria_principal())  # Atualiza a memória
    print("Simulação reiniciada!")

def imprimir_cache(cache):
    """Imprime o estado atual da memória cache, realizando as formatações necessárias"""
    if not cache:
        print("A cache está vazia.")
        return

    print("\nBlocos atualmente na cache:")
    print("-" * 80)
    print(f"{'Bloco':<8}{'n1':<8}{'n2':<8}{'n3':<8}{'n4':<8}{'n5':<8}{'LFU':<8}{'FIFO':<8}{'LRU':<8}")
    print("-" * 80)

    for c in cache:
        print(f"{c.index:<8}{c.bloco.n1:<8}{c.bloco.n2:<8}{c.bloco.n3:<8}{c.bloco.n4:<8}{c.bloco.n5:<8}{c.LFU:<8}{c.FIFO:<8}{c.LRU:<8}")

    print("-" * 80)

def imprimir_ram(memoria_principal):
    """Imprime o estado atual da memória RAM, realizando as formatações necessárias"""
    print("\nEstado atual da RAM:")
    print("-" * 48)
    print(f"{'Bloco':<8}{'n1':<8}{'n2':<8}{'n3':<8}{'n4':<8}{'n5':<8}")
    print("-" * 48)

    for i, bloco in enumerate(memoria_principal):
        print(f"{i:<8}{bloco.n1:<8}{bloco.n2:<8}{bloco.n3:<8}{bloco.n4:<8}{bloco.n5:<8}")

    print("-" * 48)

def simular_acessos(memoria_principal, cache):
    """Simula o acesso à memória, permitindo que o usuário escolha um dado da memória principal para acessar e, se desejado,
    modificar o valor desse dado. O dado é acessado conforme o algoritmo de substituição selecionado.
    A função continua solicitando entradas até que o usuário escolha sair"""
    global algoritmo_substituicao
    while True:
        try:
            dado = int(input("Digite o dado que você deseja acessar (1 a 1250): "))
            if 1 <= dado <= 1250:
                modificar = input("Deseja modificar o valor do dado? (s/n): ").strip().lower()
                novo_valor = None
                if modificar == 's':
                    novo_valor = int(input("Digite o novo valor: "))
                acessar_memoria(dado, cache, memoria_principal, algoritmo_substituicao, novo_valor)
            else:
                print("Dado inválido. Tente novamente.")
                continue

            continuar = input("Deseja acessar outro dado? (s/n): ").strip().lower()
            if continuar != 's':
                break
        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")

def alterar_algoritmo():
    """Permite ao usuário escolher um novo algoritmo de substituição para ser utilizado no gerenciamento da cache. 
    Os algoritmos disponíveis são FIFO, LRU e LFU."""
    global algoritmo_substituicao
    while True:
        limpar_tela()
        print("Escolha o novo algoritmo de substituição:")
        print("[1] FIFO")
        print("[2] LRU")
        print("[3] LFU")
        escolha = input("Digite o número correspondente: ")

        if escolha == "1":
            algoritmo_substituicao = "FIFO"
        elif escolha == "2":
            algoritmo_substituicao = "LRU"
        elif escolha == "3":
            algoritmo_substituicao = "LFU"
        else:
            print("Opção inválida. Tente novamente.")
            continue

        print(f"\nNovo algoritmo de substituição selecionado: {algoritmo_substituicao}")
        break

def main():
    global algoritmo_substituicao

    memoria_principal = inicializar_memoria_principal()
    cache = []

    while True:
        print("\nMenu:")
        print("1. Simular acessos à memória")
        print("2. Imprimir valores da cache")
        print("3. Imprimir valores da RAM")
        print("4. Alterar algoritmo de substituição (Atual: {})".format(algoritmo_substituicao))
        print("5. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            simular_acessos(memoria_principal, cache)

        elif opcao == "2":
            imprimir_cache(cache)

        elif opcao == "3":
            imprimir_ram(memoria_principal)

        elif opcao == "4":
            alterar_algoritmo()

        elif opcao == "5":
            print("Encerrando o programa.")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
