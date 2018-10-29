import time
import redis

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
object_id_raws = 'object_id_raws' # for instance segmentation
object_id_raws_2 = 'object_id_raws_2' # for class segmentation
depth_raws = 'depth_raws'


class Watcher:
    # DIRECTORY_TO_WATCH = "D:\\Program Files\\Rockstar Games\\Grand Theft Auto V\\cap"
    DIRECTORY_TO_WATCH = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Grand Theft Auto V\\cap"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            filename = event.src_path
            print(event.src_path)

            if 'object_id.raw' in filename:
                # Load the object_id.raw file and skip the first 4 bytes
                r.lpush(object_id_raws, filename)
                r.lpush(object_id_raws_2, filename)
            elif 'disparity.raw' in filename:
                # Load the disparity.raw file and skip the first 4 bytes
                r.lpush(depth_raws, filename)
            else:
                pass

            return None

        else:
            return None


if __name__ == '__main__':
    w = Watcher()
    w.run()
