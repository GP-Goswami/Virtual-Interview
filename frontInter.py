import streamlit as st

st.session_state["page"] == "frotInter"
st.set_page_config(page_title="AI Interview — Listening", layout="centered", initial_sidebar_state="expanded" )

# ------- CSS FOR DOT LOADING ANIMATION -------
st.markdown("""
            <style>
        .stApp {
            background-color: #D3D3D3;
        }
    </style>
    <style>

    /* Blinking dot animation */
    .loading-dots::after {
        content: '';
        animation: dots 1.5s infinite steps(1);
    }

    @keyframes dots {
        0%   { content: ''; }
        20%  { content: '.'; }
        40%  { content: '..'; }
        60%  { content: '...'; }
        80%  { content: '..'; }
        100% { content: '.'; }
    }

    /* Mic pulse animation */
    .mic {
        animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(1); opacity: 0.9; }
        50% { transform: scale(1.12); opacity: 1; }
        100% { transform: scale(1); opacity: 0.9; }
    }

    /* Move sidebar to right */
    [data-testid="stSidebar"] {
        left: auto;
        right: 0;
        border-left: 2px solid #eee;
        border-right: none;
    }

    </style>
""", unsafe_allow_html=True)


# ----------- LISTENING TEXT WITH DOT ANIMATION ----------
st.markdown("""
    <h1 style="text-align:center; color:#ED3B3B;">
        Listening<span class="loading-dots"></span>
    </h1>
""", unsafe_allow_html=True)

st.markdown(
    "<h4 style='text-align:center; color:gray;'>Speak now, I am capturing your voice.</h4>",
    unsafe_allow_html=True
)

st.write("")
st.write("")

# ----------- MIC IMAGE WITH PULSE ----------
col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.markdown("""
        <img class="mic" 
             src="https://png.pngtree.com/png-vector/20250514/ourmid/pngtree-podcast-mic-png-image_16279107.png" 
             width="180">
    """, unsafe_allow_html=True)

# ----------- RIGHT SIDEBAR ------------
st.sidebar.markdown("""
    <h2 style="color:#4A90E2;">💬 Interview Chat</h2>
    <hr>
    <p style="color:gray;">Your conversation will appear here.</p>
""", unsafe_allow_html=True)

