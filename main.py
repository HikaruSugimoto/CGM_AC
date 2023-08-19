import streamlit as st
import pandas as pd
import statsmodels.api as sm
from PIL import Image
import zipfile
import os
st.set_page_config(layout="wide")
st.title('CGM AC app')
st.write('This app calculates AC_Mean and AC_Var, which are derived from autocorrelation coefficients of glucose levels measured by CGM. This app also calculates the mean (Mean) and the standard deviation (Std) of glucose levels. Glucose should be measured every 5 min.')
st.write('This app accepts CGM data in the following format:')
image=Image.open("CGM_data.png")
st.image(image,width=600)

st.subheader('License')
st.write('This web app is licensed free of charge for academic use and we shall not be liable for any direct, indirect, incidental, or consequential damages resulting from the use of this web app. In addition, we are under no obligation to provide maintenance, support, updates, enhancements, or modifications.')
while not os.path.isfile('demo.zip'):
    with zipfile.ZipFile('demo.zip', 'x') as csv_zip:
        csv_zip.writestr("CGM_data.csv", 
                        pd.read_csv("CGM_data.csv").to_csv(index=False))        
with open("demo.zip", "rb") as file:
    st.download_button(label = "Download demo data",data = file,file_name = "demo.zip")

#Input
st.subheader('Upload CGM data')
df = st.file_uploader("", type="csv")

if df is not None:
    df =pd.read_csv(df)
    AC= pd.DataFrame()
    for i in range (0,len(df.iloc[:,0])):
        X = df.iloc[i,1:]
        dff=pd.DataFrame(sm.tsa.stattools.acf(X,nlags=30,fft=False))
        AC=pd.concat([AC, pd.DataFrame([df.iloc[i,0],X.mean(),X.std(),dff.iloc[1:].mean()[0],dff.iloc[1:].var()[0]]).T])
    AC=AC.rename(columns={0: 'ID'}).rename(columns={1: 'Mean'}).rename(columns={2: 'Std'}).rename(columns={3: 'AC_Mean'}).rename(columns={4: 'AC_Var'})
    st.write(AC.set_index('ID'))
  
    while not os.path.isfile('CGM_AC.zip'):
        with zipfile.ZipFile('CGM_AC.zip', 'x') as csv_zip:
            csv_zip.writestr("CGM_AC.csv",
                            AC.to_csv(index=False))
    with open("CGM_AC.zip", "rb") as file: 
        st.download_button(label = "Download the result",
                           data = file,file_name = "CGM_AC.zip")
