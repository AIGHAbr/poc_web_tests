import ipywidgets as widgets
from NELL.Selenium import Selenium

from NELL.gui.MyDataFrame import MyDataFrame
from NELL.logger.Logger import Logger

class Table:

    def __init__(self, df=None, change_data_listener=None):
        self.content = widgets.HBox()

        self.data_event = None
        self.web_event = None
        self.fire_change_data_event = change_data_listener

        self.data = df if df is not None else MyDataFrame(
            columns=["Alias", "Text", "Web", "Export", "Data", "Type", "Att"])
        self.reload()


    def try_fire_data_event(self, b, index):
        if self.data_event is not None:
            dt = self.data["Data"][index]
            self.data_event(dt)


    def try_fire_web_event(self, b, index):
        dt = self.data["Data"][index]
        self.data_event(dt)
        xpath = self.data["Web"][index]
        driver = Selenium.get('main')
        driver.highlight_element(xpath)


    def reload(self, df=None):

        if df is not None: self.data = df
        df = self.data
        lines = len(self.data) + 1
        grid = widgets.GridspecLayout(lines, 2)

        for i in range(lines):
            if i == 0: 
                grid[i, 0] = widgets.HTML(value="<b>Alias</b>")
                continue
            
            cell_value_alias = getattr(df.iloc[i-1], "Alias", '') if i > 0 else ''
            cell_value_web = getattr(df.iloc[i-1], "Web", '') if i > 0 else ''

            pnl = widgets.Button(tooltip=cell_value_web, icon='search', layout=widgets.Layout(width='50px', height='30px'))
            pnl.on_click(lambda b, index=i-1: self.try_fire_web_event(b, index))

            grid[i, 0] = widgets.Text(value=str(cell_value_alias), layout=widgets.Layout(width='250px', weight='2'))        
            grid[i, 1] = pnl

            Logger.add_page_object(cell_value_alias, cell_value_web)

        self.content.children = [grid]