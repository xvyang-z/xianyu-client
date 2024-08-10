import threading

from gui import run_gui
from handle import handle_start


threading.Thread(target=run_gui).start()
threading.Thread(target=handle_start, daemon=True).start()
