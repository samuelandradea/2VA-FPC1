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

    def search_sequential(self, target):
        current = self.head
        while current:
            if current.id == target:
                return 1
            current = current.next
        return -1


def carregar_ids(caminho):
    with open(caminho) as f:
        return [int(line) for line in f if line.strip()]


def salvar_resultados(caminho, resultados):
    with open(caminho, "w") as f:
        f.write("\n".join(map(str, resultados)))


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
        id_meio = vetor[meio][0]
        if id_meio == alvo:
            return 1
        elif alvo < id_meio:
            fim = meio - 1
        else:
            inicio = meio + 1
    return -1


def executar_buscas(func, itens):
    resultados = []
    start = perf_counter()
    for item in itens:
        resultados.append(func(item))
    end = perf_counter()
    return resultados, (end - start) * 1000


def gerar_grafico(tempo_seq, tempo_bin, caminho):
    labels = ["Sequencial", "Binária"]
    tempos = [tempo_seq, tempo_bin]
    plt.bar(labels, tempos)
    plt.ylabel("Tempo (ms)")
    plt.title("Comparação Projeto 1")
    plt.savefig(caminho)
    plt.close()


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    dados = os.path.join(base, "dados")
    resultados = os.path.join(base, "resultados")
    grafico = os.path.join(base, "grafico")

    os.makedirs(resultados, exist_ok=True)
    os.makedirs(grafico, exist_ok=True)

    entrada = carregar_ids(os.path.join(dados, "projeto_1_lista_IDs_entrada.txt"))
    busca = carregar_ids(os.path.join(dados, "projeto_1_lista_IDs_busca.txt"))
    referencia = os.path.join(dados, "projeto_1_lista_IDs_resultado.txt")

    lista = LinkedList()
    for idv in entrada:
        lista.insert_sorted(idv)

    vetor = criar_vetor_indices(lista)

    resultados_seq, t_seq = executar_buscas(lista.search_sequential, busca)
    resultados_bin, t_bin = executar_buscas(lambda x: busca_binaria_vetor(vetor, x), busca)

    salvar_resultados(os.path.join(resultados, "projeto_1_resultado_busca_sequencial.txt"), resultados_seq)
    salvar_resultados(os.path.join(resultados, "projeto_1_resultado_busca_binaria.txt"), resultados_bin)

    gerar_grafico(t_seq, t_bin, os.path.join(grafico, "comparacao.png"))

    print("Tempo sequencial:", t_seq, "ms")
    print("Tempo binária:", t_bin, "ms")

    ref_path = os.path.join(dados, "projeto_1_lista_IDs_resultado.txt")
    if os.path.exists(ref_path):
        esperados = carregar_ids(ref_path)
        print("Sequencial confere:", resultados_seq == esperados)
        print("Binária confere:", resultados_bin == esperados)


if __name__ == "__main__":
    main()
