import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Temp Folder Path
PATH = r"%TEMP%\bamboo_model"
TEMP_FOLDER = os.path.expandvars(PATH) # Change to your folder
print(TEMP_FOLDER)

# Handles what happens on events
class myHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.latest_file = None

    def on_any_event(self, event):
        if event.is_directory:
            return None
        if event.event_type in ('created', 'modified'):
            self.latest_file = event.src_path

# Handles what happens on events for specific extension types
class myFilteredHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.latest_file = None

    def on_any_event(self, event):
        if event.is_directory:
            return None
        if event.event_type in ('created', 'modified'):
            if event.src_path.endswith(".gcode"):
                self.latest_file = event.src_path

# Watches to see if any event occurs
class myObserver:
    watchDirectory = TEMP_FOLDER
    
    def __init__(self):
        self.observer = Observer()
        self.handler = myFilteredHandler()
    
    def run(self):
        self.observer.schedule(self.handler, self.watchDirectory, recursive=True)
        self.observer.start()
        try:
            while True:
                if self.handler.latest_file:
                    latest_file = self.handler.latest_file
                    print(latest_file)
                    self.handler.latest_file = None
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
        
        self.observer.join()
