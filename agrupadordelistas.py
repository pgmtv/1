import requests

url = "https://github.com/iptv-org/iptv/tree/master/streams"

response = requests.get(url)

if response.status_code == 200:
    contents = response.text
    m3u_files = []

    # Extract .m3u file links from the response HTML
    start_marker = '<td><a href="'
    end_marker = '.m3u"'
    start_index = contents.find(start_marker)

    while start_index != -1:
        end_index = contents.find(end_marker, start_index)
        m3u_file_link = contents[start_index + len(start_marker):end_index + len(end_marker)]
        m3u_files.append(m3u_file_link)
        start_index = contents.find(start_marker, end_index)

    lists = []

    for m3u_file_link in m3u_files:
        m3u_url = f"https://github.com{m3u_file_link}"
        m3u_response = requests.get(m3u_url)

        if m3u_response.status_code == 200:
            lists.append((m3u_file_link.split("/")[-1], m3u_response.text))
        else:
            print(f"Error retrieving contents from {m3u_url}")

    lists = sorted(lists, key=lambda x: x[0])

    line_count = 0

    with open("lista1.M3U", "w") as f:
        for l in lists:
            f.write(l[1])
            line_count += l[1].count("\n")
            if line_count >= 2000:  # Stop writing after 2000 lines
                break
else:
    print(f"Error retrieving contents from {url}")
