from typing import Callable


class State:
    def __init__(self, init_state):
        self.__init_state = init_state
        self.store: list[tuple[str, Callable]] = []

    def reducers(self, reducer: str, action: Callable):
        if not isinstance(reducer, str) or not isinstance(action, Callable):
            raise ValueError(
                f"Invalid value of reducer or action, expected 'str' and 'function', but found '{type(reducer).__name__}' and '{type(action).__name__}'")
        self.store.append((reducer, action))

    def dispatch(self, reducer, payload=None):
        # Get target action by reducer name
        target_action: Callable = None
        for store_reducer in self.store:
            if reducer == store_reducer[0]:
                target_action = store_reducer[1]
                break
            else:
                continue

        # Raise error if reducer not found
        if target_action is None:
            raise ValueError("Reducer not found")

        # Dispatch action
        # If payload is None, action_params is init_state
        # Else, action_params is init_state and payload
        if payload is None:
            action_params = self.__init_state
        else:
            action_params = self.__init_state, payload

        # If init_state is dict, merge init_state and target_action
        # Else, init_state is target_action
        if isinstance(self.__init_state, dict):
            self.__init_state = {**self.__init_state,
                                 **target_action(*action_params)}
        else:
            self.__init_state = target_action(*action_params)

    @property
    def state(self):
        return self.__init_state
