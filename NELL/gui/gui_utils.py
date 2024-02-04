import ipywidgets as widgets

from NELL.gui.WidgetController import WidgetController


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