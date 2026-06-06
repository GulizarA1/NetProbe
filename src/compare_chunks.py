# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt

def analyze_comparative():
    # Test dosyalarımız ve etiketleri
    files = {
        "512 Byte": "stats_512.csv",
        "1024 Byte": "stats_1024.csv",
        "2048 Byte": "stats_2048.csv"
    }

    results = {}

    for label, file_name in files.items():
        try:
            df = pd.read_csv(file_name)
            # Toplam süreyi bul (Son olayın zamanı - İlk olayın zamanı)
            start_time = df['Timestamp'].min()
            end_time = df['Timestamp'].max()
            duration = end_time - start_time
            
            # Sadece Veri Paketlerini (SEND) sayalım
            send_events = df[df['Event'] == 'SEND']
            total_packets = len(send_events)
            
            # Etiketten byte değerini çekip kabaca throughput hesaplayalım
            chunk_size = int(label.split()[0])
            total_bytes = total_packets * (chunk_size + 12) # 12 Byte bizim Header'ımız
            throughput = (total_bytes * 8) / duration if duration > 0 else 0

            results[label] = {
                "Süre (Saniye)": duration,
                "Throughput (bps)": throughput
            }
        except FileNotFoundError:
            print(f"Hata: {file_name} bulunamadı! Testi atlamış olabilirsiniz.")
            return

    # --- GRAFİK 1: Tamamlanma Süresi ---
    labels = list(results.keys())
    durations = [results[l]["Süre (Saniye)"] for l in labels]
    throughputs = [results[l]["Throughput (bps)"] / 1000 for l in labels] # kbps'ye çevirdik

    plt.figure(figsize=(12, 5))

    # Sol Grafik: Süre
    plt.subplot(1, 2, 1)
    plt.bar(labels, durations, color=['#FF9800', '#03A9F4', '#4CAF50'])
    plt.title('Paket Boyutunun Süreye Etkisi', fontsize=12)
    plt.ylabel('Toplam Aktarım Süresi (Saniye)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Sağ Grafik: Throughput
    plt.subplot(1, 2, 2)
    plt.plot(labels, throughputs, marker='o', linestyle='-', color='#E91E63', linewidth=2, markersize=8)
    plt.title('Paket Boyutunun Verime (Throughput) Etkisi', fontsize=12)
    plt.ylabel('Throughput (kbps)')
    plt.grid(axis='both', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig('deney1_paket_boyutu.png', dpi=300)
    print("Mükemmel! 'deney1_paket_boyutu.png' başarıyla oluşturuldu.")
    plt.show()

if __name__ == "__main__":
    analyze_comparative()
