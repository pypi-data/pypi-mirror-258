import sys
from typing import Dict, Any
import pprint

# append to system path
sys.path.append("..")

from agentscript import Interpreter
from agent_tools import Tool, action


# Create a fake translator tool
class Translator(Tool):
    """A fake translator tool"""

    @action
    def translate(self, text: str, options: Dict[str, Any]) -> str:
        return "Hola"

    def close(self):
        pass


def test_interpret_full_message():
    # Create the interpreter supplying our translator tool
    interpreter = Interpreter(tools=[Translator()])

    # Parse the script, find the tool, and execute it
    interpreter.execute(
        """
    We need to do translation <invoke tool="Translator" action="translate" parameters={"text": "Hello", "options": {"from": "en", "to": "es"}} />
    """
    )

    invocations = interpreter.invocations()
    assert len(invocations) == 1

    pprint.pprint(invocations[0].__dict__)
    assert invocations[0].result == "Hola"


if __name__ == "__main__":
    test_interpret_full_message()
