import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Air Quality Dashboard", layout="wide")
st.title('Air Quality Analysis 5 Distrik di Beijing')
st.header('Insight')
st.write("""
Polusi udara menampilkan variasi musiman yang berbeda, tergantung pada jenis polutan dan faktor lingkungan. 
         Di musim dingin, polutan seperti PM2.5 dan NO2 seringkali meningkat, terutama karena intensifikasi kegiatan pemanasan dan transportasi. Kondisi cuaca seperti perubahan suhu juga berkontribusi pada penumpukan polutan ini di atmosfer. 
         Sebaliknya, di musim panas, tingkat O3 biasanya meningkat karena interaksi yang lebih kuat antara sinar matahari dan polutan.
...
""")

# memilih district
district = st.sidebar.selectbox(
    "Select District", 
    ['Aotizhongxin', 'Changping', 'Dongsi', 'Shunyi', 'Tiantan']
)

# load data tanpa musim
def load_data():
    df_aotizhongxin = pd.read_csv('D:/SEMESTER 5/BANGKIT ACADEMY/MATERI BUAT BELAJAR DICODING/df_aotizhongxin_new.csv')
    df_changping = pd.read_csv('D:/SEMESTER 5/BANGKIT ACADEMY/MATERI BUAT BELAJAR DICODING/df_changping_new.csv')
    df_dongsi = pd.read_csv('D:/SEMESTER 5/BANGKIT ACADEMY/MATERI BUAT BELAJAR DICODING/df_dongsi_new.csv')
    df_shunyi = pd.read_csv('D:/SEMESTER 5/BANGKIT ACADEMY/MATERI BUAT BELAJAR DICODING/df_shunyi_new.csv')
    df_tiantan = pd.read_csv('D:/SEMESTER 5/BANGKIT ACADEMY/MATERI BUAT BELAJAR DICODING/df_tiantan_new.csv')
    
    df_aotizhongxin['District'] = 'Aotizhongxin'
    df_changping['District'] = 'Changping'
    df_dongsi['District'] = 'Dongsi'
    df_shunyi['District'] = 'Shunyi'
    df_tiantan['District'] = 'Tiantan'

    df_load = pd.concat([df_aotizhongxin, df_changping, df_dongsi, df_shunyi, df_tiantan], ignore_index=True)
    return df_load

df_load = load_data() 

df_filter = df_load[df_load['District']== district]

st.title(f"Air Quality Analisis untuk {district}")

# dataframe 
st.subheader("Data Preview")
st.dataframe(df_filter.head())

# deskripsi statistik
st.subheader("Summary Statistik")
st.write(df_filter.describe())

show_heatmap = st.sidebar.checkbox("Tampilkan Correlation Heatmap")
show_visual = st.sidebar.checkbox("Tampilkan Distribusi Polusi")

# visual barplot
if show_visual:
    st.subheader(f"Distribusi Polusi di {district}")
    pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    fig, axes = plt.subplots(3, 2, figsize=(20, 12))
    axes = axes.flatten()
    
    for i, pollutant in enumerate(pollutants):
        sns.histplot(df_filter[pollutant].dropna(), ax=axes[i], kde=True)
        axes[i].set_title(f'Distribusi dari {pollutant}')
        axes[i].set_xlabel(pollutant)
    st.pyplot(fig)

# loop menampilkan heatmap
if show_heatmap:
    st.subheader("Korelasi Heatmap dari Polusi")
    
    pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    correlation_matrix = df_filter[pollutants].corr()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

#sidebar select dataset
st.sidebar.write("PRSA Dataset")

#Rata-rata musim berdasarkan musim
def musim_avg(df, district_name):
    return df.groupby(['year', 'season']).agg({
        'PM2.5': 'mean',
        'PM10': 'mean',
        'SO2': 'mean',
        'NO2': 'mean',
        'CO': 'mean',
        'O3': 'mean'
    }).reset_index().assign(District=district_name)

