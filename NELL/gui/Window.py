import time
import ipywidgets as widgets
import NELL.gui.GuiUtils as gui

from IPython.display import clear_output, display
from NELL.Readme import readme
from NELL.ai.ai_utils import logs2robot
from NELL.gui.MyDataFrame import MyDataFrame
from NELL.gui.Properties import Properties
from NELL.gui.Table import Table
from NELL.gui.Tabs import Tabs


class Window():

    def __init__(self, on_data_changed):

        self.on_data_changed = on_data_changed
        dataframe = MyDataFrame(columns=["Alias", "Text", "Web", "Export", "Data", "Type", "Att"])
        
        _window = self
        def try_fire_data_changed_event(self, b=None):
            _window.on_data_changed(_window)
        self.table = Table(dataframe, try_fire_data_changed_event)

        self.properties = Properties()
        self.try_fire_data_changed_event = try_fire_data_changed_event
        self.table.data.set_change_listener(self.try_fire_data_changed_event) 

        # workshop
        mapping = gui.new_cell(self.table.content, width='350px', height='250px', scroll=True)
        props = gui.new_cell(self.properties.content, width='500px', height='250px', scroll=True)
        self.tabs = Tabs(mapping, props)
        self.workshop = widgets.VBox([self.tabs.content])

        # for Nell
        self.dev_n_qa = gui.new_cell(widgets.HTML(value=readme()), width='300px', height='660px', hiddable=True, visible=False)
        
        # content
        self.content = widgets.HBox([self.dev_n_qa, self.workshop])
        self.table.data_event = _window.properties.reload


    def redraw(self):
        clear_output()
        display(self.content, display_id="Playground")
        time.sleep(3)


    def reload(self, df=None, props={}):
        if df is None: return
        self.table.reload(df)
        self.table.data.set_change_listener(self.try_fire_data_changed_event)
        self.try_fire_data_changed_event()


    def on_tab_change(self, change):
        if change['new'] == 1: 
            current_logs = "<br/>\n".join(self.tab_event_logs.children[0].value)
            if current_logs != self.last_log_sent: 
                self.last_log_sent = current_logs
                robot_script = logs2robot(current_logs)
                self.tab_robot.children = [widgets.Textarea(
                                                value=robot_script, 
                                                layout=widgets.Layout(
                                                width='100%', 
                                                height='100%',
                                                border='1px solid white'
                                            ))] 