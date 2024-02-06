import ipywidgets as widgets
from NELL.gui.GuiUtils import GuiUtils as gui

class ControlCenter:

    def __init__(self):

        self.url_input = gui.new_textfield(
            'Base URL:', 
            'https://life.stg.wellzesta.com/login'
        )
        
        self.test_name_input = gui.new_textfield(
            'Test Name:', 
            'Wellzesta Valid Login Test'
        )

        # self.test_description_input = gui.new_textarea(
        #     'Descrição do Teste:', 
        #     'Descreva o propósito do teste aqui'
        # )


        self.content = widgets.VBox([
            self.url_input,
            self.test_name_input,
            # self.test_description_input,

        ],layout=widgets.Layout(
            width='90%',
            overflow='hidden' 
        ))
