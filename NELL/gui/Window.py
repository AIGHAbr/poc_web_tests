import ipywidgets as widgets
from IPython.display import display
from NELL.Readme import readme
from NELL.Selenium import Selenium
from NELL.gui.QualityAssurance import QualityAssurance
from NELL.logger.Logger import Logger
from NELL.gui.GuiUtils import GuiUtils as Gui
from NELL.gui.Tabs import Tabs


class Window:

    def __init__(self):

        self.current_url = None

        # workshop
        self.tabs = Tabs()
        self.tabs.window = self
        self.workshop = widgets.VBox([self.tabs.content]
                                     , layout=widgets.Layout(
                width='98%',
                overflow='hidden'
            ))

        # buttons
        self.start_button = Gui.new_button('Star Logs', 'success', 'play')
        self.stop_button = Gui.new_button('Pause Logs', 'warning', 'pause')
        self.delete_button = Gui.new_button('Delete Logs', 'danger', 'trash')
        self.buttons = widgets.HBox([self.start_button, self.stop_button, self.delete_button])
        self.stop_button.disabled = True
        self.delete_button.disabled = True
        self.start_button.on_click(self.start_recording)
        self.stop_button.on_click(self.stop_recording)
        self.delete_button.on_click(self.delete_logs)

        # for Nell
        self.dev_n_qa = Gui.new_cell(widgets.HTML(value=readme()), width='300px', height='660px', can_hide=True, visible=False)

        # content
        self.content = widgets.HBox([self.dev_n_qa, widgets.VBox([self.workshop, self.buttons],layout=widgets.Layout(width='98%', overflow='hidden'))])


    def start_recording(self, b=None):
        if self.start_button.disabled: return

        self.start_button.disabled = True
        self.stop_button.disabled = False
        self.delete_button.disabled = False

        url = self.tabs.control_center.url_input.value
        Selenium.instance().new_driver(url)

        Logger.enable()
        Logger.log_event({'info': 'start log events'}, reset=True)
        Logger.log_event({'info': 'selenium framework'})

        self.tabs.content.selected_index = 1


    def stop_recording(self, b=None):
        if self.stop_button.disabled: return

        self.stop_button.disabled = True
        self.start_button.disabled = False
        Logger.log_event({'info': 'stop log events'})
        Logger.disable()

        self.tabs.content.selected_index = 1


    def delete_logs(self, b=None):
        if self.delete_button.disabled: return

        self.delete_button.disabled = True
        self.stop_button.disabled = True
        self.start_button.disabled = False
        self.current_url = None
        self.tabs.reset_qa()

        Logger.reset_logs()
        Logger.enable()
        Logger.log_event({'info': 'delete log events'})
        Logger.disable()

        self.tabs.content.selected_index = 1


    def redraw(self):
        display(self.content, display_id="Playground")


    def reload(self, page_id, page_url, df, html):
        self.tabs.reload(page_id, page_url, df, html)