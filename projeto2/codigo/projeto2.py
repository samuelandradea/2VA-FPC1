import os
from time import perf_counter
import matplotlib.pyplot as plt

class Node:
    def __init__(self, id_val):
        self.id = id_val
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def search_sequential(self, target):
        current = self.head
        while current:
            if current.id == target:
                return 1
            current = current.next
        return -1


def carregar_ids(caminho):
    with open(caminho, "r") as f:
        return [int(line.strip()) for line in f if line.strip()]


def criar_lista_encadeada(ids):
    lista = LinkedList()
    current = None
    for id_val in ids:
        new_node = Node(id_val)
        if lista.head is None:
            lista.head = new_node
            current = new_node
        else:
            current.next = new_node
            current = new_node
    return lista


def criar_vetor_indices(lista):
    vetor = []
    current = lista.head
    while current:
        vetor.append((current.id, current))
        current = current.next
    # o vetor SIM deve estar ordenado
    vetor.sort(key=lambda x: x[0])
    return vetor


def busca_binaria_vetor(vetor, alvo):
    inicio, fim = 0, len(vetor) - 1
    while inicio <= fim:
        meio = (inicio + fim) // 2
        valor = vetor[meio][0]
        if valor == alvo:
            return 1
        if alvo < valor:
            fim = meio - 1
        else:
            inicio = meio + 1
    return -1


class HashTable:
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.tabela = [[] for _ in range(tamanho)]

    def funcao_hash(self, id_val):
        return id_val % self.tamanho

    def inserir(self, id_val):
        self.tabela[self.funcao_hash(id_val)].append(id_val)

    def buscar(self, id_val):
        for x in self.tabela[self.funcao_hash(id_val)]:
            if x == id_val:
                return 1
        return -1


def tempo_lista(lista, ids):
    ini = perf_counter()
    r = [lista.search_sequential(x) for x in ids]
    fim = perf_counter()
    return r, (fim - ini) * 1000


def tempo_binario(vetor, ids):
    ini = perf_counter()
    r = [busca_binaria_vetor(vetor, x) for x in ids]
    fim = perf_counter()
    return r, (fim - ini) * 1000


def tempo_hash(tabela, ids):
    ini = perf_counter()
    r = [tabela.buscar(x) for x in ids]
    fim = perf_counter()
    return r, (fim - ini) * 1000


def gerar_grafico(t1, t2, t3, caminho):
    plt.figure(figsize=(7,5))
    plt.bar(["Sequencial", "Binária", "Hash"], [t1, t2, t3])
    plt.yscale("log")
    plt.ylabel("Tempo (ms) - escala logarítmica")
    plt.title("Comparação de desempenho - Projeto 2")
    plt.tight_layout()
    plt.savefig(caminho)
    plt.close()


if __name__ == "__main__":
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    dados_dir = os.path.join(base, "dados")
    grafico_dir = os.path.join(base, "grafico")
    os.makedirs(grafico_dir, exist_ok=True)

    entrada = os.path.join(dados_dir, "projeto_2_lista_IDs_entrada.txt")
    busca = os.path.join(dados_dir, "projeto_2_lista_IDs_busca.txt")

    ids_entrada = carregar_ids(entrada)
    ids_busca = carregar_ids(busca)

    lista = criar_lista_encadeada(ids_entrada)
    vetor = criar_vetor_indices(lista)

    tabela = HashTable(7000)
    for x in ids_entrada:
        tabela.inserir(x)

    res_seq, t_seq = tempo_lista(lista, ids_busca)
    res_bin, t_bin = tempo_binario(vetor, ids_busca)
    res_hash, t_hash = tempo_hash(tabela, ids_busca)

    gerar_grafico(t_seq, t_bin, t_hash, os.path.join(grafico_dir, "projeto2_comparacao.png"))

    print("Tempo Sequencial (ms):", t_seq)
    print("Tempo Binária (ms):", t_bin)
    print("Tempo Hash (ms):", t_hash)
