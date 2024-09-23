import cv2
import numpy as np

# Membuka kamera laptop
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Tidak bisa membuka kamera")
    exit()

# Ukuran kotak virtual
tombol_atas_kiri = (100, 100)
tombol_bawah_kanan = (300, 300)

while True:
    # Membaca frame dari kamera
    ret, frame = cap.read()
    if not ret:
        print("Gagal mengambil gambar")
        break

    # Konversi frame ke grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Thresholding untuk deteksi kontur
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)

    # Mendeteksi kontur
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Gambarkan area tombol virtual
    cv2.rectangle(frame, tombol_atas_kiri, tombol_bawah_kanan, (0, 255, 0), 2)

    tombol_ditekan = False

    # Loop melalui setiap kontur yang terdeteksi
    for contour in contours:
        # Mendapatkan bounding box untuk kontur
        x, y, w, h = cv2.boundingRect(contour)

        # Filter kontur yang terlalu kecil/besar
        if w > 50 and h > 50:
            # Gambarkan bounding box di sekeliling tangan yang terdeteksi
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Cek jika tangan berada di dalam kotak virtual
            if (x > tombol_atas_kiri[0] and y > tombol_atas_kiri[1] and
                    x + w < tombol_bawah_kanan[0] and y + h < tombol_bawah_kanan[1]):
                tombol_ditekan = True

    if tombol_ditekan:
        print("Tombol virtual ditekan!")
    else:
        print("Tombol virtual tidak ditekan.")

    # Tampilkan frame dengan kotak dan kontur tangan
    cv2.imshow('Tombol Virtual', frame)

    # Tekan ESC untuk keluar
    if cv2.waitKey(10) == 27:
        break

# Bersihkan setelah selesai
cap.release()
cv2.destroyAllWindows()
