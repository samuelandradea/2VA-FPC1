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

    def insert_sorted(self, id_val):
        new_node = Node(id_val)
        if self.head is None or id_val < self.head.id:
            new_node.next = self.head
            self.head = new_node
            return

        current = self.head
        while current.next and current.next.id < id_val:
            current = current.next

        new_node.next = current.next
        current.next = new_node

    def search(self, target):
        current = self.head
        while current:
            if current.id == target:
                return 1
            current = current.next
        return -1


def carregar_ids(caminho):
    with open(caminho) as f:
        return [int(line) for line in f if line.strip()]


def criar_lista(ids):
    lista = LinkedList()
    for idv in ids:
        lista.insert_sorted(idv)
    return lista


def criar_vetor(lista):
    vetor = []
    current = lista.head
    while current:
        vetor.append((current.id, current))
        current = current.next
    return vetor


def busca_binaria(vetor, alvo):
    ini, fim = 0, len(vetor) - 1
    while ini <= fim:
        meio = (ini + fim) // 2
        valor = vetor[meio][0]
        if valor == alvo:
            return 1
        if alvo < valor:
            fim = meio - 1
        else:
            ini = meio + 1
    return -1


class HashTable:
    def __init__(self, tamanho):
        self.tabela = [[] for _ in range(tamanho)]
        self.tamanho = tamanho

    def _hash(self, val):
        return val % self.tamanho

    def inserir(self, val):
        self.tabela[self._hash(val)].append(val)

    def buscar(self, val):
        for x in self.tabela[self._hash(val)]:
            if x == val:
                return 1
        return -1


def medir_tempo(func, itens):
    ini = perf_counter()
    r = [func(x) for x in itens]
    fim = perf_counter()
    return r, (fim - ini) * 1000


def grafico(t1, t2, t3, caminho):
    plt.bar(["Sequencial", "Binária", "Hash"], [t1, t2, t3])
    plt.yscale("log")
    plt.title("Projeto 2 - comparação")
    plt.ylabel("ms")
    plt.savefig(caminho)
    plt.close()


if __name__ == "__main__":

    base = os.path.abspath(os.path.dirname(__file__))
    dados = os.path.join(base, "..", "dados")
    graf = os.path.join(base, "..", "grafico")

    os.makedirs(graf, exist_ok=True)

    ids = carregar_ids(os.path.join(dados, "projeto_2_lista_IDs_entrada.txt"))
    busca = carregar_ids(os.path.join(dados, "projeto_2_lista_IDs_busca.txt"))

    lista = criar_lista(ids)
    vetor = criar_vetor(lista)

    tabela = HashTable(7000)
    for x in ids:
        tabela.inserir(x)

    _, t_seq = medir_tempo(lista.search, busca)
    _, t_bin = medir_tempo(lambda x: busca_binaria(vetor, x), busca)
    _, t_hash = medir_tempo(tabela.buscar, busca)

    grafico(t_seq, t_bin, t_hash, os.path.join(graf, "comparacao2.png"))

    print("Sequencial:", t_seq)
    print("Binária:", t_bin)
    print("Hash:", t_hash)
