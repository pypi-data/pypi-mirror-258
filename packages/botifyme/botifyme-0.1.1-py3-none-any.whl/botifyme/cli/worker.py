import asyncio
import signal
import json
from typer import Typer
from botifyme.cli.root import app
from botifyme.registry import tool_registry

worker_app = Typer(name="worker", help="Worker commands for botifyMe.dev.")
app.add_typer(worker_app)


@worker_app.command("exec", help="Start the worker.")
def execute_worker(json_payload: str):

    # Check if the payload is a valid JSON
    try:
        payload = json.loads(json_payload)

        class_name = payload['class']
        func_name = payload['function']
        args = payload.get('args', {})

        if class_name in tool_registry:

            tool = tool_registry[class_name]
            clazz = tool["class"]
            functions = tool["functions"]
            if func_name in functions:
                func = functions[func_name]
                instance = clazz()
                _result = getattr(instance, func_name)(**args)
                args = {
                    "response": _result,
                    "status": "success"
                }

                json_string = json.dumps(args, ensure_ascii=False)
                print(json_string)
            else:
                result = f"Function {func_name} not found in {class_name}."
                args = {
                    "response": result,
                    "status": "error"
                }

    except json.JSONDecodeError:
        print("Invalid JSON payload.")
        return
