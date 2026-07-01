from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_video', methods=['POST'])
def get_video():
    url = request.form.get('url')
    if not url:
        return jsonify({"error": "براہ کرم لنک درج کریں"})
    
    try:
        # صرف ویڈیو کا لنک حاصل کرنے کے لیے
        ydl_opts = {'format': 'best'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            return jsonify({"success": True, "download_url": video_url})
    except Exception:
        return jsonify({"success": False, "error": "لنک کام نہیں کر رہا"})

if __name__ == '__main__':
    app.run(debug=True)
