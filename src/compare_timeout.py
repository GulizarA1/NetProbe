# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt

def analyze_timeout_values():
    # Deney 3 test dosyalarımız
    files = {
        "0.1s Timeout": "stats_time_01.csv",
        "0.5s Timeout": "stats_time_05.csv",
        "1.0s Timeout": "stats_time_10.csv"
    }

    results = {}

    for label, file_name in files.items():
        try:
            df = pd.read_csv(file_name)
            start_time = df['Timestamp'].min()
            end_time = df['Timestamp'].max()
            duration = end_time - start_time
            
            # Yeniden gönderim (Retransmission) sayısını bul
            retransmissions = len(df[df['Event'] == 'RETRANSMISSION'])
            
            results[label] = {
                "Süre": duration,
                "Yeniden Gönderim": retransmissions
            }
        except FileNotFoundError:
            print(f"Hata: {file_name} bulunamadı! Lütfen dosya adını kontrol edin.")
            return

    labels = list(results.keys())
    durations = [results[l]["Süre"] for l in labels]
    retrans_counts = [results[l]["Yeniden Gönderim"] for l in labels]

    plt.figure(figsize=(12, 5))

    # Sol Grafik: Toplam Aktarım Süresi
    plt.subplot(1, 2, 1)
    bars1 = plt.bar(labels, durations, color=['#E91E63', '#9C27B0', '#673AB7'])
    plt.title('Timeout Değerinin Tamamlanma Süresine Etkisi', fontsize=12)
    plt.ylabel('Toplam Süre (Saniye)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    for bar in bars1:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.2f}s', ha='center', va='bottom', fontweight='bold')

    # Sağ Grafik: Yeniden Gönderim Sayısı
    plt.subplot(1, 2, 2)
    bars2 = plt.bar(labels, retrans_counts, color=['#00BCD4', '#009688', '#4CAF50'])
    plt.title('Timeout Değerinin Yeniden Gönderim Sayısına Etkisi', fontsize=12)
    plt.ylabel('Yeniden Gönderim Sayısı')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    for bar in bars2:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.savefig('deney3_timeout_etkisi.png', dpi=300)
    print("\nHarika! 'deney3_timeout_etkisi.png' başarıyla oluşturuldu.")
    plt.show()

if __name__ == "__main__":
    analyze_timeout_values()
