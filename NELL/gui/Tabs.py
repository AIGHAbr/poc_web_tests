
import ipywidgets as widgets
from NELL.gui.gui_utils import new_cell
from NELL.logger.LogHttpServer import Logger

class Tabs():
    
    def __init__(self):
        self.content = widgets.Tab()
        self.content.observe(self.on_tab_change, 'selected_index')
        
        self.htmlLogs = widgets.HTML()
        self.tab_event_logs = new_cell(self.htmlLogs, width='900px', height='400px')
        self.tab_robot = new_cell(widgets.HTML(), width='900px', height='400px', border='0px solid white')
        self.tab_buddy = new_cell(widgets.HTML(), width='900px', height='400px')
        
        self.content.children = [self.tab_event_logs, self.tab_robot, self.tab_buddy]
        self.content.set_title(0, 'Event Logger')
        self.content.set_title(1, 'Robot') 
        self.content.set_title(2, 'Buddy')

        Logger.add_event_logger_listener(
            lambda event, events: self.log_event(event, events))


    def log_event(self, event, events):

        evets = []
        for evt in events:
            evets.append(str(evt))

        self.htmlLogs.value="<br/>\n".join(evets)
        print(events)


    def on_tab_change(self, change):
        pass
        # if change['new'] == 1: 
        #     current_logs = "<br/>\n".join(self.tab_event_logs.children[0].value)
        #     if current_logs != self.last_log_sent: 
        #         self.last_log_sent = current_logs
        #         robot_script = logs2robot(current_logs)
        #         self.tab_robot.children = [widgets.Textarea(
        #                                         value=robot_script, 
        #                                         layout=widgets.Layout(
        #                                         width='100%', 
        #                                         height='100%',
        #                                         border='1px solid white'
        #                                     ))] 