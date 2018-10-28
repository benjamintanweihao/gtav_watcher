import time
import redis

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
object_id_raws = 'object_id_raws'


class Watcher:
    DIRECTORY_TO_WATCH = "D:\\Program Files\\Rockstar Games\\Grand Theft Auto V\\cap"

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

            if 'object_id.raw' in filename:
                print(event.src_path)
                # TODO: Put this into some queue or pubsub mechanism
                # Load the object_id.raw file and skip the first 4 bytes
                r.lpush(object_id_raws, filename)
                pass
            else:
                pass

            return None

        else:
            return None


if __name__ == '__main__':
    w = Watcher()
    w.run()
