from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Any, TypeVar

Component = TypeVar('Component', bound='AbstractComponent')
Config = TypeVar('Config', bound='ComponentConfig')
Input = TypeVar('Input', bound='InputData')

class ComponentConfig(BaseModel):
  ...

class InputData(BaseModel):
  ...

class AbstractComponent(ABC):

  def __init__(self, config: Config):
    self._config = config

  @property
  def config(self) -> Config:
    return self._config
  
  @abstractmethod
  def process(self, input_data: Input) -> Any:
    """
    Process the input data.
    This method needs to be implemented by all child classes.
    """
    pass

