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

# ------------------ ESTILOS ------------------
st.markdown("""
<style>
body {
    background-color: #f5f7fb;
}

.main {
    background-color: #f5f7fb;
}

h1 {
    color: #2c3e50;
    text-align: center;
}

h3 {
    text-align: center;
    color: #7f8c8d;
}

.center {
    display: flex;
    justify-content: center;
}

.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 200px;
    font-size: 16px;
    border: none;
}

.st
