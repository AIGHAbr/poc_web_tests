import threading
import time
from IPython.display import clear_output
from NELL.Selenium import Selenium, try_instrument_webpage
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

        self.init_gui()
        Logger.log_event({'info': 'selenium framework'}, reset=True)

        self.init_logger_server()
        self.init_browser_monitoring()

    def init_gui(self):
        Selenium.instance().new_driver(restart=True)
        self.window.redraw()

    def init_browser_monitoring(self):
        browser_thread = threading.Thread(target=self.check_browser)
        browser_thread.daemon = True
        browser_thread.start()

    @staticmethod
    def init_logger_server():
        server_thread = threading.Thread(target=start_server, args=(8000,))
        server_thread.daemon = True
        server_thread.start()

    def check_browser(self):
        while True:
            if not self.can_instrument_now():
                time.sleep(0.1)
                continue

            clear_output()
            self.window.redraw()
            self.window.current_url = Selenium.instance().current_url()

            event = Logger.log_event({'info': 'page loaded', 'url': self.window.current_url})
            try_instrument_webpage(Selenium.instance(), self.window, event['page_id'], self.window.current_url)
            time.sleep(0.5)

    def can_instrument_now(self, same_url_again=False):
        if Logger.disabled(): return False
        if not Selenium.instance().is_page_loaded(): return False
        if Selenium.instance().current_url() is None: return False
        if self.window.current_url == Selenium.instance().current_url(): return same_url_again
        return True