import streamlit as st
import requests
from inter import speak
Api_url = "http://127.0.0.1:8000/interview-chat"
st.set_page_config(page_title="AI Interview", layout="centered")

# ----------- HEADER -------------
st.markdown("""
    <h1 style="text-align:center; color:#4A90E2;">
        🚀 Welcome to the AI Interview System
    </h1>
    <h3 style="text-align:center; color:gray;">
        Upload your resume to start the interview
    </h3>
""", unsafe_allow_html=True)

# st.write("")
# st.write("")


def go_to(page_name):
    st.session_state["page"] = page_name
    st.rerun()
    
    
def interview_reply():
    response1 = requests.post(Api_url, json = input_data)
    response= response1.json()
    return response


# ------------ CARD CONTAINER -------------
card = st.container()
if "page" not in st.session_state:
    st.session_state["page"] = "home"

if st.session_state["page"] == "home":
    with card:
        st.markdown("""
            <div style="
                background-color:white;
                padding:30px;
                border-radius:15px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                width:60%;
                margin:auto;
            ">
        """, unsafe_allow_html=True)

        # File Upload
        file = st.file_uploader("📄 Upload Your Resume", type=[
                                "pdf", "docx"], label_visibility="visible")

        st.write("")

        # Centered Start Button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            start_btn = st.button("▶️ Start Interview",
                                  use_container_width=True)

        # Validation
        if start_btn:
            try:
                if file:
                    st.success("Your resume has been uploaded successfully!")
                    st.session_state["resume"] = file
                    go_to("frontInter")

                    # redirect to another page
                    # st.switch_page(r"pages\frontInter.py")

                else:
                    st.error("Please upload your resume first!")
            except Exception as e:
                st.error(f"Error: {e}")

        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state["page"] == "frontInter":
    # st.set_page_config(page_title="AI Interview — Listening", layout="centered", initial_sidebar_state="expanded" )

    @st.dialog("Confirm Action")
    def show_popup():
        st.success("Are you sure you want to continue?")
        if st.button("Yes, Continue"):
            st.session_state["confirmed"] = True
            st.rerun()

    st.write("Main Page")
    if st.button("Open Popup"):
        show_popup()
    if "listening" not in st.session_state:
        st.session_state["listening"] = True

    if "mic_active" not in st.session_state:
        st.session_state["mic_active"] = True

    # ------- CSS FOR DOT LOADING ANIMATION -------
    
    
    
    st.markdown(""" 
                <style>
            .stApp {
                background-color: #D3D3D3;
            }

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
    # if st.session_state["listening"]:
    #     dots_class = "loading-dots"
    # else:
    #     dots_class = ""   # no animation

    
    dot_class = "loading-dots" if st.session_state["listening"] else ""
    
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
    mic_class = "mic-pulse" if st.session_state["mic_active"] else ""
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("""
            <img class="mic" 
                src="https://png.pngtree.com/png-vector/20250514/ourmid/pngtree-podcast-mic-png-image_16279107.png" 
                width="180">
        """, unsafe_allow_html=True)

    # ---------- CONTROL BUTTONS ----------
    st.write("")

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.write("### Controls:")

        # if st.button("🛑 Stop Listening"):
        #     st.session_state["listening"] = False
        #     st.session_state["mic_active"] = False
        #     st.rerun()
        
        val=st.text_input("enter Interview ID:")
        

        if st.button("🎙️ Start Listening"):
            # st.session_state["listening"] = True
            # st.session_state["mic_active"] = True
            
            
            input_data={
                "interview_id":val
            }
            
            if not val:
                st.error("enter interviewId")
            else:
            
                try:
                    response=interview_reply(val) 
                    
                    if response.status_code==200:
                        st.write(response)
                except requests.exceptions.ConnectionError:
                    st.info("can you tell again")
            st.rerun()
                    
                

    # ----------- RIGHT SIDEBAR ------------
    st.sidebar.markdown("""
        <h2 style="color:#4A90E2;">💬 Interview Chat</h2>
        <hr>
        <p style="color:gray;">Your conversation will appear here.</p>
    """, unsafe_allow_html=True)
    st.sidebar.write(interview_reply() )
    speak(response)
