# Network Port Scanner CLI v3.0

A fast, stylish, and powerful Command Line Interface (CLI) network port scanner written in Python. This tool features a dynamic RGB gradient ASCII banner, a clean startup screen with a legal disclaimer, and support for Discord Webhooks.

---

## Features

- **RGB Gradient ASCII Banner**: Smooth color transition from deep blue to bright cyan per character.
- **Custom Window and Tab Title**: Automatically sets the title of your Windows Terminal / CMD tab (`PORT-SCANNER v3.0 | BY KYRON`).
- **Interactive Disclaimer**: Integrated startup screen requiring user consent for ethical use.
- **Clean Interface**: Automatically clears the screen after accepting terms for an uncluttered user experience.
- **Multi-threading**: Scans multiple ports concurrently for high-speed execution.
- **Two Scan Modes**:
  - **Quick Scan**: Rapidly scans the most common/well-known network ports.
  - **Custom Range**: Allows custom start and end port selection (1 - 65535).
- **Discord Webhook Reporting**: Sends scan results, including a watermark, directly to a Discord channel.

---

## Requirements

- **Python 3.8** or higher.
- No external `pip` packages required. The script uses Python standard library modules: `socket`, `json`, `urllib`, `concurrent.futures`, `threading`, `sys`, `os`, and `time`.

---

## Installation & Usage

### 1. Download
Download the `portscanner.py` file and place it in your working directory.

### 2. Execution
Open your terminal (Command Prompt, PowerShell, or Windows Terminal) in the project directory and run:

```bash
python portscanner.py
```
How It Works
Accept Terms: Upon startup, a legal disclaimer is displayed. Type y or yes to proceed.

Enter Target: Input the target IP address or hostname (e.g., 127.0.0.1 or example.com).

Select Mode:
Choose 1 for a quick scan of common ports.
Choose 2 to specify a custom port range.

Webhook URL (Optional): Paste a Discord Webhook URL to send the report automatically, or press Enter to skip.

Webhook Payload Format
When open ports are detected and a Webhook URL is provided, the scanner dispatches a formatted Discord Embed:

```JSON
{
  "embeds": [{
    "title": "Port Scan Results",
    "color": 3066993,
    "fields": [
      { "name": "Target Host/IP", "value": "`127.0.0.1`", "inline": true },
      { "name": "Open Ports Found", "value": "`3`", "inline": true },
      { "name": "Details", "value": "• **Port 22**: SSH\n• **Port 80**: HTTP\n• **Port 443**: HTTPS", "inline": false }
    ],
    "footer": {
      "text": "PORT-SCANNER v3.0 | BY KYRON"
    }
  }]
}
```
---
Legal Disclaimer
WARNING: This tool is strictly intended for educational purposes and authorized network audits. Scanning target infrastructure without explicit, prior written permission from the system owner is illegal and unethical. The developer assumes no liability for misuse of this software.
