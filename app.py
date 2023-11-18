import os
os.environ['OPENCV_DISABLE_OPENGL'] = '1' 
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import streamlit as st
import webbrowser

st.set_page_config(page_title='QRcode Scanner')

st.title('QRcode Scanner App')

seen_barcodes = set()

run = st.checkbox('Run Scanner')
frame_placeholder = st.empty() 

cap = cv2.VideoCapture(0)

while run:

  ret, frame = cap.read()
  
  decoded_objects = decode(frame)

  for decoded_obj in decoded_objects:

    points = decoded_obj.polygon
    points = np.array(points, np.int32)
    points = points.reshape((-1, 1, 2))

    barcode_data = decoded_obj.data.decode("utf-8") 
    barcode_type = decoded_obj.type

    if barcode_data not in seen_barcodes:

      seen_barcodes.add(barcode_data)  

      st.write(f"New barcode detected: {barcode_data}")
      webbrowser.open(barcode_data)

    cv2.polylines(frame, [points], True, (0,255,0), 5)

    barcode_text = f"Data: {barcode_data} | Type: {barcode_type}"
    cv2.putText(frame, barcode_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

  frame_placeholder.image(frame, channels='BGR')

cap.release()
