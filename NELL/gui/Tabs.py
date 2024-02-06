import asyncio
import threading
import ipywidgets as widgets

from NELL.ai.ai_utils import generate_robot
from NELL.gui.GuiUtils import GuiUtils as gui
from NELL.gui.ControlCenter import ControlCenter
from NELL.logger.LogHttpServer import Logger

class Tabs():
    
    def __init__(self, mapping, props):
        height = '600px'
        self.content = widgets.Tab()
        self.tab_tests = gui.new_cell(widgets.HBox([mapping, props]), width='98%', height=height)
        self.control_center = ControlCenter()
        self.tabs_control = gui.new_cell(self.control_center.content, width='98%', height=height, border='0px solid white')
        self.htmlLogs = widgets.HTML()
        self.tab_event_logs = gui.new_cell(self.htmlLogs, width='98%', height=height, scroll=True)
        

        self.txt_robot = widgets.Textarea(
            layout=widgets.Layout(
                width='99%', 
                height=height,  
                overflow='auto'
            )
        )

        self.btn_robot = widgets.Button(description='Run AI', button_style='info')
        self.tab_robot = widgets.VBox([self.btn_robot, self.txt_robot])
        self.btn_robot.on_click(lambda _: self.on_click_ai())
        

        self.content.children = [
            self.tabs_control,
            self.tab_event_logs, 
            self.tab_tests, 
            self.tab_robot 
        ]
        
        self.content.set_title(0, 'Test Control Center')
        self.content.set_title(1, 'Event Journal')
        self.content.set_title(2, 'Quality Assurance')
        self.content.set_title(3, 'Robot Framework')

        self.last_log_sent = None

        Logger.add_event_logger_listener(
            lambda event, events: self.log_event(event, events))
        
        self.tab_robot.disabled = True


    def log_event(self, event, events):

        event_list = []
        size = len(events)
        for i, evt in enumerate(reversed(events), start=1):
            j = size - i
            event_list.append(f"{j}. {str(evt)}")

        self.htmlLogs.value = "<br/>\n".join(event_list)
        print(events)


    def on_click_ai(self):
        if len(Logger.all_events())<3:
            self.txt_robot.value = "Not enough logs to generate scripts!\n" + self.txt_robot.value
            return

        current_logs = self.htmlLogs.value
        try: 
            if current_logs == self.last_log_sent: return
        except AttributeError:
            self.last_log_sent = current_logs

        self.start_running_feedback()
        threading.Thread(target=self.generate_scripts, args=(current_logs,), daemon=True).start()


    def generate_scripts(self, logs):
        robot_script = generate_robot(logs)
        def update_ui():
            self.txt_robot.value = robot_script
            self.stop_running_feedback()
        asyncio.run_coroutine_threadsafe(update_ui(), asyncio.get_event_loop())


    async def animate_button(self, interval=0.5):
        animations = ['Running', 'Running.', 'Running..', 'Running...']
        while self.btn_robot.disabled: 
            for anim in animations:
                if not self.btn_robot.disabled: break
                self.btn_robot.description = anim
                await asyncio.sleep(interval)
        self.btn_robot.description = 'Run AI'


    def start_running_feedback(self):
        self.txt_robot.disabled = True
        self.btn_robot.disabled = True
        self.btn_robot.button_style = 'warning'
        asyncio.create_task(self.animate_button(0.5))


    def stop_running_feedback(self):
        def update_button():
            self.txt_robot.disabled = False
            self.btn_robot.disabled = False
            self.btn_robot.button_style = 'info'
        asyncio.run_coroutine_threadsafe(update_button(), asyncio.get_event_loop())