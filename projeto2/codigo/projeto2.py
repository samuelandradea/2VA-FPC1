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
        """Insere em ordem, nó por nó (O(N) por inserção)"""
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

    def search_sequential(self, target):
        current = self.head
        while current:
            if current.id == target:
                return 1
            current = current.next
        return -1


def criar_vetor_indices(lista):
    vetor = []
    current = lista.head
    while current:
        vetor.append((current.id, current))
        current = current.next
    return vetor

def busca_binaria_vetor(vetor, alvo):
    inicio, fim = 0, len(vetor) - 1
    while inicio <= fim:
        meio = (inicio + fim) // 2
        if vetor[meio][0] == alvo:
            return 1
        if alvo < vetor[meio][0]:
            fim = meio - 1
        else:
            inicio = meio + 1
    return -1


class HashNode:
    def __init__(self, id_val):
        self.id = id_val
        self.next = None

class HashTable:
    def __init__(self, tamanho):
        self.tamanho = tamanho
        #cada posição aponta para a cabeça (HashNode) da lista encadeada
        self.tabela = [None] * tamanho

    def inserir(self, id_val):
        index = id_val % self.tamanho
        novo = HashNode(id_val)
        #insere no início da lista encadeada do bucket
        novo.next = self.tabela[index]
        self.tabela[index] = novo

    def buscar(self, id_val):
        index = id_val % self.tamanho
        atual = self.tabela[index]
        while atual:
            if atual.id == id_val:
                return 1
            atual = atual.next
        return -1


def carregar_ids(caminho):
    with open(caminho, "r") as f:
        return [int(line.strip()) for line in f if line.strip()]

def salvar_resultados(caminho, resultados):
    with open(caminho, "w") as f:
        f.write("\n".join(map(str, resultados)))

def medir_tempo(func, dados):
    resultados = []
    start = perf_counter()
    for x in dados:
        resultados.append(func(x))
    end = perf_counter()
    return resultados, (end - start) * 1000  # ms

def gerar_grafico(t1, t2, t3, caminho):
    plt.figure(figsize=(8,5))
    plt.bar(["Sequencial", "Binária", "Hash"], [t1, t2, t3])
    plt.ylabel("Tempo (ms)")
    plt.yscale("log")  #fizemos o grafico em escala logaritmica para melhor visualizacao e analise!!
    plt.title("Comparação de desempenho - Projeto 2")
    plt.tight_layout()
    plt.savefig(caminho)
    plt.close()


if __name__ == "__main__":
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    dados_dir = os.path.join(base, "dados")
    resultados_dir = os.path.join(base, "resultados")
    grafico_dir = os.path.join(base, "grafico")

    os.makedirs(resultados_dir, exist_ok=True)
    os.makedirs(grafico_dir, exist_ok=True)

    entrada_path = os.path.join(dados_dir, "projeto_2_lista_IDs_entrada.txt")
    busca_path = os.path.join(dados_dir, "projeto_2_lista_IDs_busca.txt")

    #carregar arquivos (lança exceção se não existir)
    ids_entrada = carregar_ids(entrada_path)
    ids_busca = carregar_ids(busca_path)

    #lista encadeada ordenada (inserção nó a nó) 
    lista = LinkedList()
    for idv in ids_entrada:
        lista.insert_sorted(idv)

    #vetor de indices (usado para busca binária)
    vetor = criar_vetor_indices(lista)

    #hashTable com lista encadeada manual 
    tabela = HashTable(7000)  #7000, pois esse foi o numero estipulado pelo senhor, no pdf que o senhor anexou no classroom.
    for idv in ids_entrada:
        tabela.inserir(idv)

    #medições
    res_seq, t_seq = medir_tempo(lista.search_sequential, ids_busca)
    res_bin, t_bin = medir_tempo(lambda x: busca_binaria_vetor(vetor, x), ids_busca)
    res_hash, t_hash = medir_tempo(tabela.buscar, ids_busca)

    #aqui nos salvamos os arquivos de saida, nao foi exigido para esse projeto, mas, por seguranca, resolvemos colocar aqui tambem.
    salvar_resultados(os.path.join(resultados_dir, "projeto_2_resultado_sequencial.txt"), res_seq)
    salvar_resultados(os.path.join(resultados_dir, "projeto_2_resultado_binaria.txt"), res_bin)
    salvar_resultados(os.path.join(resultados_dir, "projeto_2_resultado_hash.txt"), res_hash)

    #gráfico
    gerar_grafico(t_seq, t_bin, t_hash, os.path.join(grafico_dir, "projeto2_comparacao.png"))

    #resumo
    print(f"Tempo Sequencial: {t_seq:.3f} ms")
    print(f"Tempo Binária:    {t_bin:.3f} ms")
    print(f"Tempo Hash:       {t_hash:.3f} ms")
    print("Arquivos gerados em:", resultados_dir)
    print("Gráfico gerado em:", os.path.join(grafico_dir, "projeto2_comparacao.png"))
