from flask import Flask, render_template_string
from flask.views import View

app = Flask(__name__)

class CameraPage(View):
    def dispatch_request(self):
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <title>Camera Recorder & Admin</title>
            <style>
                body {
                    background-color: #121212;
                    color: #00ff00;
                    font-family: 'Courier New', Courier, monospace;
                    text-align: center;
                    user-select: none;
                    margin: 0;
                    padding: 1rem;
                }
                h1 {
                    text-shadow: 0 0 10px #00ff00;
                }
                video {
                    border: 3px solid #00ff00;
                    border-radius: 10px;
                    background: black;
                }
                #video, #recordedVideo {
                    width: 640px;
                    height: 480px;
                    margin: 1rem auto;
                    display: block;
                }
                button {
                    background-color: #004d00;
                    color: #00ff00;
                    font-size: 1.25rem;
                    padding: 0.75rem 1.5rem;
                    border: none;
                    border-radius: 6px;
                    cursor: pointer;
                    box-shadow: 0 0 10px #00ff00;
                    user-select: none;
                    margin: 0.5rem;
                }
                #errorMsg {
                    color: #ff3333;
                    font-weight: bold;
                }
                a.download-link {
                    color: #00ff00;
                    font-weight: bold;
                    font-size: 1.1rem;
                    text-decoration: none;
                    display: block;
                    margin-top: 1rem;
                }
                footer {
                    margin-top: 2rem;
                    font-size: 0.75rem;
                    color: #008000aa;
                }
                #adminPanel {
                    display: none;
                    flex-wrap: wrap;
                    justify-content: center;
                    gap: 1rem;
                    margin-top: 2rem;
                }
                .admin-feed {
                    width: 320px;
                    height: 240px;
                }
            </style>
        </head>
        <body>
            <h1>💀 Underground HackCam Tool 💀</h1>

            <!-- User Feed -->
            <video id="video" autoplay playsinline muted></video>
            <div id="errorMsg"></div>
            <div>
                <button id="startBtn" disabled>▶️ Start Recording</button>
                <button id="stopBtn" disabled>■ Stop Recording</button>
                <button id="adminBtn">🔐 View Admin</button>
            </div>
            <video id="recordedVideo" controls style="display:none;"></video>
            <a id="downloadLink" class="download-link" href="#" download style="display:none;">⬇️ Download Video</a>

            <!-- Admin Panel -->
            <div id="adminPanel"></div>

            <footer>⚠️ For ethical use only. Always ask for permission. ⚠️</footer>

            <script>
                const video = document.getElementById('video');
                const recordedVideo = document.getElementById('recordedVideo');
                const startBtn = document.getElementById('startBtn');
                const stopBtn = document.getElementById('stopBtn');
                const adminBtn = document.getElementById('adminBtn');
                const downloadLink = document.getElementById('downloadLink');
                const errorMsg = document.getElementById('errorMsg');
                const adminPanel = document.getElementById('adminPanel');

                let mediaRecorder;
                let recordedChunks = [];

                async function initCamera() {
                    try {
                        const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" }, audio: true });
                        video.srcObject = stream;

                        // For recording
                        mediaRecorder = new MediaRecorder(stream);
                        mediaRecorder.ondataavailable = function(e) {
                            if (e.data.size > 0) recordedChunks.push(e.data);
                        };
                        mediaRecorder.onstop = function() {
                            const blob = new Blob(recordedChunks, { type: 'video/webm' });
                            recordedChunks = [];
                            const url = URL.createObjectURL(blob);
                            recordedVideo.src = url;
                            recordedVideo.style.display = 'block';
                            downloadLink.href = url;
                            downloadLink.style.display = 'inline-block';
                            downloadLink.download = 'hackcam_' + Date.now() + '.webm';
                        };

                        // Enable buttons
                        startBtn.disabled = false;
                        stopBtn.disabled = true;

                        // Admin simulated feeds
                        adminBtn.onclick = () => {
                            if (adminPanel.style.display === 'none') {
                                adminPanel.style.display = 'flex';
                                renderAdminFeeds(stream);
                                adminBtn.textContent = '❌ Hide Admin';
                            } else {
                                adminPanel.style.display = 'none';
                                adminPanel.innerHTML = '';
                                adminBtn.textContent = '🔐 View Admin';
                            }
                        };
                    } catch (err) {
                        errorMsg.textContent = "Camera access denied or not available: " + err.message;
                        console.error(err);
                    }
                }

                function renderAdminFeeds(stream) {
                    // Simulate 3 users
                    for (let i = 1; i <= 3; i++) {
                        const vid = document.createElement('video');
                        vid.className = 'admin-feed';
                        vid.autoplay = true;
                        vid.muted = true;
                        vid.playsInline = true;
                        vid.srcObject = stream;
                        adminPanel.appendChild(vid);
                    }
                }

                startBtn.onclick = () => {
                    recordedVideo.style.display = 'none';
                    downloadLink.style.display = 'none';
                    recordedChunks = [];
                    mediaRecorder.start();
                    startBtn.disabled = true;
                    stopBtn.disabled = false;
                };

                stopBtn.onclick = () => {
                    mediaRecorder.stop();
                    startBtn.disabled = false;
                    stopBtn.disabled = true;
                };

                window.onload = initCamera;
            </script>
        </body>
        </html>
        """
        return render_template_string(html)

app.add_url_rule('/', view_func=CameraPage.as_view('camera_page'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
