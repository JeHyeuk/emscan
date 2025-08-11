from functools import wraps


def mandatory(*required_keys):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            missing = [key for key in required_keys if key not in kwargs]
            if missing:
                raise ValueError(f"필수 키워드 인자가 누락되었습니다: {', '.join(missing)}")
            return func(*args, **kwargs)
        return wrapper
    return decorator
