import os
import ipywidgets as widgets
from NELL.gui.GuiUtils import GuiUtils as Gui


class ControlCenter:

    def __init__(self):
        os.environ["OPENAI_API_KEY"] = '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'

        self.url_input = Gui.new_textfield(
            'Base URL:',
            'https://active.stg.wellzesta.com/'
        )

        self.test_name_input = Gui.new_textfield(
            'Test Name:',
            'Wellzesta Valid Login Test'
        )

        self.content = widgets.VBox([
            self.url_input,
            self.test_name_input,
            # self.openai_key_input
            # self.test_description_input,

        ], layout=widgets.Layout(
            width='90%',
            overflow='hidden'
        ))

    # @staticmethod
    # def set_openai_key():
    #     global openai_key_input
