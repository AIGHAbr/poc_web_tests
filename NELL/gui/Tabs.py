
import ipywidgets as widgets

from NELL.gui.GuiUtils import GuiUtils as gui
from NELL.gui.ControlCenter import ControlCenter
from NELL.logger.LogHttpServer import Logger

class Tabs():
    
    def __init__(self, mapping, props):

        self.content = widgets.Tab()
        self.tab_tests = gui.new_cell(widgets.HBox([mapping, props]), width='98%', height='400px')
        self.control_center = ControlCenter()
        self.tabs_control = gui.new_cell(self.control_center.content, width='98%', height='400px', border='0px solid white')
        self.htmlLogs = widgets.HTML()
        self.tab_event_logs = gui.new_cell(self.htmlLogs, width='98%', height='400px', scroll=True)
        self.tab_robot = gui.new_cell(widgets.HTML(), width='98%', height='400px', border='0px solid white')
        # self.tab_buddy = new_cell(widgets.HTML(), width='900px', height='400px')
        
        self.content.children = [self.tabs_control,
                                 self.tab_event_logs, 
                                 self.tab_tests, 
                                 self.tab_robot]
        
        self.content.set_title(0, 'Test Control Center')
        self.content.set_title(1, 'Event Journal')
        self.content.set_title(2, 'Quality Assurance')
        self.content.set_title(3, 'Robot Framework') 
        # self.content.set_title(2, 'Buddy')

        Logger.add_event_logger_listener(
            lambda event, events: self.log_event(event, events))

        #self.content.observe(self.on_tab_change, 'selected_index')


    def log_event(self, event, events):

        evets = []
        for evt in events:
            evets.append(str(evt))

        self.htmlLogs.value="<br/>\n".join(evets)
        print(events)