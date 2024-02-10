import ipywidgets as widgets
from pandas import DataFrame

from NELL.Selenium import Selenium
from NELL.logger.Logger import Logger


class QualityAssurance:

    def __init__(self):       
        self.content = widgets.VBox([], layout=widgets.Layout(overflow='auto', width='98%'))

        self.data_event = None
        self.web_event = None

        self.data = DataFrame(columns=["Key", "PageId", "Locator", "Data", "Type", "UID"])
        self.reload()


    def try_fire_data_event(self, b, index):
        if self.data_event is not None:
            dt = self.data["Data"][index]
            self.data_event(dt)


    def try_fire_web_event(self, b, index):
        xpath = self.data["Locator"][index]
        Selenium.instance().highlight_element(xpath)

        # dt = self.data["Data"][index]
        # self.data_event(dt)


    def reload(self, df=None, element=None, attributes={}):

        if df is not None:
            self.data = df
        lines = len(self.data)

        if lines == 0:
            self.content.children = []
            return

        pageId = ''
        grid_layout = widgets.Layout(width='300px', grid_gap='4px')
        grid = widgets.GridspecLayout(lines, 2, layout=grid_layout)

        for i, (index, row) in enumerate(self.data.iterrows()):
            key = row["Key"]
            pageId = row["PageId"]
            locator = row["Locator"]
            uid = row["UID"]

            pnl = widgets.Button(tooltip=locator, icon='search', layout=widgets.Layout(width='50px', height='30px'))
            pnl.on_click(lambda b, index=i: self.try_fire_web_event(b, index=index))
            grid[i, 1] = pnl
            grid[i, 0] = widgets.HTML(f"<b>{key}</b>", layout=widgets.Layout(width='220px'))

            Logger.add_page_object(uid, locator)

        attributes = widgets.HTML(layout=widgets.Layout(overflow='auto', width='50%', background_color='lightblue'))
        elements = widgets.HBox([grid, attributes], layout=widgets.Layout(overflow='hidden', width='100%', background_color='lightgrey'))

        header = widgets.HTML(value=f"<b>{pageId}:</b> {Selenium.instance().current_url()}", layout=widgets.Layout(height='50px', background_color='lightgreen'))
        self.content.children = [header, elements, widgets.HTML()]

        try:
            global win
            if win is not None:
                win.redraw()
        except: pass


        # components = []
        # for (key, value) in attributes.items():
        #     alias = element.get('key') if element else key
        #     tmp = f"{alias}@{key}:{value}"
        #     txt = widgets.Text(value=tmp, tooltip=alias, layout=widgets.Layout(height='30px', width='68%'), disabled=True)
        #     components.append(txt)

        # self.content.children = components
