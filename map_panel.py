import customtkinter as ctk
from tkintermapview import TkinterMapView

class MapPanel:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent, corner_radius=10, height=300)
        
        title = ctk.CTkLabel(
            self.frame, text="🗺️ GPS LOCATION",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=10)

        # Map container
        map_container = ctk.CTkFrame(self.frame, fg_color="#1a1a2e", corner_radius=5)
        map_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Create map widget
        self.map_widget = TkinterMapView(map_container, width=500, height=250, corner_radius=0)
        self.map_widget.pack(fill="both", expand=True)

        # Set default position
        self.map_widget.set_position(0.0, 0.0)  # Lat, Lon
        self.map_widget.set_zoom(2)

    def update_location(self, lat, lon):
        """Update map to new location."""
        self.map_widget.set_position(lat, lon)
        self.map_widget.set_zoom(15)
        self.map_widget.set_marker(lat, lon, text=f"Lat: {lat}, Lon: {lon}")


# Example usage
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("600x400")

    panel = MapPanel(root)
    panel.frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Test move after 2 seconds
    root.after(2000, lambda: panel.update_location(40.748817, -73.985428))  # NYC
    root.mainloop()
