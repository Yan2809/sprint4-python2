# Camila de Mendonça da Silva - RM: 565491
# Guilherme de Araújo Moreira - RM: 561848
# Yan Breno Barutti Conceição - RM: 566412

# Importa todas as funções do módulo funcoes_enchente
from funcoes_enchente import *


# Define o caminho onde o arquivo JSON com os dados será salvo
caminho_arquivo = "bd.json"

# Define os valores válidos que o nível da água pode ter
parametroAgua = ["1", "2", "3", "4", "5"]

# Define a mensagem de menu para o usuário escolher a ação
pergunta = ("\n O que deseja realizar?\n"
            "<I> - Para Inserir caso de enchente\n"
            "<P> - Para Pesquisar um local com enchente\n"
            "<E> - Para Excluir um relato de enchente\n"
            "<L> - Para Listar relatos de enchente\n"
            "<S> - Para Sair do sistema:\n-> ")

# Carrega os dados já existentes no arquivo JSON
enchentes = carregar_usuarios(caminho_arquivo)

# Loop principal do sistema
while True:
    # Pede ao usuário uma opção do menu
    opcao = escolherOpcao(pergunta)

    if opcao == "I":
        # Insere um novo relato de enchente
        bairro = validarEntrada("Digite o bairro em que a enchente está localizada:\n-> ")
        if enchente_relatada(enchentes, bairro):
            print("A enchente já foi relatada! A equipe Arca e a população agradecem sua contribuição!")
        else:
            # Coleta os dados da enchente
            nivelAgua = validarEntradaLimitada("De 1 a 5, qual o nível da água?\n-> ", parametroAgua)
            viasInterditadas = validarEntrada("Quais ruas e avenidas foram afetadas?\n-> ")
            faltaEnergia = validarEntrada("Está faltando energia?\n-> ")
            faltaAgua = validarEntrada("Está faltando água?\n-> ")
            observacoes = input("\nHá mais detalhes? (Ex.: Quedas de postes, árvores ou deslizamentos)\n-> ")

            # Adiciona e salva os dados
            adicionar_enchente(enchentes, bairro, nivelAgua, viasInterditadas, faltaEnergia, faltaAgua, observacoes)
            salvar_enchente(enchentes, caminho_arquivo)

            print("✅ Enchente relatada com sucesso!")

    elif opcao == "P":
        # Pesquisa um bairro por relato de enchente
        bairro = validarEntrada("Digite o bairro que deseja buscar por enchente:\n-> ")
        detalhes = buscar_enchente(enchentes, bairro)
        if detalhes:
            # Exibe os detalhes encontrados
            print("Nível da Água: ", detalhes["nível_água"])
            print("Vias Interditadas: ", detalhes["vias_interditadas"])
            print("Falta de Energia: ", detalhes["falta_energia"])
            print("Falta de Água: ", detalhes["falta_água"])
            print("Observações: ", detalhes["observações"])
        else:
            print("Nenhuma enchente relatada no bairro pesquisado!")

    elif opcao == "E":
        # Exclui um relato de enchente
        bairro = validarEntrada("Digite o bairro que deseja excluir a enchente:\n-> ")
        if excluir_enchente(enchentes, bairro):
            salvar_enchente(enchentes, caminho_arquivo)
            print(f"✅ Enchente do bairro {bairro} excluída com sucesso!")
        else:
            print(f"⚠️ Nenhuma enchente relatada no bairro requerido!")

    elif opcao == "L":
        # Lista todos os relatos registrados
        listar_enchentes(enchentes)

    elif opcao == "S":
        # Sai do sistema
        print("Fechando o sistema... A equipe Arca agradece a colaboração!!")
        break

    else:
        # Caso o usuário digite uma opção inválida
        print("⚠️ Opção inválida. Tente novamente.")
