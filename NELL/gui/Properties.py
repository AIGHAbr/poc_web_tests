import ipywidgets as widgets

class Properties:
    
    def __init__(self, properties={}):        
        self.content = widgets.HBox()
        self.reload(properties)

    def reload(self, properties={}):
        num_props = len(properties)
        grid = widgets.GridspecLayout(num_props + 1, 2, width='auto')
        grid[0, 0] = widgets.HTML(value="<b>Property</b>", layout=widgets.Layout(width='80px'))
        grid[0, 1] = widgets.HTML(value="<b>Value</b>", layout=widgets.Layout(width='400px'))  

        i = 0
        for i, (key, value) in enumerate(properties.items(), start=1):
            grid[i, 0] = widgets.Text(value=key, layout=widgets.Layout(width='80px'), disabled=True, bold=True)
            grid[i, 1] = widgets.Text(value=str(value), layout=widgets.Layout(width='400px'))

        self.content.children = [grid]