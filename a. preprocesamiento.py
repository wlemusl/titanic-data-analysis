#!/usr/bin/env python
# coding: utf-8

# ### Importar las bibliotecas requeridas

# In[1]:


import pandas as pd
get_ipython().run_line_magic('matplotlib', 'inline')


# ### Importar la bd original y explorarla

# In[2]:


df = pd.read_csv('bd titanic original.csv', encoding='latin-1')


# In[3]:


df.head(5)


# In[4]:


print('Id: ', len(df.Id.unique()))
print('Sobrevivió: ', len(df.Sobrevivió.unique()))
print('Clase: ', len(df.Clase.unique()))
print('Sexo: ', len(df.Sexo.unique()))
print('HerEsp:', len(df.HerEsp.unique()))
print('PadHij: ', len(df.PadHij.unique()))
print('Ticket: ', len(df.Ticket.unique()))
print('Cabina: ', len(df.Cabina.unique()))
print('Embarcó: ', len(df.Embarcó.unique()))


# **No vale la pena incluir la columna Id ya que es un ID de pasajeros que empieza en 1 y continua a un paso de +1.**

# In[5]:


df.info()


# **No vale la pena incluir la columna Cabina ya que posee un total de 148 valores únicos y solo tiene 204 filas con datos.**

# In[6]:


df.describe()


# **¿Qué pasa con las celdas de la columna "Precio" que están en 0? ¿Cuáles son estas? ¿Son valores que hacen falta o realmente tuvieron un costo de $0?**

# In[7]:


print(len(df[df['Precio'] == 0]))
df[df['Precio'] == 0]


# In[8]:


precio_0 = df[df['Precio'] == 0]
print(precio_0['Clase'].value_counts())


# **La columna "Embarcó" tiene dos celdas vacías o sin datos. ¿Cuáles son estas? ¿Por qué estos dos registros tienen el mismo número de ticket?**

# In[9]:


df[df['Embarcó'].isnull()]


# ### Lista de acciones a realizar en bd

# **Acciones a realizar en limpieza de datos después de exploración de base de datos:**
# 
# 1. Eliminar la columna Nombre, son 891 datos únicos que no brindarán ninguna tendencia.
# 2. Eliminar la columna Ticket, son 681 datos únicos que no generarán ninguna tendencia.
# 3. Eliminar la columna Cabina, pues el 77% de las celdas está en blanco o sin dato.
# 4. Considerar las celdas de Precio iguales a $0 a como que ese fue su precio real.
# 5. Imputar los valores en blanco de Embarcó, solo son 2 celdas, basado en la categoría más frecuente.
# 6. Crear columna con rangos de Edad para facilitar análisis y encontrar tendencias.
# 7. Crear columna que determine si la persona viajó sola o acompañada.
# 8. Crear una segunda base de datos, df2, que se enfoque solo en personas menor o igual a 18 años.
# 8. Crear columna que determine si los niños menor o igual a 18 años viajaban con hermanos o solos.
# 9. Crear columna que determine si los niños menor o igual a 18 años viajaban con padres o solos. 

# ### Limpieza y preprocesamiento de datos

# #### Acción 1, 2 y 3.

# In[10]:


df = df.drop('Nombre', axis = 1)
df = df.drop('Ticket', axis = 1)
df = df.drop('Cabina', axis = 1)


# #### Acción 5.

# In[11]:


print(df['Embarcó'].value_counts())


# In[12]:


embarcó = df['Embarcó'].fillna(value = 'S')
df['Embarcó'] = embarcó


# #### Acción 6.

# In[13]:


df['RangosEdad'] = pd.cut(df['Edad'], bins=[0,13,18,29,49,90], right=True, labels=False) + 1


# In[14]:


df['GruposEdad'] = df['RangosEdad'].map({1.0: 'Niño', 2.0: 'Adolescente', 3.0: 'Adulto jóven', 
                         4.0: 'Adulto', 5.0: 'Adulto mayor'})


# In[15]:


df = df.drop('RangosEdad', axis = 1)


# In[16]:


print(df['GruposEdad'].value_counts())


# *Range 1 = 0-13 niño
# ..... Range 2 = 14-18 adolescente
# ..... Range 3 = 19-29 adulto jóven
# ..... Range 4 = 30-49 adulto
# ..... Range 5 = 50-90 adulto mayor*

# #### Acción 7.

# In[17]:


df['HerEsp + PadHij'] = df['HerEsp'] + df['PadHij']


# In[18]:


df['RangosSolAcom'] = pd.cut(df['HerEsp + PadHij'], bins=[-1,0,20], right=True, labels=False) + 1


# In[19]:


df['SolAcom'] = df['RangosSolAcom'].map({1.0: 'Solo', 2.0: 'Acompañado'})
df = df.drop('RangosSolAcom', axis = 1)


# In[20]:


print(df['SolAcom'].value_counts())


# #### Acción 8.

# In[21]:


# df2 significa el dataframe 2 y esta solo contiene filas donde los pasajeros tienen menor o igual a 18 años.
df2 = df[df['Edad'] < 19]


# #### Acción 9.

# In[22]:


df2['RangosHerEsp'] = pd.cut(df2['HerEsp'], bins=[-1,0,2,15], right=True, labels=False) + 1
df2['GruposHerEsp'] = df2['RangosHerEsp'].map({1.0: 'Sin hermanos', 2.0: 'Entre 1-2', 3.0: 'Más de 2'})
df2 = df2.drop('RangosHerEsp', axis = 1)


# #### Acción 10.

# In[23]:


df2['RangosPadHij'] = pd.cut(df2['PadHij'], bins=[-1,0,3], right=True, labels=False) + 1
df2['GruposPadHij'] = df2['RangosPadHij'].map({1.0: 'Sin padres', 2.0: 'Con 1-2 padres'})
df2 = df2.drop('RangosPadHij', axis = 1)


# ### BDs listas para analizar y comer

# **dataframe 1 or df1**

# In[24]:


df.head(5)


# In[25]:


df.info()


# In[26]:


df.to_csv('bd titanic mineros.csv', index = False, encoding = 'latin-1') 


# **dataframe 2 or df2**

# In[27]:


df2.head(5)


# In[28]:


df2.info()


# In[29]:


df2.to_csv('bd titanic mineros -19.csv', index = False, encoding = 'latin-1') 


# In[ ]:




