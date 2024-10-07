import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Title
st.title('Dashboard Air Quality Analysis di Lima Distrik Utama Beijing Tahun (2013-2017)')
# Deskripsi
st.markdown("""
Dashboard ini bertujuan untuk memberikan wawasan mengenai kualitas udara di lima distrik utama di Beijing 
(Aotizhongxin, Changping, Dongsi, Shunyi, Tiantan) dari tahun 2013 hingga 2017. 
Dua pertanyaan bisnis yang akan dijawab adalah:
1. Apa dampak kebijakan pemerintah mengenai pengendalian polusi terhadap kualitas udara pada lima distrik utama?
2. Apakah ada perbedaan tingkat polusi udara yang signifikan antara musim dingin dan musim panas pada lima distrik utama dan bagaimana faktor musim memengaruhi kualitas udara?
""")

# Data wragling
st.subheader("Data Wragling")

def load_data():
    df_aotizhongxin = pd.read_csv('D:/SEMESTER 5/BANGKIT ACADEMY/MATERI BUAT BELAJAR DICODING/Proyek Analisis Data/df_aotizhongxin_new.csv')
    df_changping = pd.read_csv('D:/SEMESTER 5/BANGKIT ACADEMY/MATERI BUAT BELAJAR DICODING/Proyek Analisis Data/df_changping_new.csv')
    df_dongsi = pd.read_csv('D:/SEMESTER 5/BANGKIT ACADEMY/MATERI BUAT BELAJAR DICODING/Proyek Analisis Data/df_dongsi_new.csv')
    df_shunyi = pd.read_csv('D:/SEMESTER 5/BANGKIT ACADEMY/MATERI BUAT BELAJAR DICODING/Proyek Analisis Data/df_shunyi_new.csv')
    df_tiantan = pd.read_csv('D:/SEMESTER 5/BANGKIT ACADEMY/MATERI BUAT BELAJAR DICODING/Proyek Analisis Data/df_tiantan_new.csv')

    df_aotizhongxin['district'] = 'Aotizhongxin'
    df_changping['district'] = 'Changping'
    df_dongsi['district'] = 'Dongsi'
    df_shunyi['district'] = 'Shunyi'
    df_tiantan['district'] = 'Tiantan'
    df_gabung= pd.concat([df_aotizhongxin, df_changping, df_dongsi, df_shunyi, df_tiantan], ignore_index=True)
    df_gabung = df_gabung.drop(['station','District'], axis=1)
    return df_gabung

def avg_polutan(df):
    rata_rata_polutan = df.groupby(['year', 'district'])[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].mean()
    rata_rata_polutan_tahun = rata_rata_polutan.unstack(level='district')
    return rata_rata_polutan_tahun

# load data 
df_gabung = load_data()
st.write(df_gabung.head())
# insight
st.markdown("""
**Insight**
- Hanya mengambil 5 distrik utama di kota Beijing yang digunakan yaitu Aotizhongxin, Changping, Dongsi, Shunyi, Tiantan dengan setiap distrik memiliki data yang tertulis mulai dari 1 Maret 2013 samapai 28 Februari 2017
- Setelah melakukan proses gathering, assesing dan cleaning mendapatkan 18 kolom yang berisi informasi tentang kualitas udara dan kondisi cuaca dan setiap distrik memiliki kolom numerik seperti year, month, day, hour, PM2.5 , PM10, SO2, NO2, CO, O3, TEMP, PRES, DEWP, RAIN, WSPM, season dan district
""")

rata_rata_polutan_tahun = avg_polutan(df_gabung)

# Hasil Explore Data
st.subheader("EDA (Exploratory Data Analysis)")
st.markdown("""
Explore Variable PM2.5, PM10, SO2, NO2, CO dan O3 pada setiap distrik (df_aotizhongxin, dan lainnya)
""")

