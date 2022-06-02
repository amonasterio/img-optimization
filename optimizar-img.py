
from PIL import Image
import urllib.request
import requests
import os
import pandas as pd
import numpy as np
import time 
import shutil

def getNombreImagen(url):
    return url[url.rfind("/")+1:len(url)]

def eliminaFichero(myfile):
    if os.path.isfile(myfile):
        os.remove(myfile)


fileDir = os.path.dirname(os.path.abspath(__file__))
newFile = r'\img_optimizadas'
path = os.path.join(fileDir + newFile)
if not os.path.exists(path):
  os.mkdir(path)


f_entrada='entradas.csv'
df=pd.read_csv(f_entrada)
df_output=pd.DataFrame(columns=['img_name', 'bytes_old', 'width_old','height_old','bytes_new', 'width_new','height_new'],
index=df.index)

for i in range(len(df)):
    url=df.iloc[i,0]
    new_width=df.iloc[i,1]
    calidad=df.iloc[i,2]
    img_name=getNombreImagen(url)
    try:
      data_headers ={"User-Agent":"Mozilla/5.0"}
      r = requests.get(url,headers=data_headers)
      with open(img_name, 'wb') as outfile:
        outfile.write(r.content)
      image = Image.open(img_name)
      tam_actual=os.stat(img_name).st_size
      df_output.iloc[i,0]=img_name
      df_output.iloc[i,1]=tam_actual
      df_output.iloc[i,2]=image.size[0]
      df_output.iloc[i,3]=image.size[1]
      width, height = image.size
      new_image_loc = r'\\'+img_name
      ruta_comprimida=path+new_image_loc
      if not np.isnan(new_width):
        new_width=int(new_width)
        new_height=int(height*new_width/width)
        image = image.resize((new_width,new_height))
      if not np.isnan(calidad):
        calidad=int(calidad)
      else:
        calidad=70 #calidad por defecto
      image.save(ruta_comprimida,optimize = True, quality = calidad)
      tam_nuevo=os.stat(ruta_comprimida).st_size
      #si el tamaño es superior, dejamos la versión actual
      if(tam_nuevo>tam_actual):
        shutil.copy(img_name,ruta_comprimida)
      df_output.iloc[i,4]=os.stat(ruta_comprimida).st_size
      df_output.iloc[i,5]=image.size[0]
      df_output.iloc[i,6]=image.size[1] 
      image.close() 
    except  Exception as e:
      print("error: "+img_name)
      df_output.iloc[i,4]="error"
      df_output.iloc[i,5]="error"
      df_output.iloc[i,6]="error" 
    eliminaFichero(img_name)
    time.sleep(1)
df["optimizacion"]=(df["bytes_new"]-df["bytes_old"])/df["bytes_old"]
df_output.to_csv("resumen.csv")