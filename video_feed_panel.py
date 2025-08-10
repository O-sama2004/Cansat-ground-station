import customtkinter as ctk
from PIL import Image, ImageTk
import requests
import io
import threading

class VideoFeedPanel:
    def __init__(self, parent, stream_url=None):
        PANEL_WIDTH = 640
        PANEL_HEIGHT = 360
        VIDEO_WIDTH = 600
        VIDEO_HEIGHT = 320

        self.stream_url = stream_url
        self.frame = ctk.CTkFrame(parent, corner_radius=10, width=PANEL_WIDTH, height=PANEL_HEIGHT)
        self.frame.pack_propagate(False)

        title = ctk.CTkLabel(self.frame, text="📹 CAMERA FEED",
                             font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=10)

        # Video display container
        video_container = ctk.CTkFrame(
            self.frame, fg_color="#000000", corner_radius=5,
            width=VIDEO_WIDTH, height=VIDEO_HEIGHT
        )
        video_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        video_container.pack_propagate(False)

        self.video_label = ctk.CTkLabel(video_container, text="")
        self.video_label.pack(expand=True)

        controls_frame = ctk.CTkFrame(video_container, fg_color="transparent")
        controls_frame.pack(side="bottom", pady=10)
        for icon in ["▶️", "⏸️", "📷"]:
            ctk.CTkButton(controls_frame, text=icon, width=40, height=30,
                          fg_color="#333333", hover_color="#444444").pack(side="left", padx=5)

        self.running = True
        if stream_url:
            threading.Thread(target=self._start_pi_stream, daemon=True).start()

    def _start_pi_stream(self):
        """Start receiving JPEG frames from Pi camera stream."""
        print(f"[INFO] Attempting to connect to Pi stream at {self.stream_url}...")
        try:
            with requests.get(self.stream_url, stream=True, timeout=5) as r:
                bytes_data = b""
                for chunk in r.iter_content(chunk_size=1024):
                    if not self.running:
                        break
                    bytes_data += chunk
                    a = bytes_data.find(b'\xff\xd8')
                    b = bytes_data.find(b'\xff\xd9')
                    if a != -1 and b != -1:
                        jpg = bytes_data[a:b+2]
                        bytes_data = bytes_data[b+2:]
                        img = Image.open(io.BytesIO(jpg)).resize((600, 320))
                        tk_img = ImageTk.PhotoImage(img)
                        self.video_label.configure(image=tk_img)
                        self.video_label.image = tk_img
        except Exception as e:
            print("[ERROR] Pi stream connection failed:", e)

    def stop(self):
        self.running = False

# Example usage/test
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("700x400")

    # Replace with your Pi's stream URL
    stream_url = "http://192.168.1.50:5000/video_feed"

    video_panel = VideoFeedPanel(root, stream_url=stream_url)
    video_panel.frame.pack(fill="both", expand=True, padx=20, pady=20)

    def on_close():
        video_panel.stop()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()