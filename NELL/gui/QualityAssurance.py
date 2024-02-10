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

        uid = self.data["UID"][index]
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
            layout={'width': 'max-content'},
            selected_index=-1
        )

        self.attributes.children = [widgets.VBox([radios])]
        radios.observe(lambda change: 
            self.attribute_selected(pageId, uid, locator, change.new, index), names='value')
        
        self.attribute_selected(pageId, uid, locator, options[0], index)


    def attribute_selected(self, pageId, uid, locator, att, index):

        self.pageId = pageId
        self.pageUrl = Selenium.instance().current_url()
        self.uid = uid
        self.locator = f"{locator}"
        self.att_name = att
        self.att_value = self.data["Data"][index][att]

        self.footer.children = [widgets.HTML(
            f"""<br/>
                <b>Page Url:</b> {self.pageUrl}<br/>                 
                <b>UID:</b> {self.uid}<br/>
                <b>Locator:</b> {self.locator}<br/>
                <b>Attribute:</b> {self.att_name}<br/>
                <div style='background-color: #fff9c4; padding: 10px; width: 350px;'>
                    <b>Attribute Value:</b><br/>{self.att_value}
                </div>
            """,
            layout=widgets.Layout(overflow='auto')
        )]



    def reload(self, df=None):

        if df is not None:
            self.data = df

        lines = len(self.data)
        if lines > 0: 

            self.grid = widgets.GridspecLayout(lines, 2, layout=widgets.Layout(width='300px', overflow='auto'))

            for i, (index, row) in enumerate(self.data.iterrows()):
                key = row["Key"]
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

            self.content.children = [elements, self.footer, widgets.HTML()]

        try:
            global win
            if win is not None:
                win.redraw()

        except: pass