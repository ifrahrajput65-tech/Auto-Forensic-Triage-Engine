🛡️ Auto-Forensic Triage Engine

An automated, lightweight **Live Forensic Triage & Incident Response Tool** built using Python and Streamlit. This application allows security analysts and forensic investigators to acquire critical system artifacts and volatile/non-volatile evidence from a live Windows machine in seconds, bypassing the need for heavy, complex third-party installations.

🎯 Key Features

* **💻 Target Machine Metadata:** Automatically gathers live machine identification metrics (Hostname, OS Platform, Local IP Address, and Processor specifications) using Python standard libraries.
* **🌐 Browser History Parser:** Extracts and parses the top 50 SQLite history entries from Google Chrome.
* **📂 Recent Files Activity:** Identifies and structures recently accessed user documents and files (`.lnk` logs).
* **🛜 Saved Wi-Fi Networks:** Queries the Windows Shell to list wireless profile network SSIDs previously connected to the device.
* **🔌 USBSTOR Registry Analysis:** Extracts historical records of connected USB mass storage devices directly from the Windows Registry (`SYSTEM\CurrentControlSet\Enum\USBSTOR`).
* **🔍 Dynamic Evidence Filter:** Integrated live search box for instant keyword filtering of collected artifacts.

---

🛠️ Installation & Setup

Follow these simple steps to run the Forensic Triage Engine locally:

1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/Auto-Forensic-Triage-Engine.git
cd Auto-Forensic-Triage-Engine
```

 2. Install Dependencies
Ensure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### 3. Run the Tool
Launch the interactive Streamlit dashboard:
```bash
streamlit run app.py
```

 📁 Project Structure

```text
├── app.py             # Streamlit Interactive UI (Neon Themed)
├── extractor.py       # Core Forensic Logic (Parser & Registry Queries)
├── requirements.txt   # Required Python Modules
└── LICENSE            # MIT License
```

⚖️ License

Distributed under the **MIT License**. See `LICENSE` for more information.


*Developed for educational and digital forensic investigation purposes.