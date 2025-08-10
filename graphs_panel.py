import customtkinter as ctk
import tkinter as tk

class GraphsPanel:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent, corner_radius=10)
        title = ctk.CTkLabel(self.frame, text="📊 REAL-TIME GRAPHS", font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=10)
        graphs_grid = ctk.CTkFrame(self.frame, fg_color="transparent")
        graphs_grid.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        for i in range(3): graphs_grid.grid_rowconfigure(i, weight=1)
        for i in range(2): graphs_grid.grid_columnconfigure(i, weight=1)
        graph_titles = [
            "Container Pressure", "Descent Speed", "Gyro X-Y-Z",
            "S2S1 Temperature", "S2S2 Temperature", "Elevation"
        ]
        self.graph_canvases = []
        for i, title_text in enumerate(graph_titles):
            row, col = divmod(i,2)
            graph_container = ctk.CTkFrame(graphs_grid, corner_radius=5)
            graph_container.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            ctk.CTkLabel(graph_container, text=title_text, font=ctk.CTkFont(size=11, weight="bold"), text_color="#4a9eff").pack(pady=5)
            canvas = tk.Canvas(graph_container, bg='#1a1a2e', highlightthickness=0, height=80)
            canvas.pack(fill="both", expand=True, padx=5, pady=(0, 5))
            self.graph_canvases.append(canvas)
            self.draw_graph_grid(canvas)
    def draw_graph_grid(self, canvas):
        canvas.update_idletasks()
        w, h = canvas.winfo_width(), canvas.winfo_height()
        for i in range(0, w, 20):
            canvas.create_line(i, 0, i, h, fill='#2a2a3e', width=1)
        for i in range(0, h, 20):
            canvas.create_line(0, i, w, i, fill='#2a2a3e', width=1)