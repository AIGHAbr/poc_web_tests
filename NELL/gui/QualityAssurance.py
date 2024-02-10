import ipywidgets as widgets
from pandas import DataFrame

from NELL.Selenium import Selenium
from NELL.logger.Logger import Logger
from IPython.display import display

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

        elementId = self.data["Key"][index]
        pageId = self.data["PageId"][index]
        locator = self.data["Locator"][index]
        Selenium.instance().highlight_element(locator)

        options = []
        for key, value in self.data["Data"][index].items():
            if key == "selector": continue
            options.append(key)

        radios = widgets.RadioButtons(
            options=options,
            disabled=False,
            layout={'width': 'max-content'}
        )

        self.attributes.children = [widgets.VBox([radios])]
        radios.observe(lambda change: 
            self.attribute_selected(pageId, elementId, locator, change.new, index), names='value')

        self.attribute_selected(pageId, elementId, locator, radios.options[0], index)


    def attribute_selected(self, pageId, elementId, locator, att, index):
        self.pageId = pageId
        self.elementId = elementId
        self.locator = f"{locator}@{att}"

        value = self.data["Data"][index][att]
        self.footer.children = [widgets.HTML(
            f"""<br/>
                <b>PageId:</b>{pageId}<br/> 
                <b>ObjectId:</b>{elementId}<br/>
                <b>Locator:</b>{self.locator}<br/>
                <div style='background-color: yellow; width: 300px'>
                <b style='background-color: yellow; width: 300px'>Value:</b><br/>{value}<div>
            """)]


    def reload(self, df=None):

        if df is not None:
            self.data = df

        lines = len(self.data)
        if lines > 0: 

            pageId = ''
            self.grid = widgets.GridspecLayout(lines, 2, layout=widgets.Layout(width='300px', overflow='auto'))

            for i, (index, row) in enumerate(self.data.iterrows()):
                key = row["Key"]
                pageId = row["PageId"]
                locator = row["Locator"]
                uid = row["UID"]

                pnl = widgets.Button(tooltip=locator, icon='search', layout=widgets.Layout(width='50px', height='30px'))
                pnl.on_click(lambda b, index=i: self.try_fire_web_event(b, index=index))
                self.grid[i, 1] = pnl
                self.grid[i, 0] = widgets.HTML(f"<div style='background-color: white; width: 220px;'>{key}</div>")

                Logger.add_page_object(uid, locator)

            self.attributes = widgets.VBox(layout=widgets.Layout(overflow='auto'))
            self.footer = widgets.VBox(layout=widgets.Layout(overflow='auto'))
            
            pgObjs = widgets.VBox([self.grid, widgets.HTML()])
            elements = widgets.HBox([pgObjs, self.attributes], layout=widgets.Layout(overflow='hidden'))

            header = widgets.HTML(value=f"<b>{pageId}:</b> {Selenium.instance().current_url()}<br/>", layout=widgets.Layout(height='50px'))
            self.content.children = [header, elements, self.footer, widgets.HTML()]

        try:
            global win
            if win is not None:
                win.redraw()

        except: pass