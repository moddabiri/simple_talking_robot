__author__ = "Mohammad Dabiri"
__copyright__ = "Free to use, copy and modify"
__credits__ = ["Mohammad Dabiri"]
__license__ = "MIT Licence"
__version__ = "0.0.1"
__maintainer__ = "Mohammad Dabiri"
__email__ = "moddabiri@yahoo.com"

import time
class StateMachineNode():
    def __init__(self, node_value, action, is_terminal=False, gap=0.0):
        self._node_value = node_value
        self._action = action
        self._is_terminal = is_terminal
        self._edges_out = {}
        self._unknown_target = None
        self._gap = 0.0
        self._return_activations = []
        self._previous = None

    _node_value = None
    _action = None
    _edges_out = {}
    _is_terminal = False
    _unknown_target = None
    _gap = 0.2
    _previous=None
    _return_activations = []

    @staticmethod
    def start(machine):
        new_target, new_act, skip_entry = machine.activate()
        while new_target:
            new_target, new_act, skip_entry = new_target.activate(skip_entry)

    def add_edge(self, target_machine, activation):
        if target_machine is None or not isinstance(target_machine, StateMachineNode):
            raise ValueError("The target machine given is not a valid StateMachineNode.")
        
        self._edges_out[activation] = target_machine

    def set_unknown_target(self, target_machine):
        self._unknown_target = target_machine

    def set_prev(self, previous_node):
        self._previous = previous_node

    def activate(self, skip_entry_action=False):
        new_activation = self.execute(skip_entry_action)
        
        if self._gap > 0:
            time.sleep(self._gap)

        my_print("Activating %s"%new_activation)

        if new_activation in self._return_activations:
            my_print("Returning back to the previous step.")
            return self._previous, new_activation, False

        target = self._edges_out.get(new_activation, None)

        if target is None and self._unknown_target:
            my_print("Going to the unknow target")
            target = self._unknown_target

        if target is None:
            raise KeyError("Requested activation {0} was not matching any edges on the current state {1}. Halted.".format(new_activation, self._node_value))
        
        my_print("Going from state %s to %s"%(self._node_value, target._node_value))
        target.set_prev(self)

        if not self._is_terminal:
            return target, new_activation, self == target

        return None, None, False

    def loop(self, activation):
        self.add_edge(self, activation)

    def return_back(self, activation):
        self._return_activations.append(activation)

    def execute(self, skip_entry_action):
        accepted_activations = [act for act,target in self._edges_out.items()] + self._return_activations
        return self._action(skip_entry_action, accepted_activations)

state_subscribers = []
def raise_state_changed(old_state, new_state, activation):
    for subscriber in state_subscribers:
        subscriber(old_state, new_state, activation)

def subscriber_to_state_change(event_handler):
    state_subscribers.append(event_handler)

def my_print(message):
    #print(message)
    pass