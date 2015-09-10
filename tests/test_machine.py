
import pyfsm
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
    

def test_complete():
    def dummy():
        pass

    pyfsm.default_machine = pyfsm.Machine()
    dummy2 = transition(on='a', go_from='b', to='c')(dummy)
    dummy3 = transition(on='a', go_from='c', to='b')(dummy)
    default_machine = pyfsm.default_machine
    assert len(default_machine.events) == 2
    default_machine.build_events()
    assert default_machine.events_are_complete() 
