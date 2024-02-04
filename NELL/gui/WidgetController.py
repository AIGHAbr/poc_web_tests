class WidgetController:
    
    def __init__(self, component):
        self.display = None
        self.component = component

    def hideWidget(self):
        if self.component.layout.display != "none":
            self.display = self.component.layout.display
        self.component.layout.display = "none"

    def showWidget(self):
        if self.component.layout.display is None: return
        self.component.layout.display = self.display