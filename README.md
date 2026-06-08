# NetProbe: UDP-Based Reliable Data Transfer Protocol

NetProbe is a custom Application Layer protocol designed to bring **100% reliability** to UDP using the **Stop-and-Wait ARQ (Automatic Repeat reQuest)** mechanism. Developed as a computer networking project, it ensures data integrity and ordered delivery in highly lossy network environments, complete with an automated performance logging and analysis suite.

## 🚀 Features

- **Custom Application Layer Header:** A lightweight 12-byte header managing packet types, explicit sequence numbers, payload length, and bit-level error detection.
- **Stop-and-Wait Reliability:** Guarantees loss-free transmission over UDP with connection timeout management and a 5-step retransmission policy (`MAX_RETRIES`).
- **Data Integrity via CRC32:** Validates packet state using a 32-bit Cyclic Redundancy Checksum, automatically discarding corrupted datagrams.
- **Automated Logging:** Tracks every networking event (`SEND`, `ACK`, `TIMEOUT`, `RETRANSMISSION`) with millisecond-precision timestamps exported to CSV.
- **Comparative Analytics:** Built-in Python scripts using `pandas` and `matplotlib` to evaluate protocol behavior under various network anomalies.

---

## 📊 Performance Analysis & Experimental Results

The protocol was rigorously tested in a local loopback environment under three distinct engineering scenarios:

### 1. Influence of Chunk Size
Increasing packet chunk sizes from 512 to 2048 bytes significantly optimizes throughput by maximizing the payload-to-header ratio and minimizing the overall Round-Trip Time (RTT) spent waiting for ACKs.
*Graph location: `reports/deney1_paket_boyutu.png`*

### 2. Resilience to Network Packet Loss
Tested under 0%, 10%, and 20% simulated random packet drop rates. The protocol handles intense packet losses gracefully, dynamically triggering retransmissions without data corruption.
*Graph location: `reports/deney2_kayip_orani.png`*

### 3. Timeout Value Optimization
Analyses on 0.1s, 0.5s, and 1.0s timeouts illustrate the classic networking trade-off: oversized timeout values cause dead-time stalls during packet drops, while overly aggressive windows risk spurious retransmissions in high-RTT wide area networks.
*Graph location: `reports/deney3_timeout_etkisi.png`*

---

## 💻 Installation & Usage

### Prerequisites
Ensure you have Python 3.x installed along with the required data analytics stack:
```bash
pip install pandas matplotlib
```

### Running the Simulation

1. **Start the Receiver (Server):**
   ```bash
   python src/server.py
   ```
2. **Execute the Sender (Client):**
   ```bash
   python src/client.py
   ```
3. **Generate Comparative Metrics:**
   ```bash
   # Run the specific analysis scripts after generating your stats
   python reports/compare_loss.py
   ```

---

## 🎥 Proje Demo Videosu
Projeyi canlı olarak çalıştırdığımız, ideal ve kayıplı ağ senaryolarını test ettiğimiz sunum videomuzu aşağıdan izleyebilirsiniz:

[▶️ NetProbe Uygulamalı Demo Videosunu İzlemek İçin Tıklayın](https://www.youtube.com/watch?v=lVtV2eUXqbs)

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
