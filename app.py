from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_video', methods=['POST'])
def get_video():
    url = request.form.get('url')
    # سادہ اور طاقتور طریقے سے لنک نکالنا
    ydl_opts = {
        'format': 'best',
        'noplaylist': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({"success": True, "download_url": info['url']})
    except Exception as e:
        return jsonify({"success": False, "error": "لنک کام نہیں کر رہا، کوئی اور ویڈیو چیک کریں"})

if __name__ == '__main__':
    app.run(debug=True)
