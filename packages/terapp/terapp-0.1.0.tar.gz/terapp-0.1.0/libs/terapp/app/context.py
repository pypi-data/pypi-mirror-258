import os
from .interfaces import Component, Context
from .errors import RoutesError


class AppContext(Context):
    '''
    App Context contains current component and routes of components\n
    This class is used for create context of `Ter()` file\n
    Beware to use this class, it's not for user\n
    ---
    Methods:
    - `register_routes`: Register routes for app
    - `init_component`: Initialize component as first element in routes
    - `navigate`: Navigate to other component, change current component
    '''

    def __init__(self):
        # Current component, initialize as None
        # This variable will be changed when navigate
        self.component: Component = None

        # Routes of components
        self.routes: dict[str, Component] = {}

        # Terminal size
        self.width, self.height = self.__get_window_size()

    def __get_window_size(self):
        _width, _height = os.get_terminal_size()
        return _width, _height

    def register_routes(self, routes: dict[str, Component]):
        for key in routes.keys():
            if not issubclass(routes[key], Component):
                RoutesError.register_error()
        self.routes = routes

    def init_component(self):
        if self.component is None:
            # Check if routes isn't define
            if self.routes == {}:
                RoutesError.undefine_error()
            # Initialize component as first element in routes
            first_element = list(self.routes.keys())[0]
            # Self component is the instance of first element in routes
            self.component = self.routes[first_element]()

    def navigate(self, path_name: str):
        # Check if routes isn't define
        if path_name not in self.routes.keys():
            RoutesError.not_found_route()
        # Self component is the instance of dict value of routes
        self.component = self.routes[path_name]()
        # Update terminal size
        self.width, self.height = self.__get_window_size()
