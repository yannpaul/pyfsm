
import pyfsm
from pyfsm import transition, FSM



def test_simple_machine():
    event = pyfsm.EventBuilder('baz').go_from('foo').to('bar')
    event(lambda : 10)

    event = pyfsm.EventBuilder('baz').go_from('bar').to('foo')
    event(lambda : -10)

    old_default = pyfsm.default_machine
    machine = FSM('foo')
    assert machine != pyfsm.default_machine
    assert machine == old_default
    assert machine.current_state == 'foo'
