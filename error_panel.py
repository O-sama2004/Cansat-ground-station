import customtkinter as ctk
import tkinter as tk

class ErrorPanel:
    def __init__(self, parent, app=None):
        self.app = app

        self.error_items = [
            ('Container Descent', '12-14 m/s'),
            ('Payload Descent', '6-8 m/s'),
            ('Container Pressure', 'DATA OK'),
            ('Payload Position', 'DATA OK'),
            ('Separation Status', 'READY'),
            ('Filter System', 'OPERATIONAL')
        ]
        self.num_slots = len(self.error_items)
        self.status_values = [0] * self.num_slots  # 0=OK, 1=Error

        self.frame = ctk.CTkFrame(parent, corner_radius=10, width=420, height=240)
        self.frame.pack_propagate(False)

        # --- Top Title
        title = ctk.CTkLabel(
            self.frame, text="⚠️ SYSTEM STATUS",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title.pack(pady=(2, 3))

        # --- Error System Bar
        container = ctk.CTkFrame(self.frame, fg_color="transparent")
        container.pack(pady=(0, 2), padx=8, fill="x")
        for i, (name, desc) in enumerate(self.error_items):
            col = ctk.CTkFrame(container, fg_color="transparent")
            col.grid(row=0, column=i, padx=4, sticky="nsew")
            ctk.CTkLabel(
                col, text=name, font=ctk.CTkFont(size=10, weight="bold"),
                wraplength=70, justify="center"
            ).pack()
            ctk.CTkLabel(
                col, text=desc, font=ctk.CTkFont(size=10),
                text_color="#999", wraplength=70, justify="center"
            ).pack()
        self.status_canvas = tk.Canvas(
            container, height=32, bg="white", highlightthickness=0
        )
        self.status_canvas.grid(row=1, column=0, columnspan=self.num_slots, sticky="ew", pady=(2, 4))
        for i in range(self.num_slots):
            container.grid_columnconfigure(i, weight=1)

        self.error_code_display = ctk.CTkLabel(
            self.frame, text="ERR: 000000",
            font=ctk.CTkFont(family="Courier New", size=12, weight="bold"),
            text_color="#bbb", fg_color="#222", corner_radius=5, height=26
        )
        self.error_code_display.pack(padx=8, pady=(0, 5), fill="x")

        # --- Smaller MISSION CONTROLS title ---
        mc_title = ctk.CTkLabel(
            self.frame, text="MISSION CONTROLS",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#81b0ff"
        )
        mc_title.pack(pady=(4, 0))

        # --- Modern Mission Control Toolbar
        toolbar = ctk.CTkFrame(self.frame, fg_color="#191f2e", corner_radius=10)
        toolbar.pack(padx=8, pady=(1, 4), fill="x")

        # BUTTONS GROUP
        buttons_group = ctk.CTkFrame(toolbar, fg_color="#232133", corner_radius=8)
        buttons_group.pack(side="left", padx=(8,18), pady=6)
        self.launch_button = ctk.CTkButton(
            buttons_group, text="🚀 LAUNCH", width=85, height=32,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#ff4444", hover_color="#ff6666",
            command=(self.app.handle_launch if self.app else None)
        )
        self.launch_button.pack(side="left", padx=(6,8), pady=5)
        self.separate_button = ctk.CTkButton(
            buttons_group, text="📦 SEPARATE", width=94, height=32,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#0066ff", hover_color="#4a9eff",
            command=(self.app.handle_separation if self.app else None)
        )
        self.separate_button.pack(side="left", padx=(8,8), pady=5)

        # VERTICAL DIVIDER
        separator = ctk.CTkFrame(toolbar, width=2, height=38, fg_color="#313850", corner_radius=4)
        separator.pack(side="left", padx=14, pady=7)

        # FILTER GROUP ("card" style)
        filter_group = ctk.CTkFrame(toolbar, fg_color="#313850", corner_radius=8)
        filter_group.pack(side="left", padx=(0,8), pady=6, fill="both", expand=True)
        self.filter_entry = ctk.CTkEntry(
            filter_group, placeholder_text="N-L-N-L (e.g., 1A2B)", width=105,
            font=ctk.CTkFont(family="Courier New", size=12)
        )
        self.filter_entry.pack(side="left", padx=(8,3), pady=8)
        self.apply_button = ctk.CTkButton(
            filter_group, text="APPLY", width=62, height=28, fg_color="#00d4ff", hover_color="#0099cc",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=(self.app.apply_filter if self.app else None)
        )
        self.apply_button.pack(side="left", padx=(3,8), pady=8)
        presets_frame = ctk.CTkFrame(filter_group, fg_color="transparent")
        presets = ['1A1A', '2B2B', '3C3C', '4D4D', '5E5E', '6F6F']
        for preset in presets:
            ctk.CTkButton(
                presets_frame, text=preset, width=28, height=18, font=ctk.CTkFont(size=9),
                fg_color="#4a9eff", hover_color="#6ab0ff",
                command=lambda p=preset: self.filter_entry.insert(0, p)
            ).pack(side="left", padx=1, pady=3)
        presets_frame.pack(side="left", padx=(0,6), pady=7)

        # --- Canvas resizing support
        self.status_canvas.bind("<Configure>", lambda e: self.update_status_bar())
        self.update_status_bar()

    def update_status_bar(self, values=None):
        if values is not None:
            self.status_values = values
        else:
            values = self.status_values

        self.status_canvas.delete("all")
        col_width = self.status_canvas.winfo_width() / self.num_slots
        for i, val in enumerate(self.status_values):
            x1 = i * col_width + 2
            x2 = (i + 1) * col_width - 2
            fill = "#6ec86e" if val == 0 else "#e53935"
            self.status_canvas.create_rectangle(x1, 0, x2, 32, fill=fill, outline='black', width=2)

        error_code = ''.join(str(e) for e in self.status_values)
        self.error_code_display.configure(text=f"ERR: {error_code}")

# # To test in isolation:
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("750x270")
    panel = ErrorPanel(root)
    panel.frame.pack(pady=10, padx=10, fill="x")
    root.mainloop()