st.write(rata_rata_polutan_tahun, index = False)
st.markdown("""
Terdapat variasi signifikan dalam konsentrasi polutan seperti PM2.5, PM10, SO2, NO2, CO, dan O3 di berbagai distrik. 
Konsentrasi PM2.5 menunjukkan penurunan dari rata-rata 80.164 pada tahun 2013 menjadi 71.003 pada tahun 2016, namun meningkat kembali menjadi 82.941 pada tahun 2017. 
PM10 juga mengalami fluktuasi serupa, dengan penurunan dari rata-rata 111.570 pada tahun 2013 menjadi 92.533 pada tahun 2016, dan kembali naik menjadi 100.030 pada tahun 2017. 
SO2 menunjukkan penurunan yang lebih konsisten dari rata-rata 19.536 pada tahun 2013 menjadi 10.340 pada tahun 2016, dan sedikit naik menjadi 18.570 pada tahun 2017. 
NO2 dan CO menunjukkan variasi yang kurang konsisten, dengan NO2 berkisar antara rata-rata 63.154 pada tahun 2013 dan 65.348 pada tahun 2017, dan CO berkisar antara rata-rata 1137.790 pada tahun 2013 dan 1308.503 pada tahun 2017. 
O3, di sisi lain, menunjukkan penurunan dari rata-rata 49.156 pada tahun 2013 menjadi 47.574 pada tahun 2017.
""")


# Buat visualisasi rata-rata polutan
polutans = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']

st.subheader("Analisis Tren Kualitas Udara per Tahun")
# visualisasi rata-rata PM2.5 per tahun di lima distrik
fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.set_title('Rata-rata PM2.5 di Lima Distrik Utama (2013-2017)', fontsize=16)
for district in rata_rata_polutan_tahun.columns.levels[1]:
    ax1.plot(rata_rata_polutan_tahun.index, rata_rata_polutan_tahun['PM2.5'], marker='o', label=district)
ax1.set_xlabel('Tahun', fontsize=12)
ax1.set_ylabel('Rata-rata PM2.5', fontsize=12)
ax1.set_xticks(rata_rata_polutan_tahun.index)
ax1.set_xticklabels(rata_rata_polutan_tahun.index.astype(str), rotation=0)
ax1.legend(title='Distrik', loc='upper right', fontsize=8)
ax1.grid(True)
plt.tight_layout()
st.pyplot(fig1)
st.markdown("""
Tren kualitas udara di berbagai distrik menunjukkan perubahan yang signifikan dalam periode tertentu.PM2.5 dan PM10 umumnya mengalami fluktuasi dengan puncak pada tahun 2014, diikuti oleh penurunan yang jelas pada tahun 2016, 
meskipun tingkat PM2.5 di distrik Aotizhongxin dan Changping tetap lebih tinggi, menandakan masalah kualitas udara yang lebih serius.
""")


# matrix korelasi hubungan antar jenis polutan
st.subheader("Matrix korelasi hubungan antar jenis polutan")
fig2, ax2 = plt.subplots(figsize=(10, 8))
correlation_matrix = df_gabung[polutans].corr()
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", ax=ax2)
ax2.set_title("Matriks Korelasi antara Polutan", fontsize=16)
st.pyplot(fig2)
st.markdown("""
Dari matrix korelasi di atas menunjukkan bahwa jenis polutan PM2.5 dan PM10 memiliki kaitan yang kuat yaitu sekitar 0.89, 
sehingga menjadi alasan mengapa PM2.5 dan PM10 dijadikan untuk menentukan suatu cluster.
""")

#---------------------------------------------------------------------------------------------------------------------------------------------------
# Pertanyaan 1: Rata-rata jenis polutan berdasarkan per-tahun untuk kelima distrik
st.subheader('Pertanyaan 1: Rata-rata jenis polutan berdasarkan per-tahun')

