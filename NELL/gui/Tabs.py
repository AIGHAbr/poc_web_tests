import asyncio
import threading
import ipywidgets as widgets

from NELL.ai.ai_utils import generate_robot
from NELL.logger.LogHttpServer import Logger
from NELL.gui.GuiUtils import GuiUtils as gui
from NELL.gui.ControlCenter import ControlCenter
from NELL.gui.QualityAssurance import QualityAssurance

class Tabs():
    
    def __init__(self):

        height = '600px'
        self.animating = False
        self.content = widgets.Tab()
        self.tab_qa = QualityAssurance()
        self.control_center = ControlCenter()
        self.tabs_control = gui.new_cell(self.control_center.content, width='98%', height=height, border='0px solid white')
        self.htmlLogs = widgets.HTML()
        self.tab_event_logs = gui.new_cell(self.htmlLogs, width='98%', height=height, scroll=True)

        self.txt_robot01 = widgets.Textarea(
            layout=widgets.Layout(
                width='49%', 
                height='564px',  
                overflow='auto'
            )
        )

        self.txt_robot02 = widgets.Textarea(
            layout=widgets.Layout(
                width='49%', 
                height='564px',  
                overflow='auto'
            )
        )

        self.txt_robot = widgets.HBox([self.txt_robot01, self.txt_robot02])
        self.btn_robot = widgets.Button(description='Run AI', button_style='info')
        self.tab_robot = widgets.VBox([self.btn_robot, self.txt_robot])
        self.btn_robot.on_click(lambda _: self.on_click_ai())
        

        self.content.children = [
            self.tabs_control,
            self.tab_event_logs, 
            gui.new_cell(self.tab_qa.content, width='98%', height=height, border='0px solid white'), 
            self.tab_robot 
        ]
        
        self.content.set_title(0, 'Configuration')
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

        if self.animating:
            self.txt_robot01.value = "I'm working, relax Man!\n" + self.txt_robot01.value
            self.txt_robot02.value = "Idem!\n" + self.txt_robot02.value
            return

        if len(Logger.all_events())<3:
            self.txt_robot01.value = "Not enough logs to generate scripts!\n" + self.txt_robot01.value
            self.txt_robot02.value = "Idem!\n" + self.txt_robot02.value
            return

        current_logs = self.htmlLogs.value
        try: 
            if current_logs == self.last_log_sent: return
        except AttributeError:
            self.last_log_sent = current_logs

        self.start_running_feedback()
        threading.Thread(target=self.generate_scripts, args=(current_logs,), daemon=True).start()


    def generate_scripts(self, logs):
        robot_script = None
        try:
            robot_script = generate_robot(logs)
            print(robot_script)

        except Exception as ex:
            self.txt_robot01.value = ex.error
            self.txt_robot02.value = ""
            self.animating = False
            self.txt_robot.disabled = False
            self.btn_robot.disabled = False
            return

        def update_ui():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            async def async_update_ui():
                try:
                    scripts = robot_script.split('<inicio testsuit.robot>')
                    if len(scripts) == 1 or len(scripts) >2:
                        scripts = robot_script.split('===')

                    script1 = scripts[0].replace("<inicio keyword.resource>", "").replace("<fim keyword.resource>", "").replace("===", "")
                    script2 = scripts[1].replace("<inicio testsuit.robot>", "").replace("<fim testsuit.robot>'", "").replace("===", "")
                    
                    self.txt_robot01.value = '*** Keywords.Resources ***\n\n' + script1.lstrip()
                    self.txt_robot02.value = '*** TestSuit.Robot ***\n\n' + script2.lstrip()
                    
                except:
                    self.txt_robot01.value = robot_script
                    self.txt_robot02.value = ''

                self.stop_running_feedback()

            loop.run_until_complete(async_update_ui())
            loop.close()

        update_ui()


    async def animate_button(self, interval=0.5):
        self.animating = True
        animations = ['Running', '.Running.', '..Running..', '...Running...', 
                      '....Running....', '...Running...', '..Running..', '.Running.']
        while self.animating: 
            for anim in animations:
                if not self.animating: break
                self.btn_robot.description = anim
                await asyncio.sleep(interval)

        self.btn_robot.description = 'Run AI'
        self.btn_robot.disabled = False
        self.txt_robot.disabled = False


    def start_running_feedback(self):
        self.txt_robot.disabled = True
        self.btn_robot.disabled = True
        asyncio.create_task(self.animate_button(0.2))


    def stop_running_feedback(self):
        self.animating = False
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.run_coroutine_threadsafe(self.update_button(), loop)
            return


    async def update_button(self):
        self.txt_robot.disabled = False
        self.btn_robot.disabled = False