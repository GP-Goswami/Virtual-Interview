import streamlit as st
import requests
# from inter import speak
import base64
from database import checkId
from config import retriveid
import time

endpoints=["user-input", "model-output", "interviewId","speakAns"]
Api_url = "http://127.0.0.1:8000/"

# ----------- HEADER -------------

def user_input():
    api= Api_url + endpoints[0]
    speech = requests.get(api)
    return speech

def interview_reply( inter_reply, resume):
    api=Api_url + endpoints[1]
    print(api)
    
    resume_content = resume.read()
    resume_base64 = base64.b64encode(resume_content).decode("utf-8")
    # "interview_id" : inter_id,
    input_data={
        
        "inter_reply" : inter_reply,
        "resume" : resume_base64
    }
    ai_reply = requests.post(api, json = input_data)
    # response= response1.json()
    return ai_reply

def animation():
    st.markdown("""
            <h1 style="text-align:center; color:#ED3B3B;">
                Listening<span class="loading-dots"></span>
            </h1>
        """, unsafe_allow_html=True)

    st.markdown(
        "<h4 style='text-align:center; color:gray;'>Speak now, I am capturing your voice.</h4>",
        unsafe_allow_html=True
    )
    st.markdown("""
        <img class="mic" 
            src="https://png.pngtree.com/png-vector/20250514/ourmid/pngtree-podcast-mic-png-image_16279107.png" 
            width="180">
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    st.write("")
    st.write("")

def getInter():
    return requests.get(Api_url + endpoints[2])

def speak(reply):
    api=Api_url + endpoints[3]
    print(api)
    
    input_data={
        
        "interviewerReply" : reply,
    }
    
    ai_reply = requests.post(api, json = input_data)
    # response= response1.json()
    return ai_reply

states=["Start", "Recognising...", "Interview-Over"]
def recognition(state):
    st.markdown(f"""
            <h1 style="text-align:center; color:#ED3B3B;">
                {state}
            </h1>
        """, unsafe_allow_html=True)

    st.markdown("""
        <img class="mis" 
            src="https://png.pngtree.com/png-vector/20250514/ourmid/pngtree-podcast-mic-png-image_16279107.png" 
            width="180">
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    st.write("")
    st.write("")
    
# if "step" not in st.session_state:
#     st.session_state.step = 1
# ------------ CARD CONTAINER -------------
if "screen" not in st.session_state:
    st.session_state.screen = "home"
    
if "show_popup" not in st.session_state:
    st.session_state.show_popup = False
    
def stage_container():
    parent = st.empty()       
    parent.empty()            
    time.sleep(0.01)          
    return parent.container()

# if st.session_state.screen == "pop":
#     @st.dialog("Interview start Notification", dismissible=True)
#     def resume_popup():
#         with stage_container():
#             st.info("After clicking Yes, your interview will start.")

#             if st.button("Yes", key="working_close"):
                
#                 st.session_state.screen = "frontInter"
#                 st.session_state.show_popup = False
#                 st.rerun()
                
#     resume_popup()

    
        
# ------count for control page rendering

        

    
# if st.session_state.step == 1:
if st.session_state.screen == "home":
        with stage_container():
            st.set_page_config(page_title="AI Interview", layout="centered")
            st.markdown("""
            <h1 style="text-align:center; color:#4A90E2;">
                🚀 Welcome to the AI Interview System
            </h1>
            <h3 style="text-align:center; color:gray;">
                Upload your resume to start the interview
            </h3>
        """, unsafe_allow_html=True)
            
            st.write("")
            st.write("")
            
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
            
            # inter_id=st.text_input("enter Interview ID:")

            # Centered Start Button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                start_btn = st.button("▶️ Start Interview",
                                    use_container_width=True)

            # Validation
            if start_btn:
                try:
                    if file :
                        st.success("Your resume has been uploaded successfully!")
                        st.session_state["resume"] = file
                        st.session_state.screen = "pop"
                        st.rerun()

                    else:
                        st.error("Please upload your resume first!")
                except Exception as e:
                    st.error(f"Error: {e}")

elif st.session_state.screen == "pop":
    with stage_container():
        # @st.dialog("Interview start Notification", dismissible=True)
        # def resume_popup():
                st.info("After clicking Yes, your interview will start.")

                if st.button("Yes", key="working_close"):
                    
                    st.session_state.screen = "frontInter"
                    st.session_state.show_popup = False
                    st.rerun()
                    
        # resume_popup()
            

