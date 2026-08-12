 Network Port Scanner v3.0

A high-performance, multi-threaded TCP port scanner and network audit utility built with Python. Featuring an intuitive dark-themed Graphical User Interface (GUI), flexible profiling modes, non-blocking socket probes, and automated HTTP/Discord Webhook result dispatching.

---

## Key Features

- **Asynchronous Multithreading:** Utilizes Python's `concurrent.futures.ThreadPoolExecutor` to manage worker threads efficiently. Scans hundreds of ports simultaneously without freezing or locking the user interface.
- **Dual Scanning Profiles:**
  - **Quick Scan:** Probes a curated list of top well-known service ports (HTTP, HTTPS, SSH, MySQL, RDP, SMB, etc.).
  - **Custom Range:** Fully customizable port range scan supporting any spectrum from port 1 to 65535.
- **Real-Time Execution Control:** Safely abort active scans at any point during execution with worker cancellation flags.
- **Automated Webhook Integration:** Delivers clean, structured JSON payloads (formatted as rich Discord embeds) containing scan summaries upon completion.
- **Thread-Safe Logging:** Built with explicit thread locking (`threading.Lock`) to ensure result arrays and console outputs remain clean without data corruption or race conditions.
- **Zero External Dependencies:** Built entirely using Python's Native Standard Library (`socket`, `tkinter`, `concurrent.futures`, `json`, `urllib`). No `pip install` required.

---

## Architecture & Technical Design

The application separates UI management, scan thread execution, and background worker logic to maintain smooth GUI performance during intensive network I/O.

### Execution Flow

1. **User Input & Validation:** Target hostname or IPv4 address and scan preferences are collected and validated.
2. **DNS Resolution:** Hostname is resolved to an IP address using `socket.gethostbyname()`.
3. **Thread Dispatch:** The main thread spawns a background worker thread, which initializes a `ThreadPoolExecutor` (up to 50 concurrent workers).
4. **Non-blocking TCP Probes:** Workers perform full 3-way TCP handshakes (`socket.SOCK_STREAM`) with a 1.0-second connection timeout (`connect_ex`).
5. **Thread-Safe Result Aggregation:** Open ports are registered safely using mutex locks (`threading.Lock`).
6. **Webhook Dispatch:** If enabled, an asynchronous HTTP POST request sends formatted scan results via `urllib.request`.

---

## Monitored Common Ports (Quick Scan Mode)

When executing a **Quick Scan**, the scanner focuses on high-priority network services including:

| Port | Service | Protocol / Description |
| :--- | :--- | :--- |
| **21** | FTP | File Transfer Protocol |
| **22** | SSH | Secure Shell / SFTP |
| **23** | Telnet | Unencrypted Text Communications |
| **25** | SMTP | Simple Mail Transfer Protocol |
| **53** | DNS | Domain Name System |
| **80** | HTTP | Hypertext Transfer Protocol |
| **110** | POP3 | Post Office Protocol v3 |
| **135** | RPC | Microsoft EPMAP / RPC |
| **139** | NetBIOS | NetBIOS Session Service |
| **143** | IMAP | Internet Message Access Protocol |
| **443** | HTTPS | Encrypted Web Traffic (SSL/TLS) |
| **445** | SMB | Server Message Block (File Sharing) |
| **1433** | MSSQL | Microsoft SQL Server |
| **1521** | Oracle | Oracle Database Listener |
| **3306** | MySQL | MySQL / MariaDB Database |
| **3389** | RDP | Remote Desktop Protocol |
| **5432** | PostgreSQL| PostgreSQL Database |
| **5900** | VNC | Virtual Network Computing |
| **6379** | Redis | In-memory Data Structure Store |
| **8080** | HTTP-Proxy| Alternative Web Server / Proxy |
| **8443** | HTTPS-Alt | Alternative Secure Web Server |
| **27017**| MongoDB | NoSQL Database System |

---

## Installation & Prerequisites

### Prerequisites

- **Python 3.8** or higher installed on your operating system.
- Compatible with **Windows**, **macOS**, and **Linux**.

### Installation Steps

1. Clone the repository to your local machine:
   ```bash
   git clone [https://github.com/your-username/network-port-scanner.git](https://github.com/your-username/network-port-scanner.git)
   cd network-port-scanner
   
Run the application: Bash python main.py
Note for Linux Users (Ubuntu/Debian/Kali):If your system Python installation lacks tkinter, install it via your package manager:Bashsudo apt update && sudo apt install python3-tk

---

## Application ConfigurationFieldTypeRequiredDescriptionTarget Host / IPTextYesTarget IPv4 address (e.g., 127.0.0.1) or Domain (e.g., scanme.nmap.org).
## Scan ModeSelectionYesChoose between Quick Scan (Top 50 ports) or Custom Range.
## Port RangeNumericOptional*Start and End port numbers (1 - 65535). 
## Only active in Custom Mode.Webhook URLTextOptionalDiscord or HTTP Webhook URL for posting automated scan reports.

---

# Webhook Payload Format

When open ports are discovered and a valid Webhook URL is supplied, the utility sends an HTTP POST request formatted as a Discord Embed:

```json
{
  "embeds": [
    {
      "title": "Port Scan Summary",
      "color": 3066993,
      "fields": [
        {
          "name": "Target",
          "value": "`127.0.0.1`",
          "inline": true
        },
        {
          "name": "Open Ports Found",
          "value": "`3`",
          "inline": true
        },
        {
          "name": "Details",
          "value": "• **Port 22**: SSH\n• **Port 80**: HTTP\n• **Port 443**: HTTPS",
          "inline": false
        }
      ]
    }
  ]
}

Contributing
Contributions are welcome! If you want to enhance this tool:

Fork the Project Repository.

Create your Feature Branch (git checkout -b feature/NewFeature).

Commit your Changes (git commit -m 'Add NewFeature').

Push to the Branch (git push origin feature/NewFeature).

Open a Pull Request.

Legal & Ethical Disclaimer
This tool is designed strictly for educational purposes, authorized administrative auditing, and network security testing. Scanning target infrastructure without explicit, prior written authorization from the system owner is illegal and unethical. The authors assume no liability and are not responsible for any misuse or damage caused by this software.
