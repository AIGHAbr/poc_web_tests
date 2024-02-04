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


        self.content = widgets.VBox([
            self.url_input,
            self.test_name_input,
            self.test_description_input,

        ],layout=widgets.Layout(
            width='90%',
            overflow='hidden' 
        ))
