import requests

def obter_filmes_ganhadores_oscar(ano, chave_api):
    if not chave_api:
        print("Por favor, forneça uma chave de API válida.")
        return None

    url = f'https://api.themoviedb.org/3/discover/movie?api_key={chave_api}&primary_release_year={ano}&sort_by=popularity.desc&with_awards=true'
    
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        dados = resposta.json()
        
        filmes = dados.get('results', [])
        return filmes
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter dados: {e}")
        return None

def main():
    chave_api = 'sua_chave_api'  # Substitua pela sua chave real obtida no site do TMDb
    ano_oscar = 2022  # Você pode substituir pelo ano desejado
    filmes_oscar = obter_filmes_ganhadores_oscar(ano_oscar, chave_api)

    if filmes_oscar:
        print(f"Filmes que ganharam o Oscar em {ano_oscar}:\n")
        for filme in filmes_oscar:
            print(f"{filme['title']} ({filme['release_date'][:4]})")
    else:
        print("Não foi possível obter a lista de filmes vencedores do Oscar.")

if __name__ == "__main__":
    main()
