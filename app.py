import streamlit as st
import pandas as pd
import time
from extractor import get_chrome_history, get_recent_files, get_usb_logs, get_wifi_logs, get_system_metadata  

# UI Neon Styling with Custom Sidebar CSS
st.set_page_config(page_title="Forensic Triage Engine", layout="wide")
custom_css = """
<style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    h1, h2, h3 { color: #00f2fe !important; font-family: 'Courier New', monospace; }
    .stButton>button { background-color: #00f2fe; color: #0d1117; font-weight: bold; border-radius: 5px; box-shadow: 0 0 10px #00f2fe; width: 100%; }
    .stButton>button:hover { background-color: #4facfe; box-shadow: 0 0 20px #4facfe; }
    div[data-testid="stMetricValue"] { color: #00f2fe !important; }
    section[data-testid="stSidebar"] { background-color: #161b22 !important; border-right: 2px solid #00f2fe; }
    button[data-baseweb="tab"] { color: #c9d1d9 !important; font-size: 16px !important; }
    button[aria-selected="true"] { color: #00f2fe !important; border-bottom-color: #00f2fe !important; font-weight: bold !important; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- Left Sidebar: Target Machine Specifications ---
sys_info = get_system_metadata()
with st.sidebar:
    st.markdown("## 💻 TARGET MACHINE METADATA")
    st.markdown("---")
    st.markdown(f"**🖥️ Hostname:** `{sys_info['Hostname']}`")
    st.markdown(f"**💿 OS Platform:** `{sys_info['OS']} {sys_info['OS Release']}`")
    st.markdown(f"**🌐 Local IP:** `{sys_info['Local IP Address']}`")
    st.markdown(f"**⚡ Processor:**\n`{sys_info['Processor']}`")
    st.markdown("---")
    st.info("ℹ️ Metadata is extracted automatically using Python standard libraries for live machine identification.")

# --- Main Dashboard ---
st.title("🛡️ AUTO-FORENSIC TRIAGE ENGINE")
st.subheader("Automated Live System Artifact Acquisition")
st.markdown("---")

col1, col2 = st.columns([3, 1])
with col1:
    target_os = st.selectbox("Select Target OS Partition", ["C:\\ (Current System Local Drive)"])
with col2:
    st.write(" ")
    start_btn = st.button("▶️ START TRIAGE")

# Session State
if "chrome_data" not in st.session_state:
    st.session_state.chrome_data = None
    st.session_state.recent_data = None
    st.session_state.usb_data = None
    st.session_state.wifi_data = None

if start_btn:
    st.write("### ⚙️ Acquisition in Progress...")
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    steps = ["Extracting Chrome...", "Parsing Recent Files...", "Querying USBSTOR...", "Extracting Wi-Fi Profiles..."]
    for i, step in enumerate(steps):
        status_text.text(step)
        progress_bar.progress((i + 1) * 25)
        time.sleep(0.2)
        
    c_df = get_chrome_history()
    r_df = get_recent_files()
    u_df = get_usb_logs()
    w_df = get_wifi_logs()
    
    # Format Chrome
    if isinstance(c_df, pd.DataFrame) and not c_df.empty:
        c_df['Artifact Source'] = 'Chrome History'
        c_df = c_df.rename(columns={'Title': 'Details / Value'})
        st.session_state.chrome_data = c_df[['Timestamp', 'Artifact Source', 'Details / Value', 'Visit Count']]
    else:
        st.session_state.chrome_data = pd.DataFrame(columns=['Timestamp', 'Artifact Source', 'Details / Value', 'Visit Count'])
        
    # Format Others
    st.session_state.recent_data = r_df if isinstance(r_df, pd.DataFrame) else pd.DataFrame(columns=['Timestamp', 'Artifact Source', 'Details / Value', 'Visit Count'])
    st.session_state.usb_data = u_df if isinstance(u_df, pd.DataFrame) else pd.DataFrame(columns=['Timestamp', 'Artifact Source', 'Details / Value', 'Visit Count'])
    st.session_state.wifi_data = w_df if isinstance(w_df, pd.DataFrame) else pd.DataFrame(columns=['Timestamp', 'Artifact Source', 'Details / Value', 'Visit Count'])

    progress_bar.progress(100)
    status_text.text("Triage Completed!")
    st.success("🎉 All Artifacts Separated Successfully!")

# Display Data if Extracted
if st.session_state.chrome_data is not None:
    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(label="🌐 Chrome Links", value=f"{len(st.session_state.chrome_data)} URLs")
    m2.metric(label="📂 Recent Files", value=f"{len(st.session_state.recent_data)} Artifacts")
    m3.metric(label="🔌 USB Devices", value=f"{len(st.session_state.usb_data)} Devices")
    m4.metric(label="🛜 Wi-Fi Networks", value=f"{len(st.session_state.wifi_data)} Networks")
    
    st.markdown("---")
    st.markdown("### 🔍 Category-Wise Forensic Investigation")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🌐 Chrome History", "📂 Recent Files Logs", "🔌 USB Registry Logs", "🛜 Saved Wi-Fi Networks"])
    
    with tab1:
        st.write("#### Chrome Browser History")
        search_c = st.text_input("Filter Chrome Logs:", "", key="search_c")
        df = st.session_state.chrome_data
        if search_c:
            df = df[df['Details / Value'].str.contains(search_c, case=False, na=False)]
        st.dataframe(df, use_container_width=True)
        
    with tab2:
        st.write("#### Recently Accessed Files (.lnk)")
        search_r = st.text_input("Filter Recent Files:", "", key="search_r")
        df = st.session_state.recent_data
        if search_r:
            df = df[df['Details / Value'].str.contains(search_r, case=False, na=False)]
        st.dataframe(df, use_container_width=True)
        
    with tab3:
        st.write("#### Windows Registry USBSTOR Devices")
        search_u = st.text_input("Filter USB Logs:", "", key="search_u")
        df = st.session_state.usb_data
        if search_u:
            df = df[df['Details / Value'].str.contains(search_u, case=False, na=False)]
        st.dataframe(df, use_container_width=True)
        
    with tab4:
        st.write("#### Saved Wireless Network Profiles")
        search_w = st.text_input("Filter Wi-Fi Logs:", "", key="search_w")
        df = st.session_state.wifi_data
        if search_w:
            df = df[df['Details / Value'].str.contains(search_w, case=False, na=False)]
        st.dataframe(df, use_container_width=True)