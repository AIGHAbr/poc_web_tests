import threading
import time
from IPython.display import clear_output
from NELL.Selenium import Selenium, instrument_webpage
from NELL.gui.Window import Window
from NELL.logger.LogHttpServer import start_server
from NELL.logger.Logger import Logger


class Main:

    def __init__(self):
        self.window = Window()

        global win
        win = self.window
        
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
        self.window.redraw()

    @staticmethod
    def init_logger_server():
        server_thread = threading.Thread(target=start_server, args=(8000,))
        server_thread.daemon = True
        server_thread.start()

    def init_browser_monitoring(self):
        browser_thread = threading.Thread(target=self.check_browser)
        browser_thread.daemon = True
        browser_thread.start()

    def check_browser(self):
        while True:
            if not self.can_instrument_now():
                time.sleep(0.1)
                continue

            clear_output()
            self.window.redraw()

            event = Logger.log_event({'info': 'page loaded', 'url': self.selenium.current_url()})
            self.current_url = instrument_webpage(event['page_id'], self.selenium, self.window)
            time.sleep(0.5)

    def can_instrument_now(self, same_url_again=False):
        if Logger.disabled(): return False
        if not self.selenium.is_page_loaded(): return False
        if self.selenium.current_url() is None: return False
        if self.current_url == self.selenium.current_url(): return same_url_again
        return True
