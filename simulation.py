import threading
import time
import random

def start_threads(app):
    def update_timer():
        mission_time = 0
        while True:
            if app.is_launched:
                mission_time += 1
                h, m, s = mission_time // 3600, (mission_time % 3600) // 60, mission_time % 60
                time_str = f"{h:02d}:{m:02d}:{s:02d}"
                app.mission_timer_label.configure(text=f"MISSION TIME: {time_str}")
                app.telemetry_panel.labels["packet_no"].configure(text=f"{mission_time:04d}")
            time.sleep(1)
    def update_data():
        while True:
            if app.is_launched:
                app.telemetry_panel.labels['altitude'].configure(text=f"{random.uniform(0,700):.1f} m")
                app.telemetry_panel.labels['x_position'].configure(text=f"{random.uniform(-10, 10):.2f} m")
                app.telemetry_panel.labels['y_position'].configure(text=f"{random.uniform(-10, 10):.2f} m")
            time.sleep(0.5)
    threading.Thread(target=update_timer, daemon=True).start()
    threading.Thread(target=update_data, daemon=True).start()