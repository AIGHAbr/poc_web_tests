import ipywidgets as widgets
from NELL.Selenium import Selenium
from NELL.logger.Logger import Logger


class QualityAssurance:

    def __init__(self):
        self.content = widgets.Tab([], layout=widgets.Layout(overflow='hidden', width='99%', height='99%'))
        self.reload(None, None, None)
        self.pages = {}


    def reset(self):
        self.pages = {}
        self.content.children = []
        self.reload(None, None, None)


    def try_fire_web_event(self, page_url, uid, locator, data, handle, attributes, footer):
        Selenium.instance().driver.switch_to.window(handle)
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
                       self.attribute_selected(page_url, uid, locator, change.new, data[change.new], footer),
                       names='value')
        self.attribute_selected(page_url, uid, locator, options[0], data[options[0]], footer)


    def attribute_selected(self, page_url, uid, locator, att_name, att_value, footer):

        html_widget = widgets.HTML(
            value=f"""<br/>
                <b>Page Url:</b> {page_url}<br/>
                <b>Locator:</b> {locator}<br/>
                <b>Attribute:</b> {att_name}<br/>
                <div style='background-color: #fff9c4; padding: 10px; width: 330px;'>
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
        footer.children = [html_widget, memo, btn]


    def log_attribute_data(self, memo, uid, locator, att_name, att_value):
        Logger.log_event({'qa': memo.value,
                          'uid': uid,
                          'locator': locator,
                          'attribute_name': att_name,
                          'attribute_value': att_value
                          })


    def reload(self, page_id, df, html_src):
        if page_id is not None:
            for pid in self.content.children:
                if pid.title == page_id:
                    self.content.children.remove(page_id)
                    break


        page_url = Selenium.instance().current_url()
        if df is None or len(df) == 0:
            if page_url is None: return
            html = widgets.Textarea(html_src, layout=widgets.Layout(overflow='hidden', height='98%', width='98%', disabled=True))
            place_holder = widgets.VBox([widgets.HTML(f"<div>{page_url}</div><h2>No page objects found</h2>"), html], 
                                        layout=widgets.Layout(overflow='hidden', width='99%', height='99%'))
            place_holder.title = page_id
            i = len(self.content.children)
            self.content.children += (place_holder,)
            self.content.set_title(i, f"{page_id}")
            return

        page_ojects = widgets.VBox([], layout=widgets.Layout(overflow='hidden', width='500px', height='100%'))

        html = widgets.Textarea(html_src, layout=widgets.Layout(overflow='hidden', height='98%', width='80%', disabled=True))
        tab = widgets.HBox([page_ojects, html], layout=widgets.Layout(overflow='hidden', width='98%', height='100%'))
        all = widgets.VBox([widgets.HTML(f"<div>{page_url}</div>"), tab],
                           layout=widgets.Layout(overflow='hidden', width='98%', height='100%'))
        self.redraw_tab(page_ojects, df)
        all.title = page_id
        i = len(self.content.children)
        self.content.children += (all,)
        self.content.set_title(i, f"{page_id}")


    def redraw_tab(self, tab, df):
        lines = len(df)
        grid = widgets.GridspecLayout(lines, 2, layout=widgets.Layout(width='300px', overflow='auto'))
        attributes = widgets.VBox(layout=widgets.Layout(overflow='auto'))
        footer = widgets.VBox(layout=widgets.Layout(overflow='auto'))

        for i, (index, row) in enumerate(df.iterrows()):
            key = row["Key"]
            locator = row["Locator"]
            uid = row["UID"]
            data = row["Data"]
            Logger.add_page_object(uid, locator)

            btn_search = widgets.Button(tooltip=locator, icon='search',
                                        layout=widgets.Layout(width='50px', height='30px'))
            btn_search.uid = uid
            btn_search.data = data
            btn_search.url = Selenium.instance().current_url()
            btn_search.handle = Selenium.instance().driver.current_window_handle
            btn_search.on_click(lambda b: self.try_fire_web_event(b.url, b.uid, b.tooltip, b.data, b.handle, attributes, footer))
            grid[i, 1] = btn_search
            grid[i, 0] = widgets.HTML(f"<div style='background-color: white; width: 220px;'>{key}</div>")

        page_objects = widgets.VBox([grid, widgets.HTML()])
        elements = widgets.HBox([page_objects, attributes], layout=widgets.Layout(overflow='hidden'))
        tab.children = [elements, footer, widgets.HTML()]
