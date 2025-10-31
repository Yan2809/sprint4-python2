

def obter_dados_api(endpoint, params):
    """
    Faz uma requisição GET para a API-Football.
    - endpoint: o recurso da API (ex: 'teams', 'players')
    - params: parâmetros da consulta (ex: {'league': 74, 'season': 2023})
    Retorna os dados já convertidos para dicionário Python.
    """
    url = f'{BASE_URL}/{endpoint}'
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()  # Lança exceção para status de erro (4xx ou 5xx)
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

    except requests.exceptions.HTTPError as errh:
        if response.status_code == 401:
            print("❌ Erro de autenticação: verifique sua API KEY.")
        elif response.status_code == 404:
            print("⚠️ Dados não encontrados para esta consulta.")
        elif response.status_code == 429:
            print("🚫 Limite de requisições atingido! Tente novamente mais tarde.")
        else:
            print(f"❌ Erro HTTP: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"❌ Erro de Conexão: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"❌ Timeout da Requisição: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"❌ Erro Inesperado na Requisição: {err}")
    except json.JSONDecodeError:
        print("❌ Erro ao decodificar a resposta JSON da API.")

    return None


# --- FUNÇÕES DE PERSISTÊNCIA (CRUD) ---

def carregar_favoritas():
    """Carrega a lista de jogadoras favoritas do arquivo JSON."""
    if not os.path.exists(FAVORITAS_FILE):
        return []
    try:
        with open(FAVORITAS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"⚠️ Aviso: O arquivo {FAVORITAS_FILE} está corrompido ou vazio. Criando nova lista.")
        return []
    except IOError as e:
        print(f"❌ Erro de I/O ao carregar favoritas: {e}")
        return []


def salvar_favoritas(favoritas):
    """Salva a lista de jogadoras favoritas no arquivo JSON."""
    try:
        with open(FAVORITAS_FILE, 'w', encoding='utf-8') as f:
            json.dump(favoritas, f, indent=4, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"❌ Erro de I/O ao salvar favoritas: {e}")
        return False


def adicionar_favorita(jogadora_data):
    """Adiciona uma nova jogadora à lista de favoritas (CREATE)."""
    favoritas = carregar_favoritas()

    # Gera um ID simples (apenas para este exemplo de CRUD)
    novo_id = 1
    if favoritas:
        # Pega o maior ID e soma 1
        novo_id = max(f['id'] for f in favoritas) + 1

    jogadora_data['id'] = novo_id
    favoritas.append(jogadora_data)

    if salvar_favoritas(favoritas):
        print(f"✅ Jogadora '{jogadora_data['nome']}' adicionada às favoritas com ID: {novo_id}.")
        return True
    return False


def listar_favoritas(termo_busca=None):
    """Lista todas as favoritas ou filtra por termo de busca (READ)."""
    favoritas = carregar_favoritas()

    if not favoritas:
        print("A lista de jogadoras favoritas está vazia.")
        return []

    if termo_busca:
        termo_lower = termo_busca.lower()
        resultados = [
            fav for fav in favoritas
            if termo_lower in fav['nome'].lower() or
               termo_lower in fav['apelido'].lower() or
               termo_lower in fav['observacao'].lower()
        ]
    else:
        resultados = favoritas

    if not resultados:
        if termo_busca:
            print(f"Nenhuma jogadora favorita encontrada com o termo: '{termo_busca}'.")
        else:
            print("Nenhuma jogadora favorita encontrada.")
        return []

    print("\n--- Jogadoras Favoritas ---")
    for fav in resultados:
        print(f"ID: {fav['id']} | Nome: {fav['nome']} | Apelido: {fav['apelido']} | Observação: {fav['observacao']}")
        print(f"  Clube: {fav['clube']} | Ano: {fav['ano']}")
        print("-" * 30)

    return resultados


def atualizar_favorita(favoritas):
    """Permite ao usuário alterar apelido ou observação de uma favorita (UPDATE)."""
    if not favoritas:
        print("Não há jogadoras favoritas para atualizar.")
        return

    while True:
        try:
            id_alvo = int(input("\nDigite o ID da jogadora favorita que deseja alterar (ou 0 para cancelar): "))
            if id_alvo == 0:
                print("Operação de alteração cancelada.")
                return

            jogadora_alvo = next((fav for fav in favoritas if fav['id'] == id_alvo), None)

            if jogadora_alvo:
                print(
                    f"\nAlterando: ID {jogadora_alvo['id']} | Nome: {jogadora_alvo['nome']} | Apelido Atual: {jogadora_alvo['apelido']} | Observação Atual: {jogadora_alvo['observacao']}")

                novo_apelido = input("Novo Apelido (deixe em branco para manter): ").strip()
                nova_observacao = input("Nova Observação (deixe em branco para manter): ").strip()

                if novo_apelido:
                    jogadora_alvo['apelido'] = novo_apelido
                if nova_observacao:
                    jogadora_alvo['observacao'] = nova_observacao

                if salvar_favoritas(favoritas):
                    print(f"✅ Jogadora ID {id_alvo} atualizada com sucesso.")
                return
            else:
                print(f"❌ ID {id_alvo} não encontrado na lista de favoritas.")

        except ValueError:
            print("❌ Entrada inválida. Por favor, digite um número inteiro para o ID.")
        except Exception as e:
            print(f"❌ Ocorreu um erro inesperado: {e}")
            return


def excluir_favorita(favoritas):
    """Remove uma jogadora da lista de favoritas (DELETE)."""
    if not favoritas:
        print("Não há jogadoras favoritas para excluir.")
        return

    while True:
        try:
            id_alvo = int(input("\nDigite o ID da jogadora favorita que deseja excluir (ou 0 para cancelar): "))
            if id_alvo == 0:
                print("Operação de exclusão cancelada.")
                return

            # Cria uma nova lista sem a jogadora com o ID alvo
            nova_lista = [fav for fav in favoritas if fav['id'] != id_alvo]

            if len(nova_lista) < len(favoritas):
                if salvar_favoritas(nova_lista):
                    print(f"✅ Jogadora ID {id_alvo} excluída com sucesso.")
                return
            else:
                print(f"❌ ID {id_alvo} não encontrado na lista de favoritas.")

        except ValueError:
            print("❌ Entrada inválida. Por favor, digite um número inteiro para o ID.")
        except Exception as e:
            print(f"❌ Ocorreu um erro inesperado: {e}")
            return


def menu_crud():
    """Exibe o menu de operações CRUD e executa a função escolhida."""
    while True:
        print("\n--- Menu de Favoritas (CRUD) ---")
        print("1 - Listar todas as favoritas")
        print("2 - Pesquisar favorita (por nome, apelido ou observação)")
        print("3 - Alterar apelido/observação de uma favorita")
        print("4 - Excluir favorita")
        print("5 - Voltar ao menu principal")

        escolha = forcar_escolha("Escolha uma opção:", ['1', '2', '3', '4', '5'], "Opção inválida.")

        if escolha == '1':
            listar_favoritas()
        elif escolha == '2':
            termo = input("Digite o termo de busca (nome, apelido ou observação): ").strip()
            listar_favoritas(termo)
        elif escolha == '3':
            favoritas = listar_favoritas()
            atualizar_favorita(favoritas)
        elif escolha == '4':
            favoritas = listar_favoritas()
            excluir_favorita(favoritas)
        elif escolha == '5':
            break


def perguntar_adicionar_favorita(jogadora_info, estatisticas, escolhaTime, temporada):
    """
    Pergunta ao usuário se deseja adicionar a jogadora recém-consultada como favorita.
    """
    resposta = forcar_escolha("Deseja adicionar esta jogadora às favoritas? [s/n]", ['s', 'n'], "Digite 's' ou 'n'.")

    if resposta == 's':
        apelido = input("Digite um apelido para a jogadora (opcional, deixe em branco para pular): ").strip()
        observacao = input("Digite uma observação sobre a jogadora (opcional, deixe em branco para pular): ").strip()

        # Prepara os dados para salvar
        dados_favorita = {
            'nome': jogadora_info['firstname'] + ' ' + jogadora_info['lastname'],
            'clube': escolhaTime,
            'ano': temporada,
            'apelido': apelido,
            'observacao': observacao,
            'estatisticas': {
                'posicao': estatisticas['games']['position'],
                'partidas': estatisticas['games']['appearences'],
                'gols': estatisticas['goals']['total'] or 0,
                'assistencias': estatisticas['goals']['assists'] or 0
            }
        }
        adicionar_favorita(dados_favorita)


# --- PROGRAMA PRINCIPAL ---

def main():
    """Função principal para organizar o fluxo do programa."""
    print("\nBem-vindo ao canal de informações do Brasileirão Feminino! ⚽")

    liga = 74  # ID fixo da liga (Brasileirão Feminino)
    anos = ["2021", "2022", "2023"]

    while True:
        print("\n--- Menu Principal ---")
        print("1 - Consultar estatísticas de jogadoras")
        print("2 - Gerenciar jogadoras favoritas")
        print("3 - Sair")

        escolha_menu = forcar_escolha("Escolha uma opção:", ['1', '2', '3'], "Opção inválida.")

        if escolha_menu == '1':
            consultar_jogadoras(liga, anos)
        elif escolha_menu == '2':
            menu_crud()
        elif escolha_menu == '3':
            print("\n🚧 Encerrando o sistema...")
            break


def consultar_jogadoras(liga, anos):
    """Função para o fluxo de consulta de jogadoras via API."""
    print("\n--- Consulta de Futebol Feminino ---")

    # 1) Escolher temporada
    temporada = forcar_escolha(f'Qual temporada deseja consultar? {anos}', anos, 'Temporada não está na lista!')

    # 2) Buscar times dessa temporada
    times = obter_dados_api('teams', {'league': liga, 'season': temporada})

    # 3) Tratamento de Erro do item 2
    if not times:
        print("Nenhum time encontrado para esta temporada")
        return

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
        return

    # 9) Lista as jogadoras encontradas do time escolhido, junto de suas respectivas nacionalidades
    print(f"\nJogadoras do {escolhaTime}:")
    nomesJogadoras = []
    for item in jogadoras:
        jogadora = item['player']
        nomesJogadoras.append(jogadora['name'])
        print(f"Nome: {jogadora['name']}, Nacionalidade: {jogadora['nationality']}")

    # 10) Escolher uma jogadora e identificar o id da mesma para achá-la na API
    escolhaJogadora = forcar_escolha('Qual jogadora você deseja consultar as estatísticas?', nomesJogadoras,
                                     'Jogadora não está na lista!')
    idJogadoraEscolhida = consultar_id(escolhaJogadora, nomesJogadoras)

    # A lista 'jogadoras' contém o objeto completo da jogadora, mas precisamos do ID da API
    # Vamos encontrar o ID da jogadora escolhida na lista original 'jogadoras'
    jogadora_api_id = next(item['player']['id'] for item in jogadoras if item['player']['name'] == escolhaJogadora)

    # 11) Buscar estatísticas da jogadora
    print(f"\nBuscando estatísticas da jogadora: {escolhaJogadora}...")
    stats = obter_dados_api('players', {'id': jogadora_api_id, 'season': temporada})

    # 12) Verifica se a consulta retornou dados (stats) e se dentro desses dados existe a chave "statistics"
    if stats and stats.get('statistics'):
        jogadora_info = stats['player']
        estatisticas = stats['statistics'][0]

        # 13) Exibe principais estatísticas
        print(
            f"\n--- Estatísticas de {jogadora_info.get('firstname', '')} {jogadora_info.get('lastname', '')} ({jogadora_info['name']}) ---")
        print(f"Time: {estatisticas['team']['name']}")
        print(f"Liga: {estatisticas['league']['name']}")
        print(f"Posição: {estatisticas['games']['position']}")
        print(f"Partidas Jogadas: {estatisticas['games']['appearences']}")
        print(f"Gols: {estatisticas['goals']['total'] or 0}")
        print(f"Assistências: {estatisticas['goals']['assists'] or 0}")

        # 14) Pergunta se quer adicionar aos favoritos
        perguntar_adicionar_favorita(jogadora_info, estatisticas, escolhaTime, temporada)
    else:
        # 15) Se dentro dos dados não existir as estatísticas da jogadora, printa que não foram encontradas
        print("Não foram encontradas estatísticas para esta jogadora na temporada selecionada.")


if __name__ == "__main__":
    main()