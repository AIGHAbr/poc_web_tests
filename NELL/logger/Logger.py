from NELL.logger.Snapshoter import Snapshoter


class Logger:

    singleton = None
    def __new__(cls, *args, **kwargs):
        if cls.singleton is None:
            cls.singleton = super(Logger, cls).__new__(cls)
            cls.singleton.reset_logs()
            cls.singleton.log_event_listeners =[]
            
        cls.singleton.disabled=True
        return cls.singleton


    @staticmethod
    def reset_logs():
        singleton = Logger.singleton
        singleton.logged_events = set()
        singleton.processedEventIds = set()
        singleton.events = []
        singleton.page_objects = {}


    @staticmethod
    def enable(): 
        if Logger.singleton == None:
            Logger.singleton = Logger()
        Logger.singleton.disabled = False


    @staticmethod
    def disable(): 
        if Logger.singleton == None:
            Logger.singleton = Logger()
        Logger.singleton.disabled = True


    @staticmethod
    def reset_listeners():
        Logger.singleton.log_event_listeners = []


    @staticmethod
    def add_page_object(alias, xpath):
        Logger.singleton.page_objects[alias] = xpath


    @staticmethod
    def log_event(event, reset=False):
        if reset: Logger.singleton.reset_logs()
        if event is None: return
        if Logger.singleton.disabled: return

        alias = event.get('alias', None)
        if alias is not None:
            xpath = Logger.singleton.page_objects.get(alias, None)
            if xpath is not None:
                event['xpath'] = xpath

        sevent = str(event)
        if sevent in Logger.singleton.logged_events: return

        Logger.singleton.logged_events.add(sevent)
        Logger.singleton.events.append(event)

        for listener in Logger.singleton.log_event_listeners:
            listener(event, Logger.singleton.events)


    @staticmethod
    def all_events():
        return Logger.singleton.logged_events


    @staticmethod
    def add_event_logger_listener(event_logger):
        if event_logger is None: return
        try:
            Logger.singleton.log_event_listeners.append(event_logger)
        except:
            if Logger.singleton == None: Logger.singleton = Logger()
            Logger.singleton.log_event_listeners = [event_logger]
