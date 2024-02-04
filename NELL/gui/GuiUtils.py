import ipywidgets as widgets

from NELL.gui.WidgetController import WidgetController

class GuiUtils():

    @staticmethod
    def new_cell(content, width='100%', height='100%', scroll=False, 
                border='5px solid white', hiddable=False, visible=True):
        
        cell_box = widgets.Box([content], layout=widgets.Layout(
            border=border,
            width=width,
            height=height,
            overflow='auto' if scroll else 'hidden'
        )) 
        if not hiddable: return cell_box
        
        btnShowHide = widgets.Button(description='x')
        btnShowHide.layout.width = '30px'
        btnShowHide.layout.height = '30px'
        controller = WidgetController(cell_box)
        
        def toggle_visibility(b):
            if btnShowHide.description == 'x':
                btnShowHide.description = '+'
                controller.hideWidget()
                return
            
            btnShowHide.description = 'x'
            controller.showWidget()

        btnShowHide.on_click(toggle_visibility)
        result = widgets.VBox([btnShowHide, cell_box])

        if not visible: 
            controller.hideWidget()
            btnShowHide.description = '+'

        return result
    
    @staticmethod
    def new_textfield(description, value=None, 
                        width='100%', height='30px', border='5px solid white'):
        return widgets.Text(
            value=value,
            description=description,
            style={'description_width': 'initial'},
            layout=widgets.Layout(
                width=width,
                height=height,
                border=border
            )
        )

    @staticmethod
    def new_textarea(description, value=None,
                            width='100%', height='100px', border='5px solid white'):
        return widgets.Textarea(
            value=value,
            description=description,
            style={'description_width': 'initial'},
            layout=widgets.Layout(
                width=width,
                height=height,
                border=border
            )
        )
    
    @staticmethod
    def new_divider(width='100%', border='5px solid white'):
        
        return widgets.HTML(
            '<hr>',
            layout=widgets.Layout(
                width=width,
                border=border
            )
        )

    @staticmethod
    def new_button(description, button_style, icon):
        button = widgets.Button(
            description=description,
            button_style=button_style,
            icon=icon
        )
        return button