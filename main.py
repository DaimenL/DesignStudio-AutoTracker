import threading
import time

# import config
import watcher
import user_interface
import parser
import logger

watch = watcher.myObserver()
t_watch = threading.Thread(target=watch.run, daemon=True)
#t_ui = threading.Thread(target =)

t_watch.start()
#t_ui.start()

while True:
    try:
        # Look for new file:
        if watch.handler.latest_file != None:
            print(watch.handler.latest_file)
            info = parser.parse_gcode(watch.handler.latest_file, parser.keys)
        # After final temp file found, write to logger
    
    except KeyboardInterrupt:
        print("Exiting Program")