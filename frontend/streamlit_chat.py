import streamlit as st
import requests

st.set_page_config(page_title="Titan AI Chat", layout="wide")
st.title("Amazon Titan AI Assistant")

# Display current token for debug (remove in prod)
#st.sidebar.title("Session Info")
#st.sidebar.write("Current token:", st.session_state.get("token", "None"))

# --- AUTHENTICATION FLOW ---
if "token" not in st.session_state or not st.session_state.get("logged_in", False):
    auth_mode = st.radio("Choose action", ["Login", "Signup"], key="auth_mode")

    if auth_mode == "Signup":
        with st.form("signup"):
            st.subheader("Sign Up")
            new_username = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")
            signup_submitted = st.form_submit_button("Create Account")
            if signup_submitted:
                res = requests.post(
                    "http://localhost:8000/signup",
                    data={"username": new_username, "password": new_password},
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                if res.status_code == 200:
                    st.success("Account created! You can now log in.")
                else:
                    st.error(res.json().get("detail", "Signup failed"))

    else:  # Login
        with st.form("login"):
            st.subheader("🔐 Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                res = requests.post(
                    "http://localhost:8000/login",
                    data={"username": username, "password": password}
                )
                if res.status_code == 200:
                    st.session_state.token = res.json()["access_token"]
                    st.session_state.logged_in = True
                    st.success("Logged in!")
                else:
                    st.error("Login failed")

# --- MAIN APP FLOW ---
elif "token" in st.session_state and st.session_state.get("logged_in"):
    tab1, tab2 = st.tabs(["Chat", "Monitor"])

    with tab1:
        prompt = st.text_input("Enter your prompt:")
        if st.button("Send") and prompt:
            res = requests.post(
                "http://localhost:8000/chat",
                headers={"Authorization": f"Bearer {st.session_state.token}"},
                data={"prompt": prompt}
            )
            if res.status_code == 200:
                st.success(res.json()["response"])
            else:
                st.error(f"Error {res.status_code}: {res.text}")

    with tab2:
        st.subheader("Monitoring Metrics")
        res = requests.get("http://localhost:8000/metrics")
        if res.status_code == 200:
            data = res.json()
            st.metric("Model", data["model"])
            st.metric("Last Latency (s)", data["last_latency_sec"])
            st.metric("Total Requests", data["requests"])
        else:
            st.error("Could not fetch monitoring data")

    st.sidebar.title("User Guide")
    st.sidebar.markdown("""
    ### What this app does:
    - Secure login and signup
    - Connects to Amazon Bedrock (Titan)
    - Lets you send prompts and view model responses
    - Tracks usage (total requests, last latency)

    ### How to use:
    1. Sign up or log in
    2. Go to Chat tab to send queries
    3. Check Monitor tab to view usage stats
    """)
else:
    st.error("Something went wrong with session state. Please reload the app.")