fig3, axes3 = plt.subplots(3, 2, figsize=(15, 12))
fig1.suptitle('Rata-rata Polutan di Lima Distrik Utama (2013-2017)', fontsize=16)
axes3 = axes3.flatten()
for i, polutan in enumerate(polutans):
    ax3 = axes3[i]
    for district in rata_rata_polutan_tahun.columns.levels[1]:
        ax3.plot(rata_rata_polutan_tahun.index, rata_rata_polutan_tahun[polutan][district], marker='o', label=district)
    ax3.set_title(f'Rata-rata {polutan} per Tahun', fontsize=12)
    ax3.set_xlabel('Tahun', fontsize=10)
    ax3.set_xticks(rata_rata_polutan_tahun.index)
    ax3.set_xticklabels(rata_rata_polutan_tahun.index.astype(str), rotation=0)
    ax3.set_ylabel(f'Rata-rata {polutan}', fontsize=10)
    ax3.grid(True)
    ax3.legend(title='Distrik', loc='upper right', fontsize=8)
plt.tight_layout(rect=[0, 0, 1, 0.95])

#visualisasi di streamlit
st.pyplot(fig3)
st.subheader("Insight")
st.markdown("""
Sebaran rata-rata jenis polusi udara diberbagai distrik menunjukkan perubahan yang signifikan dalam periode tertentu.
PM2.5 dan PM10 umumnya mengalami fluktuasi dengan puncak pada tahun 2014, diikuti oleh penurunan yang jelas pada tahun 2016, 
meskipun tingkat PM2.5 di distrik Aotizhongxin dan Changping tetap lebih tinggi, menandakan masalah kualitas udara yang lebih serius.
Sementara itu, SO2 menunjukkan penurunan konsisten dari tahun 2013 hingga 2017, terutama di Aotizhongxin yang mencatatkan penurunan tertinggi, 
menunjukkan efektivitas intervensi pengendalian emisi sulfur dioksida.NO2 fluktuatif tanpa tren yang jelas, namun penurunan signifikan tercatat di Shunyi tahun 2017, 
sering kaitannya dengan aktivitas lalu lintas.CO menunjukkan variasi tinggi tanpa adanya penurunan signifikan, menunjukkan pengaruh faktor lokal terhadap kadar karbon monoksida.
Akhirnya, O3 secara umum menurun, mencerminkan perbaikan dalam pengendalian emisi, walaupun ada peningkatan di Shunyi.
 """)

#---------------------------------------------------------------------------------------------------------------------------------
# Fungsi untuk mendapatkan musim berdasarkan bulan
def seasons(month):
    if month in [12, 1, 2]:  # Musim Dingin
        return 'Winter'
    elif month in [3, 4, 5]:  # Musim Semi
        return 'Spring'
    elif month in [6, 7, 8]:  # Musim Panas
        return 'Summer'
    else:
        return 'Fall'  # Musim Gugur

#gabung
df_gabung['season'] = df_gabung['month'].apply(seasons)
# Menghitung rata-rata polutan berdasarkan musim untuk pertanyaan 2
seasonal_data = {}
polusi = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3']

for polutan in polusi:
    seasonal_data[polutan] = df_gabung.groupby(['season', 'district'])[polutan].mean().unstack()

# Pertanyaan 2: Perbandingan jenis polutan berdasarkan musim
st.subheader('Pertanyaan 2: Perbandingan jenis polutan berdasarkan musim')
# visualisasi untuk setiap polutan
fig4, axes4 = plt.subplots(len(polutans), 1, figsize=(12, 5 * len(polutans)), sharex=True)
for ax4, polutan in zip(axes4, polutans):
    seasonal_data[polutan].plot(kind='bar', ax=ax4)
    ax4.set_title(f'Rata-rata {polutan} Berdasarkan Musim di Lima Distrik Utama', fontsize=14)
    ax4.set_ylabel(f'Rata-rata {polutan}', fontsize=12)
    ax4.legend(title='Distrik', loc='upper right')
    ax4.set_xticklabels(seasonal_data[polutan].index, rotation=0)
    ax4.grid(True)
    # nama musim di tengah setiap bar
    for i in range(len(seasonal_data[polutan])):
        ax4.text(i, seasonal_data[polutan].max().max() * -0.1, seasonal_data[polutan].index[i],
                ha='center', va='bottom', fontsize=10, color='black')

