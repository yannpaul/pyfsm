
import pytest
import pyfsm
import types

transition = pyfsm.transition


def test_build_events():
    def dummy():
        pass

    pyfsm.default_machine = pyfsm.Machine()
    dummy2 = transition(on='a', go_from='b', to='c')(dummy)
    dummy3 = transition(on='a', go_from='c', to='b')(dummy)
    default_machine = pyfsm.default_machine
    assert len(default_machine.events) == 2
    default_machine.build_events()
    assert len(default_machine.states) == 2
    

def test_events_complete():
    def dummy():
        pass

    pyfsm.default_machine = pyfsm.Machine()
    dummy2 = transition(on='a', go_from='b', to='c')(dummy)
    dummy3 = transition(on='a', go_from='c', to='b')(dummy)
    default_machine = pyfsm.default_machine
    assert len(default_machine.events) == 2
    default_machine.build_events()
    assert default_machine.events_are_complete() 


def test_not_events_complete():
    def dummy():
        pass

    pyfsm.default_machine = pyfsm.Machine()
    dummy2 = transition(on='a', go_from='b', to='c')(dummy)
#    dummy3 = transition(on='a', go_from='c', to='b')(dummy)
    default_machine = pyfsm.default_machine
    assert len(default_machine.events) == 1
    default_machine.build_events()
    assert not default_machine.events_are_complete() 
    

def test_method_wrapper():
    machine = pyfsm.Machine()
    machine.current_state = 'foo'

    event = pyfsm.EventBuilder('baz').go_from('foo').to('bar')
    @event
    def method():
        return 10
    machine.add_transition(event)

    wrapper = machine.method_wrapper('baz')
    assert type(wrapper) == types.MethodType
    assert wrapper() == 10

    setattr(machine, 'baz', wrapper)
    machine.current_state = 'foo'
    assert machine.baz() == 10

# need to spy on self?
def test_build_methods():
    machine = pyfsm.Machine()
    machine.current_state = 'foo'
    def foobaz():
        return 10
    def barbaz():
        return -10

    event = pyfsm.EventBuilder('baz').go_from('foo').to('bar')
    event(lambda : 10)
    machine.add_event(event)

    event = pyfsm.EventBuilder('baz').go_from('bar').to('foo')
    event(lambda : -10)
    machine.add_event(event)
    machine.build_events()

    machine.build_methods()
    assert machine.baz() == 10
    assert machine.current_state == 'bar'
    assert machine.baz() == -10

def test_start():
    machine = pyfsm.Machine()
    machine2 = machine.start('foo')
    assert machine == machine2
    assert machine.current_state == 'foo'
    
def test_build():
    machine = pyfsm.Machine()
    event = pyfsm.EventBuilder('baz').go_from('foo').to('bar')
    event(lambda : 10)
    machine.add_event(event)

    event = pyfsm.EventBuilder('baz').go_from('bar').to('foo')
    event(lambda : -10)
    machine.add_event(event)

    machine.build()
    assert machine.current_state == 'foo'
    assert machine.baz() == 10
    assert machine.current_state == 'bar'
    assert machine.baz() == -10
    assert machine.current_state == 'foo'
    assert machine.get_events() == set(('baz',))

def test_build_fail():
    machine = pyfsm.Machine()
    event = pyfsm.EventBuilder('baz').go_from('foo').to('bar')
    event(lambda : 10)
    machine.add_event(event)
    
    with pytest.raises(pyfsm.IncompleteError):
        machine.build()


def test_dumplicate_transitions():
    machine = pyfsm.Machine()
    event = pyfsm.EventBuilder('baz').go_from('foo').to('bar')
    event(lambda : 10)
    machine.add_transition(event)

    event = pyfsm.EventBuilder('biz').go_from('foo').to('bar')
    event(lambda : 10)
    machine.add_transition(event)

    event = pyfsm.EventBuilder('baz').go_from('foo').to('bar')
    event(lambda : 10)
    with pytest.raises(pyfsm.DuplicateTransition):
        machine.add_transition(event)