# elif st.session_state.step == 2:
elif st.session_state.screen == "frontInter":
    with stage_container():   
        
            try:
                inter_reply=""
                st.set_page_config(page_title="AI Interview — Listening", layout="centered", initial_sidebar_state="expanded" ) 
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
                    
                st.sidebar.markdown("""
                        <h2 style="color:#4A90E2;">💬 Interview Chat</h2>
                        <hr>
                        <p style="color:gray;">Your conversation will appear here.</p>
                    """, unsafe_allow_html=True)
                
                if "step" not in st.session_state:
                    st.session_state.step= "start"
                    st.rerun()
                    
                if st.session_state.step == "start":
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        with st.container():
                         recognition(states[0])
                    print("---------start------")
                    
                    st.session_state.turn = 0
                    st.session_state.total_turns = 2
                    if "listening" not in st.session_state:
                        st.session_state["listening"] = True

                    if "mic_active" not in st.session_state:
                        st.session_state["mic_active"] = True
                        
                    if st.session_state.turn==0:
                        st.sidebar.write(" **Interviewer:-** Hello! How are you.")
                        speak("Hello! How are you.")
                    print(st.session_state.step)
                    
                    st.session_state.step = "listen"
                    st.rerun()
                    
                
            
                # ----------- LISTENING TEXT WITH DOT ANIMATION ----------

                if st.session_state.step == "listen":
                    
                    """Asking Quesions to users"""
                    
                    dot_class = "loading-dots" if st.session_state["listening"] else ""
                    mic_class = "mic-pulse" if st.session_state["mic_active"] else "" 
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        with st.container():  
                            animation()   
                    
                    try:
                        userRes = user_input() 
                        inter_reply = userRes.json()
                        # speak(inter_reply)
                        # if userRes.status_code==200:
                        #     st.sidebar.write(inter_reply)
                            
                        st.session_state.user_text = inter_reply
                        st.session_state.step = "recognise"
                        st.rerun()
                        
                    except requests.exceptions.ConnectionError:
                        st.info("can you tell again")
                
                if st.session_state.step == "recognise":
                    
                    """for stable recognition send request to ai model for user interview questions"""
                    print("<-------------mai yaha aaya hu----------->")
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        with st.container(): 
                            recognition(states[1])
                    if "resume" in st.session_state:
                        resume = st.session_state["resume"]
                        # inter_id = st.session_state["interId"]
                        user = st.session_state.user_text

                        try:
                            aiRes=interview_reply(user, resume) 
                            print("D----",aiRes)
                            ai_reply = aiRes.json()
                            
                            interNext = checkId(st.session_state.get("interConfigId"))
                            print("inter----->history ", st.session_state.get("interConfigId"))
                            
                            if interNext:
                                stud_data = interNext["stud_info"]
                                st.sidebar.write("**Interviewer:-** hello! How are you.")
                                
                                for chat in stud_data:
                                    if chat["role"] == "user":
                                        st.sidebar.write(f" **You:-** {chat['parts'][0]['text']}")
                                    else:
                                        st.sidebar.write(f" **Interviewer:-** {chat['parts'][0]['text']}")
                            
                            # if aiRes.status_code==200:
                                # st.session_state.his.append(f'"Interviewer" : {ai_reply}')
                                # st.sidebar.write(f'**Interviewer:-**  {ai_reply}')  
                            st.session_state.turn += 1
                            print(st.session_state.turn)
                            speak(ai_reply)
                            st.session_state["interConfigId"] = getInter().json() 
                            
                            if st.session_state.turn > st.session_state.total_turns:
                                st.write(st.session_state.turn,st.session_state.total_turns)
                                print(st.session_state.turn)
                                st.success("Interview Completed!")
                            else:
                                st.write(st.session_state.turn,st.session_state.total_turns)
                                st.session_state.step = "listen"
                                st.rerun()
                            
                        except requests.exceptions.ConnectionError:
                            st.error("Network error during recognition.")
                    else:
                        st.warning("resume or interviewId missing!")
                
                
                # NEXT TURN
                    
            except Exception as e:
                st.error(f"error in streamlit is {e}")

