

pyfsm is a package used to quickly make Finite State Machines. As a developer,
you focus on coding the actions that result from transitions, and pyFSM makes
it easy to wrap that code up into a FSM. For example, consider a subway 
turnstile:

    >>> from pyfsm import transition, FSM
    
    >>> @transition(on='coin', go_from='closed', to='open')
    ... def pay_for_entry():
    ...     print("You just paid your fare")
    ...
    
We just defined what happens when someone inserts a coin, triggering the
`coin` event. The state machine goes from the 'closed' state to the 'open' 
state. As it does so, it will execute the action `pay_for_entry()`. 

So far we have an incomplete set of transitions. There are 3 other cases to 
worry about:

    >>> @transition(on='coin', go_from='open', to='open')
    ... def return_coin():
    ...     print("The fare has been paid, no need for more money")
    ...
    >>> @transition(on='enter', go_from='open', to='closed')
    ... def close_gate():
    ...     print("Thank you")
    ...
    >>> @transition(on='enter', go_from='closed', to='closed')
    ... def sound_alarm():
    ...     print("Alarm! Alarm!")

Ok, now what? We've defined our states: ('closed', 'open'). We've defined the
events that cause enter and exit transitions from/to these states. And we've
recorded all the actions that result from all the combinations of events and
states. To create a new machine, just call FSM with the initial state:

    >>> turnstile = FSM('closed')
    >>> turnstile.coin()
    You just paid your fare
    >>> turnstile.coin()
    The fare has been paid, no need for more money
    >>> turnstile.enter()
    Thank you
    >>> turnstile.enter()
    Alarm! Alarm!

    
