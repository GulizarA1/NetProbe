# -*- coding: utf-8 -*-
import socket
import zlib
import random
from packet import parse_packet, create_packet, HEADER_SIZE

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5005
BUFFER_SIZE = 4096
LOSS_RATE = 0.0  # GERÇEK TEST İÇİN KAYBI ŞİMDİLİK %0 YAPTIK (0.0)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    
    print(f"[SERVER] Başlatıldı. {SERVER_IP}:{SERVER_PORT} dinleniyor...")
    
    received_chunks = {}
    dosya_adi = "bilinmeyen_dosya.bin" # Varsayılan isim
    
    while True:
        data, client_address = server_socket.recvfrom(BUFFER_SIZE)
        
        if random.random() < LOSS_RATE:
            continue
            
        pkt_type, seq_num, payload_len, checksum, payload = parse_packet(data)
        
        if pkt_type is None:
            continue
            
        calc_checksum = zlib.crc32(payload) & 0xffffffff
        if calc_checksum != checksum:
            continue 
            
        if pkt_type == 3:
            # Dosyanın orijinal adını yakalıyoruz
            orijinal_isim = payload.decode('utf-8')
            dosya_adi = f"kopya_{orijinal_isim}"
            print(f"[SERVER] Transfer İsteği -> Dosya: {orijinal_isim}")
            
            ack_pkt = create_packet(pkt_type=2, seq_num=seq_num)
            server_socket.sendto(ack_pkt, client_address)
            
        elif pkt_type == 1:
            if seq_num not in received_chunks:
                received_chunks[seq_num] = payload
            
            ack_pkt = create_packet(pkt_type=2, seq_num=seq_num)
            server_socket.sendto(ack_pkt, client_address)
            
        elif pkt_type == 4:
            print("[SERVER] FIN paketi alındı. Dosya birleştiriliyor...")
            ack_pkt = create_packet(pkt_type=2, seq_num=seq_num)
            server_socket.sendto(ack_pkt, client_address)
            
            # Yakaladığımız orijinal dosya adıyla kaydediyoruz
            with open(dosya_adi, "wb") as f:
                for s in sorted(received_chunks.keys()):
                    f.write(received_chunks[s])
            print(f"[SERVER] İşlem Tamam! Dosya kaydedildi: {dosya_adi}\n")
            received_chunks.clear()

if __name__ == "__main__":
    start_server()