# load data
df_aotizhongxin_new = pd.read_csv('D:/SEMESTER 5/BANGKIT ACADEMY/MATERI BUAT BELAJAR DICODING/df_aotizhongxin_new.csv')
df_changping_new = pd.read_csv('D:/SEMESTER 5/BANGKIT ACADEMY/MATERI BUAT BELAJAR DICODING/df_changping_new.csv')
df_dongsi_new = pd.read_csv('D:/SEMESTER 5/BANGKIT ACADEMY/MATERI BUAT BELAJAR DICODING/df_dongsi_new.csv')
df_shunyi_new = pd.read_csv('D:/SEMESTER 5/BANGKIT ACADEMY/MATERI BUAT BELAJAR DICODING/df_shunyi_new.csv')
df_tiantan_new = pd.read_csv('D:/SEMESTER 5/BANGKIT ACADEMY/MATERI BUAT BELAJAR DICODING/df_tiantan_new.csv')

# buat data baru guna menghitung rata-rata per musim
df_aotizhongxin_avg = musim_avg(df_aotizhongxin_new, 'Aotizhongxin')
df_changping_avg = musim_avg(df_changping_new, 'Changping')
df_dongsi_avg = musim_avg(df_dongsi_new, 'Dongsi')
df_shunyi_avg = musim_avg(df_shunyi_new, 'Shunyi')
df_tiantan_avg = musim_avg(df_tiantan_new, 'Tiantan')

# gabung dengan pd.concat
df_avg_musim = pd.concat([df_aotizhongxin_avg, df_changping_avg, df_dongsi_avg, df_shunyi_avg, df_tiantan_avg])

# buat kriteria hasil clustering analisis
df_avg_musim['Cluster'] = np.where((df_avg_musim['PM2.5'] > df_avg_musim['PM2.5'].mean()) &
                                   (df_avg_musim['PM10'] > df_avg_musim['PM10'].median()), 
                                   'Tinggi Polusi', 'Rendah Polusi')

# menampilkan dataframe
st.write("Dataframe rata-rata polusi berdasarkan musim dan distrik")
st.write(df_avg_musim.columns)
st.write(df_avg_musim[['year','season','District', 'Cluster']])

# menggunakan boxplot untuk PM2.5
st.subheader('Distribusi PM2.5 Berdasarkan Musim')
fig, ax = plt.subplots(figsize=(14, 7))
sns.boxplot(data=df_avg_musim, x='season', y='PM2.5', hue='District', ax=ax)
ax.set_title('Distribusi PM2.5 Berdasarkan Musim di 5 Distrik Utama Beijing')
st.pyplot(fig)

# visualisasi clustering dengan heatmap
st.subheader('Clustering Polusi Udara Berdasarkan Musim dan Tahun')
df_cluster = df_avg_musim[['year', 'season', 'District', 'Cluster']]
df_cluster_pivot = df_cluster.pivot_table(index='District', columns=['season', 'year'], values='Cluster', aggfunc='first')
df_cluster_pivot_num = df_cluster_pivot.replace({'Rendah Polusi': 0, 'Tinggi Polusi': 1})

# visualisasi Barplot Sebaran Cluster Polusi Berdasarkan Distrik
st.subheader('Sebaran Cluster Polusi Berdasarkan Distrik dan Musim')
fig, ax = plt.subplots(figsize=(12, 6))
sns.countplot(x='District', hue='Cluster', data=df_cluster, palette='coolwarm', ax=ax)
ax.set_title('Sebaran Cluster Polusi Berdasarkan Distrik dan Musim')
ax.set_xlabel('District')
ax.set_ylabel('Jumlah')
st.pyplot(fig)

st.subheader('Kesimpulan')
st.write("""
- **Dampak Kebijakan Pemerintah**: Pengurangan tingkat polusi setelah 2015 terlihat di beberapa distrik, menyoroti dampak positif dari kebijakan pengendalian polusi.
- **Dampak Musiman**: Polusi udara lebih tinggi selama musim dingin dibandingkan musim panas, yang mungkin disebabkan oleh penggunaan alat pemanas dan faktor meteorologis.
""")