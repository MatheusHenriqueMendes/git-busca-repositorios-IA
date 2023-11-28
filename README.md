# Análise de Projetos de IA no GitHub

## Visão Geral
Este projeto foca na coleta e análise de dados sobre projetos de Inteligência Artificial (IA) no GitHub. Utiliza a API do GitHub para buscar repositórios com base em palavras-chave relacionadas à IA, armazena esses dados em um banco de dados MySQL e, opcionalmente, os converte para um DataFrame do Pandas para análise.

## Funcionalidades
- **Coleta de Dados:** Busca por repositórios no GitHub usando palavras-chave relacionadas à IA.
- **Armazenamento de Dados:** Salva os dados coletados em um banco de dados MySQL.
- **Conversão para DataFrame:** Opcionalmente, converte os dados para um DataFrame do Pandas.
- **Preparação para Análise no Power BI:** O script prepara os dados para análise e visualização no Power BI.

## Tecnologias Utilizadas
- **Python**
- **Bibliotecas:** requests, mysql.connector, pandas
- **MySQL**
- **Power BI** (para análise e visualização de dados)

## Estrutura do Código
- `Repository`: Classe que representa um repositório do GitHub.
- `GitHubAPI`: Classe para interagir com a API do GitHub.
- `RepoTable`: Classe que converte a lista de repositórios em um DataFrame do Pandas.

## Como Usar
1. Insira seu token pessoal do GitHub na variável `token`.
2. Execute o script para coletar dados dos repositórios e salvá-los no banco de dados MySQL.
3. Opcional: Converta os dados para um DataFrame para visualização.

## Resultados
O link para o dashboard do Power BI será adicionado aqui após a conclusão do projeto.

## Contribuições
Instruções sobre como contribuir para este projeto.

## Licença
Detalhes da licença do projeto.

