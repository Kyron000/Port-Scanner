# Port Scanner | Profesional

A high-performance, multi-threaded TCP port scanner with a graphical interface (GUI) and real-time Webhook logging. Built entirely in Python using native libraries.

---

## Technical Overview

The application utilizes non-blocking socket probes and concurrent thread execution to analyze network endpoints efficiently. By leveraging Python's `concurrent.futures` module, the program can audit hundreds of target ports simultaneously while keeping the user interface completely responsive.

## Key Features

- **Asynchronous Execution:** Uses `ThreadPoolExecutor` (100 parallel workers) for rapid network probing.
- **Responsive Interface:** Dark-mode UI built with `tkinter.ttk` that remains functional during active scans.
- **Real-Time Cancellation:** Allows immediate termination of active scanning operations via thread state flags.
- **Structured Webhook Logging:** Generates JSON payloads (formatted for Discord/Slack embeds) containing scan summaries upon completion.
- **Zero External Dependencies:** Relies strictly on Python's standard library. No `pip install` required.

---

## Network & Protocol Details

### 1. Host Resolution
Before initiating port checks, the target host string is resolved to an IPv4 address using `socket.gethostbyname()`.

### 2. TCP Handshake Probing
The scanner uses full TCP connect probes (`socket.SOCK_STREAM`):
- For each target port, an OS-level 3-way TCP handshake ($SYN \rightarrow SYN-ACK \rightarrow ACK$) is attempted.
- A connection timeout is set to **0.6 seconds** via `socket.settimeout(0.6)`.
- The `connect_ex()` method returns `0` if the connection succeeds (Port Open), or an error code if filtered/closed.

### 3. Concurrency Control
Rather than launching unlimited system threads, the scanner caps execution at 100 concurrent workers. This balances speed while preventing socket starvation or local OS resource limits.

---

## Installation & Execution

### System Requirements

- **Python:** Version 3.8 or higher.
- **OS:** Windows, macOS, or Linux.

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/network-port-scanner.git](https://github.com/your-username/network-port-scanner.git)
   cd network-port-scanner
   
Run the script:Bashpython main.py
Note for Linux Distributions (Ubuntu/Debian/Kali):If your Python environment lacks tkinter, install it via your package manager:Bashsudo apt update && sudo apt install python3-tk

Application Layout & SettingsParameterTypeDescriptionTarget Host / IPStringDomain name (e.g., example.com) or IPv4 address (127.0.0.1).Start PortIntegerBeginning of port range ($1 - 65535$).End PortIntegerEnd of port range ($1 - 65535$).Webhook URLStringOptional HTTP/Discord Webhook endpoint for result transmission.Webhook Output StructureWhen a Webhook URL is provided and open ports are discovered, an HTTP POST request is dispatched with the following payload format:

JSON{
  "embeds": [
    {
      "title": "Port Scan Results",
      "color": 3066993,
      "fields": [
        {
          "name": "Target",
          "value": "`127.0.0.1`",
          "inline": true
        },
        {
          "name": "Open Ports",
          "value": "`22, 80, 443`",
          "inline": false
        }
      ]
    }
  ]
}

**DisclaimerThis software is developed strictly for educational purposes, authorized security assessments, and network troubleshooting. Scanning target networks without prior explicit authorization from the infrastructure owner is illegal and unauthorized.**