plt.xlabel('Musim', fontsize=10)
plt.tight_layout()
st.pyplot(fig4)

st.subheader("Insight")
st.markdown("""Polusi udara menampilkan variasi musiman yang berbeda, tergantung pada jenis polutan dan faktor lingkungan. 
Di musim dingin, polutan seperti PM2.5 dan NO2 seringkali meningkat, terutama karena intensifikasi kegiatan pemanasan dan transportasi.
Kondisi cuaca seperti perubahan suhu juga berkontribusi pada penumpukan polutan ini di atmosfer. Sebaliknya, di musim panas, 
tingkat O3 biasanya meningkat karena interaksi yang lebih kuat antara sinar matahari dan polutan, sementara polutan seperti PM10 dan SO2 cenderung menurun, 
yang mungkin dikaitkan dengan penurunan aktivitas industri dan peningkatan kapasitas penyerapan oleh vegetasi.
Terdapat juga perbedaan yang signifikan dalam distribusi polutan antar distrik yang dapat dipengaruhi oleh faktor-faktor seperti kepadatan penduduk, jenis sumber polusi, dan 
kebijakan lingkungan. Konsentrasi tinggi polutan tertentu di musim tertentu menimbulkan risiko kesehatan yang serius, seperti masalah pernapasan dan penyakit paru-paru 
yang lebih sering terjadi selama bulan-bulan dingin karena tingginya kadar PM2.5.
""")

## analisis lanjutan
st.subheader("Analisis Lanjutan Dengan Clustering Analysis")
st.markdown("""Membuat rata-rata untuk menentukan cluster dengan Metode Groupping""")

## fungsi musim rata"
def seasonal_avg(df, district_name):
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

# buat data rata-rata musim
df_aotizhongxin_avg = seasonal_avg(df_aotizhongxin_new, 'Aotizhongxin')
df_changping_avg = seasonal_avg(df_changping_new, 'Changping')
df_dongsi_avg = seasonal_avg(df_dongsi_new, 'Dongsi')
df_shunyi_avg = seasonal_avg(df_shunyi_new, 'Shunyi')
df_tiantan_avg = seasonal_avg(df_tiantan_new, 'Tiantan')

# gabung data menjadi avg_musim
df_avg_musim = pd.concat([df_aotizhongxin_avg, df_changping_avg, df_dongsi_avg, df_shunyi_avg, df_tiantan_avg])

# tambah kolom cluster
df_avg_musim['Cluster'] = np.where((df_avg_musim['PM2.5'] > df_avg_musim['PM2.5'].mean()) &
                                              (df_avg_musim['PM10'] > df_avg_musim['PM10'].median()),
                                              'Tinggi Polusi', 'Rendah Polusi')
df_avg_musim[['year', 'season', 'District', 'Cluster']]

st.subheader("Visualisasi PM2.5 dengan Boxplot")

#----------------------------------------------------------------------------------------------------------------------------------------
# visualisasi PM2.5
fig5, ax5 = plt.subplots(figsize=(14, 7))
sns.boxplot(data=df_avg_musim, x='season', y='PM2.5', hue='District', ax=ax5)
ax5.set_title('Distribusi PM2.5 Berdasarkan Musim di 5 Distrik Utama Beijing', fontsize=16)
ax5.set_xlabel('Musim', fontsize=12)
ax5.set_ylabel('PM2.5', fontsize=12)
plt.legend(title='Distrik', loc='upper right')
st.pyplot(fig5)
# markdown
st.markdown("""
Dari boxplot PM2.5 menunjukkan adanya variasi signifikan antar musim dan distrik. Musim dingin secara konsisten memiliki tingkat polusi PM2.5 yang lebih tinggi dibandingkan musim lainnya, menandakan pengaruh faktor musiman terhadap kualitas udara. 
Beberapa distrik, terutama Aotizhongxin dan Changping, menunjukkan variasi PM2.5 yang lebih besar, khususnya di musim dingin. 
Adanya outlier pada musim dingin juga mengindikasikan kemungkinan terjadinya polusi berat. 
Hal ini menyoroti pentingnya strategi pengendalian polusi yang mempertimbangkan variasi musiman dan karakteristik spesifik tiap distrik.
""")

