import time
import threading
from NELL.Selenium import Selenium
from NELL.gui.Window import Window
from NELL.logger.Logger import Logger
from NELL.logger.LogHttpServer import start_server
from IPython.display import display, clear_output

class Main:

    def __init__(self):
        self.pageCounter = 0
        self.current_url = None
        self.last_instrumented_url = None
        self.selenium = Selenium.instance()

        self.init_gui()
        Logger.log_event({'info': 'selenium framework'}, reset=True)

        self.init_logger_server()
        self.init_browser_monitoring()

    def init_gui(self):
        self.selenium.new_driver(restart=True)
        self.window = Window()
        self.window.redraw()

    def init_logger_server(self):
        server_thread = threading.Thread(target=start_server, args=(8000,))
        server_thread.daemon = True
        server_thread.start()

    def init_browser_monitoring(self):
        browser_thread = threading.Thread(target=self.check_browser)
        browser_thread.daemon = True
        browser_thread.start()

    def check_browser(self):
        while True:
            if Logger.disabled():
                time.sleep(1)
                continue

            # try:
            
            if not self.selenium.is_page_loaded():
                time.sleep(0.1)
                continue

            if self.selenium.current_url() is None:
                time.sleep(0.1)
                continue

            if self.current_url == self.selenium.current_url():
                time.sleep(0.1)
                continue

            clear_output()
            self.window.redraw()
            event = Logger.log_event({'info': 'page loaded', 'url': self.selenium.current_url()})
            self.current_url = self.selenium.current_url()
            self.selenium.execute_script("window.hasEventListeners=false;")
            self.selenium.instrument_webpage(self.window, event['page_id'])

            # except Exception as e:
            #     traceback.print_exc()
            #     print(f"Exception: {e}")
            #     self.selenium.new_driver(restart=True)

            time.sleep(0.1)
