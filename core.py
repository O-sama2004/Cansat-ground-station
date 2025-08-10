import customtkinter as ctk
from telemetry_panel import TelemetryPanel
from video_feed_panel import VideoFeedPanel
from map_panel import MapPanel
from graphs_panel import GraphsPanel
from error_panel import ErrorPanel
import simulation
from PIL import Image


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class CanSatGroundStation:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("CanSat Ground Station")
        self.root.state("zoomed")

        # State
        self.is_launched = False
        self.is_separated = False

        # Main Frame & Header
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.header_frame, self.status_indicator, self.mission_timer_label = self.create_header()

        # Content grid: [Telem][Vid/Map][Err/Graph] (3 cols), 2 rows
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, pady=(10, 0))

        self.content_frame.grid_columnconfigure(0, weight=1) # Telemetry
        self.content_frame.grid_columnconfigure(1, weight=2) # Video/Map
        self.content_frame.grid_columnconfigure(2, weight=2) # Error/Graph
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)

        # --- Left Side ---
        self.telemetry_panel = TelemetryPanel(self.content_frame)
        self.telemetry_panel.frame.grid(row=0, column=0, rowspan=2,
                                        sticky="nsew", padx=(0, 8), pady=(0,0))

        # --- Video & Map Stacked Right of Telem ---
        self.video_feed_panel = VideoFeedPanel(self.content_frame)
        self.video_feed_panel.frame.grid(row=0, column=1,
                                          sticky="nsew", padx=(0,8), pady=(0,4))
        self.map_panel = MapPanel(self.content_frame)
        self.map_panel.frame.grid(row=1, column=1,
                                  sticky="nsew", padx=(0,8), pady=(4,0))

        # --- Right Side: ErrorPanel (Mission Controls)/Graphs stacked ---
        # Use an inner Frame to stack vertically in col 2
        right_stack = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        right_stack.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=(0,0), pady=(0,0))
        right_stack.grid_rowconfigure(0, weight=1) # ErrorPanel
        right_stack.grid_rowconfigure(1, weight=2) # GraphsPanel
        right_stack.grid_columnconfigure(0, weight=1)

        self.error_panel = ErrorPanel(right_stack, app=self)
        self.error_panel.frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=(0,4))
        self.graphs_panel = GraphsPanel(right_stack)
        self.graphs_panel.frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=(4,0))

        # Start simulation/control threads
        simulation.start_threads(self)

    def create_header(self):
        header_frame = ctk.CTkFrame(self.main_frame, height=60, corner_radius=10)
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.pack_propagate(False)

        # Load team logo
        try:
            logo_img = ctk.CTkImage(
                light_image=Image.open("assets/team_logo.png"),  # Change path if needed
                dark_image=Image.open("assets/team_logo.png"),
                size=(70, 50)  # Adjust to fit your header
            )
            logo_label = ctk.CTkLabel(header_frame, image=logo_img, text="")
            logo_label.pack(side="left", padx=(30, 10), pady=10)
        except FileNotFoundError:
            print("⚠ Logo image not found! Check path.")

        # Title text
        title = ctk.CTkLabel(
            header_frame,
            text="HYPERSAT TEAM GROUND STATION",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(side="left", pady=10)

        status_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        status_frame.pack(side="right", padx=30)
        status_indicator = ctk.CTkLabel(status_frame, text="● SYSTEM ONLINE",
                                        font=ctk.CTkFont(size=14), text_color="#00ff00")
        status_indicator.pack(side="left", padx=20)
        mission_timer_label = ctk.CTkLabel(status_frame, text="MISSION TIME: 00:00:00",
                                           font=ctk.CTkFont(size=14, weight="bold"))
        mission_timer_label.pack(side="left", padx=20)
        return header_frame, status_indicator, mission_timer_label

    # =======================
    # Button handlers for mission control buttons
    # =======================
    def handle_launch(self):
        self.is_launched = True
        self.error_panel.launch_button.configure(fg_color="#00ff00", text="✓ LAUNCHED")
        self.telemetry_panel.labels['status_code'].configure(text="ASCENDING")
        print("Launch sequence initiated!")

    def handle_separation(self):
        if self.is_launched:
            self.is_separated = True
            self.error_panel.separate_button.configure(fg_color="#00ff00", text="✓ SEPARATED")
            self.telemetry_panel.labels['status_code'].configure(text="DEPLOYED")
            print("Payload separation command sent!")
        else:
            print("Cannot separate - not launched yet!")

    def apply_filter(self):
        filter_value = self.error_panel.filter_entry.get().upper()
        if len(filter_value) == 4 and filter_value[0].isdigit() and filter_value[1].isalpha() and \
           filter_value[2].isdigit() and filter_value[3].isalpha():
            print(f"Filter command {filter_value} applied!")
            self.error_panel.filter_entry.delete(0, 'end')
        else:
            print("Invalid filter format! Use N-L-N-L format (e.g., 1A2B)")

    def run(self):
        self.root.mainloop()