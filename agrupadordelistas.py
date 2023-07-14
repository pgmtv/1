from github import Github

# Token de acesso pessoal do GitHub (opcional)
# Caso você esteja acessando um repositório privado, será necessário um token de acesso válido.
# Caso contrário, deixe a variável 'access_token' como uma string vazia.
access_token = ''

# URL do diretório do GitHub
github_url = 'https://github.com/iptv-org/iptv/tree/master/streams'

# Extrai o nome do usuário e do repositório do URL
github_user, github_repo = github_url.split('/')[3], github_url.split('/')[4]

# Cria uma instância do objeto Github
if access_token:
    g = Github(access_token)
else:
    g = Github()

# Obtém o repositório e o branch (ramo) principal
repo = g.get_repo(f'{github_user}/{github_repo}')
branch = repo.get_branch(repo.default_branch)

# Obtém o conteúdo do diretório
contents = repo.get_contents('', ref=branch.name)

# Percorre o conteúdo do diretório
for item in contents:
    if item.type == 'file' and item.name.endswith('.m3u'):
        playlist_url = item.download_url
        print(playlist_url)

