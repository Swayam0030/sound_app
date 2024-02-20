import streamlit as st
from PIL import Image
import librosa
import ffmpeg
from pydub import AudioSegment
from io import BytesIO
import librosa.display
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
import numpy as np
import h5py
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.xception import Xception, preprocess_input
import pandas as pd
# from huggingface_hub import from_pretrained_keras

def main():

    page = st.sidebar.selectbox("App Selections", ["Homepage", "About", "Identify", "Contact Us"])
    if page == "Identify":
        st.title("Sound Classifier for Oil Rig Sounds")
        identify()
    elif page == "About":
        about()
    elif page == "Homepage":
        homepage()
    elif page == "Contact Us":
        contact()

def contact():
    html_temp = """
    <html>
    <head>
    <style>
    body {
      background-color: #fe2631;
    }
    </style>
    </head>
    <body>
    </body>
    """
    img = Image.open('lastpage.png')
    # st.image(img, unsafe_allow_html = True)
    st.image(img, caption="Example Image")

    st.markdown(html_temp, unsafe_allow_html = True)
    linked_in = '''[![LinkedIn](https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/LinkedIn_Logo.svg/120px-LinkedIn_Logo.svg.png)](https://www.linkedin.com/in/prashant-mudgal-ba210420/)'''
    st.markdown(linked_in, unsafe_allow_html=True)
    #github = '''[![Github](https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Github-desktop-logo-symbol.svg/64px-Github-desktop-logo-symbol.svg.png)](https://github.com/Prashantmdgl9/Oil_rig_sounds)'''
    #st.markdown(github, unsafe_allow_html=True)
    github = '''[![Github](https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/GitHub_logo_2013.svg/64px-GitHub_logo_2013.svg.png)](https://github.com/Prashantmdgl9/Oil_rig_sounds)'''
    st.markdown(github, unsafe_allow_html=True)
    img = Image.open('tweet.png')
    st.image(img)

    



def about():
    set_png_as_page_bg('oil2.png')
    st.title("About present work")
    st.subheader("Billions of dollars are spent in oil rig operations including the safety on deck, quick analysis, efficiency etc. While multiple systems and heavy machinery are"
     " used for various tasks at hand, there always are avenues that can be explored to bring the efficiency and safety at optimum level.")
    st.subheader("Multiple sounds are generated at the rigs during the extraction process and classifying the sounds correctly can help the engineers in reinforcing their"
    " initial estimates and quick decisioning.")
    audio_file = open("./machine_6.wav", 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/wav')

    st.subheader("In the present POC, we are classifying the sounds obtained from oil rigs into 10 categories:")
    Final_Sound = ['Blowout', 'Gas Emission', 'Rock Bed', 'Heavy Gas', 'Heavy Metal', 'Oil Drill Rig Exterior', 'Operatre Pump', 'Dieseling' , 'Fracturing', 'Hydraulic']
    df = pd.DataFrame(Final_Sound, columns=['Sound Class'])
    st.table(df)
    #st.subheader("Blowout, Gas Emission, Rock Bed, Heavy Gas, Heavy Metal, Oil Drill Rig Exterior, Operatre Pump, Dieseling, Fracturing, Hydraulic")





def homepage():
    html_temp = """
    <html>
    <head>
    <style>
    body {
      background-color: #fe2631;
    }
    </style>
    </head>
    <body>
    </body>
    """
    st.markdown(html_temp, unsafe_allow_html = True)

    image = Image.open('home6.png')
    st.image(image, use_column_width = True)

import base64

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)
    return


# datapath = '/Users/prashantmudgal/Documents/Quantplex Labs/Sound_app/data/'
datapath = 'D:/Study/Projects/Sound_app/data/'

import os

