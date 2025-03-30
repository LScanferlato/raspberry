from flask import Flask, render_template, request, redirect, url_for
import time
import picamera
import cv2
import numpy as np
from datetime import datetime
import threading

app = Flask(__name__)

# Variabili globali per i parametri di scatto
duration = 12 * 60 * 60  # 12 ore in secondi
interval = 20  # intervallo di scatto in secondi
num_frames = duration // interval
is_recording = False

def capture_timelapse():
    global is_recording
    is_recording = True

    with picamera.PiCamera() as camera:
        camera.resolution = (1920, 1080)  # Risoluzione della foto (Full HD)
        camera.framerate = 24  # Framerate per il video
        camera.iso = 800  # Imposta ISO iniziale
        camera.exposure_mode = 'auto'  # Imposta l'autoesposizione
        time.sleep(2)  # Tempo per stabilizzare la fotocamera

        for i in range(num_frames):
            image_path = f'image_{i:04d}.jpg'
            camera.capture(image_path)

            # Aggiungi timestamp all'immagine
            img = cv2.imread(image_path)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cv2.putText(img, timestamp, (10, img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.imwrite(image_path, img)

            print(f'Frame {i + 1}/{num_frames} catturato: {image_path}')
            time.sleep(interval)

    # Creazione del video
    video_path = 'timelapse_video.avi'
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter(video_path, fourcc, 24, (1920, 1080))

    for i in range(num_frames):
        image_path = f'image_{i:04d}.jpg'
        img = cv2.imread(image_path)
        video.write(img)

    video.release()
    is_recording = False
    print(f'Video creato: {video_path}')

@app.route('/')
def index():
    return render_template('index.html', is_recording=is_recording)

@app.route('/start', methods=['POST'])
def start_timelapse():
    if not is_recording:
        threading.Thread(target=capture_timelapse).start()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)