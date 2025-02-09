# BNA DATA
Kami percaya bahwa data adalah kunci untuk pengambilan keputusan yang lebih baik. Oleh karena itu, kami menghadirkan BNA DASHBOARD, sebuah platform open-source yang menyediakan data, dashboard, dan visualisasi interaktif untuk mendukung transparansi, inovasi, dan kemajuan di BNA. Kami memfokuskan terlebih dahulu pada pengolahan dan pengembangan data pendidikan, bencana, penduduk, pariwisata, dan kesehatan. Data-data tersebut sangat penting karena dapat memberikan wawasan yang mendalam untuk meningkatkan kualitas hidup masyarakat, merencanakan pembangunan yang lebih efektif, serta mengelola sumber daya dengan lebih baik.

#### Catatan
- Semua data .csv ada di folder dataset.
- Semua data boleh diunduh.
- Semua data diambil dari BPS Kabupaten Banjarnegara, Banajarnegara Satu Datu, dan Sumber data resmi lainya milik pemerintah/lembaga/organsiasi resmi.

#### Teknologi
- Bahasa Pemograman: Python
- Framework: Streamlit
  
#### Menjalankan Aplikasi di Lokal
- Clone repository ke lokal
- Install Dependencies
- Run python -m streamlit run app.py

# DOKUMENTASI
### Format .csv file untuk data GIS
| kecamatan  | x          | y          | total  |
|------------|------------|------------|--------|
| Mandiraja  | bla        | bli        | 28000  |
| Sigaluh    | bla        | bli        | 34000  |
| dst.       | dst.       | dst        | dst    |

##### Harus ada kolom kecamatan dan kolom total.
##### Dataset harus dari sumber resmi (BPS atau website milik pemerintah)

### Struktur Konten (Pages)
#### example:
- Judul (DATA KESEHATAN BNA)
    - Sub Judul 1 (DATA TENAGA KESEHATAN BNA)
        - Filter
        - Card
        - Chart
        - Map (Opsional)
        - Dataset
    - Sub Judul 2 (DATA FASILITAS KESEHATAN BNA)
        - Filter
        - Card
        - Chart
        - Dataset
  
## TERIMA KASIH
