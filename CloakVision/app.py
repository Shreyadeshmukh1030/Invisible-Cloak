import customtkinter as ctk
import cv2
import threading
import time
import os
import glob
from PIL import Image, ImageTk
from datetime import datetime

from camera import Camera
from background_manager import BackgroundManager
from cloak_detector import CloakDetector
from utils import cv2_to_photoimage, save_screenshot, get_lighting_status

# --- Theme Constants ---
BG_COLOR = "#0B1120"
CARD_COLOR = "#16213E"
ACCENT_COLOR = "#00E5FF"
SEC_ACCENT = "#7C4DFF"
TEXT_COLOR = "#FFFFFF"
TEXT_MUTED = "#8B9BB4"
SUCCESS_COLOR = "#00E676"
WARNING_COLOR = "#FFC107"
ERROR_COLOR = "#FF5252"

FONT_MAIN = ("Inter", 14)
FONT_H1 = ("Poppins", 32, "bold")
FONT_H2 = ("Poppins", 24, "bold")
FONT_H3 = ("Poppins", 18, "bold")

class CloakVisionApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("CloakVision - AI Invisible Cloak")
        self.geometry("1400x900")
        self.minsize(1200, 800)
        self.configure(fg_color=BG_COLOR)
        
        # Core Modules
        self.camera = Camera()
        self.bg_manager = BackgroundManager(countdown_seconds=5)
        self.detector = CloakDetector()
        
        # State
        self.is_running = False
        self.invisibility_active = False
        self.is_recording = False
        self.video_writer = None
        self.current_frame = None
        self.display_frame = None
        
        self.console_logs = []
        
        self.setup_ui()
        
        self.bind("<F11>", self.toggle_fullscreen)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Start on Landing Page
        self.show_page("landing")

    def log_msg(self, msg, m_type="INFO"):
        time_str = datetime.now().strftime("%H:%M:%S")
        self.console_logs.append(f"[{time_str}] [{m_type}] {msg}")
        if len(self.console_logs) > 50:
            self.console_logs.pop(0)
        if hasattr(self, 'console_textbox'):
            self.console_textbox.configure(state="normal")
            self.console_textbox.delete("1.0", "end")
            self.console_textbox.insert("end", "\n".join(self.console_logs))
            self.console_textbox.see("end")
            self.console_textbox.configure(state="disabled")

    def setup_ui(self):
        # Container for pages
        self.container = ctk.CTkFrame(self, fg_color=BG_COLOR)
        self.container.pack(fill="both", expand=True)
        
        self.pages = {}
        
        self.pages["landing"] = LandingPage(self.container, self)
        self.pages["dashboard"] = DashboardPage(self.container, self)
        self.pages["gallery"] = GalleryPage(self.container, self)
        self.pages["about"] = AboutPage(self.container, self)
        
        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")
            
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    def show_page(self, page_name):
        frame = self.pages[page_name]
        frame.tkraise()
        if page_name == "gallery":
            frame.load_images()

    def toggle_fullscreen(self, event=None):
        self.attributes("-fullscreen", not self.attributes("-fullscreen"))
        
    def on_closing(self):
        self.is_running = False
        self.camera.stop()
        if self.video_writer:
            self.video_writer.release()
        self.destroy()

# ==========================================
# PAGES
# ==========================================

class LandingPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_COLOR)
        self.controller = controller
        
        # Navbar
        navbar = ctk.CTkFrame(self, fg_color=BG_COLOR, height=80)
        navbar.pack(fill="x", padx=40, pady=20)
        
        logo_lbl = ctk.CTkLabel(navbar, text="CV  CloakVision", font=FONT_H2, text_color=ACCENT_COLOR)
        logo_lbl.pack(side="left")
        
        btn_start = ctk.CTkButton(navbar, text="Start Application", font=FONT_MAIN, 
                                  fg_color=SEC_ACCENT, hover_color=ACCENT_COLOR, corner_radius=20,
                                  command=lambda: self.controller.show_page("dashboard"))
        btn_start.pack(side="right")
        
        # Hero Section
        hero = ctk.CTkFrame(self, fg_color=BG_COLOR)
        hero.pack(fill="both", expand=True, padx=40, pady=20)
        hero.grid_columnconfigure(0, weight=1)
        hero.grid_columnconfigure(1, weight=1)
        
        left_hero = ctk.CTkFrame(hero, fg_color=BG_COLOR)
        left_hero.grid(row=0, column=0, sticky="nsew", pady=100)
        
        ctk.CTkLabel(left_hero, text="Become Invisible\nUsing Computer Vision", font=("Poppins", 48, "bold"), 
                     text_color=TEXT_COLOR, justify="left").pack(anchor="w")
        ctk.CTkLabel(left_hero, text="Inspired by Harry Potter's Invisible Cloak,\nCloakVision uses real-time Computer Vision\nto make white cloth disappear instantly.", 
                     font=("Inter", 18), text_color=TEXT_MUTED, justify="left").pack(anchor="w", pady=20)
                     
        hero_btns = ctk.CTkFrame(left_hero, fg_color=BG_COLOR)
        hero_btns.pack(anchor="w", pady=20)
        
        ctk.CTkButton(hero_btns, text="Start Camera", font=FONT_MAIN, width=200, height=50,
                      fg_color=ACCENT_COLOR, text_color="#000000", hover_color=SEC_ACCENT, corner_radius=25,
                      command=lambda: self.controller.show_page("dashboard")).pack(side="left", padx=(0, 20))
                      
        ctk.CTkButton(hero_btns, text="Watch Demo", font=FONT_MAIN, width=200, height=50,
                      fg_color=CARD_COLOR, border_width=2, border_color=ACCENT_COLOR, hover_color=BG_COLOR, corner_radius=25).pack(side="left")
        
        # Features Section (Bottom)
        features = ctk.CTkFrame(self, fg_color=BG_COLOR)
        features.pack(fill="x", padx=40, pady=40)
        features.grid_columnconfigure((0,1,2,3), weight=1)
        
        feature_data = [
            ("📷", "Real-Time Webcam", "Uses webcam to process every frame instantly."),
            ("🎭", "Invisible Cloak", "Detects white cloth and replaces it with background."),
            ("⚡", "30 FPS Processing", "Optimized OpenCV pipeline for smooth performance."),
            ("🧠", "AI Vision", "Uses Computer Vision techniques for segmentation.")
        ]
        
        for i, (icon, title, desc) in enumerate(feature_data):
            card = ctk.CTkFrame(features, fg_color=CARD_COLOR, corner_radius=16)
            card.grid(row=0, column=i, padx=10, sticky="ew")
            ctk.CTkLabel(card, text=icon, font=("Segoe UI Emoji", 40)).pack(pady=(20, 10))
            ctk.CTkLabel(card, text=title, font=FONT_H3, text_color=ACCENT_COLOR).pack()
            ctk.CTkLabel(card, text=desc, font=FONT_MAIN, text_color=TEXT_MUTED, wraplength=200).pack(pady=(10, 20), padx=10)


