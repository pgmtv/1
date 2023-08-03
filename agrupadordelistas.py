import requests

repo_urls = [
    "https://github.com/punkstarbr/STR-YT/raw/main/REALITY'SLIVE.m3u",
    "https://github.com/atsushi444/iptv-epg/raw/main/CCTV.m3u",    
    "https://github.com/iptv-org/iptv/raw/master/streams/mx_multimedios.m3u",
    "https://github.com/strikeinthehouse/M3UPT/raw/main/M3U/M3UPT.m3u",
    "https://api.github.com/repos/strikeinthehouse/YT2M3U/contents",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/fr.m3u",
    "https://api.github.com/repos/Nuttypro69/YouTube_to_m3u/contents",
    "https://api.github.com/repos/cqcbrasil/YouTube_to_m3u/contents",
    "https://api.github.com/repos/punkstarbr/STR-YT/contents"
]



lists = []
for url in repo_urls:
    response = requests.get(url)

    if response.status_code == 200:
        if url.endswith(".m3u"):
            lists.append((url.split("/")[-1], response.text))
        else:
            try:
                contents = response.json()

                m3u_files = [content for content in contents if content["name"].endswith(".m3u")]

                for m3u_file in m3u_files:
                    m3u_url = m3u_file["download_url"]
                    m3u_response = requests.get(m3u_url)

                    if m3u_response.status_code == 200:
                        lists.append((m3u_file["name"], m3u_response.text))
            except requests.exceptions.JSONDecodeError:
                print(f"Error parsing JSON from {url}")
    else:
        print(f"Error retrieving contents from {url}")

lists = sorted(lists, key=lambda x: x[0])

line_count = 0
with open("lista1.M3U", "w") as f:
    for l in lists:
        f.write(l[1])
        line_count += l[1].count("\n")
        if line_count >= 2023:  # Stop writing after 2023 lines
            break