def identify():
    set_png_as_page_bg('oil5.png')
    st.set_option('deprecation.showfileUploaderEncoding', False)
    st.subheader("Choose a mp3 file that you extracted from the work site")
    uploaded_file = st.file_uploader("Select")
    print("Uploaded file: ", uploaded_file)
    # print("UPLOADED FILE: ",uploaded_file)
    # print("PATHS: ",datapath+uploaded_file.name)
    # if os.path.exists(datapath):
    #     print(f"The path '{datapath}' exists.")
    #     if os.path.exists(datapath+uploaded_file.name):
    #         print(f"The path '{datapath+uploaded_file.name}' exists.")
    #     else:
    #         print(f"The path '{datapath+uploaded_file.name}' does not exist")
    # else:
    #     print(f"The path '{datapath}' does not exist.")

    if uploaded_file is not None:
        audio_bytes = uploaded_file.read()
        #st.audio(audio_bytes, format='audio/mp3')
        sound = AudioSegment.from_mp3(datapath+uploaded_file.name)

        # audio_bytes = BytesIO(uploaded_file.read())
        # sound = AudioSegment.from_file(audio_bytes)

        sound.export(datapath+'wav_file'+'.wav', format="wav")
        wav_file = datapath+'wav_file'+'.wav'
        y, sr = librosa.load(wav_file)
        plot_spectrogram(y, sr)



def plot_spectrogram(y, sr):
    st.header('Spectrogram of the audio is')
    return mel_gram(y, sr)


def mel_gram(signal, sampling_rate, slider_length = 512):
    y_axis="log"
    fig = plt.figure(figsize=(10, 6))
    librosa.display.specshow(librosa.core.amplitude_to_db(librosa.feature.melspectrogram( y=signal,sr=sampling_rate)), hop_length=slider_length, x_axis="time",
                             y_axis=y_axis)
    plt.colorbar(format="%+2.f")
    st.pyplot(fig)
    #name = 'spects/test/spect.png'
    #fig.savefig(datapath[:-5]+name)
    saveMel(signal)


def saveMel(y):

    N_FFT = 1024         # Number of frequency bins for Fast Fourier Transform
    HOP_SIZE = 1024      # Number of audio frames between STFT columns
    SR = 44100           # Sampling frequency
    N_MELS = 30          # Mel band parameters
    WIN_SIZE = 1024      # number of samples in each STFT window
    WINDOW_TYPE = 'hann' # the windowin function
    FEATURE = 'mel'      # feature representation

    spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=SR)[0]
    frames = range(len(spectral_centroids))
    t = librosa.frames_to_time(frames)

    plt.rcParams['figure.figsize'] = (10,2)
    fig = plt.figure(1,frameon=False)
    fig.set_size_inches(4,4)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    #ax1 = plt.subplot(2, 1, 1)
    spectogram = librosa.display.specshow(
             librosa.core.amplitude_to_db(
                librosa.feature.melspectrogram(
                                y=y,
                                sr=SR)))
    # name = 'spects/test/0Euras/spect.png'
    name = 'spects/test/spect.png'
    fig.savefig(datapath[:-5]+name)
    classify(fig)

Final_Sound = ['Blowout', 'Gas Emission', 'Rock Bed', 'Heavy Gas', 'Heavy Metal', 'Oil Drill Rig Exterior', 'Operatre Pump', 'Dieseling' , 'Fracturing', 'Hydraulic']
#!echo "backend: TkAgg" >> ~/.matplotlib/matplotlibrc
import tensorflow.keras.backend as K
path = "models/VGG16_CNN_5.h5"
def classify(fig):
    TARGET_SIZE = (224, 224)
    BATCH_SIZE = 10
    model = load_model_x(path)
    #model.summary()
    test_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
    test_batches = test_datagen.flow_from_directory(datapath[:-5]+'spects'+'/test',
                                                      target_size = TARGET_SIZE,
                                                      batch_size = BATCH_SIZE)

    pred = model.predict(test_batches)
    rounded_prediction = np.argmax(pred, axis = 1)
    st.header("The sound belongs to the  category of: ")
    st.title(Final_Sound[rounded_prediction[0]])


@st.cache(allow_output_mutation=True)
def load_model_x(path):
    # model = from_pretrained_keras('Swayam007/sound_model')
    model = load_model(path) # included to make it visible when model is reloaded
    return model

if __name__ == "__main__":
    main()
