import urllib.request

url = "https://talent.baidu.com/jobs/list?recruitType=INTERN"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as response:
    html = response.read().decode('utf-8')
    with open("baidu_page.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Saved baidu_page.html")
