import ipywidgets as widgets

from IPython.display import display
from NELL.Readme import readme
from NELL.Selenium import Selenium
from NELL.logger.Logger import Logger
from NELL.gui.GuiUtils import GuiUtils as gui
from NELL.gui.Tabs import Tabs

class Window():

    def __init__(self):

        # workshop
        self.tabs = Tabs()

        self.workshop = widgets.VBox([self.tabs.content]
            ,layout=widgets.Layout(
                width='98%',
                overflow='hidden' 
            ))

        # buttons
        self.start_button = gui.new_button('Star Logs', 'success', 'play')  
        self.stop_button = gui.new_button('Pause Logs', 'warning', 'pause')
        self.delete_button = gui.new_button('Delete Logs', 'danger', 'trash')
        self.buttons = widgets.HBox([self.start_button, self.stop_button, self.delete_button])
        self.stop_button.disabled = True   
        self.start_button.on_click(self.start_recording)
        self.stop_button.on_click(self.stop_recording)
        self.delete_button.on_click(self.delete_logs)

        # for Nell
        self.dev_n_qa = gui.new_cell(widgets.HTML(value=readme()), width='300px', height='660px', hiddable=True, visible=False)
        
        # content
        self.content = widgets.HBox([self.dev_n_qa, widgets.VBox([self.workshop, self.buttons],
                                     layout=widgets.Layout(width='98%',overflow='hidden'))])


    def start_recording(self, b=None):
        if self.start_button.disabled: return

        self.start_button.disabled = True
        self.stop_button.disabled = False
        self.tabs.content.selected_index = 1

        Logger.enable()
        Logger.log_event({'info':'start log events'}, reset=True)
        Logger.log_event({'info':'selenium framework'})

        url = self.tabs.control_center.url_input.value
        Selenium.instance().new_driver(url)


    def stop_recording(self, b):
        if self.stop_button.disabled: return

        self.stop_button.disabled = True
        self.start_button.disabled = False
        Logger.log_event({'info':'stop log events'})
        Logger.disable()


    def delete_logs(self, b):
        self.tabs.content.selected_index = 1
        Logger.enable()
        Logger.log_event({'info':'clear logs'}, True)
        if self.start_button.disabled:
            Logger.disable()


    def redraw(self):
        # clear_output()
        display(self.content, display_id="Playground")
        # time.sleep(3)


    def reload(self, df=None):
        if df is None: return
        self.tabs.tab_qa.reload(df)