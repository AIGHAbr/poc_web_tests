import datetime
from bs4 import BeautifulSoup, Tag
from NELL.Selenium import Selenium

class Snapshoter:

    def __init__(self, logger):
        self.current = None
        self.last = None

        self.current_url = None
        self.last_url = None

        self.snapshot_ids = {} 
        self.next_id = 1
        self.selenium = Selenium.instance()

        self.logger = logger
        self.logger.add_event_logger_listener(
            lambda event, events: self.log_event(event))


    def log_event(self, event):

        evType =  event.get("event", None)
        if evType == None: return

        self.last_url = self.current_url
        self.current_url = self.selenium.current_url()

        html = self.selenium.driver.page_source.encode("utf-8")
        if self.last == None:
            self.last = html
            self.current = html
            self.take_snapshot(html)
            return

        if self.last_url != self.current_url: return
        if self.current == html: return

        self.last = self.current
        self.current = html
        self.take_snapshot(html)

        diffs = self.compare_snapshots(self.last, self.current)
        for diff in diffs:
            self.logger.log_event(diff)
        

    def take_snapshot(self, html):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        snapshot_id = self.next_id
        self.next_id += 1
   
        event = {
            'info': 'page src snapshot',
            'id': f"snapshot_{snapshot_id}",
            'timestamp': timestamp
        }

        self.logger.log_event(event)
        return (html, timestamp)   


    def compare_snapshots(self, last_html, current_html):
        soup1 = BeautifulSoup(last_html, 'html.parser')
        soup2 = BeautifulSoup(current_html, 'html.parser')
        diffs = self.compare_elements(soup1.body, soup2.body)
        return diffs


    def compare_elements(self, elem1, elem2):
        diffs = []

        selenium = Selenium.instance()

        if elem1.name != elem2.name: 
            return diffs

        for attr1, value1 in elem1.attrs.items():
            value2 = elem2.attrs.get(attr1)
            if value1 != value2:
                xpath = selenium.generate_selector(elem1)

                if attr1 == 'class':
                    classes_from = set(value1 if isinstance(value1, list) else value1.split())
                    classes_to = set(value2 if isinstance(value2, list) else value2.split())
                    added_classes = classes_to - classes_from
                    removed_classes = classes_from - classes_to

                    diffs.append({
                        'change': 'html class',
                        'tagName': elem1.name,
                        'attribute': attr1,
                        'added': list(added_classes),
                        'removed': list(removed_classes),
                        'xpath': xpath
                    })
                    continue

                diffs.append({
                    'change': 'html attribute',
                    'tagName': elem1.name,
                    'attribute': attr1,
                    'value_from': value1,
                    'value_to': value2 if value2 else 'N/A',
                    'xpath': xpath
                })

        for attr2, value2 in elem2.attrs.items():
            if attr2 not in elem1.attrs:
                xpath = selenium.generate_selector(elem2)
                diffs.append({
                    'change': 'html attribute addition',
                    'tagName': elem2.name,
                    'attribute': attr2,
                    'value': value2,
                    'xpath': xpath
                })

        for child1, child2 in zip(elem1.children, elem2.children):
            if isinstance(child1, Tag) and isinstance(child2, Tag):  
                child_diffs = self.compare_elements(child1, child2)
                diffs.extend(child_diffs)

        return diffs
