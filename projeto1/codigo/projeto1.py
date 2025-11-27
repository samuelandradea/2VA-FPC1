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
        if self.head is None:
            self.head = new_node
            return
        if id_val < self.head.id:
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


    def to_list(self):
        out = []
        cur = self.head
        while cur:
            out.append(cur.id)
            cur = cur.next
        return out


def carregar_ids(caminho):
    with open(caminho, "r") as f:
        return [int(line.strip()) for line in f if line.strip()]


def salvar_resultados(caminho, resultados):
    with open(caminho, "w") as f:
        for r in resultados:
            f.write(str(r) + "\n")


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


def executar_buscas_sequenciais(lista, ids_busca):
    resultados = []
    start = perf_counter()
    for idv in ids_busca:
        resultados.append(lista.search_sequential(idv))
    end = perf_counter()
    tempo_ms = (end - start) * 1000
    return resultados, tempo_ms


def executar_buscas_binarias(vetor, ids_busca):
    resultados = []
    start = perf_counter()
    for idv in ids_busca:
        resultados.append(busca_binaria_vetor(vetor, idv))
    end = perf_counter()
    tempo_ms = (end - start) * 1000
    return resultados, tempo_ms


def gerar_grafico(tempo_seq_ms, tempo_bin_ms, caminho_grafico):
    labels = ["Busca Sequencial", "Busca Binária"]
    tempos = [tempo_seq_ms, tempo_bin_ms]
    plt.figure(figsize=(6,4))
    plt.bar(labels, tempos)
    plt.ylabel("Tempo (ms)")
    plt.title("Comparação de Desempenho - Projeto 1")
    plt.tight_layout()
    plt.savefig(caminho_grafico)
    plt.close()


if __name__ == "__main__":
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    dados_dir = os.path.join(base, "dados")
    resultados_dir = os.path.join(base, "resultados")
    grafico_dir = os.path.join(base, "grafico")
    os.makedirs(resultados_dir, exist_ok=True)
    os.makedirs(grafico_dir, exist_ok=True)
    entrada_path = os.path.join(dados_dir, "projeto_1_lista_IDs_entrada.txt")
    busca_path = os.path.join(dados_dir, "projeto_1_lista_IDs_busca.txt")
    referencia_path = os.path.join(dados_dir, "projeto_1_lista_IDs_resultado.txt")
    ids_entrada = carregar_ids(entrada_path)
    ids_busca = carregar_ids(busca_path)
    lista = LinkedList()
    for idv in ids_entrada:
        lista.insert_sorted(idv)
    vetor = criar_vetor_indices(lista)
    resultados_seq, tempo_seq_ms = executar_buscas_sequenciais(lista, ids_busca)
    resultados_bin, tempo_bin_ms = executar_buscas_binarias(vetor, ids_busca)
    salvar_resultados(os.path.join(resultados_dir, "projeto_1_resultado_busca_sequencial.txt"), resultados_seq)
    salvar_resultados(os.path.join(resultados_dir, "projeto_1_resultado_busca_binaria.txt"), resultados_bin)
    gerar_grafico(tempo_seq_ms, tempo_bin_ms, os.path.join(grafico_dir, "comparacao.png"))
    print("Tempo busca sequencial (ms):", tempo_seq_ms)
    print("Tempo busca binária (ms):", tempo_bin_ms)
    print("Arquivo resultados sequencial:", os.path.join(resultados_dir, "projeto_1_resultado_busca_sequencial.txt"))
    print("Arquivo resultados binária:", os.path.join(resultados_dir, "projeto_1_resultado_busca_binaria.txt"))
    print("Gráfico salvo em:", os.path.join(grafico_dir, "comparacao.png"))
    if os.path.exists(referencia_path):
        refer = carregar_ids(referencia_path)
        ok_seq = all(int(a)==int(b) for a,b in zip(refer, resultados_seq))
        ok_bin = all(int(a)==int(b) for a,b in zip(refer, resultados_bin))
        print("Sequencial bate com referência:", ok_seq)
        print("Binária bate com referência:", ok_bin)
