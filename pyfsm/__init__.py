
from collections import namedtuple
import types

Transition = namedtuple('Transition', 'to action')

class IncompleteError(Exception):
    pass

class Machine:

    def __init__(self):
        self.events = []
        self.states = dict()

    def add_event(self, event):
        self.events.append(event)
        return self

    def add_state(self, state):
        state = self.states.setdefault(state, {})
        #print(self.states)
        return state

    def add_transition(self, event):
        state = self.add_state(event.from_state)
        assert event.to_state not in state, (
            'Repeated event transition! %{}: %{}->%{}'.format(
                event.name,
                event.from_state, 
                event.to_state))
        state[event.name] = Transition(event.to_state, event.action)

    def build_events(self):
        for event in self.events:
            self.add_transition(event)

    def build(self):
        self.build_events()
        if not self.events_are_complete():
            raise IncompleteError
            pass
        self.build_methods()
        self.current_state = self.events[0].go_from

    def method_wrapper(self, method_name):
        def method(self, *args, **kwargs):
            transition = self.states[self.current_state][method_name]
            self.current_state = transition.to
            return transition.action(*args, **kwargs)
        return types.MethodType(method, self)

    def build_methods(self):
        events = self.get_events()
        for event in events:
            setattr(self, event, self.method_wrapper(event))

    def get_events(self, state=None):
        if state is None:
            state = next(iter(self.states.keys()))
        return set(self.states[state].keys())
        
    def events_are_complete(self):
        events = self.get_events()
        for state in self.states:
            if events != self.get_events(state):
                return False
        return True

    def start(self, initial):
        self.current_state = initial
        return self
            
        

default_machine = Machine()


def calling(func):
    def wrapper(*args, **kwargs):
        print("calling:", func.__name__)
        print("inputs: ", args, kwargs)
        ret = func(*args, **kwargs)
        print("retval: ", ret, "\n")
        return ret
    return wrapper

class EventBuilder:

    def __init__(self, name, machine=None):
        self.name = name
        self.from_state = ''
        self.to_state = ''
        self.action = ''
        if machine is None:
            default_machine.add_event(self)

    def go_from(self, state):
        self.from_state = state
        return self

    def to(self, state):
        self.to_state = state
        return self

    def __call__(self, action):
        self.action = action
        return action

    def __str__(self):
        text = "-".join((self.name, self.from_state, self.to_state))
        try:
            text += " " + self.action.__name__
        except AttributeError:
            text += str(self.action)
        return text + " is builder " + str(self.is_builder())

    def is_builder(self):
        global _builder
        return self is _builder


_builder = None


def event(name):
    print('first dec')
    global _builder
    _builder = EventBuilder(name)
    return _builder


def go_from(state):
    print('second dec')
    global _builder
    _builder.from_state = state
    return _builder


def to(state):
    print('third dec')
    global _builder
    _builder.to_state = state
    return _builder


def transition(on='event', go_from='state1', to='state2'):
    builder = EventBuilder(on).go_from(go_from).to(to)
    return builder


def FSM(initial):
    global default_machine
    default_machine.build()
    default_machine.start(initial)
    new_machine = default_machine
    default_machine = Machine()
    return new_machine
