class ControlBlock:
    def __init__(self):

        # Constants
        self.ADDRESS_GENERATOR_BUS_WIDTH = 20
        self.SCALE_CONFIG_BUS_WIDTH = 2
        self.ROUNDING_CONFIG_BUS_WIDTH = 2

        # Wires and buses
        self.s_axis_user_configs = 0
        self.s_axis_valid = 0
        self.s_axis_ready = 0
        self.s_axis_last = 0
        self.underflow_exception = 0
        self.overflow_exception = 0
        self.axis = 0
        self.m_axis_valid = 0
        self.m_axis_last = 0
        self.m_axis_ready = 0
        self.m_axis_user_exceptions = 0
