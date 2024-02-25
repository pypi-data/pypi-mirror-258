class Config:
    '''
    Class `Config`,
    set default config for app\n
    ---
    Attributes:
    - `default_pause_message`: Default pause message
    '''
    DEFAULT_PAUSE_MESSAGE = "> "

    def __init__(self, default_pause_message=DEFAULT_PAUSE_MESSAGE):
        self.default_pause_message = default_pause_message
