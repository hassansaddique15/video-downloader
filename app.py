from flask import Flask, render_template, request, jsonify
from pytube import YouTube

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_video', methods=['POST'])
def get_video():
    url = request.form.get('url')
    try:
        yt = YouTube(url)
        # سب سے بہترین کوالٹی کا لنک نکالنا
        stream = yt.streams.get_highest_resolution()
        return jsonify({"success": True, "download_url": stream.url})
    except Exception:
        return jsonify({"success": False, "error": "لنک کام نہیں کر رہا"})

if __name__ == '__main__':
    app.run(debug=True)
