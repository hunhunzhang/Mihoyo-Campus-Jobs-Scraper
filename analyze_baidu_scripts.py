import urllib.request
import re
import json

url = "https://talent.baidu.com/jobs/list?recruitType=INTERN"

    print(f"Fetching main page: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            print("Main page loaded successfully.")
            
            # Find script tags
            script_pattern = re.compile(r'<script.*?src=["\'](.*?)["\']', re.IGNORECASE)
            scripts = script_pattern.findall(html)
            
            list_scripts = [s for s in scripts if "list" in s or "chunk" in s]
            print(f"Found {len(list_scripts)} potentially relevant scripts.")
            
            for script_url in list_scripts:
                if not script_url.startswith("http"):
                    # Handle relative URLs if necessary, Baidu seems to use absolute CDN URLs
                    if script_url.startswith("//"):
                         script_url = "https:" + script_url
                    else:
                         continue # Skip weird relative paths for now

                print(f"Analyzing script: {script_url}")
                try:
                    s_req = urllib.request.Request(script_url, headers=headers)
                    with urllib.request.urlopen(s_req) as s_resp:
                        js_content = s_resp.read().decode('utf-8')
                        
                        # Look for API-like patterns
                        # specific to Baidu talent: usually contain "talent.baidu.com" or just "/jobs/"
                        api_pattern = re.compile(r'["\'](https?://[\w\.-]*baidu\.com)?/?[a-zA-Z0-9_/]*(list|search|query|jobs)[a-zA-Z0-9_/]*["\']', re.IGNORECASE)
                        urls = api_pattern.findall(js_content)
                        for u in urls:
                            # u is a tuple due to groups
                            full_match = u[0] if u[0] else "" 
                            if "list" in full_match or "jobs" in full_match:
                                print(f"  POTENTIAL API FOUND: {full_match}")
                                
                        # Also look for POST / GET text near "url:"
                        # This is harder with regex on minified JS but worth a try
                        # Look for "POST", "GET"
                        if "POST" in js_content and "url" in js_content:
                             # print(f"  Contains POST and url")
                             pass

                        # Look for specific known endpoints in text
                        if "/external/baidu/recruit/getJob" in js_content:
                             print("  Found specific known endpoint: /external/baidu/recruit/getJob")

                except Exception as e:
                    print(f"  Error fetching script {script_url}: {e}")

    except Exception as e:
        print(f"Error fetching main page: {e}")
