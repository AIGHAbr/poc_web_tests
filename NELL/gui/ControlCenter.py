import os
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

        self.openai_key_input = gui.new_textfield(
            'OpenAI Key:', 
            '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'
        )
        self.set_openai_key(self.openai_key_input.value)
        self.openai_key_input.blur = lambda _: self.set_openai_key(self.openai_key_input.value)

        self.content = widgets.VBox([
            self.url_input,
            self.test_name_input,
            self.openai_key_input
            # self.test_description_input,

        ],layout=widgets.Layout(
            width='90%',
            overflow='hidden' 
        ))

    def set_openai_key(self, key):
        os.environ["OPENAI_API_KEY"]=key
