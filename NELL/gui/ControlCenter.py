import ipywidgets as widgets
from NELL.Selenium import Selenium
from NELL.gui.GuiUtils import GuiUtils as gui
from NELL.logger.Logger import Logger

class ControlCenter:

    def __init__(self):

        self.url_input = gui.new_textfield(
            'URL Inicial:', 
            'https://life.stg.wellzesta.com/login'
        )
        
        self.test_name_input = gui.new_textfield(
            'Nome do Teste:', 
            'Nome do Teste'
        )

        self.test_description_input = gui.new_textarea(
            'Descrição do Teste:', 
            'Descreva o propósito do teste aqui'
        )

        self.start_button = gui.new_button(
            'Iniciar Gravação', 'success', 'play'
        )
        self.start_button.on_click = self.start_recording
        
        self.stop_button = gui.new_button(
            'Parar Gravação', 'danger', 'stop'
        )
        self.stop_button.disabled = True       

        self.content = widgets.VBox([
            self.url_input,
            self.test_name_input,
            self.test_description_input,
            gui.new_divider(),
            widgets.HBox([self.start_button, self.stop_button])

        ],layout=widgets.Layout(
            width='90%',
            overflow='hidden' 
        ))

    def start_recording(self):
        Logger.enable()
        Logger.log_event({'info':'selenium framework'}, reset=True)
        Selenium.singleton().get(self.url_input.value)

