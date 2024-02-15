import time
import threading
import traceback
from IPython.display import clear_output, display
from NELL.Selenium import Selenium
from NELL.ai.ai_utils import get_open_ai_key
import NELL.logger.js_injector as injector
from NELL.logger.LogHttpServer import LogHttpHandler, LogHttpServer, LoggerHolder

class Mimic:

    instance = None
    
    def __init__(self):

        get_open_ai_key()
        if Mimic.instance is None:
            Mimic.instance = self

        self.events = []
        self.selenium = Selenium.instance()
        self.doppelganger = Selenium.instance("doppelganger")
        self.selenium_handles = set()
        self.doppelganger_handles = set()
        self.selenium_current_url = None
        self.doppelganger_current_url = None

        self.disabled = False 

        self.selenium.new_driver(url="http://google.com", restart=True)
        Mimic.log_event({
            'event':'new_driver', 
            'window_handle': self.selenium.driver.current_window_handle, 
            'url': self.selenium.driver.current_url
        }, True)

        self.check_browser(True)

        self.init_browser_monitoring()
        self.init_doppelganger_server()


    @staticmethod
    def log_event(event, reset=False):
        try:
            if event.get('is_clone'): return
            etype = event.get('event')

            if etype == 'new_driver': # open doppleganger window
                Mimic.singleton().doppelganger.new_driver(url=event.get('url'), restart=reset)
                return

            if etype == 'instrument': # main window
                handle = event.get('window_handle')
                Mimic.singleton().selenium_handles.add(handle)
                Mimic.singleton().selenium.driver.execute_script(injector.js)
                return


        finally:
            events=Mimic.singleton().events
            events.append(event)
            clear_output(wait=True)
            display(events)


    @classmethod
    def singleton(cls, reset=False):
        if cls.instance is None:
            cls.instance = Mimic()
        if reset: 
            cls.instance.events = []
        return cls.instance


    @classmethod
    def enable(cls): 
        cls.singleton().disabled = False

    @classmethod
    def disable(cls): 
        cls.singleton().disabled = True

    @classmethod
    def disabled(cls):
        return cls.singleton().disabled

    def init_browser_monitoring(self):
        clear_output(wait=True)
        browser_thread = threading.Thread(target=self.check_browser)
        browser_thread.daemon = True
        browser_thread.start()


    def init_doppelganger_server(self):
        clear_output(wait=True)
        server_thread = threading.Thread(target=start_doppelganger, args=(8000,))
        server_thread.daemon = True
        server_thread.start()


    def check_browser(self, halt=False):
        while True:
            if not self.is_page_ready():
                time.sleep(0.1)
                continue

            self.find_new_windows()

            self.selenium_current_url = self.selenium.driver.current_url
            self.doppelganger_current_url = self.doppelganger.current_url

            if halt: break
            time.sleep(0.5)


    def find_new_windows(self):
        if self.selenium.driver is None: return
        all_handles = self.selenium.driver.window_handles
        for h in all_handles:
            if self.selenium_handles.__contains__(h): continue
            if self.selenium.driver.current_url is None: continue

            self.selenium.driver.switch_to.window(h)     
            self.selenium_handles.add(h)
            Mimic.log_event(
                {'event':'instrument', 
                 'window_handle': h, 
                 'url': self.selenium.driver.current_url}
            )


    def is_page_ready(self, same_url_again=False):

        if Mimic.disabled(): return False
        
        if self.selenium is None: return False
        if self.selenium.driver is None: return False
        if self.selenium.driver.current_url is None: return False

        if not self.selenium.is_page_loaded(): return False

        if self.selenium_current_url == self.selenium.driver.current_url: 
            return same_url_again
        
        return True
    
    
def start_doppelganger(port):

    LoggerHolder.get(logger=Mimic)
    server = LogHttpServer(("", port), LogHttpHandler)
    with server as httpd:

        print(f"Doppelganging at port {port}")
        try:
            httpd.serve_forever()

        except KeyboardInterrupt:
            print("Doppelganger Stopped by User.")
            pass

        except Exception as e:
            traceback.print_exc()
            print(f"Doppelganger Start Error: {e}")

        finally:
            httpd.server_close()