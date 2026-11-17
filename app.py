import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from pathlib import Path

st.set_page_config(page_title="Domino's | Infrastructure Command", page_icon="🍕", layout="wide")

RED = "#E31837"
DARK = "#111827"
MUTED = "#94A3B8"
GREEN = "#16A34A"
ORANGE = "#F59E0B"
PURPLE = "#9333EA"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: Inter, sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #080e1b, #111c30);
    color: #e5e7eb;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #101827, #17243a);
    border-right: 1px solid #34445f;
}

section[data-testid="stSidebar"] * {
    color: #e5e7eb;
}

.block-container {
    padding-top: 1.4rem;
    max-width: 1600px;
}

.hero {
    background: linear-gradient(115deg, #111827, #263b5a, #111827);
    border: 1px solid #3b5275;
    padding: 28px;
    border-radius: 20px;
    margin-bottom: 20px;
    box-shadow: 0 8px 30px #0005;
}

.hero h1 {
    font-size: 29px;
    color: white;
    font-weight: 800;
    letter-spacing: -.7px;
}

.hero p {
    color: #b8c9e2;
    font-size: 13px;
}

.kpi {
    background: linear-gradient(145deg, #1b2a40, #111c2e);
    border: 1px solid #34445f;
    border-left: 5px solid #E31837;
    border-radius: 16px;
    padding: 19px;
    min-height: 115px;
    box-shadow: 0 5px 18px #0003;
    transition: .2s ease;
}

div[data-testid="column"]:nth-child(1) .kpi {
    border-left-color: #E31837;
}
div[data-testid="column"]:nth-child(2) .kpi {
    border-left-color: #16A34A;
}
div[data-testid="column"]:nth-child(3) .kpi {
    border-left-color: #F59E0B;
}
div[data-testid="column"]:nth-child(4) .kpi {
    border-left-color: #9333EA;
}

.kpi-label {
    font-size: 11px;
    color: #b8c9e2;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 700;
}

.kpi-value {
    font-size: 32px;
    color: white;
    font-weight: 800;
    margin-top: 8px;
}

.kpi-sub {
    font-size: 11px;
    color: #9eb0ca;
    margin-top: 3px;
}

.panel {
    background: linear-gradient(145deg, #18263b, #111c2e);
    border: 1px solid #34445f;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 5px 18px #0003;
}

.panel-title {
    font-size: 15px;
    color: white;
    font-weight: 800;
    margin-bottom: 12px;
}

.small-muted {
    font-size: 12px;
    color: #a4b5cc;
}

.branch-card {
    background: linear-gradient(120deg, #1b2a40, #111c2e);
    border: 1px solid #34445f;
    border-left: 4px solid #2563EB;
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 10px;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #34445f;
    border-radius: 13px;
}

.stButton>button {
    border-radius: 10px;
    font-weight: 700;
    border: 1px solid #E31837;
    transition: .2s ease;
}

.stButton>button:hover {
    background: #E31837;
    color: white;
}

div[data-testid="stMetric"] {
    background: #18263b;
    border: 1px solid #34445f;
    padding: 15px;
    border-radius: 14px;
}

hr {
    border-color: #34445f;
}
header[data-testid="stHeader"] {
    background: #111827 !important;
    height: 75px;
    position: relative;
    border-bottom: 2px solid #E31837;
}

header[data-testid="stHeader"] [data-testid="stToolbar"] {
    visibility: hidden;
}

header[data-testid="stHeader"]::after {
    content: "SERVER MONITORING CENTER";
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    color: white;
    font-size: 25px;
    font-weight: 800;
    letter-spacing: 2px;
    white-space: nowrap;
}
</style>
""", unsafe_allow_html=True)

def starter_data():
    # 82 editable starter rows. Replace names/IPs using the branch master CSV.
    rows=[]
    for i in range(1,83):
        rows.append({
            "Branch ID": f"BR-{i:03d}",
            "Branch Name": f"Branch {i:02d} — Update Name",
            "City": "Karachi" if i<=35 else ("Lahore" if i<=55 else "Other"),
            "Host-1 IP": "",
            "Host-2 IP": "",
            "Host-1 Status": "Unknown",
            "Host-2 Status": "Unknown",
            "CPU %": None,
            "RAM %": None,
            "Disk Health": "Not Connected",
            "Uptime": "—",
            "Last Check": "Not connected"
        })
    return pd.DataFrame(rows)

if "branches" not in st.session_state:
    st.session_state.branches = starter_data()
if "events" not in st.session_state:
    st.session_state.events = pd.DataFrame([
        {"Time": datetime.now().strftime("%Y-%m-%d %H:%M"), "Severity":"INFO", "Branch":"Head Office", "Event":"Command Center demo initialized"}
    ])
if "restart_requests" not in st.session_state:
    st.session_state.restart_requests = []

df=st.session_state.branches.copy()
st.sidebar.markdown("## 🍕 DOMINO'S")
st.sidebar.image("innovation_garage.jpg", use_container_width=True)
st.sidebar.caption("IT OPERATIONS • COMMAND CENTER")
page=st.sidebar.radio("NAVIGATION", ["Executive Overview","Branch Monitoring","Server Intelligence","Event Center","Data Management","Deployment Guide"])
st.sidebar.markdown("---")
st.sidebar.markdown("**System mode**")
st.sidebar.warning("DEMO MODE — No live server connection")
st.sidebar.caption("Python • Streamlit • Secure integration required")

st.markdown(f"""
<div class="hero">
  <div style="display:flex;justify-content:space-between;align-items:center;gap:15px;flex-wrap:wrap">
    <div><h1>INFRASTRUCTURE COMMAND CENTER</h1>
    <p>Centralized visibility for branch servers • Host-1 / Host-2 • Pakistan Operations</p></div>
    <div style="text-align:right"><div style="color:#fff;font-weight:800;letter-spacing:1px">DOMINO'S</div>
    <div class="small-muted">IT OPERATIONS CONTROL</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

total=len(df)
online=((df["Host-1 Status"]=="Online") | (df["Host-2 Status"]=="Online")).sum()
offline=((df["Host-1 Status"]=="Offline") & (df["Host-2 Status"]=="Offline")).sum()
unknown=total-online-offline
alerts=len(st.session_state.events[st.session_state.events["Severity"].isin(["CRITICAL","WARNING"])]) if len(st.session_state.events) else 0

if page=="Executive Overview":
    cols=st.columns(4)
    metrics=[("TOTAL BRANCHES",total,"Configured branch records"),("ONLINE BRANCHES",int(online),"At least one host online"),("OFFLINE BRANCHES",int(offline),"Both hosts reported offline"),("ACTIVE ALERTS",int(alerts),"Warning / critical events")]
    for c,(label,val,sub) in zip(cols,metrics):
        c.markdown(f'<div class="kpi"><div class="kpi-label">{label}</div><div class="kpi-value">{val:02d}</div><div class="kpi-sub">{sub}</div></div>',unsafe_allow_html=True)
    st.write("")
    left,right=st.columns([1.35,1])
    with left:
        st.markdown('<div class="panel"><div class="panel-title">Branch fleet status</div>',unsafe_allow_html=True)
        status_counts=pd.DataFrame({"Status":["Online","Offline","Unknown"],"Branches":[int(online),int(offline),int(unknown)]})
        fig=px.bar(status_counts,x="Status",y="Branches",color="Status",text="Branches",color_discrete_map={"Online":"#22c55e","Offline":RED,"Unknown":"#64748b"})
        fig.update_layout(template="plotly_dark",paper_bgcolor="#131e2e",plot_bgcolor="#131e2e",height=280,showlegend=False,margin=dict(l=10,r=10,t=10,b=10),xaxis_title="",yaxis_title="Branches")
        st.plotly_chart(fig,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel"><div class="panel-title">Operational readiness</div>',unsafe_allow_html=True)
        st.markdown(f"""
        <p class="small-muted">Branch records loaded</p><h2 style="margin:0;color:white">{total} / 82</h2>
        <hr><p class="small-muted">Live telemetry</p><h3 style="margin:0;color:#fbbf24">Not connected</h3>
        <hr><p class="small-muted">Remote restart capability</p><h3 style="margin:0;color:#fbbf24">Approval workflow only</h3>
        """,unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)
    st.write("")
    st.markdown("### Latest operational events")
    st.dataframe(st.session_state.events.sort_values("Time",ascending=False),use_container_width=True,hide_index=True)
    st.info("This is a working dashboard prototype. Metrics remain blank until approved monitoring agents and a secure backend are connected.")

elif page=="Branch Monitoring":
    st.markdown("### Branch Monitoring")
    c1,c2,c3=st.columns([2,1,1])
    search=c1.text_input("Search branch / ID / city",placeholder="e.g. Karachi, BR-001")
    host_filter=c2.selectbox("Host status",["All","Online","Offline","Unknown"])
    city_filter=c3.selectbox("City",["All"]+sorted([x for x in df["City"].dropna().unique()]))
    view=df.copy()
    if search:
        view=view[view.astype(str).apply(lambda col: col.str.contains(search,case=False,na=False)).any(axis=1)]
    if host_filter!="All":
        view=view[(view["Host-1 Status"]==host_filter)|(view["Host-2 Status"]==host_filter)]
    if city_filter!="All": view=view[view["City"]==city_filter]
    st.caption(f"Showing {len(view)} of {total} branch records")
    st.dataframe(view,use_container_width=True,hide_index=True,height=520)
    st.download_button("⬇ Download branch inventory CSV",view.to_csv(index=False).encode("utf-8"),"dominos_branch_inventory.csv","text/csv")

elif page=="Server Intelligence":
    st.markdown("### Server Intelligence")
    st.warning("CPU, RAM, disk health and uptime are placeholders until live agents report telemetry.")
    selected=st.selectbox("Select branch",df["Branch Name"].tolist())
    row=df[df["Branch Name"]==selected].iloc[0]
    st.markdown(f"#### {row['Branch ID']} • {row['Branch Name']}")
    a,b=st.columns(2)
    for col,host in [(a,"Host-1"),(b,"Host-2")]:
        with col:
            st.markdown(f'<div class="panel"><div class="panel-title">{host}</div>',unsafe_allow_html=True)
            st.write("**IP address:**",row[f"{host} IP"] or "Not configured")
            st.write("**Status:**",row[f"{host} Status"])
            st.write("**CPU:**", "—" if pd.isna(row["CPU %"]) else f"{row['CPU %']}%")
            st.write("**RAM:**", "—" if pd.isna(row["RAM %"]) else f"{row['RAM %']}%")
            st.write("**Disk health:**",row["Disk Health"])
            st.write("**Uptime:**",row["Uptime"])
            st.markdown('</div>',unsafe_allow_html=True)
    st.markdown("#### Controlled restart request")
    st.caption("A restart request is logged for administrator approval. This demo does not send a command to any server.")
    host_choice=st.selectbox("Target host",["Host-1","Host-2"],key="restart_host")
    reason=st.text_input("Reason for restart",placeholder="Enter approved maintenance reason")
    confirm=st.checkbox("I confirm this request requires authorization and may interrupt branch operations")
    if st.button("Submit restart request",type="primary",disabled=not(reason.strip() and confirm)):
        item={"Time":datetime.now().strftime("%Y-%m-%d %H:%M"),"Branch":selected,"Host":host_choice,"Reason":reason,"Status":"Pending approval"}
        st.session_state.restart_requests.append(item)
        st.session_state.events.loc[len(st.session_state.events)]={"Time":item["Time"],"Severity":"WARNING","Branch":selected,"Event":f"{host_choice} restart request submitted — pending approval"}
        st.success("Request recorded in this demo. No server was restarted.")
    if st.session_state.restart_requests:
        st.markdown("#### Restart request queue")
        st.dataframe(pd.DataFrame(st.session_state.restart_requests),use_container_width=True,hide_index=True)

elif page=="Event Center":
    st.markdown("### Event Center")
    if len(st.session_state.events)==0: st.info("No events recorded.")
    else: st.dataframe(st.session_state.events.sort_values("Time",ascending=False),use_container_width=True,hide_index=True)
    st.markdown("### Add a test event")
    with st.form("event_form"):
        branch=st.selectbox("Branch",["Head Office"]+df["Branch Name"].tolist())
        severity=st.selectbox("Severity",["INFO","WARNING","CRITICAL"])
        message=st.text_input("Event description")
        submitted=st.form_submit_button("Add event")
        if submitted and message.strip():
            st.session_state.events.loc[len(st.session_state.events)]={"Time":datetime.now().strftime("%Y-%m-%d %H:%M"),"Severity":severity,"Branch":branch,"Event":message}
            st.success("Event added.")

elif page=="Data Management":
    st.markdown("### Branch Data Management")
    st.write("Upload your verified branch master CSV to replace the 82 starter records.")
    st.download_button("⬇ Download CSV template",df.to_csv(index=False).encode("utf-8"),"dominos_82_branch_template.csv","text/csv")
    uploaded=st.file_uploader("Upload branch inventory CSV",type=["csv"])
    if uploaded:
        try:
            incoming=pd.read_csv(uploaded)
            required=["Branch ID","Branch Name","City","Host-1 IP","Host-2 IP","Host-1 Status","Host-2 Status","CPU %","RAM %","Disk Health","Uptime","Last Check"]
            missing=[x for x in required if x not in incoming.columns]
            if missing: st.error("Missing columns: "+", ".join(missing))
            else:
                st.dataframe(incoming.head(10),use_container_width=True)
                if st.button("Confirm and load uploaded inventory",type="primary"):
                    st.session_state.branches=incoming
                    st.success(f"Loaded {len(incoming)} branch records.")
                    st.rerun()
        except Exception as e: st.error(f"Could not read CSV: {e}")
    st.markdown("#### Current inventory")
    st.dataframe(df,use_container_width=True,hide_index=True,height=350)

elif page=="Deployment Guide":
    st.markdown("### From demo to live monitoring")
    st.warning("Do not expose server restart controls directly to users. Use authentication, role permissions, approval, and audit logs.")
    steps=[
        ("1. Host the dashboard","Install Python on a Head Office Windows Server or approved VM. Run behind IIS reverse proxy or an approved internal web gateway."),
        ("2. Create the backend","Use FastAPI or .NET API with SQL Server to store branch inventory, telemetry, alerts, users and audit records."),
        ("3. Install branch agents","Deploy a signed Windows service on each authorized Host-1 / Host-2 server to send CPU, RAM, disk SMART and uptime metrics over outbound HTTPS."),
        ("4. Secure connectivity","Use VPN / firewall allow-listing, TLS certificates, service credentials, least privilege and MFA for administrators."),
        ("5. Enable restart safely","Use a restricted service account and a queued approval workflow. Log requester, approver, target, reason, timestamp and result."),
        ("6. Pilot before rollout","Test on one non-critical branch, validate telemetry and recovery, then expand in controlled batches.")
    ]
    for title,desc in steps:
        st.markdown(f'<div class="branch-card"><b style="color:white">{title}</b><div class="small-muted" style="margin-top:6px">{desc}</div></div>',unsafe_allow_html=True)
    st.markdown("#### Suggested stack")
    st.code("Frontend: Streamlit (prototype) / React (production UI)\nBackend: Python FastAPI\nDatabase: Microsoft SQL Server\nAgent: Windows Service (PowerShell / Python packaged service)\nHosting: Head Office Windows Server + IIS / internal reverse proxy\nSecurity: VPN + TLS + MFA + RBAC + audit logs",language="text")
st.markdown("---")
st.markdown("""
<div style="text-align:center; padding:15px;">
    <div style="color:#E31837; font-size:17px; font-weight:800;">
        DOMINO'S IT OPERATIONS
    </div>
    <div style="color:#94A3B8; font-size:13px; margin-top:6px;">
        Designed & Developed by <b style="color:white;">Muhammad Junaid Luqman</b>
    </div>
    <div style="color:#64748B; font-size:11px; margin-top:5px;">
        Infrastructure Command Center
    </div>
</div>
""", unsafe_allow_html=True)

