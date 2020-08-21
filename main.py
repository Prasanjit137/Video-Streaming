from flask import Flask, render_template, Response
import cv2
import socket
import io
import time
from twilio.rest import Client
from pyngrok import ngrok

app = Flask(__name__)
vc = cv2.VideoCapture(0)

@app.route('/')
def index():
    return render_template('index.html')

def gen():
    while True:
        rval, frame = vc.read()
        if rval == True:
            b = cv2.resize(frame,(256,144),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
            byteArray = cv2.imencode('.jpg', b)[1].tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + byteArray + b'\r\n')
        time.sleep(0.1)

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def start_ngrok():
    url = ngrok.connect(5000)
    print("Link from ngrok : " + url)
    return url

def Wp_bot(url):
	account_sid = 'AC795cfa06bd3ec1a14397e78d0d53ed2b'
	auth_token = 'becdd7c4e09f96a6495ad37df6e36df2'
	client = Client(account_sid, auth_token)
	message = client.messages.create(
        	                      body="Video streaming started. Please go through the link : " + url,
                	              from_='whatsapp:+14155238886',
                        	      to='whatsapp:+917551071252'
                          	)
	print("Whatsapp messege sid : " + message.sid)
    
if __name__ == '__main__':
    url = start_ngrok()
    Wp_bot(url)
    app.run()
               