class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_COLOR)
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=0, minsize=250) # Sidebar
        self.grid_columnconfigure(1, weight=3) # Main Camera
        self.grid_columnconfigure(2, weight=1, minsize=350) # Right Panel
        self.grid_rowconfigure(0, weight=1)
        
        self.build_sidebar()
        self.build_main_area()
        self.build_right_panel()

    def build_sidebar(self):
        sidebar = ctk.CTkFrame(self, fg_color=CARD_COLOR, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(sidebar, text="CV CloakVision", font=FONT_H2, text_color=ACCENT_COLOR).pack(pady=30)
        
        navs = [("Dashboard", "dashboard"), ("Gallery", "gallery"), ("About", "about"), ("Home", "landing")]
        
        for text, page in navs:
            btn = ctk.CTkButton(sidebar, text=text, font=FONT_MAIN, fg_color="transparent", 
                                text_color=TEXT_COLOR, hover_color=SEC_ACCENT, anchor="w",
                                command=lambda p=page: self.controller.show_page(p))
            btn.pack(fill="x", padx=20, pady=5)
            
        # Status Console
        console_frame = ctk.CTkFrame(sidebar, fg_color="#000000", corner_radius=10)
        console_frame.pack(fill="both", expand=True, padx=10, pady=20)
        ctk.CTkLabel(console_frame, text="Status Console", font=FONT_MAIN, text_color=ACCENT_COLOR).pack(pady=5)
        
        self.controller.console_textbox = ctk.CTkTextbox(console_frame, fg_color="#000000", text_color=SUCCESS_COLOR, font=("Consolas", 12))
        self.controller.console_textbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.controller.console_textbox.configure(state="disabled")

    def build_main_area(self):
        main = ctk.CTkFrame(self, fg_color=BG_COLOR)
        main.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        main.grid_rowconfigure(1, weight=1)
        main.grid_columnconfigure(0, weight=1)
        
        # Top Stats
        stats_frame = ctk.CTkFrame(main, fg_color=BG_COLOR)
        stats_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        stats_frame.grid_columnconfigure((0,1,2,3), weight=1)
        
        self.stat_fps = self.create_stat_card(stats_frame, 0, "FPS", "0")
        self.stat_white = self.create_stat_card(stats_frame, 1, "White Pixels", "0%")
        self.stat_area = self.create_stat_card(stats_frame, 2, "Status", "Ready")
        self.stat_light = self.create_stat_card(stats_frame, 3, "Lighting", "Unknown")
        
        # Camera Preview
        cam_frame = ctk.CTkFrame(main, fg_color=CARD_COLOR, corner_radius=20, border_width=2, border_color=ACCENT_COLOR)
        cam_frame.grid(row=1, column=0, sticky="nsew")
        
        self.video_label = ctk.CTkLabel(cam_frame, text="Camera Feed Offline", font=FONT_H3, text_color=TEXT_MUTED)
        self.video_label.pack(fill="both", expand=True, padx=10, pady=10)

    def create_stat_card(self, parent, col, title, value):
        card = ctk.CTkFrame(parent, fg_color=CARD_COLOR, corner_radius=12)
        card.grid(row=0, column=col, padx=5, sticky="ew")
        ctk.CTkLabel(card, text=title, font=("Inter", 12), text_color=TEXT_MUTED).pack(pady=(10, 0))
        val_lbl = ctk.CTkLabel(card, text=value, font=FONT_H3, text_color=ACCENT_COLOR)
        val_lbl.pack(pady=(0, 10))
        return val_lbl

    def build_right_panel(self):
        panel = ctk.CTkFrame(self, fg_color=BG_COLOR)
        panel.grid(row=0, column=2, sticky="nsew", padx=(0, 20), pady=20)
        
        # Controls Card
        ctrl = ctk.CTkFrame(panel, fg_color=CARD_COLOR, corner_radius=16)
        ctrl.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(ctrl, text="Controls", font=FONT_H3, text_color=ACCENT_COLOR).pack(pady=10)
        
        self.btn_start_cam = ctk.CTkButton(ctrl, text="Start Camera", font=FONT_MAIN, fg_color=SEC_ACCENT, hover_color=ACCENT_COLOR, command=self.toggle_camera)
        self.btn_start_cam.pack(fill="x", padx=20, pady=5)
        
        self.btn_capture_bg = ctk.CTkButton(ctrl, text="Capture Background", font=FONT_MAIN, state="disabled", command=self.capture_background)
        self.btn_capture_bg.pack(fill="x", padx=20, pady=5)
        
        self.btn_invisibility = ctk.CTkButton(ctrl, text="Start Invisibility", font=FONT_MAIN, state="disabled", command=self.toggle_invisibility)
        self.btn_invisibility.pack(fill="x", padx=20, pady=5)
        
        actions = ctk.CTkFrame(ctrl, fg_color="transparent")
        actions.pack(fill="x", padx=20, pady=10)
        actions.grid_columnconfigure((0,1), weight=1)
        
        self.btn_ss = ctk.CTkButton(actions, text="Screenshot", font=("Inter", 12), state="disabled", fg_color=BG_COLOR, border_width=1, command=self.take_screenshot)
        self.btn_ss.grid(row=0, column=0, padx=5)
        
        self.btn_rec = ctk.CTkButton(actions, text="Record", font=("Inter", 12), state="disabled", fg_color=BG_COLOR, border_width=1, command=self.toggle_recording)
        self.btn_rec.grid(row=0, column=1, padx=5)
        
        # Settings Tabs
        self.tabview = ctk.CTkTabview(panel, fg_color=CARD_COLOR, segmented_button_selected_color=SEC_ACCENT, segmented_button_selected_hover_color=ACCENT_COLOR)
        self.tabview.pack(fill="both", expand=True)
        
        t_hsv = self.tabview.add("HSV")
        t_proc = self.tabview.add("Processing")
        
        self.build_hsv_tab(t_hsv)
        self.build_proc_tab(t_proc)

    def build_hsv_tab(self, parent):
        self.slider_h_upper = self.add_slider(parent, "Hue Upper", 180, 180)
        self.slider_s_upper = self.add_slider(parent, "Sat Upper", 40, 255)
        self.slider_v_lower = self.add_slider(parent, "Value Lower", 180, 255)

    def build_proc_tab(self, parent):
        self.slider_open = self.add_slider(parent, "Noise Removal", 3, 15, 1)
        self.slider_close = self.add_slider(parent, "Fill Holes", 3, 15, 1)
        self.slider_blur = self.add_slider(parent, "Edge Smoothness", 5, 21, 1)
        
        self.switch_mp = ctk.CTkSwitch(parent, text="AI Pose (MediaPipe)", progress_color=ACCENT_COLOR, command=self.update_mp)
        self.switch_mp.pack(pady=20)
        if not self.controller.detector.mp_available:
            self.switch_mp.configure(state="disabled", text="AI Pose (Not Installed)")

    def add_slider(self, parent, label, default, to_val, from_val=0):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=5)
        ctk.CTkLabel(frame, text=label, font=("Inter", 12)).pack(anchor="w")
        slider = ctk.CTkSlider(frame, from_=from_val, to=to_val, button_color=ACCENT_COLOR, button_hover_color=SEC_ACCENT, command=self.on_slider_change)
        slider.set(default)
        slider.pack(fill="x")
        return slider

    # --- Logic ---
    def on_slider_change(self, _):
        h = int(self.slider_h_upper.get())
        s = int(self.slider_s_upper.get())
        v = int(self.slider_v_lower.get())
        self.controller.detector.update_hsv_thresholds([0, 0, v], [h, s, 255])
        
        o = int(self.slider_open.get())
        c = int(self.slider_close.get())
        b = int(self.slider_blur.get())
        self.controller.detector.update_filter_params(o, c, b)
        
    def update_mp(self):
        state = self.switch_mp.get() == 1
        self.controller.detector.toggle_mediapipe(state)
        self.controller.log_msg(f"MediaPipe Pose: {'Enabled' if state else 'Disabled'}")

    def toggle_camera(self):
        c = self.controller
        if not c.is_running:
            if c.camera.start():
                c.is_running = True
                self.btn_start_cam.configure(text="Stop Camera", fg_color=ERROR_COLOR, hover_color="#D32F2F")
                self.btn_capture_bg.configure(state="normal")
                self.btn_ss.configure(state="normal")
                self.btn_rec.configure(state="normal")
                c.log_msg("Camera Started successfully")
                
                c.process_thread = threading.Thread(target=self.process_video_loop, daemon=True)
                c.process_thread.start()
            else:
                c.log_msg("Camera Failed to start", "ERROR")
        else:
            c.is_running = False
            c.invisibility_active = False
            c.camera.stop()
            c.bg_manager.reset()
            self.btn_start_cam.configure(text="Start Camera", fg_color=SEC_ACCENT, hover_color=ACCENT_COLOR)
            self.btn_capture_bg.configure(state="disabled", text="Capture Background")
            self.btn_invisibility.configure(state="disabled", text="Start Invisibility")
            self.btn_ss.configure(state="disabled")
            self.btn_rec.configure(state="disabled")
            self.video_label.configure(image="", text="Camera Feed Offline")
            self.stat_area.configure(text="Stopped")
            c.log_msg("Camera Stopped")

    def capture_background(self):
        c = self.controller
        if c.is_running:
            c.invisibility_active = False
            self.btn_invisibility.configure(text="Start Invisibility", fg_color="#1f538d")
            c.bg_manager.start_capture()
            c.log_msg("Background capture initiated (5s)")

    def toggle_invisibility(self):
        c = self.controller
        if c.bg_manager.has_background():
            c.invisibility_active = not c.invisibility_active
            if c.invisibility_active:
                self.btn_invisibility.configure(text="Stop Invisibility", fg_color=ERROR_COLOR)
                c.log_msg("Invisibility activated!")
            else:
                self.btn_invisibility.configure(text="Start Invisibility", fg_color="#1f538d")
                c.log_msg("Invisibility deactivated")

    def take_screenshot(self):
        if self.controller.display_frame is not None:
            save_screenshot(self.controller.display_frame)
            self.controller.log_msg("Screenshot saved to /screenshots")

    def toggle_recording(self):
        c = self.controller
        if not c.is_recording:
            if not os.path.exists("screenshots"):
                os.makedirs("screenshots")
            filename = os.path.join("screenshots", f"vid_{datetime.now().strftime('%Y%m%d_%H%M%S')}.avi")
            if c.current_frame is not None:
                h, w = c.current_frame.shape[:2]
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                c.video_writer = cv2.VideoWriter(filename, fourcc, 20.0, (w, h))
                c.is_recording = True
                self.btn_rec.configure(text="Stop Rec", fg_color=ERROR_COLOR)
                c.log_msg("Video recording started")
        else:
            c.is_recording = False
            if c.video_writer:
                c.video_writer.release()
                c.video_writer = None
            self.btn_rec.configure(text="Record", fg_color=BG_COLOR)
            c.log_msg("Video recording stopped")

    def process_video_loop(self):
        c = self.controller
        while c.is_running:
            ret, frame = c.camera.get_frame()
            if not ret:
                time.sleep(0.01)
                continue
            
            c.current_frame = frame.copy()
            
            if c.bg_manager.is_capturing:
                processed_frame = c.bg_manager.update(frame)
            elif c.invisibility_active and c.bg_manager.has_background():
                processed_frame = c.detector.apply_cloak(frame, c.bg_manager.get_background())
            else:
                processed_frame = frame

            c.display_frame = processed_frame.copy()

            if c.is_recording and c.video_writer:
                c.video_writer.write(c.display_frame)

            self.after(0, self.update_ui_frame, processed_frame)
            time.sleep(0.01)

    def update_ui_frame(self, frame):
        c = self.controller
        img = cv2_to_photoimage(frame)
        self.video_label.configure(image=img, text="")
        self.video_label.image = img
        
        self.stat_fps.configure(text=f"{c.camera.get_fps()}")
        self.stat_light.configure(text=f"{get_lighting_status(frame)}")
        
        if c.bg_manager.capture_completed:
            self.stat_area.configure(text="BG Ready")
            self.btn_invisibility.configure(state="normal")
            self.btn_capture_bg.configure(text="Re-Capture Background")
            c.bg_manager.capture_completed = False
            c.log_msg("Background captured successfully", "SUCCESS")
            
        if c.invisibility_active:
            self.stat_white.configure(text=f"{c.detector.white_pixels_percent:.1f}%")
        else:
            self.stat_white.configure(text="0%")


class GalleryPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_COLOR)
        self.controller = controller
        
        header = ctk.CTkFrame(self, fg_color=BG_COLOR)
        header.pack(fill="x", padx=40, pady=20)
        
        ctk.CTkButton(header, text="← Back to Dashboard", font=FONT_MAIN, fg_color="transparent", border_width=1,
                      command=lambda: self.controller.show_page("dashboard")).pack(side="left")
        
        ctk.CTkLabel(header, text="Capture Gallery", font=FONT_H2, text_color=ACCENT_COLOR).pack(side="right")
        
        self.scroll = ctk.CTkScrollableFrame(self, fg_color=CARD_COLOR, corner_radius=16)
        self.scroll.pack(fill="both", expand=True, padx=40, pady=20)
        
    def load_images(self):
        for widget in self.scroll.winfo_children():
            widget.destroy()
            
        if not os.path.exists("screenshots"):
            ctk.CTkLabel(self.scroll, text="No captures found.", font=FONT_MAIN, text_color=TEXT_MUTED).pack(pady=50)
            return
            
        files = glob.glob("screenshots/*.png")
        if not files:
            ctk.CTkLabel(self.scroll, text="No screenshots found.", font=FONT_MAIN, text_color=TEXT_MUTED).pack(pady=50)
            return
            
        row, col = 0, 0
        for f in files:
            try:
                img = Image.open(f)
                img.thumbnail((250, 250))
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(200, 150))
                
                card = ctk.CTkFrame(self.scroll, fg_color=BG_COLOR, corner_radius=8)
                card.grid(row=row, column=col, padx=10, pady=10)
                
                ctk.CTkLabel(card, image=ctk_img, text="").pack(padx=10, pady=10)
                ctk.CTkLabel(card, text=os.path.basename(f), font=("Inter", 10)).pack()
                
                col += 1
                if col > 3:
                    col = 0
                    row += 1
            except Exception:
                pass


class AboutPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_COLOR)
        self.controller = controller
        
        btn = ctk.CTkButton(self, text="← Back to Dashboard", font=FONT_MAIN, fg_color="transparent", border_width=1,
                      command=lambda: self.controller.show_page("dashboard"))
        btn.pack(anchor="w", padx=40, pady=20)
        
        card = ctk.CTkFrame(self, fg_color=CARD_COLOR, corner_radius=20)
        card.pack(expand=True, padx=100, pady=50)
        
        ctk.CTkLabel(card, text="CloakVision", font=FONT_H1, text_color=ACCENT_COLOR).pack(pady=(40, 10))
        ctk.CTkLabel(card, text="Version 1.0", font=FONT_MAIN, text_color=TEXT_MUTED).pack(pady=(0, 20))
        
        info = "Built with:\n\n• Python 3\n• OpenCV\n• NumPy\n• CustomTkinter\n• MediaPipe"
        ctk.CTkLabel(card, text=info, font=FONT_MAIN, justify="center").pack(pady=20, padx=40)
        
        ctk.CTkLabel(card, text="AI-Powered Invisible Cloak Project", font=("Inter", 12, "italic"), text_color=SEC_ACCENT).pack(pady=(20, 40))

if __name__ == "__main__":
    app = CloakVisionApp()
    app.mainloop()
