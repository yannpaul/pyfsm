
import pytest
import pyfsm
transition = pyfsm.transition




def test_first_transition():
    def dummy():
        pass
    pyfsm.default_machine = pyfsm.Machine()
    dummy2 = transition(on='a', go_from='b', to='c')(dummy)
    default_machine = pyfsm.default_machine
    assert len(default_machine.events) == 1
    event = default_machine.events[0]
    assert event.from_state == 'b'
    assert event.to_state == 'c'
    assert event.name == 'a'
    assert event.action == dummy
    assert dummy2 == dummy


def test_complete_transitions():
    def dummy():
        pass

    pyfsm.default_machine = pyfsm.Machine()
    dummy2 = transition(on='a', go_from='b', to='c')(dummy)
    dummy3 = transition(on='a', go_from='c', to='b')(dummy)
    default_machine = pyfsm.default_machine
    assert len(default_machine.events) == 2
