import struct
import zlib

# Header formatı: !H I H I (Network byte order: 2B unsigned short, 4B unsigned int, 2B unsigned short, 4B unsigned int)
# Toplam = 12 Byte Başlık
HEADER_FORMAT = "!H I H I"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

def create_packet(pkt_type, seq_num, payload=b""):
    """Veriyi ve başlığı birleştirerek gönderilmeye hazır bir paket (bytes) üretir."""
    payload_len = len(payload)
    # Checksum hesaplama (Şimdilik payload'un CRC32'sini alıyoruz, başlık için de geliştirilecek)
    checksum = zlib.crc32(payload) & 0xffffffff
    
    # Başlığı paketle
    header = struct.pack(HEADER_FORMAT, pkt_type, seq_num, payload_len, checksum)
    return header + payload

def parse_packet(packet_bytes):
    """Gelen ham byte verisini Başlık bileşenlerine ve Payload'a ayırır."""
    if len(packet_bytes) < HEADER_SIZE:
        return None, None, None, None, b""
    
    header_bytes = packet_bytes[:HEADER_SIZE]
    payload = packet_bytes[HEADER_SIZE:]
    
    pkt_type, seq_num, payload_len, checksum = struct.unpack(HEADER_FORMAT, header_bytes)
    return pkt_type, seq_num, payload_len, checksum, payload