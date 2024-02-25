# General errors
class GeneralError:
    CONFIG_TYPE_ERROR = "Config must be a Config object"
    NOT_IMPLEMENTED = "Method not implemented"

    @staticmethod
    def config_type_error():
        raise TypeError(GeneralError.CONFIG_TYPE_ERROR)

    @staticmethod
    def not_implemented():
        raise NotImplementedError(GeneralError.NOT_IMPLEMENTED)


# Routes error
class RoutesError:
    REGISTER_ERROR = "Routes element must be a Component"
    UNDEFINE_ERROR = "Routes must be defined"
    NOT_FOUND_ROUTE = "Route not found"

    @staticmethod
    def register_error():
        raise ValueError(RoutesError.REGISTER_ERROR)

    @staticmethod
    def undefine_error():
        raise ValueError(RoutesError.UNDEFINE_ERROR)

    @staticmethod
    def not_found_route():
        raise IndexError(RoutesError.NOT_FOUND_ROUTE)


# Component error
class ComponentError:
    MISSING_RENDER = "Component must override render method"

    @staticmethod
    def missing_render():
        raise SyntaxError(ComponentError.MISSING_RENDER)
