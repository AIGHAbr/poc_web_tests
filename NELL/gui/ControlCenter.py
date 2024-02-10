import os
import ipywidgets as widgets
from NELL.gui.GuiUtils import GuiUtils as gui

class ControlCenter:
    global openai_key_input
    openai_key_input = None


    def __init__(self):

        os.environ["OPENAI_API_KEY"]='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'

        self.url_input = gui.new_textfield(
            'Base URL:', 
            'https://life.stg.wellzesta.com/login'
        )
        
        self.test_name_input = gui.new_textfield(
            'Test Name:', 
            'Wellzesta Valid Login Test'
        )    

        self.content = widgets.VBox([
            self.url_input,
            self.test_name_input,
            # self.openai_key_input
            # self.test_description_input,

        ],layout=widgets.Layout(
            width='90%',
            overflow='hidden' 
        ))


    # @staticmethod
    # def set_openai_key():
    #     global openai_key_input