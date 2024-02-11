import ipywidgets as widgets
from pandas import DataFrame
from NELL.Selenium import Selenium
from NELL.logger.Logger import Logger
from IPython.display import clear_output


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
        key = self.data["Key"][index]
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
        self.locator = locator
        self.att_name = att
        self.att_value = self.data["Data"][index][att]

        html_widget = widgets.HTML(
            value=f"""<br/>
                <b>Page Url:</b> {self.pageUrl}<br/>
                <b>Locator:</b> {self.locator}<br/>
                <b>Attribute:</b> {self.att_name}<br/>
                <div style='background-color: #fff9c4; padding: 10px; width: 350px;'>
                    <b>Attribute Value:</b><br/>{self.att_value}
                </div>
            """
        )

        self.memo = widgets.Textarea(
            placeholder='Store this for what purpose?',
            layout=widgets.Layout(width='350px', height='50px')
        )

        btn = widgets.Button(description='Store Attribute Value', icon='save', layout=widgets.Layout(width='200px'))
        btn.on_click(lambda b: self.log_attribute_data(b))
        self.footer.children = [html_widget, self.memo, btn]


    def log_attribute_data(self, b=None):
        Logger.log_event({'qa':self.memo.value, 
                          'uid': self.uid,
                          'locator': self.locator,
                          'attribute_name': self.att_name,
                          'attribute_value': self.att_value
                        })


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

        else:
            self.content.children = [widgets.HTML("<h2>No page objects found</h2>")]

        try:
            global win
            if win is not None:
                win.redraw()

        except: pass