
import ipywidgets as widgets
from NELL.ai.ai_utils import generate_robot

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
        self.tab_robot = widgets.HTML()
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
        
        self.content.observe(self.on_tab_change, 'Robot Framework')


    def log_event(self, event, events):

        evets = []
        size = len(events)
        for i, evt in enumerate(reversed(events), start=1):
            j = size - i
            evets.append(f"{j}. {str(evt)}")

        self.htmlLogs.value="<br/>\n".join(evets)
        print(events)


    def on_tab_change(self, change):
        if change['new'] == 3: 
            current_logs = "<br/>\n".join(self.tab_event_logs.children[0].value)
            if current_logs != self.last_log_sent: 
                self.last_log_sent = current_logs
                robot_script = generate_robot(current_logs)
                self.tab_robot.children = [widgets.Textarea(
                                                value=robot_script, 
                                                layout=widgets.Layout(
                                                width='100%', 
                                                height='100%',
                                                border='1px solid white'
                                            ))] 
