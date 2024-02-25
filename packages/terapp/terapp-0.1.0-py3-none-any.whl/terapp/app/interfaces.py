from .errors import ComponentError


class Component:
    '''
    Abstract class `Component` contains render method, prompt method and logic method\n
    ---
    Attributes:
    - `default_pause_message`: Default pause message

    Methods:
    - `render`: This method used to print interfaces
    - `prompt`: Prompt message when paused
    - `logic`: Logic block, run after enter inputs
    '''

    def __init__(self, default_pause_message=None):
        self.default_pause_message = default_pause_message

    def render(self, context: 'Context' = None):
        '''
        `required`\n
        This method used to print interfaces\n
        Other class extended Component must specifying render method
        '''
        raise ComponentError.missing_render()

    def prompt(self):
        '''
        `optional`\n
        '''
        return self.default_pause_message

    def logic(self, command: str = None, context: 'Context' = None): ...


class Context:
    '''
        Abstract class `Context` contains current component and routes of components\n
        ---
        Attributes:
        - `component`: Current component, initialize as None
        - `routes`: Routes of components
        - `width`: Terminal width
        - `height`: Terminal height
    '''

    def __init__(self):
        self.component: Component = None
        self.routes: dict[str, Component] = None
        self.width: int = None
        self.height: int = None

    def __get_window_size(self): ...

    def register_routes(self, routes: dict[str, Component]): ...

    def init_component(self): ...

    def navigate(self, path_name: str): ...
