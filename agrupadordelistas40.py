import requests

repo_urls = [
    "https://github.com/punkstarbr/STR-YT/raw/main/REALITY'SLIVE.m3u",
    "https://github.com/iptv-org/iptv/blob/master/streams/mx.m3u",    
    "https://github.com/iptv-org/iptv/raw/master/streams/jp.m3u",
    "https://github.com/strikeinthehouse/Navez/raw/main/playlist.m3u",
]

lists = []

for url in repo_urls:
    response = requests.get(url)
    
    if response.status_code == 200:
        if url.endswith(".m3u"):
            # Verifica se o conteúdo é realmente uma lista .m3u
            if "#EXTM3U" in response.text:
                lists.append((url.split("/")[-1], response.text))
            else:
                print(f"Content from {url} does not seem to be a valid .m3u playlist.")
        else:
            try:
                contents = response.json()
                
                m3u_files = [content for content in contents if content.get("name", "").endswith(".m3u")]
                
                for m3u_file in m3u_files:
                    m3u_url = m3u_file["download_url"]
                    m3u_response = requests.get(m3u_url)
                    
                    if m3u_response.status_code == 200 and "#EXTM3U" in m3u_response.text:
                        lists.append((m3u_file["name"], m3u_response.text))
                    else:
                        print(f"Content from {m3u_url} does not seem to be a valid .m3u playlist.")
            except requests.exceptions.JSONDecodeError:
                print(f"Error parsing JSON from {url}")
    else:
        print(f"Error retrieving contents from {url}")

# Ordena a lista pelo nome do arquivo
lists = sorted(lists, key=lambda x: x[0])

# Escreve no arquivo lista1.m3u, limitando a 200 linhas
line_count = 0
with open("lista1.m3u", "a") as f:
    for l in lists:
        lines = l[1].split("\n")
        for line in lines:
            if line_count >= 200:
                break
            if line.strip():  # Pula linhas em branco
                f.write(line + "\n")
                line_count += 1
        if line_count >= 200:
            break