st.subheader("Visualisasi Cluster dengan Headmap")
# visualisasi heatmap 
df_cluster = df_avg_musim[['year', 'season', 'District', 'Cluster']]
df_cluster_pivot = df_cluster.pivot_table(index='District', columns=['season', 'year'], values='Cluster', aggfunc='first')
df_cluster_pivot_num = df_cluster_pivot.replace({'Rendah Polusi': 0, 'Tinggi Polusi': 1})

fig6, ax6 = plt.subplots(figsize=(10, 6))
sns.heatmap(df_cluster_pivot_num, annot=True, cmap='coolwarm', ax=ax6, cbar_kws={'label': 'Pollution Level (0 = Rendah, 1 = Tinggi)'})
ax6.set_title('Clustering Polusi Udara di 5 Distrik Utama Beijing Berdasarkan Musim', fontsize=14)
ax6.set_xlabel('Musim dan Tahun', fontsize=12)
ax6.set_ylabel('Distrik', fontsize=12)
st.pyplot(fig6)
# markdown
st.markdown("""
Musim dingin mendominasi dalam cluster polusi 
Dalam headmap ini, kita dapat melihat bahwa sebagian besar wilayah masuk dalam kategori 
"Polusi Tinggi" pada musim dingin, sesuai dengan hasil pada Gambar 3.
Warna headmap menunjukkan bahwa musim dingin setiap tahunnya cenderung meningkat.
menjadi lebih tercemar dibandingkan musim lainnya.
""")

st.subheader("Visualisasi Cluster dengan Barplot")
#visualisasi cluster barplot
fig7, ax7 = plt.subplots(figsize=(14, 7))
sns.countplot(x='District', hue='Cluster', data=df_cluster, palette='coolwarm')
ax7.set_title('Sebaran Cluster Polusi Berdasarkan Distrik dan Musim', fontsize=16)
ax7.set_xlabel('Musim', fontsize=12)
ax7.set_ylabel('PM2.5', fontsize=12)
st.pyplot(fig7)

#markdown
st.markdown("""
a. Cluster Musim Dingin vs Musim Panas
Sebagian besar distrik di Beijing mengalami tingkat polusi yang lebih tinggi pada musim dingin jika dibandingkan dengan musim panas. 
Hal ini bisa jadi akibat dari penggunaan alat pemanas, kondisi meteorologis, dan berbagai faktor lain selama musim dingin. 
Di sisi lain, tingkat polusi biasanya berkurang pada musim panas.

b. Cluster Berdasarkan Pasca kebijakan Pemerintah
Pasca tahun 2015, terlihat adanya perbaikan di beberapa wilayah yang ditandai dengan penurunan kadar polusi. 
Hal ini menunjukkan bahwa kebijakan pengendalian polusi yang dilaksanakan pemerintah mulai berdampak pada beberapa distrik.
""")


# Conclusion
st.subheader("Conclusion")
st.markdown("""
- Dampak positif dari kebijakan pemerintah melihat data dibeberapa distrik menunjukkan pengurangan polusi yang tercatat di beberapa cluster pada kelima distrik di Beijing sejak tahun 2015 menyoroti dampak positif dari tindakan pengendalian polusi. 
Tren penurunan ini terlihat jelas di beberapa distrik, yang menunjukkan bahwa penerapan kebijakan tersebut telah memberikan hasil yang diharapkan.
- Dampak musiman terhadap kualitas udara, dari analisis di beberapa distrik menunjukkan bahwa polusi udara cenderung lebih tinggi pada musim dingin dibandingkan pada musim panas. 
Hal ini menunjukkan bahwa perubahan musim mempunyai dampak yang signifikan terhadap kondisi kualitas udara.
""")