import customtkinter as ctk

class TelemetryPanel:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent, corner_radius=16, fg_color="#161c22", width=380)
        self.frame.pack_propagate(False)
        title = ctk.CTkLabel(
            self.frame, text="📡 TELEMETRY", 
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#81baf6"
        )
        title.pack(pady=(16, 12), anchor="center")

        items = [
            ('packet_no',      "Packet No",      "0000",      "🔢"),
            ('status_code',    "Status",         "READY",     "🟢"),
            ('mission_time',   "Mission Time",   "00:00:00",  "⏱️"),
            ('x_position',     "X Position",     "0.00 m",    "🡱"),
            ('y_position',     "Y Position",     "0.00 m",    "🡲"),
            ('yaw',            "Yaw",            "0.0°",      "🧭"),
            ('pitch',          "Pitch",          "0.0°",      "↔️"),
            ('roll',           "Roll",           "0.0°",      "↻"),
            ('altitude',       "Altitude",       "0.0 m",     "🗻"),
            ('heat',           "Heat",           "25.0°C",    "🔥"),
            ('sp_pressure',    "SP Pressure",    "101.3 kPa", "🌬️"),
            ('container_pressure', "Container P", "101.3 kPa", "🧃"),
            ('s2s_temp1',      "S2S Temp1",      "25.0°C",    "🌡️"),
            ('s2s_temp2',      "S2S Temp2",      "25.0°C",    "🌡️"),
        ]
        self.labels = {}

        # --- Vertical Stat Cards ---
        for i, (key, label, default, icon) in enumerate(items):
            row_bg = "#232d37" if i % 2 == 0 else "#1c232a"
            card = ctk.CTkFrame(self.frame, fg_color=row_bg, corner_radius=12)
            card.pack(fill="x", pady=6, padx=16, ipady=6)
            icon_lab = ctk.CTkLabel(
                card, text=f"{icon}", font=ctk.CTkFont(size=18), text_color="#3ce6ff", width=35, anchor="center"
            )
            icon_lab.pack(side="left", padx=(8, 8))
            lab = ctk.CTkLabel(
                card, text=label, font=ctk.CTkFont(size=15, weight="bold"), text_color="#7ab5e5", width=120, anchor="w"
            )
            lab.pack(side="left", padx=(0,5))
            value_label = ctk.CTkLabel(
                card, text=default, font=ctk.CTkFont(size=18, weight="bold"), text_color="#00ffe6", width=102, anchor="e"
            )
            value_label.pack(side="right", padx=(5,18))
            self.labels[key] = value_label

# ------------- TEST IN ISOLATION ------------------
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("420x950")  # Tall window to fit all
    panel = TelemetryPanel(root)
    panel.frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Dynamically test that updating a value also changes color and is visible!
    def toggle_alert():
        panel.labels["heat"].configure(text="99.0°C", text_color="#ff1a42")
        panel.labels["status_code"].configure(text="ALERT", text_color="#fc3")
        panel.labels["mission_time"].configure(text="04:12:44")
        panel.labels["altitude"].configure(text="1879.6 m", text_color="#eacb33")
    root.after(2000, toggle_alert)

    root.mainloop()