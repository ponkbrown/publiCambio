from flask import Flask, render_template, request, redirect
from flask_uploads import UploadSet, configure_uploads, IMAGES
from funciones import findGPS

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        cordenadas = findGPS('static/img/'+filename)
        return redirect('https://www.google.com.mx/maps/@{0},{1}'.format(cordenadas[0], cordenadas[1]))
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
