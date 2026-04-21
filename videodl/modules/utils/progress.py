'''
Function:
    Implementation of rich.progress Utils
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from __future__ import annotations
import threading
from rich.console import Console
from typing import Iterable, Optional, TypeVar
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskID, TaskProgressColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn
T = TypeVar("T")


'''GlobalProgressManager'''
class GlobalProgressManager:
    _instance: Optional["GlobalProgressManager"] = None
    _instance_lock = threading.Lock()
    def __init__(self) -> None:
        self._started = False
        self._active_tasks = 0
        self._lock = threading.RLock()
        self._console = Console()
        self._progress = Progress(SpinnerColumn(), TextColumn("[bold blue]{task.description}"), BarColumn(), TaskProgressColumn(), TimeElapsedColumn(), TimeRemainingColumn(), console=self._console, expand=True, transient=True)
    '''instance'''
    @classmethod
    def instance(cls) -> "GlobalProgressManager":
        if cls._instance is None:
            with cls._instance_lock: cls._instance = cls._instance or cls()
        return cls._instance
    '''ensurestarted'''
    def ensurestarted(self) -> None:
        if not self._started: self._progress.start(); self._started = True
    '''createtask'''
    def createtask(self, description: str, total: Optional[float] = None) -> TaskID:
        with self._lock: self.ensurestarted(); task_id = self._progress.add_task(description=description, total=total); self._active_tasks += 1; return task_id
    '''update'''
    def update(self, task_id: TaskID, *, advance: Optional[float] = None, completed: Optional[float] = None, total: Optional[float] = None, description: Optional[str] = None, visible: Optional[bool] = None) -> None:
        kwargs = {k: v for k, v in {"advance": advance, "completed": completed, "total": total, "description": description, "visible": visible}.items() if v is not None}
        with self._lock: self._progress.update(task_id, **kwargs)
    '''removetask'''
    def removetask(self, task_id: TaskID) -> None:
        with self._lock:
            try: self._progress.remove_task(task_id)
            finally: self._active_tasks -= 1; self._active_tasks = max(self._active_tasks, 0); (self._progress.stop(), setattr(self, "_started", False)) if self._active_tasks == 0 and self._started else None
    '''log'''
    def log(self, *args, **kwargs) -> None:
        with self._lock: self.ensurestarted(); self._progress.console.log(*args, **kwargs)


'''TaskProgress'''
class TaskProgress:
    def __init__(self, description: str, total: Optional[float] = None) -> None:
        self.total = total
        self.description = description
        self._task_id: Optional[TaskID] = None
        self._manager = GlobalProgressManager.instance()
    '''enter'''
    def __enter__(self) -> "TaskProgress":
        self._task_id = self._manager.createtask(description=self.description, total=self.total)
        return self
    '''exit'''
    def __exit__(self, exc_type, exc, tb) -> bool:
        if self._task_id is not None: self._manager.removetask(self._task_id); self._task_id = None
        return False
    '''aenter'''
    async def __aenter__(self) -> "TaskProgress":
        return self.__enter__()
    '''aexit'''
    async def __aexit__(self, exc_type, exc, tb) -> bool:
        return self.__exit__(exc_type, exc, tb)
    '''advance'''
    def advance(self, n: float = 1) -> None:
        if self._task_id is None: raise RuntimeError("Progress task has not been entered yet. Use 'with' or 'async with'.")
        self._manager.update(self._task_id, advance=n)
    '''update'''
    def update(self, *, advance: Optional[float] = None, completed: Optional[float] = None, total: Optional[float] = None, description: Optional[str] = None, visible: Optional[bool] = None) -> None:
        if self._task_id is None: raise RuntimeError("Progress task has not been entered yet. Use 'with' or 'async with'.")
        self._manager.update(self._task_id, advance=advance, completed=completed, total=total, description=description, visible=visible)
    '''track'''
    def track(self, iterable: Iterable[T]) -> Iterable[T]:
        for item in iterable: yield item; self.advance(1)
    '''log'''
    def log(self, *args, **kwargs) -> None:
        self._manager.log(*args, **kwargs)


'''taskprogress'''
def taskprogress(description: str, total: Optional[float] = None) -> TaskProgress:
    return TaskProgress(description=description, total=total)


'''progresslog'''
def progresslog(*args, **kwargs) -> None:
    GlobalProgressManager.instance().log(*args, **kwargs)