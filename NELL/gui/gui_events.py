from NELL.gui.MyDataFrame import MyDataFrame
from NELL.logger.js_injector import instrument_webpage


def data_changed(window=None):
    print("data changed")
    pass


def inspect_webpage(selenium, window=None, table=None, properties=None):

    global selectors
    metadata = selenium.read_page_objects_metadata()
    #print(metadata)
    selectors = {}
    rows = []

    for tag_name, elements in metadata.items():
        for element in elements:

            att = element.pop('attributes', {})
            clazz =  att.pop('class', [])

            for k, v in att.items():
                element[k] = v

            element['class'] = clazz
            key = element.get('key', '')
            selector = element.get('selector', '')

            js = f"""
    var element = document.evaluate('{selector}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    if (element) element.setAttribute('key','{key}');
            """
            
            rows.append({
                "Export": False,
                "Alias": key,
                "key": key,
                "Web": selector,
                "Type": tag_name,
                "Data": element
            })
            
            selenium.execute_script(js)
            selectors[key]=selector

    df = MyDataFrame(rows)
    table.reload(df)
    properties.reload({})
    
    df.set_change_listener(window.try_fire_data_changed_event)
    window.try_fire_data_changed_event(window)

    instrument_webpage(selenium)