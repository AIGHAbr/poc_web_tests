import time
import threading
from IPython.display import clear_output
from NELL.Selenium import Selenium
from NELL.ai.ai_utils import get_open_ai_key
from NELL.logger.LogHttpServer import start_doppelganger
from NELL.logger.MimicControls import MimicControls


class Mimic:

    def __init__(self):
        get_open_ai_key()
        self.selenium = Selenium.instance()
        self.doppelganger = Selenium.instance("doppelganger")

        self.selenium_handles = set()
        self.doppelganger_handles = set()

        self.selenium_current_url = None
        self.doppelganger_current_url = None

        self.init_browser_monitoring()
        self.init_doppelganger_server()

        time.sleep(5)
        self.selenium.new_driver(url="http://google.com", restart=True)
        MimicControls.log_event({
            'event':'new_driver', 
            'window_handle': self.selenium.driver.current_window_handle, 
            'url': self.selenium.driver.current_url
        })        



    def init_browser_monitoring(self):
        clear_output(wait=True)
        browser_thread = threading.Thread(target=self.check_browser)
        browser_thread.daemon = True
        browser_thread.start()


    def init_doppelganger_server(self):
        clear_output(wait=True)
        server_thread = threading.Thread(target=start_doppelganger, args=(9000,))
        server_thread.daemon = True
        server_thread.start()


    def check_browser(self):
        while True:
            if not self.is_page_ready():
                time.sleep(0.1)
                continue

            self.selenium_current_url = self.selenium.driver.current_url
            self.doppelganger_current_url = self.doppelganger.current_url
            self.try_instrument_webpage()       

            time.sleep(0.5)


    def try_instrument_webpage(self):
        if self.selenium.driver is None: return
        all_handles = self.selenium.driver.window_handles
        for h in all_handles:
            if self.selenium_handles.__contains__(h): continue
            if self.selenium.driver.current_url is None: continue

            self.selenium.driver.switch_to.window(h)     
            self.selenium_handles.add(h)
            MimicControls.log_event(
                {'event':'instrument', 
                 'window_handle': h, 
                 'url': self.selenium.driver.current_url}
            )


    def is_page_ready(self, same_url_again=False):

        if MimicControls.disabled(): return False
        
        if self.selenium is None: return False
        if self.selenium.driver is None: return False
        if self.selenium.driver.current_url is None: return False

        if not self.selenium.is_page_loaded(): return False

        if self.selenium_current_url == self.selenium.driver.current_url: 
            return same_url_again
        
        return True