from playwright.sync_api import sync_playwright
import json
import time

def run():
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(channel="msedge", headless=True)
        except:
            try:
                browser = p.chromium.launch(channel="chrome", headless=True)
            except:
                 browser = p.chromium.launch(headless=True)

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        # Add init script to mask webdriver
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)

        print("Navigating to https://talent.baidu.com/jobs/list?recruitType=INTERN")
        
        found_api = False

        def handle_request(request):
            print(f"Request: {request.method} {request.url}")

        def handle_response(response):
            print(f"Response: {response.status} {response.url} ({response.headers.get('content-type', '')})")
            
        page.on("request", handle_request)
        page.on("response", handle_response)
        
        try:
            response = page.goto("https://talent.baidu.com/jobs/list?recruitType=INTERN", timeout=60000)
            print("Page loaded.")
            
            content = page.content()
            if "jobId" in content or "post" in content:
                print("Found 'jobId' or 'post' in HTML content.")
                # print(content[:1000]) # Print beginning to see if it's SSR
            else:
                 print("Did not find 'jobId' or 'post' in HTML content.")

            # Search for anything that looks like a JSON blob in the HTML
            import re
            json_blob = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.*?});', content)
            if json_blob:
                print("Found INITIAL_STATE!")
                print(json_blob.group(1)[:500])

            # Wait for some dynamic content to load
            page.wait_for_timeout(5000)
            print("Scrolling down...")
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(15000)
            
        except Exception as e:
            print(f"Error during navigation: {e}")

        browser.close()

if __name__ == "__main__":
    run()
