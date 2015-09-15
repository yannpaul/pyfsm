

import pyfsm
from pyfsm import on, go_from, to

def test_simple_machine():
    pyfsm.default_machine = pyfsm.Machine()
    
    @on('baz')
    @go_from('foo')
    @to('bar')
    def do_baz():
        return 10

    @on('baz')
    @go_from('bar')
    @to('foo')
    def do_baz():
        return -10

    assert len(pyfsm.default_machine.events) == 2
    assert pyfsm._builder == pyfsm.default_machine.events[1]
    assert pyfsm._builder.from_state == 'bar'
    assert pyfsm._builder.to_state == 'foo'
    assert pyfsm._builder.name == 'baz'

    machine = pyfsm.FSM('foo')
    assert machine.baz() == 10
    assert machine.baz() == -10
