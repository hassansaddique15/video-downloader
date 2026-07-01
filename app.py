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
    
    # yt-dlp کی سیٹنگز جو ہر ویڈیو کے لیے بہترین ہیں
    ydl_opts = {
        'format': 'best',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # ویڈیو کی معلومات نکالنا
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            return jsonify({"success": True, "download_url": video_url})
    except Exception as e:
        return jsonify({"success": False, "error": "لنک کام نہیں کر رہا، کوئی اور ویڈیو چیک کریں"})

if __name__ == '__main__':
    app.run(debug=True)
