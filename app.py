import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob
import paho.mqtt.client as paho
import json
from gtts import gTTS
from googletrans import Translator


def on_publish(client,userdata,result):
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received=str(message.payload.decode("utf-8"))
    st.write(message_received)

broker="broker.mqttdashboard.com"
port=1883
client1= paho.Client("voiceC-AngRP10")
client1.on_message = on_message

# ------------------ UI ------------------
st.markdown("<h1>🎙️ INTERFACES MULTIMODALES</h1>", unsafe_allow_html=True)
st.markdown("<h3>Control por Voz Inteligente</h3>", unsafe_allow_html=True)

# Imagen centrada
image = Image.open('voice_ctrl.jpg')
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image(image, width=220)

# Tarjeta visual
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Presiona el botón y comienza a hablar</p>", unsafe_allow_html=True)

# Botón
stt_button = Button(label="🎤 Iniciar Grabación", width=200, button_type="success")

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
 
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
"""))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0
)

# Resultado
if result:
    if "GET_TEXT" in result:
        texto = result.get("GET_TEXT")
        
        st.success("Texto reconocido:")
        st.markdown(f"<h3 style='text-align:center; color:#2c3e50;'>🗣️ {texto}</h3>", unsafe_allow_html=True)

        client1.on_publish = on_publish                            
        client1.connect(broker,port)  
        message =json.dumps({"Act1":texto.strip()})
        ret= client1.publish("voice_ctrl-arp1007", message)

# Cierre tarjeta
st.markdown('</div>', unsafe_allow_html=True)

# Carpeta temp
try:
    os.mkdir("temp")
except:
    pass
