import customtkinter as ctk

class ControlPanel:
    def __init__(self, parent, app=None):
        self.app = app
        self.frame = ctk.CTkFrame(parent, corner_radius=10)
        title = ctk.CTkLabel(self.frame, text="🎮 MISSION CONTROL", font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=10)
        buttons_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        buttons_frame.pack(pady=10)
        self.launch_button = ctk.CTkButton(buttons_frame, text="🚀 LAUNCH", width=150, height=40,
                                           font=ctk.CTkFont(size=14, weight="bold"),
                                           fg_color="#ff4444", hover_color="#ff6666",
                                           command=(self.app.handle_launch if self.app else None))
        self.launch_button.pack(side="left", padx=10)
        self.separate_button = ctk.CTkButton(buttons_frame, text="📦 SEPARATE PAYLOAD", width=180, height=40,
                                             font=ctk.CTkFont(size=14, weight="bold"),
                                             fg_color="#0066ff", hover_color="#4a9eff",
                                             command=(self.app.handle_separation if self.app else None))
        self.separate_button.pack(side="left", padx=10)
        filter_frame = ctk.CTkFrame(self.frame, corner_radius=5)
        filter_frame.pack(fill="x", padx=20, pady=(10, 20))
        filter_title = ctk.CTkLabel(filter_frame, text="CAMERA MULTI-SPECTRAL FILTER CONTROL",
                                     font=ctk.CTkFont(size=12, weight="bold"), text_color="#4a9eff")
        filter_title.pack(pady=10)
        input_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        input_frame.pack(pady=5)
        self.filter_entry = ctk.CTkEntry(input_frame, placeholder_text="N-L-N-L (e.g., 1A2B)", width=150, font=ctk.CTkFont(family="Courier New", size=14))
        self.filter_entry.pack(side="left", padx=5)
        self.apply_button = ctk.CTkButton(
            input_frame, text="APPLY FILTER", width=120, fg_color="#00d4ff", hover_color="#0099cc",
            command=(self.app.apply_filter if self.app else None))
        self.apply_button.pack(side="left", padx=5)
        presets_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        presets_frame.pack(pady=(5, 10))
        presets = ['1A1A', '2B2B', '3C3C', '4D4D', '5E5E', '6F6F', '7G7G', '8H8H', '9I9I']
        for preset in presets:
            ctk.CTkButton(presets_frame, text=preset, width=50, height=25, font=ctk.CTkFont(size=10),
                          fg_color="#4a9eff", hover_color="#6ab0ff",
                          command=lambda p=preset: self.filter_entry.insert(0, p)).pack(side="left", padx=2)