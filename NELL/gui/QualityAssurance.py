import ipywidgets as widgets
from NELL.Selenium import Selenium
from NELL.logger.Logger import Logger


class QualityAssurance:

    def __init__(self):
        self.content = widgets.Tab([], layout=widgets.Layout(overflow='hidden', width='99%', height='99%'))
        self.reload(None, None, None)
        self.pages = {}


    def try_fire_web_event(self, page_url, uid, locator, data, attributes):
        Selenium.instance().highlight_element(locator)
        options = []
        for key, value in data.items():
            if key == "selector": continue
            options.append(key)

        radios = widgets.RadioButtons(
            options=options,
            disabled=False,
            layout={'width': 'max-content'},
            selected_index=-1
        )

        attributes.children = [widgets.VBox([radios])]
        radios.observe(lambda change:
                       self.attribute_selected(page_url, uid, locator, change.new, data[change.new]), names='value')
        self.attribute_selected(page_url, uid, locator, options[0], data[options[0]])


    def attribute_selected(self, page_url, uid, locator, att_name, att_value):

        html_widget = widgets.HTML(
            value=f"""<br/>
                <b>Page Url:</b> {page_url}<br/>
                <b>Locator:</b> {locator}<br/>
                <b>Attribute:</b> {att_name}<br/>
                <div style='background-color: #fff9c4; padding: 10px; width: 350px;'>
                    <b>Attribute Value:</b><br/>{att_value}
                </div>
            """
        )

        memo = widgets.Textarea(
            placeholder='Store this for what purpose?',
            layout=widgets.Layout(width='350px', height='50px')
        )

        btn = widgets.Button(description='Store Attribute Value', icon='save', layout=widgets.Layout(width='200px'))
        btn.on_click(lambda b: self.log_attribute_data(memo, uid, locator, att_name, att_value))

        self.footer.children = [html_widget, memo, btn]

    def log_attribute_data(self, memo, uid, locator, att_name, att_value):
        Logger.log_event({'qa': memo.value,
                          'uid': uid,
                          'locator': locator,
                          'attribute_name': att_name,
                          'attribute_value': att_value
                          })


    def reload(self, page_id, page_url, df):
        if page_id is not None:
            for pid in self.content.children:
                if pid.title == page_id:
                    self.content.children.remove(page_id)
                    break

        if df is None or len(df) == 0:
            if page_url is None: return
            place_holder = widgets.HTML(f"<div>{page_url}</div><h2>No page objects found</h2>")
            place_holder.title = page_id
            i = len(self.content.children)
            self.content.children += (place_holder,)
            self.content.set_title(i, f"{page_id}")  
            return

        tab = widgets.VBox([], layout=widgets.Layout(overflow='auto', width='98%'))
        
        self.redraw_tab(page_url, tab, df)
        tab.title = page_id
        i = len(self.content.children)
        self.content.children += (tab,)
        self.content.set_title(i, f"{page_id}")  


    def redraw_tab(self, page_url, tab, df):
            lines = len(df)
            grid = widgets.GridspecLayout(lines, 2, layout=widgets.Layout(width='300px', overflow='auto'))
            attributes = widgets.VBox(layout=widgets.Layout(overflow='auto'))

            for i, (index, row) in enumerate(df.iterrows()):
                key = row["Key"]
                locator = row["Locator"]
                uid = row["UID"]
                data = row["Data"]

                pnl = widgets.Button(tooltip=locator, icon='search', layout=widgets.Layout(width='50px', height='30px'))

                pnl.on_click(lambda b: self.try_fire_web_event(page_url, uid, str(locator), data, attributes))
                grid[i, 1] = pnl
                grid[i, 0] = widgets.HTML(f"<div style='background-color: white; width: 220px;'>{key}</div>")

                Logger.add_page_object(uid, locator)

            footer = widgets.VBox(layout=widgets.Layout(overflow='auto'))

            page_objects = widgets.VBox([grid, widgets.HTML()])
            elements = widgets.HBox([page_objects, attributes], layout=widgets.Layout(overflow='hidden'))
            tab.children = [widgets.HTML(f"<div>{page_url}</div>"), elements, footer, widgets.HTML()]