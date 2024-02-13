from datetime import datetime as datetime

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
        singleton.page_counter = 0


    @staticmethod
    def disabled(): 
        if Logger.singleton == None:
            Logger.singleton = Logger()
        return Logger.singleton.disabled


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
        if Logger.singleton == None:
            Logger.singleton = Logger()        
        Logger.singleton.log_event_listeners = []


    @staticmethod
    def add_page_object(uid, xpath):
        if Logger.singleton == None:
            Logger.singleton = Logger()
        Logger.singleton.page_objects[uid] = xpath


    @staticmethod
    def log_event(event, reset=False):
        logger = Logger.singleton
        if reset: logger.reset_logs()
        if event is None: return event
        if logger.disabled: return event

        if event.get('timestamp', None) is None:
            event['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        uid = event.get('widget_id', None)
        if id is not None:
            xpath = logger.page_objects.get(uid, None)
            if xpath is not None:
                event['xpath'] = xpath

        url = event.get('url', None)
        if url is not None:
            if event.get('info', None) == 'page loaded':
                logger.page_counter = logger.page_counter + 1
                event['page_id'] = logger.current_page_id()
                try:
                    if url == logger.events[-1].get('url', None):
                        pass
                except:
                    pass

        sevent = str(event)
        if sevent in logger.logged_events: return event

        logger.logged_events.add(sevent)
        logger.events.append(event)

        for listener in logger.log_event_listeners:
            listener(event, logger.events)

        return event

    @staticmethod
    def current_page_id() :
        if Logger.singleton == None:
            Logger.singleton = Logger()
        return f'Page_{Logger.singleton.page_counter}'

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
