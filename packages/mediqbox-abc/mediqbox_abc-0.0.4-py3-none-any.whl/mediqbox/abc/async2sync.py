import asyncio
import threading

from typing import Any

from mediqbox.abc.abc_component import AbstractComponent, Component, Input

def start_loop(loop: asyncio.AbstractEventLoop) -> None:
  asyncio.set_event_loop(loop)
  loop.run_forever()

class Async2Sync(AbstractComponent):

  def __init__(self, async_component: Component) -> None:
    self._ac = async_component

  @property
  def ac(self) -> Component:
    return self._ac
  
  def process(self, input_data: Input) -> Any:
    """
    Run the asynchronous _process method in a new thread.
    """
    # Create a new event loop and start it in a new thread.
    loop = asyncio.new_event_loop()
    thread = threading.Thread(target=start_loop, args=(loop,))
    thread.start()

    # Run the async `process` method in the new event loop
    future = asyncio.run_coroutine_threadsafe(
      self._ac.process(input_data), loop
    )

    # Wait for the result of the `_process` method
    result = future.result()

    # Stop the loop and join the thread
    loop.call_soon_threadsafe(loop.stop)
    thread.join()

    return result
