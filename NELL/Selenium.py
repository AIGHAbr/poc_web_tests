import re
import time
import traceback
from bs4 import BeautifulSoup
from collections import defaultdict
from xml.sax.saxutils import quoteattr
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from NELL.gui.MyDataFrame import MyDataFrame
import NELL.logger.js_injector as injector

class Selenium:

    instances = {}

    @staticmethod
    def instance(name="main"):
        if name not in Selenium.instances:
            Selenium.instances[name] = Selenium()
        return Selenium.instances[name]

    def driver(self):
        self.driver


    def __init__(self):
        self.driver = None
        prefs = {"profile.default_content_setting_values.notifications": 1}
        self.chrome_options = Options()
        #self.chrome_options.add_argument("--headless")
        self.chrome_options.add_experimental_option("prefs", prefs)
        self.chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
        self.service = Service(ChromeDriverManager().install())
        

    def is_page_loaded(self):
        try: 
            if self.driver is None:
                return self.driver.execute_script("return document.readyState;") == "complete"     
            return self.driver.execute_script("return document.readyState;") == "complete" 
        except: 
            return False


    def is_logging_instrumented(self):
        try: return self.driver.execute_script("return window.hasEventListeners === true;")
        except: return False


    def execute_script(self, script):
        try: 
            return self.driver.execute_script(script)
        except Exception as e: 
            print("Error while executing the script:", e)
            traceback.print_exc()


    def new_driver(self, url="http://www.google.com", restart=False):
        if restart:
            try: self.driver.quit()
            except: self.driver = None

        self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
        self.driver.get(url)
        while not self.is_page_loaded(): time.sleep(0.1)
        return self.driver
    
    
    def highlight_element(self, selector):
            
        script = f"""
        var element = document.evaluate('{selector}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        if (element) {{
            var originalStyle = element.style.border;
            var count = 0;
            var interval = setInterval(function() {{
                count += 1;
                element.style.border = count % 2 ? '3px solid red' : '';
                if (count > 9) {{
                    clearInterval(interval);
                    element.style.border = originalStyle;
                }}
            }}, 500);
        }}
        """
        try:
            self.driver.execute_script(script)
        except Exception as e:
            print("Error while highlighting the element:", e)


    # generate keys
    def generate_key(self, tag, element, counter):
        base = {"input": "txt", "button": "btn", "a": "lnk", "img": "img"}
        prefix = base.get(tag, "elem")

        parts = [prefix]

        if element.get('id'):
            parts.append(element['id'])
            return self.key_builder(parts, counter)
        
        txt = element.get_text(strip=True)
        if txt:
            parts.append(txt.replace(" ", "_"))
            return self.key_builder(parts, counter)
        
        if element.get('name'):
            parts.append(element['name'])
            return self.key_builder(parts, counter)
        
        if element.get('aria-label'):
            parts.append(element['aria-label'].replace(" ", "_"))
            return self.key_builder(parts, counter)
        
        if element.get('data-test-id'):
            parts.append(element['data-test-id'])
            return self.key_builder(parts, counter)
        
        return self.key_builder(parts, counter)


    def key_builder(self, parts, counter):
        key = '_'.join(filter(None, parts)).lower().replace("-", "_")
        counter[key] += 1
        return key if counter[key] == 1 else f"{key}_{counter[key]}"


    # Generate Selectors
    def generate_selector(self, element):
        selectors = []

        for attr in ['id', 'name', 'placeholder', 'aria-label', 'data-test-id', 'alt']:
            v = element.get(attr, None)
            if v == None: continue
            selectors.append(f"@{attr}={quoteattr(v)}")
            if attr == 'id': break

        if len(selectors)>0:
            xpath_selector = f"//{element.name}[{' and '.join(selectors)}]"
            elements_found = self.driver.find_elements("xpath", xpath_selector)
            if len(elements_found) == 1:
                return xpath_selector

        txt = element.get_text(strip=True)
        if txt:
            xpath_selector = f"//{element.name}[contains(text(), {quoteattr(txt)})]"
            elements_found = self.driver.find_elements("xpath", xpath_selector)
            if len(elements_found) == 1:
                return xpath_selector

        if element.get('class'):
            classes = '.'.join(element.get('class'))
            xpath_selector = f"//{element.name}[contains(@class, {quoteattr(classes)})]"
            elements_found = self.driver.find_elements("xpath", xpath_selector)
            if len(elements_found) == 1:
                return xpath_selector

        return self.bs4_xpath(element)


    def bs4_xpath(self, element):
        components = []
        child = element if element.name else element.parent
        while child is not None:
            if child.name is None: break
        
            if 'id' in child.attrs:
                components.append(f"[@id='{child.attrs['id']}']")
                break

            siblings = []
            try: siblings = [sib for sib in child.parent.find_all(child.name, recursive=False) if sib is not None]
            except: pass

            if len(siblings) > 1:
                index = siblings.index(child) + 1
                components.append(f"{child.name}[{index}]")
                child = child.parent
                continue

            components.append(child.name)
            child = child.parent

        components.reverse()
        return "//*"+'/'.join(components)
    


    # read page objects
    def read_page_objects_metadata(self):

        html = self.driver.page_source.encode("utf-8")
        soup = BeautifulSoup(html, 'html.parser')
        elements = soup.find_all(['input', 'button', 'a', 'img'])

        counter = defaultdict(int)
        result = defaultdict(list)

        for element in elements:
            tag = element.name
            selector = self.generate_selector(element)
            key = self.generate_key(tag, element, counter)

            result[tag].append({
                "key": key,
                "selector": selector,
                "attributes": {attr: element.get(attr) for attr in element.attrs},
                "text": element.get_text(strip=True),
                "visibility": "visible" if element.get('type') != 'hidden' else "invisible"
            })
        return result
    
    
    def current_url(self):
        if self.driver is None: return None
        return self.driver.current_url
    

    def instrument_webpage(self, window):

        global selectors
        metadata = self.read_page_objects_metadata()
        selectors = {}
        rows = []

        for tag_name, elements in metadata.items():
            for element in elements:

                att = element.pop('attributes', {})
                clazz =  att.pop('class', [])

                for k, v in att.items():
                    element[k] = v

                element['class'] = clazz
                key = element.get('key', '')
                selector = element.get('selector', '')
                       
                rows.append({
                    "Export": False,
                    "Alias": key,
                    "key": key,
                    "Web": selector,
                    "Type": tag_name,
                    "Data": element
                })
                
                selector = selector.replace('"', "'")  
                js = f"""
                        var e01 = document.evaluate("{selector}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        if (e01) e01.setAttribute('key','{key}');
                """ 

                self.execute_script(js)
                selectors[key]=selector


        window.reload(MyDataFrame(rows))
        self.execute_script(injector.js)