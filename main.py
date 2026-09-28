"""Add shuffled decks and regenerate the cumulative matchup heatmap."""
from src.datagen import main
from functools import wraps
from typing import Callable, Any
from datetime import datetime as dt
import time

def log_calls(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        print(f'{func.__name__} was called: {dt.now()}')
        print(f'Positional arguments: {args}')
        print(f'Keyword arguments: {kwargs}')
        
        t0 = dt.now()
        result = func(*args, **kwargs)
        runtime = dt.now() - t0
        
        print(f'Runtime: {runtime}')
        return result
    return wrapper

if __name__ == "__main__":
    main()
