import streamlit as st
import subprocess
from subprocess import STDOUT, check_call
import os
import base64
import camelot as cam

@st.cache_data
def gh():
    proc = subprocess.Popen('apt-get install -y ghostscript', shell=True, stdin=None, stdout=open(os.devnull,'wb'), stderr=STDOUT, executable="/bin/bash")

gh()

st.title("Extract Tables from PDFs")

input_pdf = st.file_uploader(label="Upload PDF here",type='pdf')

st.markdown("### Page Number")

page_number = st.text_input("Enter the page # from where you want the table", value=1)

if input_pdf is not None:
    
    with open("input.pdf","wb") as f:
        base64_pdf = base64.b64encode(input_pdf.read()).decode('utf-8')
        f.write(base64.b64decode(base64_pdf))
    f.close()

    table = cam.read_pdf("input.pdf",pages = page_number, flavor = 'stream')
    
    st.markdown("## Number of Tables")
    
    st.write(table)
    
    if len(table)>0:
        
        option = st.selectbox(label="Select the table to be displayed", options = range(len(table)+1))
        
        st.markdown("### Output Table")
        
        st.dataframe(table[int(option)-1].df)
        
        