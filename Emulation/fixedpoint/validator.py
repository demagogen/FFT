import functools

class Validator:
    @staticmethod
    def width_settings(with_sign: int, int_width: int, width: int):
        if with_sign not in (0, 1):
            raise ValueError("with_sign must be 0 or 1")
        if int_width < 0:
            raise ValueError("int_width cannot be negative")
        if width - int_width - with_sign < 0:
            raise ValueError(f"Constraint failed: {width} - {int_width} - {with_sign} < 0")

def validate(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import inspect
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        params = bound_args.arguments
        Validator.width_settings(
            params.get('with_sign'),
            params.get('int_width'),
            params.get('width')
        )

        return func(*args, **kwargs)
    return wrapper

class Fixedpoint:
    @staticmethod
    @validate
    def float_to_fixedpoint(float_value: float, with_sign: int, int_width: int, width: int):
        fractional_bits = width - with_sign - int_width
        tmp = int(round(float_value * (2 ** fractional_bits)))
        max_limit = 1 << (width - with_sign)
        return max(-max_limit, min(max_limit - 1, tmp))

    @staticmethod
    @validate
    def some_other_function(with_sign: int, int_width: int, width: int):
        return True
