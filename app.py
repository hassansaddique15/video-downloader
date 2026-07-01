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
        return jsonify({"error": "براہ کرم کوئی لنک درج کریں!"})

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_url = info_dict.get('url', None)
            video_title = info_dict.get('title', 'Video')
            # یہ نئی لائن ویڈیو کا تھمب نیل نکالے گی
            video_thumbnail = info_dict.get('thumbnail', '')
            
            return jsonify({
                "success": True,
                "title": video_title,
                "download_url": video_url,
                "thumbnail": video_thumbnail
            })
    except Exception as e:
        return jsonify({"success": False, "error": "لنک غلط ہے یا ویڈیو پرائیویٹ ہے!"})

if __name__ == '__main__':
    app.run(debug=True)