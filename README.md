# Global Superstore — Streamlit Dashboard

Proyek ini mengubah dataset Global Superstore menjadi aplikasi dashboard interaktif menggunakan Streamlit.

## Isi proyek
- `app.py` — aplikasi dashboard.
- `Global Superstore.xlsx` — dataset Excel asli (sheet Orders, Returns, People).
- `requirements.txt` — dependensi Python.
- `.gitignore` — file/folder yang tidak perlu dikirim ke GitHub.

## Fitur
- Dashboard KPI: Total Sales, Total Profit, Quantity, Unique Orders, Profit Margin, dan Returned Orders.
- Worksheet 1: Sales Trend.
- Worksheet 2: Profit by Category.
- Worksheet 3: Sales by Country (Top 20).
- Story 1: Sales Performance Analysis.
- Story 2: Profitability Analysis.
- Filter interaktif: Tahun, Market, Segment, dan Category.

## Menjalankan di GitHub Codespaces
1. Buat repository baru di GitHub.
2. Upload semua isi ZIP ini ke repository (ekstrak ZIP terlebih dahulu).
3. Buka repository, tekan **Code** → **Codespaces** → **Create codespace on main**.
4. Di terminal Codespaces jalankan:

   ```bash
   pip install -r requirements.txt
   streamlit run app.py --server.address 0.0.0.0
   ```

5. Codespaces biasanya menawarkan tombol **Open in Browser** atau **Make Public** pada port 8501. Pilih sesuai kebutuhan agar aplikasi dapat dibuka.

## Deploy permanen ke Streamlit Community Cloud
1. Push semua file proyek ke GitHub.
2. Buka https://share.streamlit.io/ dan masuk dengan akun GitHub.
3. Pilih **New app**, repository, branch `main`, dan file `app.py`.
4. Tekan **Deploy**. Setelah proses selesai, Streamlit memberikan URL aplikasi.

## Catatan penting tentang persyaratan tugas
Aplikasi Streamlit ini menyediakan struktur analisis yang diminta (3 worksheet/visualisasi, 2 story, dan 1 dashboard) dalam bentuk aplikasi web. **Namun, Streamlit bukan Tableau Public dan URL Streamlit bukan link publikasi Tableau Public.** Jika dosen secara khusus mewajibkan workbook dipublikasikan di Tableau Public, konfirmasikan apakah Streamlit dapat diterima sebagai alternatif sebelum mengumpulkan.

## Catatan data
Angka dan insight dihitung dari data sesuai filter yang dipilih. Returned Orders dihitung dengan mencocokkan `Order ID` di sheet Orders dan Returns.
