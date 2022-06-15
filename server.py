from flask import Flask, render_template, Response, request, url_for
import cv2

camera=cv2.VideoCapture(0)

app = Flask(__name__)

#web cam streaming function
def generate_frames():
    while True:
        ## read the camera frame
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
               
@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return render_template('index.html', url_for="/video")



if __name__=='__main__':
    app.run('0.0.0.0', port= 8092, debug=True)