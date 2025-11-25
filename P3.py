import time
from datetime import datetime

def carregar_produtos(arquivo):
    produtos = []
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            for linha in f:
                linha = linha.strip()
                if not linha:
                    continue
                
                partes = [p.strip() for p in linha.split('|')]
                if len(partes) == 6:
                    produto = {
                        'id': partes[0],
                        'nome': partes[1],
                        'preco': float(partes[2]),
                        'estoque': int(partes[3]),
                        'popularidade': int(partes[4]),
                        'data_cadastro': partes[5]
                    }
                    produtos.append(produto)
        
        print(f"✓ {len(produtos)} produtos carregados com sucesso!")
        return produtos
    except FileNotFoundError:
        print(f"✗ Erro: Arquivo '{arquivo}' não encontrado!")
        return []
    except Exception as e:
        print(f"✗ Erro ao carregar produtos: {e}")
        return []


def insertion_sort(lista, criterio):
    n = len(lista)
    i = 1
    while i < n:
        chave = lista[i]
        j = i - 1
        while j >= 0 and lista[j][criterio] > chave[criterio]:
            lista[j + 1] = lista[j]
            j = j - 1
        lista[j + 1] = chave
        i = i + 1
    return lista


def merge_sort(lista, criterio):
    if len(lista) <= 1:
        return lista
    
    meio = len(lista) // 2
    esquerda = merge_sort(lista[:meio], criterio)
    direita = merge_sort(lista[meio:], criterio)
    
    return merge(esquerda, direita, criterio)


def merge(esquerda, direita, criterio):
    resultado = []
    i = 0
    j = 0
    
    while i < len(esquerda) and j < len(direita):
        if esquerda[i][criterio] <= direita[j][criterio]:
            resultado.append(esquerda[i])
            i = i + 1
        else:
            resultado.append(direita[j])
            j = j + 1
    
    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])
    
    return resultado


def ordenar_produtos(lista_produtos, criterio, algoritmo):
    lista_copia = lista_produtos.copy()
    
    criterios_validos = ['preco', 'estoque', 'popularidade', 'data', 'nome']
    if criterio not in criterios_validos:
        print(f"✗ Critério inválido: {criterio}")
        return lista_copia
    
    campo_ordenacao = 'data_cadastro' if criterio == 'data' else criterio
    
    if algoritmo == 'insercao':
        return insertion_sort(lista_copia, campo_ordenacao)
    elif algoritmo == 'intercalacao':
        return merge_sort(lista_copia, campo_ordenacao)
    else:
        print(f"✗ Algoritmo inválido: {algoritmo}")
        return lista_copia


def salvar_resultado(lista_produtos, arquivo_saida):
    try:
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            for produto in lista_produtos:
                linha = f"{produto['id']} | {produto['nome']} | {produto['preco']} | {produto['estoque']} | {produto['popularidade']} | {produto['data_cadastro']}\n"
                f.write(linha)
        print(f"✓ Resultado salvo em '{arquivo_saida}'")
        return True
    except Exception as e:
        print(f"✗ Erro ao salvar resultado: {e}")
        return False


def carregar_requisicoes(arquivo):
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            requisicoes = [linha.strip() for linha in f if linha.strip()]
        print(f"✓ {len(requisicoes)} requisições carregadas!")
        return requisicoes
    except FileNotFoundError:
        print(f"✗ Erro: Arquivo '{arquivo}' não encontrado!")
        return []


def executar_testes():
    print("COMPARAÇÃO DE ALGORITMOS DE ORDENAÇÃO")
    print()
    
    arquivo_entrada = 'projeto_3_lista_produtos_entrada.txt'
    produtos = carregar_produtos(arquivo_entrada)
    
    if not produtos:
        print("Não foi possível carregar os produtos. Encerrando...")
        return
    
    print()
    
    arquivo_requisicoes = 'projeto_3_requisicoes_listagem.txt'
    requisicoes = carregar_requisicoes(arquivo_requisicoes)
    
    if not requisicoes:
        print("Não foi possível carregar as requisições. Encerrando...")
        return
    
    print()
    print("EXECUTANDO TESTES")
    print()
    
    algoritmos = ['insercao', 'intercalacao']
    tempos = {algo: {crit: 0 for crit in requisicoes} for algo in algoritmos}
    
    for algoritmo in algoritmos:
        print(f"TESTANDO ALGORITMO: {algoritmo.upper()}")
        
        tempo_total_algoritmo = 0
        
        for criterio in requisicoes:
            print(f"  Ordenando por: {criterio}... ", end='', flush=True)
            
            inicio = time.time()
            lista_ordenada = ordenar_produtos(produtos, criterio, algoritmo)
            fim = time.time()
            
            tempo_execucao = fim - inicio
            tempos[algoritmo][criterio] = tempo_execucao
            tempo_total_algoritmo = tempo_total_algoritmo + tempo_execucao
            
            print(f"✓ [{tempo_execucao:.6f}s]")
            
            nome_arquivo = f"projeto_3_resultado_{algoritmo}_{criterio}.txt"
            salvar_resultado(lista_ordenada, nome_arquivo)
        
        print(f"\n  Tempo total ({algoritmo}): {tempo_total_algoritmo:.6f}s")
    
    print()
    print("RESUMO DA COMPARAÇÃO")
    print()
    print(f"{'Critério':<20} {'Inserção (s)':<15} {'Intercalação (s)':<15} {'Mais Rápido':<15}")
    print("─" * 70)
    
    for criterio in requisicoes:
        tempo_insercao = tempos['insercao'][criterio]
        tempo_intercalacao = tempos['intercalacao'][criterio]
        mais_rapido = 'Inserção' if tempo_insercao < tempo_intercalacao else 'Intercalação'
        
        print(f"{criterio:<20} {tempo_insercao:<15.6f} {tempo_intercalacao:<15.6f} {mais_rapido:<15}")
    
    print("─" * 70)
    tempo_total_insercao = sum(tempos['insercao'].values())
    tempo_total_intercalacao = sum(tempos['intercalacao'].values())
    
    print(f"{'TOTAL':<20} {tempo_total_insercao:<15.6f} {tempo_total_intercalacao:<15.6f}")
    print()
    
    if tempo_total_insercao < tempo_total_intercalacao:
        diferenca = tempo_total_intercalacao - tempo_total_insercao
        percentual = (diferenca / tempo_total_intercalacao) * 100
        print(f"✓ Insertion Sort foi {percentual:.2f}% mais rápido no total!")
    else:
        diferenca = tempo_total_insercao - tempo_total_intercalacao
        percentual = (diferenca / tempo_total_insercao) * 100
        print(f"✓ Merge Sort foi {percentual:.2f}% mais rápido no total!")
    
    print()
    print("TESTE CONCLUÍDO COM SUCESSO!")


if __name__ == "__main__":
    executar_testes()