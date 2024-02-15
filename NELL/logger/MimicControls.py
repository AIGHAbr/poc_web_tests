from IPython.display import display

class MimicControls:

    instance = None

    def __init__(self):
        self.disabled = False    

    @staticmethod
    def log_event(event, reset=False):
        try:
            if event.get('is_clone'): return
            etype = event.get('event')
            if etype == 'new_driver':
                MimicControls.singleton().selenium_handles.add(event.get('window_handle'))


        finally:
            display(event, display_id='mimic_controls')

    @classmethod
    def singleton(cls):
        if cls.instance is None:
            cls.instance = MimicControls()
        return cls.instance

    @classmethod
    def enable(cls): 
        cls.singleton().disabled = False

    @classmethod
    def disable(cls): 
        cls.singleton().disabled = True

    @classmethod
    def disabled(cls):
        return cls.singleton().disabled
