import urllib.request
import re
import json

def analyze():
    url = "https://talent.baidu.com/jobs/list?recruitType=INTERN"
    print(f"Fetching main page: {url}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
            print("Main page loaded successfully.")
            
            # Find script tags (simplified regex)
            script_pattern = re.compile(r'<script\s+[^>]*src=["\'](.*?)["\']', re.IGNORECASE)
            scripts = script_pattern.findall(content)
            
            print(f"Found {len(scripts)} scripts in HTML.")
            
            # Check for JS map in HTML
            # Look for webpack runtime chunks
            
            relevant_scripts = []
            for s in scripts:
                full_url = s
                if s.startswith("//"):
                    full_url = "https:" + s
                elif s.startswith("/"):
                    full_url = "https://talent.baidu.com" + s
                
                if "list" in full_url or "chunk" in full_url or "index" in full_url:
                     relevant_scripts.append(full_url)
            
            print(f"Analyzing {len(relevant_scripts)} relevant scripts.")
            
            for script_url in relevant_scripts:
                print(f"Checking script: {script_url}")
                try:
                    s_req = urllib.request.Request(script_url, headers=headers)
                    with urllib.request.urlopen(s_req) as s_resp:
                        js_code = s_resp.read().decode('utf-8')
                        
                        # Look for likely API patterns
                        # "/external/baidu/recruit/getJob"
                        # "/jobs/list"
                        # "recruit/getOpenJob"
                        
                        patterns = [
                            r'["\'](/external/[^"\']+)["\']',
                            r'["\'](/jobs/[^"\']+)["\']',
                            r'["\'](/recruit/[^"\']+)["\']',
                            r'["\'](http[^"\']*baidu\.com[^"\']*list[^"\']*)["\']'
                        ]
                        
                        found_in_file = False
                        for p in patterns:
                            matches = re.findall(p, js_code)
                            for m in matches:
                                if len(m) < 100: # filter out long JS nonsense
                                    print(f"  FOUND ENDPOINT: {m}")
                                    found_in_file = True
                        
                        if "POST" in js_code:
                            print("  Script contains 'POST'")

                except Exception as e:
                    print(f"Error reading script {script_url}: {e}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze()
