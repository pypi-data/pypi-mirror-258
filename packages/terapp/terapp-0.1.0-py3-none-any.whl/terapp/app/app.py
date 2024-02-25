import os
from .interfaces import Component
from .context import AppContext
from .config import Config
from .errors import GeneralError


# Main Class of Libraries
class Ter:
    '''
    class `Ter`, terminal app\n
    Ter applies other front-end language's syntax to python\n
    Application recursion diagram:\n
    >>> clear screen -> render component -> pause program -> run logic -> clear screen\n
    ---
    Example:
    ```
    app = Ter()
    ```

    Params:
    - `config`: Config object, contains default pause message, etc...
    - `context`: AppContext object, contains current component, routes of components, size of terminal.
    - `is_exit`: Boolean, check if app is exit or not.

    Methods:
    - `register_routes`: Register routes for app
    - `run`: Run app
    '''

    def __init__(self, config: Config = Config()):
        # Check if Config object is valid
        if not isinstance(config, Config):
            raise GeneralError.config_type_error()

        # Config variables
        self.config: Config = config

        # Context variables. Initialize when run
        self.context: AppContext = AppContext()

        # Exit variable
        self.is_exit: bool = False

    def register_routes(self, routes: dict[str, Component]):
        '''
        `required` This method registers all components for app\n
        Value of routes must be a class, not an instance of class\n
        ---
        Example
        ```
        app.register_routes({
            'route_name': Your_Component
        })
        ```
        '''
        self.context.register_routes(routes=routes)

    def run(self):
        '''
        `required` This method runs this app\n
        ---
        Example
        ```
        app.run()
        ```
        '''
        # Clear screen
        os.system("cls" if os.name == "nt" else "clear")

        # Init component when first run
        self.context.init_component()

        # Render component
        self.context.component.render(context=self.context)

        # Pause program
        if isinstance(self.context.component, Component):
            self.context.component.default_pause_message = self.config.default_pause_message
        command = input(self.context.component.prompt())

        # Run logic
        self.context.component.logic(command=command, context=self.context)

        # Recursion function
        if not self.is_exit:
            self.run()

    def exit(self):
        # Exit app
        self.is_exit = True

    def config(self, config: Config):
        '''
        `optional` This method configures app\n
        ---
        Example
        ```
        app.config(Config(default_pause_message="Press Enter to continue..."))
        ```
        '''
        # Check if Config object is valid
        if not isinstance(config, Config):
            raise GeneralError.config_type_error()
        self.config = config
