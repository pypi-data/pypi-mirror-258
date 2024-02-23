from typing import ClassVar, Optional, Any


class Singleton:
    """一个用于实现单例设计模式的类。"""
    _instance: ClassVar[Optional[Any]] = None

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def _drop(cls) -> None:
        cls._instance = None
