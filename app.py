from flask import Flask, request
from flask.views import View
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

class CameraPage(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        scrape_result = ""
        if request.method == 'POST':
            url = request.form.get("target_url", "")
            try:
                response = requests.get(url, timeout=5)
                soup = BeautifulSoup(response.content, 'html.parser')
                title = soup.title.string if soup.title else "No title found"
                headings = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2'])]
                scrape_result = f"<h3>Title: {title}</h3><ul>" + "".join(f"<li>{h}</li>" for h in headings) + "</ul>"
            except Exception as e:
                scrape_result = f"<p style='color:red;'>Error: {str(e)}</p>"

        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <title>Camera & Scraper Tool</title>
            <style>
                body {{
                    background-color: #121212;
                    color: #00ff00;
                    font-family: 'Courier New', Courier, monospace;
                    text-align: center;
                    user-select: none;
                    margin: 0;
                    padding: 1rem;
                }}
                h1 {{
                    text-shadow: 0 0 10px #00ff00;
                }}
                video {{
                    border: 3px solid #00ff00;
                    border-radius: 10px;
                    background: black;
                }}
                #video {{
                    width: 640px;
                    height: 480px;
                    margin: 1rem auto;
                    display: block;
                }}
                button, input[type='text'] {{
                    background-color: #004d00;
                    color: #00ff00;
                    font-size: 1rem;
                    padding: 0.5rem;
                    border: none;
                    border-radius: 6px;
                    margin: 0.25rem;
                    box-shadow: 0 0 5px #00ff00;
                }}
                form {{
                    margin-top: 2rem;
                }}
                #scrapeResult {{
                    text-align: left;
                    margin: 1rem auto;
                    max-width: 800px;
                    color: #00ff00;
                }}
            </style>
        </head>
        <body>
            <h1>💻 Ethical Camera & Web Scraper Tool 💻</h1>
            <video id="video" autoplay playsinline muted></video>
            <div id="errorMsg"></div>

            <form method="POST">
                <label for="target_url">🔍 Enter a domain to scrape:</label><br>
                <input type="text" id="target_url" name="target_url" placeholder="https://example.com" required>
                <button type="submit">Scrape</button>
            </form>

            <div id="scrapeResult">{scrape_result}</div>

            <footer>⚠️ This tool is for educational, ethical, and transparent use only. Always respect website terms and privacy policies. ⚠️</footer>

            <script>
                async function initCamera() {{
                    try {{
                        const stream = await navigator.mediaDevices.getUserMedia({{ video: true, audio: false }});
                        document.getElementById('video').srcObject = stream;
                    }} catch (err) {{
                        document.getElementById('errorMsg').textContent = "Camera access error: " + err.message;
                        console.error(err);
                    }}
                }}
                window.onload = initCamera;
            </script>
        </body>
        </html>
        """
        return html

app.add_url_rule('/', view_func=CameraPage.as_view('camera_page'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
