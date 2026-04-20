class Scale:
    def __init__(self):

        # Constants
        self.SELECTOR_BUS_WIDTH = 8 * 16
        self.SCALE_CONFIG_BUS_WIDTH = 2

        # Wire and buses
        self.underflow_exception = 0
        self.scale_config = [0] * self.SCALE_CONFIG_BUS_WIDTH
        self.selector = [0] * self.SELECTOR_BUS_WIDTH
        self.one_depth_buffer = 0
