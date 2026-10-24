import os
from flask import Flask, render_template, request, send_file
import yt_dlp

app = Flask(__name__)
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    pesan = None
    file_unduhan = None

    if request.method == "POST":
        url = request.form.get("url")
        format_pilihan = request.form.get("format")

        if url:
            opsi = {
                "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
            }

            if format_pilihan == "mp3":
                opsi.update({
                    "format": "bestaudio/best",
                    "postprocessors": [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }],
                })
            else:
                opsi.update({
                    "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                })

            try:
                with yt_dlp.YoutubeDL(opsi) as ydl:
                    info = ydl.extract_info(url, download=True)
                    nama_file = ydl.prepare_filename(info)
                    if format_pilihan == "mp3":
                        nama_file = os.path.splitext(nama_file)[0] + ".mp3"
                    file_unduhan = os.path.basename(nama_file)
                    pesan = "Unduhan berhasil disiapkan!"
            except Exception as e:
                pesan = f"Terjadi kesalahan: {str(e)}"

    return render_template("index.html", pesan=pesan, file_unduhan=file_unduhan)

@app.route("/get/<filename>")
def get_file(filename):
    path = os.path.join(DOWNLOAD_DIR, filename)
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
