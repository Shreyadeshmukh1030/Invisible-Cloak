import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode
import cv2
import numpy as np
import threading
import sys
import os

# Add backend directory to path so we can import cloak_detector
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
from cloak_detector import CloakDetector

st.set_page_config(page_title="CloakVision", page_icon="🎭", layout="wide")

# Theme styling
st.markdown("""
<style>
    .stApp {
        background-color: #0B1120;
        color: #ffffff;
    }
    .st-bb { background-color: #16213E; }
    h1, h2, h3, h4 { color: #00E5FF; font-family: 'Poppins', sans-serif; }
    .stButton>button {
        border-radius: 20px;
        background-color: #7C4DFF;
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background-color: #00E5FF;
        color: black;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎭 CloakVision")
st.markdown("### AI Invisible Cloak using Streamlit")

if "detector" not in st.session_state:
    st.session_state.detector = CloakDetector()
if "capture_bg" not in st.session_state:
    st.session_state.capture_bg = False
if "bg_frame" not in st.session_state:
    st.session_state.bg_frame = None
if "invisibility_active" not in st.session_state:
    st.session_state.invisibility_active = False

class CloakVideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.detector = st.session_state.detector
        self.lock = threading.Lock()
        
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        with self.lock:
            # Capture background logic
            if st.session_state.capture_bg:
                st.session_state.bg_frame = img.copy()
                st.session_state.capture_bg = False
                
            # Apply invisibility
            if st.session_state.invisibility_active and st.session_state.bg_frame is not None:
                bg = st.session_state.bg_frame
                if bg.shape != img.shape:
                    bg = cv2.resize(bg, (img.shape[1], img.shape[0]))
                img = self.detector.apply_cloak(img, bg)
                
        return frame.from_ndarray(img, format="bgr24")

col1, col2 = st.columns([3, 1])

with col1:
    webrtc_streamer(
        key="cloakvision",
        mode=WebRtcMode.SENDRECV,
        video_processor_factory=CloakVideoProcessor,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )

with col2:
    st.markdown("### Controls")
    
    if st.button("📸 Capture Background"):
        st.session_state.capture_bg = True
        st.success("Background captured! Ensure you stepped out of the frame.")
        
    if st.button("✨ Toggle Invisibility"):
        if st.session_state.bg_frame is not None:
            st.session_state.invisibility_active = not st.session_state.invisibility_active
            if st.session_state.invisibility_active:
                st.success("Invisibility ACTIVE")
            else:
                st.info("Invisibility INACTIVE")
        else:
            st.error("Capture a background first!")

    st.markdown("---")
    st.markdown("### Settings")
    
    with st.expander("HSV Thresholds"):
        h_upper = st.slider("Hue Upper", 0, 180, 180)
        s_upper = st.slider("Saturation Upper", 0, 255, 40)
        v_lower = st.slider("Value Lower", 0, 255, 180)
        
        st.session_state.detector.update_hsv_thresholds(
            [0, 0, v_lower],
            [h_upper, s_upper, 255]
        )
        
    with st.expander("Processing Filters"):
        open_k = st.slider("Noise Removal (Open)", 1, 15, 3, step=2)
        close_k = st.slider("Fill Holes (Close)", 1, 15, 3, step=2)
        blur_k = st.slider("Edge Smoothness (Blur)", 1, 21, 5, step=2)
        
        st.session_state.detector.update_filter_params(open_k, close_k, blur_k)

st.markdown("---")
st.markdown("Built with ❤️ using Streamlit & OpenCV")
