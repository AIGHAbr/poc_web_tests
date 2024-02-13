import ipywidgets as widgets
from NELL.gui.WidgetController import WidgetController


class GuiUtils:

    @staticmethod
    def new_cell(content, width='100%', height='100%', scroll=False,
                 border='5px solid white', can_hide=False, visible=True):

        cell_box = widgets.Box([content],
                               layout=widgets.Layout(
                                   border=border,
                                   overflow='auto' if scroll else 'hidden'
                               ))

        if width is not None: cell_box.layout.width = width
        if height is not None: cell_box.layout.height = height

        if not can_hide: return cell_box

        btn_show_hide = widgets.Button(description='x')
        btn_show_hide.layout.width = '30px'
        btn_show_hide.layout.height = '30px'
        controller = WidgetController(cell_box)

        def toggle_visibility():
            if btn_show_hide.description == 'x':
                btn_show_hide.description = '+'
                controller.hide_widget()
                return

            btn_show_hide.description = 'x'
            controller.show_widget()

        btn_show_hide.on_click(toggle_visibility)
        result = widgets.VBox([btn_show_hide, cell_box])

        if not visible:
            controller.hide_widget()
            btn_show_hide.description = '+'

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
        txt = widgets.Textarea(
            value=value,
            description=description,
            style={'description_width': 'initial'},
            layout=widgets.Layout(
                border=border
            )
        )
        if width is not None: txt.layout.width = width
        if height is not None: txt.layout.height = height

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
