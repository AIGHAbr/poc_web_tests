
import time
import threading
import traceback

from IPython.display import clear_output
from NELL.Selenium import Selenium
from NELL.gui.gui_events import data_changed, inspect_webpage
from NELL.gui.Window import Window

from NELL.logger.Logger import Logger
from NELL.logger.LogHttpServer import start_server

class Playground:

    def __init__(self):
        self.pageCounter = 0
        self.current_url = None
        self.last_instrumented_url = None
        self.selenium = Selenium.get('main')

        self.init_gui()
        Logger.log_event({'event':'test_env', 'framework': 'selenium'}, reset=True)
        
        self.init_logger_server()
        self.init_browser_monitoring()
      

    def init_gui(self):
        self.selenium.new_driver(restart=True)
        self.window = Window(data_changed)
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
            try:
                if not self.selenium.is_page_loaded():
                    time.sleep(0.1)
                    continue

                if self.selenium.current_url() is None: 
                    time.sleep(0.1)
                    continue

                if self.current_url == self.selenium.current_url():
                    time.sleep(0.1)
                    continue

                self.current_url = self.selenium.current_url()
                self.instrument_browser()

            except Exception as e:
                print(f"Exception: {e}")
                self.selenium.new_driver(restart=True)
                traceback.print_exc()

            time.sleep(0.5)

    def instrument_browser(self):
        try:
            self.selenium.execute_script("window.hasEventListeners=false;")
            inspect_webpage(self.selenium, self.window, self.window.table, self.window.properties)
            Logger.log_event({'event':'browser_info', 'url': self.selenium.current_url()})
            print(f"Instrumented: {self.selenium.current_url()}")
        
        except Exception as e:
            print(f"Exception: {e}")
            traceback.print_exc()

        finally:
            clear_output()
            self.window.redraw()
