# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt

def analyze_and_plot(csv_file):
    try:
        # Veriyi Pandas DataFrame olarak oku
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Hata: {csv_file} bulunamadı. Önce client.py'yi çalıştırın.")
        return

    # Olay türlerinin frekansını hesapla
    event_counts = df['Event'].value_counts()

    # Terminale özet istatistikleri yazdır
    print("--- AKTARIM İSTATİSTİKLERİ ---")
    print(f"Toplam Olay Sayısı: {len(df)}")
    for event, count in event_counts.items():
        print(f"- {event}: {count} kez")

    # Retransmission Rate (Yeniden Gönderim Oranı) Hesaplama
    total_sends = event_counts.get('SEND', 0)
    total_retransmissions = event_counts.get('RETRANSMISSION', 0)
    
    if total_sends > 0:
        retrans_rate = (total_retransmissions / total_sends) * 100
        print(f"\nYeniden Gönderim Oranı (Retransmission Rate): %{retrans_rate:.2f}")

    # Grafik Çizimi (Matplotlib)
    plt.figure(figsize=(8, 5))
    bars = plt.bar(event_counts.index, event_counts.values, color=['#4CAF50', '#2196F3', '#FFC107', '#F44336'])
    
    plt.title('Ağ Olayları Frekans Dağılımı (NetProbe)', fontsize=14)
    plt.xlabel('Olay Türü', fontsize=12)
    plt.ylabel('Gerçekleşme Sayısı', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Barların üzerine sayıları ekle
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, int(yval), ha='center', va='bottom', fontweight='bold')

    # Grafiği PNG olarak kaydet ve göster
    plt.savefig('olay_dagilimi_grafiyi.png', dpi=300, bbox_inches='tight')
    print("\nGrafik 'olay_dagilimi_grafiyi.png' adıyla kaydedildi.")
    plt.show()

if __name__ == "__main__":
    analyze_and_plot("transfer_stats.csv")