# Phyton_sbp_kel3

Aplikasi CLI expert system sederhana untuk rekomendasi jurusan kuliah. Sistem berbasis forward chaining dan kini mendukung CRUD profil agar mudah diujicoba secara lokal.

## Persiapan

Gunakan Python 3.10+ yang sudah terpasang di mesin lokal.

## Cara menjalankan

### Mode interaktif (default)

```bash
python expert_system.py
```

Jawab pertanyaan yang muncul. Setelah rekomendasi tampil, Anda bisa memilih menyimpan profil ke file `profiles.json` (lokasi dapat diubah dengan `--data-file`).

### CRUD profil

Profil berisi fakta (minat, nilai, lingkungan belajar) yang bisa disimpan ke file JSON sehingga rekomendasi dapat diulang tanpa input ulang.

Simpan di lokasi lain:

```bash
python expert_system.py --data-file data/profiles.json
```

**Daftar profil:**

```bash
python expert_system.py list
```

**Lihat profil:**

```bash
python expert_system.py show NAMA_PROFIL
```

**Hapus profil:**

```bash
python expert_system.py delete NAMA_PROFIL
```

**Dapatkan rekomendasi dari profil tersimpan:**

```bash
python expert_system.py recommend NAMA_PROFIL
```

## Pengujian

```bash
python expert_system.py --test
```
