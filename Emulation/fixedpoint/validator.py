import functools

# from fixedpoint.fixedpoint import Fixedpoint


class Validator:
    @staticmethod
    def width_settings(with_sign: int, frac_width: int, width: int):
        if with_sign not in (0, 1):
            raise ValueError("with_sign must be 0 or 1")
        if frac_width < 0:
            raise ValueError("frac_width cannot be negative")
        if width - frac_width - with_sign < 0:
            raise ValueError(
                f"Constraint failed: {width} - {frac_width} - {with_sign} < 0"
            )

    # def same_params(fp1 : Fixedpoint, fp2 : Fixedpoint):
    # if not fp1.with_sign == fp2.with_sign:
    # raise ValueError("with_sign not the same")
    # if not fp1.frac_width == fp2.frac_width:
    # raise ValueError("frac_width not the same")
    # if not fp1.width == fp2.width:
    # raise ValueError("width not the same")


def validate_init(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import inspect

        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        params = bound_args.arguments
        Validator.width_settings(
            params.get("with_sign"), params.get("frac_width"), params.get("width")
        )

        return func(*args, **kwargs)

    return wrapper


# def validate_same_params(func):
# @functools.wraps(func)
# def wrapper(*args, **kwargs):
# import inspect
# sig = inspect.signature(func)
# bound_args = sig.bind(*args, **kwargs)
# bound_args.apply_defaults()
#
# params = bound_args.arguments
# Validator.same_params(
# params.get('fp1'),
# params.get('fp2')
# )
#
# return func(*args, **kwargs)
# return wrapper
