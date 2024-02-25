from typing import List, Dict, Any, Optional
from enum import Enum
import time
import uuid

from agent_tools import Tool

from agentscript_rs import Parser, InvokeData


class InvokationStatus(Enum):
    CREATED = "created"
    FINISHED = "finished"
    IN_PROGRESS = "in progress"
    FAILED = "failed"
    NOT_STARTED = "not started"


class Invocation:
    """An action invocation"""

    def __init__(
        self,
        tool: Tool,
        action: str,
        parameters: Dict[str, Any],
        index: int,
        created_time: float = time.time(),
        status: InvokationStatus = InvokationStatus.CREATED,
        finished_time: Optional[float] = None,
        result: Optional[Any] = None,
        approved: bool = False,
    ):
        self.tool = tool
        self.action = action
        self.parameters = parameters
        self.created_time = created_time
        self.status = status
        self.finished_time = finished_time
        self.index = index
        self.id = str(uuid.uuid4())
        self.result = result
        self.approved = approved


class Interpreter:
    """An agentscript interpreter"""

    def __init__(self, tools: List[Tool], approve: bool = False):
        self.parser = Parser()
        self.tools: Dict[str, Tool] = {tool.__class__.__name__: tool for tool in tools}
        self.approve = approve
        self._invocations: List[Invocation] = []

    def execute(self, msg: str) -> None:
        self.parser.parse(msg)

        for i, data in enumerate(self.parser.get_parsed_data()):
            tool: Optional[Tool] = self.tools.get(data.tool)
            if not tool:
                raise Exception(f"Tool {data.tool} not found")

            invocation = Invocation(tool, data.action, data.get_parameters(), index=i)

            # check to see if the invocation has already happened based on the index
            if len(self._invocations) >= i + 1:
                print("invocation already happened")
                continue

            invocation = self.invoke(invocation)
            self._invocations.append(invocation)

    def get_parsed_data(self) -> list[InvokeData]:
        return self.parser.get_parsed_data()

    def invocations(self) -> List[Invocation]:
        return self._invocations

    def invoke(self, invocation: Invocation) -> Invocation:

        invocation.status = InvokationStatus.IN_PROGRESS

        action = invocation.tool.find_action(invocation.action)
        if not action:
            raise (Exception(f"Action {invocation.action} not found"))

        try:
            result = invocation.tool.use(action, **invocation.parameters)
        except Exception as e:
            invocation.status = InvokationStatus.FAILED
            invocation.result = e
            raise e

        invocation.finished_time = time.time()
        invocation.result = result
        invocation.status = InvokationStatus.FINISHED

        return invocation
