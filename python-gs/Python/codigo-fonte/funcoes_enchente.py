import json  # Biblioteca para manipular arquivos JSON
import os    # Biblioteca para verificar existência de arquivos


# Função que carrega o conteúdo do arquivo JSON (caso exista)
def carregar_usuarios(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        return {}  # Retorna dicionário vazio se o arquivo não existir
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)  # Retorna os dados carregados do JSON


# Função que salva os dados de enchentes no arquivo JSON
def salvar_enchente(enchentes, caminho_arquivo):
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        json.dump(enchentes, arquivo, indent=4, ensure_ascii=False)


# Função que lê a opção escolhida pelo usuário e converte para maiúscula
def escolherOpcao(msg):
    return input(msg).upper()


# Verifica se um bairro já possui enchente registrada
def enchente_relatada(enchentes, bairro):
    return bairro in enchentes


# Adiciona uma nova enchente ao dicionário de enchentes
def adicionar_enchente(enchentes, bairro, nivelAgua, viasInterditadas, faltaEnergia, faltaAgua, observacoes):
    enchentes[bairro] = {
        "nível_água": nivelAgua,
        "vias_interditadas": viasInterditadas,
        "falta_energia": faltaEnergia,
        "falta_água": faltaAgua,
        "observações": observacoes
    }


# Busca as informações de enchente de um bairro
def buscar_enchente(enchentes, bairro):
    return enchentes.get(bairro)  # Retorna None se não encontrar


# Remove um relato de enchente de um bairro
def excluir_enchente(enchentes, bairro):
    return enchentes.pop(bairro, None)  # Remove o bairro se existir


# Exibe todos os bairros com enchente relatada
def listar_enchentes(enchentes):
    for bairro, detalhes in enchentes.items():
        print("\nBairro: ", bairro)
        print("Nível da Água: ", detalhes["nível_água"])
        print("Vias Interditadas: ", detalhes["vias_interditadas"])
        print("Falta de Energia: ", detalhes["falta_energia"])
        print("Falta de Água: ", detalhes["falta_água"])
        print("Observações: ", detalhes["observações"])
        print("-" * 30)


# Valida se o usuário preencheu algum texto
def validarEntrada(msg):
    valor = input(f"\n{msg}")
    while valor == "":
        print("\nÉ necessário preencher o campo")
        valor = input(msg)
    return valor


# Valida se o valor digitado está dentro de uma lista permitida (ex: nível da água)
def validarEntradaLimitada(msg, lista):
    valor = input(f"\n{msg}")
    while valor not in lista:
        print("\nÉ necessário preencher o campo com um valor dentro do parâmetro")
        valor = input(msg)
    return valor
