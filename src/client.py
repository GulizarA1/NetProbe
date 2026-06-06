# -*- coding: utf-8 -*-
print("\n>>> [SİSTEM] client.py okundu ve çalışmaya başladı! <<<")

import socket
import os
import time
import csv
from packet import create_packet, parse_packet, HEADER_SIZE

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5005
CHUNK_SIZE = 2048
TIMEOUT_VALUE = 1.0
MAX_RETRIES = 5      

log_data = []
total_sent_bytes = 0  # Throughput hesabı için ağa basılan tüm baytlar

def log_event(event_type, seq_num, retry_count):
    log_data.append({
        "Timestamp": time.time(),
        "Event": event_type,
        "SeqNum": seq_num,
        "RetryCount": retry_count
    })

def send_packet_reliably(client_socket, pkt_type, seq_num, payload=b""):
    global total_sent_bytes
    packet = create_packet(pkt_type, seq_num, payload)
    retries = 0
    
    while retries <= MAX_RETRIES:
        try:
            if retries > 0:
                print(f"[CLIENT] Timeout! Yeniden Gönderiliyor ({retries}/{MAX_RETRIES}) -> Seq No: {seq_num}")
                log_event("RETRANSMISSION", seq_num, retries)
            else:
                print(f"[CLIENT] Gönderiliyor -> Seq No: {seq_num}")
                log_event("SEND", seq_num, retries)
                
            client_socket.sendto(packet, (SERVER_IP, SERVER_PORT))
            total_sent_bytes += len(packet) # Ağa çıkan her baytı sayıyoruz
            
            data, _ = client_socket.recvfrom(HEADER_SIZE + 100)
            ack_type, ack_seq, _, _, _ = parse_packet(data)
            
            if ack_type == 2 and ack_seq == seq_num:
                print(f"[CLIENT] Başarılı ACK Alındı -> ACK No: {ack_seq}")
                log_event("ACK_RECEIVED", ack_seq, retries)
                return True
                
        except socket.timeout:
            retries += 1
            log_event("TIMEOUT", seq_num, retries)
            
    print(f"[CLIENT] !!! HATA !!! Paket iletilemedi, sınır aşıldı -> Seq No: {seq_num}")
    return False

def send_file(file_path):
    global total_sent_bytes
    total_sent_bytes = 0 
    
    print(f"\n[CLIENT] '{file_path}' transferi başlıyor...")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(TIMEOUT_VALUE)
    
    if not os.path.exists(file_path):
        print(f"[CLIENT] Hata: '{file_path}' bulunamadı.")
        return

    net_dosya_boyutu = os.path.getsize(file_path)
    start_time = time.time()

    file_name = os.path.basename(file_path)
    if not send_packet_reliably(client_socket, pkt_type=3, seq_num=0, payload=file_name.encode('utf-8')):
        return

    seq_num = 1
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            
            success = send_packet_reliably(client_socket, pkt_type=1, seq_num=seq_num, payload=chunk)
            if not success:
                return
                
            seq_num += 1
            
    send_packet_reliably(client_socket, pkt_type=4, seq_num=seq_num)
    end_time = time.time()
    
    # --- PERFORMANS METRİKLERİ HESAPLAMA ---
    toplam_sure = end_time - start_time
    throughput_bps = (total_sent_bytes * 8) / toplam_sure # Bit per second
    goodput_bps = (net_dosya_boyutu * 8) / toplam_sure    # Bit per second
    
    print("\n" + "="*40)
    print(" 🚀 AKTARIM İSTATİSTİKLERİ VE PERFORMANS")
    print("="*40)
    print(f"Toplam Süre       : {toplam_sure:.4f} saniye")
    print(f"Net Dosya Boyutu  : {net_dosya_boyutu} byte")
    print(f"Ağa Basılan Veri  : {total_sent_bytes} byte")
    print(f"Throughput        : {throughput_bps / 1000:.2f} kbps")
    print(f"Goodput           : {goodput_bps / 1000:.2f} kbps")
    print("="*40 + "\n")

    csv_file = "transfer_stats.csv"
    with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Timestamp", "Event", "SeqNum", "RetryCount"])
        writer.writeheader()
        writer.writerows(log_data)

if __name__ == "__main__":
    test_dosyasi = "gercek_test.bin"
    # Tekrar 100 KB'lık dosya üretiyoruz
    with open(test_dosyasi, "wb") as f:
        f.write(os.urandom(1024 * 100)) 
        
    send_file(test_dosyasi)