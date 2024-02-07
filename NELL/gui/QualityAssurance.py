import ipywidgets as widgets

from NELL.Selenium import Selenium
from NELL.logger.Logger import Logger
from NELL.gui.MyDataFrame import MyDataFrame


class QualityAssurance:

    def __init__(self):       
        objs = widgets.HTML(value="<b>Page Objects</b>", layout=widgets.Layout(height="30px", width='30%'))
        attrs = widgets.HTML(value="<b>Attributes</b>", layout=widgets.Layout(height="30px", width='68%'))
        self.header = widgets.HBox([objs, attrs], layout=widgets.Layout(height="30px", width='98%'))

        self.page_objects = widgets.VBox([], layout=widgets.Layout(overflow='auto', width='98%'))
        self.attributes = widgets.VBox([], layout=widgets.Layout(overflow='auto', width='98%'))

        self.body = widgets.HBox([self.page_objects, self.attributes], layout=widgets.Layout(height="30px", width='98%'))        
        self.content = widgets.VBox([self.header, self.body], layout=widgets.Layout(width='98%'))

        self.data_event = None
        self.web_event = None

        self.data = MyDataFrame(columns=["Alias", "Text", "Web", "Export", "Data", "Type", "Att"])
        self.reload()


    def try_fire_data_event(self, b, index):
        if self.data_event is not None:
            dt = self.data["Data"][index]
            self.data_event(dt)


    def try_fire_web_event(self, b, index):
        dt = self.data["Data"][index]
        self.data_event(dt)
        xpath = self.data["Web"][index]
        Selenium.instance().highlight_element(xpath)


    def reload(self, df=None, element=None, attributes={}):

        print("Reloading Quality Assurance *************************************")
        if df is not None: self.data = df
        df = self.data
        lines = len(self.data) + 1
        grid = widgets.GridspecLayout(lines, 2)

        for i in range(lines):
            
            cell_value_alias = getattr(df.iloc[i-1], "Alias", '') if i > 0 else ''
            cell_value_web = getattr(df.iloc[i-1], "Web", '') if i > 0 else ''

            pnl = widgets.Button(tooltip=cell_value_web, icon='search', layout=widgets.Layout(width='50px', height='30px'))
            pnl.on_click(lambda b, index=i-1: self.try_fire_web_event(b, index))

            grid[i, 0] = widgets.Text(value=str(cell_value_alias), layout=widgets.Layout(width='250px', weight='2'))        
            grid[i, 1] = pnl

            Logger.add_page_object(cell_value_alias, cell_value_web)

        print(grid)
        self.page_objects.children = [grid]


        components = []
        for (key, value) in attributes.items():
            alias = element.get('key') if element else key  # Ajuste caso 'element' seja None
            tmp = f"{alias}@{key}:{value}"
            txt = widgets.Text(value=tmp, tooltip=alias, layout=widgets.Layout(height='30px', width='68%'), disabled=True)
            components.append(txt)

        self.content.children = components
