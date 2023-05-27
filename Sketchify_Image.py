import streamlit as st
import cv2
import time
import os
from PIL import Image
import webbrowser


def autoclear(current_time):
    list_of_files = os.listdir('./uploads')
    print(list_of_files)
    day = 120
    for i in list_of_files:
        file_time = os.stat(os.path.join(os.getcwd(),'uploads', i)).st_mtime
        if(file_time < current_time-day):
            os.remove(os.path.join(os.getcwd(),'uploads', i))


def convert_tosketch(file):
    img = cv2.imread(file)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img_invert=cv2.bitwise_not(img_gray)
    img_soothing=cv2.GaussianBlur(img_invert,(21,21),sigmaX=0,sigmaY=0)
    final=cv2.divide(img_gray,255-img_soothing,scale=255)

    return final

def save_uploaded_image(uploaded_image):
    try:
        with open(os.path.join('uploads',uploaded_image.name),'wb') as f:
            f.write(uploaded_image.getbuffer())
        return True
    except:
        return False
    
current_time = time.time()
autoclear(current_time)
st.title('Image Sketchify')
if st.button("Created by @adi323 :sunglasses:"):
    webbrowser.open_new_tab('https://github.com/adi323')

uploaded_file=st.file_uploader("Upload an image and transform into sketch",accept_multiple_files=False,type=['png','jpg','jpeg'])

if uploaded_file is not None and save_uploaded_image(uploaded_image=uploaded_file):

    final_img=convert_tosketch(os.path.join('uploads',uploaded_file.name))


    st.header('Original Image')
    st.image(Image.open(os.path.join('uploads',uploaded_file.name)),channels="RGB",width=500)
    st.header('Sketchified Image')
    st.image(final_img,channels="RGB",width=500)
    st.empty()
    
    cv2.imwrite('./uploads/final_img{}.jpg'.format(current_time),final_img)
    with open('./uploads/final_img{}.jpg'.format(current_time),'rb') as file:
        st.download_button('Download Sketch Image',file,file_name="sketch.png",
            mime="image/png")