class Messenger:

    def __init__(self):
        self.events=[]
        self.listeners={}

        #Add scheduled events to this list in the format self.scheduled.append([scheduled, timeleft])
        self.scheduled=[]

    def get(self, name=None):
        return_events=[]
        if name is None:
            for i in range(len(self.events)-1, -1, -1):
                return_events.append(self.events.pop(i))
        else: 
            for i in range(len(self.events)-1, -1, -1):
                if self.events[i].name==name:
                    return_events.append(self.events.pop(i))
        return return_events

    def queue(self, event):
        self.events.append(event)

    def add_listener(self, listener):
        if listener.name not in self.listeners:
            self.listeners[listener.name]=[listener]
        else:
            self.listeners[listener.name].append(listener)

    #dt is the time since the last update
    def update(self, dt=None):
       
        if dt is not None:
            for i in range(len(self.scheduled)-1, -1, -1):
                self.scheduled[i][1]-=dt
                if self.scheduled[i][1]<=0:
                    self.queue(self.scheduled.pop(i)[0])


        the_events=self.get()
        for event in the_events:
            if event.name in self.listeners:
                for i in range(len(self.listeners[event.name])-1, -1, -1):
                    self.listeners[event.name][i].call(event)
                    if self.listeners[event.name][i].remove==True:
                        self.listeners.pop(i)
                if len(self.listeners[event.name])==0:
                    self.listeners.pop(event.name, None)

    def schedule(self, event, time):
        self.scheduled.append([event, time])      

    def clear_events(self, name=None):
        if name is not None:
            for i in range(len(self.events)-1, -1, -1):
                if self.events[i].name==name:
                    self.events.pop(i, None)
        else:
            self.events=[]

    def clear_listeners(self, name=None):
        if name is not None:
            self.listeners.pop(name, None)            
        else:
            self.listeners={}


class Event:
    def __init__(self, name, callback=None, args=None):
        self.name=name
        self.callback=callback
        self.args=args


class Listener:
    def __init__(self, name, function, remove=False):
        self.name=name
        self.function=function
        self.remove=remove

    def call(self, event):
        self.function(event)
