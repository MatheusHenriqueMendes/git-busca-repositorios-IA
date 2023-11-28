import requests
import mysql.connector
import pandas as pd
from datetime import datetime

class Repository:
    def __init__(self, repo_data, headers):
        self.name = repo_data['name']
        self.url = repo_data['html_url']
        self.stars = repo_data['stargazers_count']
        self.language = repo_data['language']
        self.created_at = self._convert_datetime(repo_data['created_at'])
        self.query_term = None
        self.owner_url = repo_data['owner']['url']
        self.country = self._get_owner_country(headers)

    #Conversão de data para o formato esperado para o banco de dados 
    def _convert_datetime(self, datetime_str):
        # Certifique-se de que este método esteja alinhado com os outros métodos da classe
        return datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M:%S')

    #Truncar dados para não exceder 100 caracteres, para não exceder o limite da coluna do banco     
    def _get_owner_country(self, headers):
        try:
            response = requests.get(self.owner_url, headers=headers)
            if response.status_code == 200:
                owner_data = response.json()
                country = owner_data.get('location', 'Unknown')
                # Garantir que country não seja None antes de truncar
                if country is not None:
                    return country[:100]
                else:
                    return 'Unknown'
            else:
                return 'Unknown'
        except requests.RequestException:
            return 'Unknown'

#Classe para acessar a API do Git e realizar a busca nos respositórios 
class GitHubAPI:
    def __init__(self, token):
        self.base_url = 'https://api.github.com/search/repositories'
        self.headers = {'Authorization': f'token {token}'}

    def search_repos(self, query, sort='stars', order='desc'):
        url = f'{self.base_url}?q={query}&sort={sort}&order={order}'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return [Repository(repo_data, self.headers) for repo_data in response.json()['items']]
        else:
            return []

#Termos utilizados para busca
token = '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'
github_api = GitHubAPI(token)
query_terms = ['IA', 'AI', 'deep learning', 'machine learning', 'inteligência artificial', 'artificial intelligence', 
'aprendizado profundo', 'aprendizado de máquina', 'inteligencia artificial', 'aprendizaje profundo', 'aprendizaje automático']
repos = []

for term in query_terms:
    term_repos = github_api.search_repos(term)
    for repo in term_repos:
        repo.query_term = term
    repos.extend(term_repos)

#Conexão com o banco de dados 
conn = None
cursor = None

try:
    with mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234',  
        database='github_data'
    ) as conn:
        with conn.cursor() as cursor:
            insert_query = """
            INSERT INTO repositorios (name, url, stars, language, created_at, country, query_term, linguagens)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            for repo in repos:
                cursor.execute(insert_query, (repo.name, repo.url, repo.stars, repo.language, repo.created_at, repo.country, repo.query_term, repo.language))
            conn.commit()
except mysql.connector.Error as e:
    print("Erro ao conectar ao MySQL ou ao executar inserções:", e)
finally:
    if cursor is not None:
        cursor.close()
    if conn is not None:
        conn.close()

# Feche o cursor e a conexão
cursor.close()
conn.close()

        
# Definindo a classe RepoTable
class RepoTable:
    def __init__(self, repos):
        self.repos = repos

    def to_dataframe(self):
        data = {
            'Name': [repo.name for repo in self.repos],
            'URL': [repo.url for repo in self.repos],
            'Stars': [repo.stars for repo in self.repos],
            'Language': [repo.language for repo in self.repos],
            'Created At': [repo.created_at for repo in self.repos],
            'Country': [repo.country for repo in self.repos],
            'Query Term': [repo.query_term for repo in self.repos]
        }
        return pd.DataFrame(data)


# Opcional: converter para DataFrame e imprimir
repo_table = RepoTable(repos)
df = repo_table.to_dataframe()
print(df)