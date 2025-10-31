import requests
import json  # Biblioteca para manipular arquivos JSON
import os    # Biblioteca para verificar existência de arquivos

# --- CONFIGURAÇÕES DA API ---
API_KEY = "4705a32acd79d708e8ad2d69c55523d5"
BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': API_KEY
}

caminho_arquivo = "favoritas.json"


# --- FUNÇÕES AUXILIARES ---

def forcar_escolha(msg, lista, erro):
    """
    Exibe uma mensagem e obriga o usuário a escolher um valor presente em 'lista'.
    Caso digite algo inválido, mostra a mensagem de erro e pergunta novamente.
    """
    escolha = input(f"\n{msg}\n-> ")
    while escolha not in lista:
        print(f'\n{erro}')
        escolha = input(f"{msg}\n-> ")
    return escolha


def consultar_id(escolha, lista):
    """
    Retorna o índice do item 'escolha' dentro da lista.
    Usado para mapear o que o usuário digitou ao ID correspondente.
    """
    return lista.index(escolha)


def criar_lista(informacoes, chave, campo):
    """
    Cria uma lista simples contendo apenas os valores de um campo específico.
    """
    lista = []
    for objeto in informacoes:
        lista.append(objeto[chave][campo])
    return lista


def obter_dados_api(endpoint, params):
    """
    Faz uma requisição GET para a API-Football.
    - endpoint: o recurso da API (ex: 'teams', 'players')
    - params: parâmetros da consulta (ex: {'league': 74, 'season': 2023})
    Retorna os dados já convertidos para dicionário Python.
    """
    url = f'{BASE_URL}/{endpoint}'
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code == 200:
        dados = response.json()

        # Se a API retornou erros explícitos
        if dados.get('errors') and dados['errors']:
            print(f"Erro retornado pela API: {dados.get('errors')}")
            return None

        # Caso especial: estatísticas de uma jogadora específica (retorna 1 objeto só)
        if endpoint == 'players' and 'id' in params:
            if dados.get("response"):
                return dados["response"][0]
            else:
                return None

        # Retorna lista padrão (times, jogadoras, etc.)
        return dados.get('response', [])

    # Tratamento de erros da API
    elif response.status_code == 401:
        print("❌ Erro de autenticação: verifique sua API KEY.")
    elif response.status_code == 404:
        print("⚠️ Dados não encontrados para esta consulta.")
    elif response.status_code == 429:
        print("🚫 Limite de requisições atingido! Tente novamente mais tarde.")
    else:
        print(f"❌ Erro inesperado da API: {response.status_code}, {response.text}")
    return None


# --- PROGRAMA PRINCIPAL ---

print("\nBem-vindo ao canal de informações do Brasileirão Feminino! ⚽")

liga = 74  # ID fixo da liga (Brasileirão Feminino)
anos = ["2021", "2022", "2023"]

while True:
    print("\n--- Consulta de Futebol Feminino ---")

    # 1) Escolher temporada
    temporada = forcar_escolha(f'Qual temporada deseja consultar? {anos}', anos, 'Temporada não está na lista!')

    # 2) Buscar times dessa temporada
    times = obter_dados_api('teams', {'league': liga, 'season': temporada})
    # 3) Tratamento de Erro do item 2
    if not times:
        print("Nenhum time encontrado para esta temporada")
        continue

    # 4) Cria uma lista apenas com os nomes dos times
    nomesTimes = criar_lista(times, 'team', 'name')

    # 5) Lista os times encontrados
    print("\nTimes encontrados:")
    for item in times:
        print(f"{item['team']['name']}")

    # 6) Escolher um time e identificar o id do mesmo para achá-lo na API
    escolhaTime = forcar_escolha('Qual time você deseja consultar as jogadoras?', nomesTimes, 'Time não está na lista!')
    idTimeEscolhido = consultar_id(escolhaTime, nomesTimes)
    timeEscolhido = times[idTimeEscolhido]['team']['id']

    # 7) Buscar jogadoras do time
    print(f"\nBuscando jogadoras do time: {escolhaTime}")
    jogadoras = obter_dados_api('players', {'team': timeEscolhido, 'season': temporada})

    # 8) Tratamento de erro do item 7
    if not jogadoras:
        print("Nenhuma jogadora encontrada para este time.")
    else:
        # 9) Lista as jogadoras encontradas do time escolhido, junto de suas respectivas nacionalidades
        print(f"\nJogadoras do {escolhaTime}:")
        for item in jogadoras:
            jogadora = item['player']
            print(f"Nome: {jogadora['name']}, Nacionalidade: {jogadora['nationality']}")

        # 10) Escolher uma jogadora e identificar o id da mesma para achá-la na API
        nomesJogadoras = criar_lista(jogadoras, 'player', 'name')
        escolhaJogadora = forcar_escolha('Qual jogadora você deseja consultar as estatísticas?', nomesJogadoras,
                                         'Jogadora não está na lista!')
        idJogadoraEscolhida = consultar_id(escolhaJogadora, nomesJogadoras)
        jogadoraEscolhida = jogadoras[idJogadoraEscolhida]['player']['id']

        # 11) Buscar estatísticas da jogadora
        print(f"\nBuscando estatísticas da jogadora: {escolhaJogadora}...")
        stats = obter_dados_api('players', {'id': jogadoraEscolhida, 'season': temporada})

        # 12) Verifica se a consulta retornou dados (stats) e se dentro desses dados existe a chave "statistics", na qual está as estatísticas da jogadora
        if stats and stats.get('statistics'):
            jogadora_info = stats['player']
            estatisticas = stats['statistics'][0]

            # 13) Exibe principais estatísticas
            print(f"\n--- Estatísticas de {jogadora_info['firstname']} {jogadora_info['lastname']} ---")
            print(f"Time: {estatisticas['team']['name']}")
            print(f"Liga: {estatisticas['league']['name']}")
            print(f"Posição: {estatisticas['games']['position']}")
            print(f"Partidas Jogadas: {estatisticas['games']['appearences']}")
            print(f"Gols: {estatisticas['goals']['total'] or 0}")
            print(f"Assistências: {estatisticas['goals']['assists'] or 0}")
        else:
            # 14) Se dentro dos dados não existir as estatísticas da jogadora, printa que não foram encontradas
            print("Não foram encontradas estatísticas para esta jogadora na temporada selecionada.")

    # 15) Pergunta se o usuário quer continuar
    resposta = ['s', 'n']
    continuar = forcar_escolha('Deseja continuar? [s/n]', resposta, 'Digite s ou n!')

    # 16) Se não quiser continuar, encerra o sistema
    if continuar == 'n':
        print("\n🚧 Encerrando o sistema...")
        break
