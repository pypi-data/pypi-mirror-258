import json
from slugify import slugify
from typer import Typer
from botifyme.cli.root import app
from botifyme.registry import tool_registry
from botifyme.utils.tools import get_class_details, get_function_details

worker_app = Typer(name="worker", help="Worker commands for botifyMe.dev.")
app.add_typer(worker_app)


@worker_app.command("exec", help="Execute worker.")
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


@worker_app.command("tools", help="List all available tools.")
def list_tools():

    tools = []
    for tool_name, details in tool_registry.items():
        class_details = get_class_details(details["class"])

        tool_payload = {
            "name": tool_name,
            "description": class_details["description"],
            "slug": slugify(tool_name),
        }

        functions = []

        for func_name, func in details["functions"].items():
            function_details = get_function_details(func)

            function_payload = {
                "name": func_name,
                "description": function_details["description"],
                "function_call": function_details,
                "slug": slugify(func_name),
            }
            functions.append(function_payload)

        tool_payload["functions"] = functions
        tools.append(tool_payload)

    print(json.dumps(tools, ensure_ascii=False))
