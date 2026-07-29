

class Validator:
    """
    Validates and normalizes execution plans before execution.
    """

    def __init__(self):

        self.schemas = {

            "application": {

                "launch": ["target"],
                "terminate": ["target"],
                "activate": ["target"],
                "minimize": ["target"],
                "maximize": ["target"],
                "close_window": ["target"],
            },

            "browser": {

                "open_url": ["url"],
                "search": ["query"],
                "new_tab": [],
                "list_tabs": [],
                "switch_tab": ["index"],
                "close_tab": [],
                "title": [],
                "metadata": [],
                "text": [],
                "close": [],
            },

            "filesystem": {
                "create_file": ["path"],
                "delete_file": ["path"],
                "rename_file": ["source", "destination"],
                "move_file": ["source", "destination"],
                "copy_file": ["source", "destination"],
                "read_file": ["path"],
                "write_file": ["path", "content"],
                "append_file": ["path", "content"],
                "create_folder": ["path"],
                "delete_folder": ["path"],
                "list_folder": ["path"],
                "search_file": ["root", "filename"],
                },

                "desktop": {
                "move_mouse": ["x", "y"],
                "click": [],
                "double_click": [],
                "right_click": [],
                "scroll": ["amount"],
                "type_text": ["text"],
                "press_key": ["key"],
                "hotkey": ["keys"],
                "drag": ["x", "y"],
                "screenshot": ["path"],
                "wait": ["seconds"],
                "position": [],
                "screen_size": [],
                },
                "system": {
    "battery": [],
    "system_info": [],
    "current_time": [],
    "clipboard_get": [],
    "clipboard_set": ["text"],
    "list_processes": [],
    "shutdown": [],
    "restart": [],
    "lock": [],
    "sleep": [],
    "get_brightness": [],
    "set_brightness": ["value"],
    "get_volume": [],
    "set_volume": ["value"],
    "mute": [],
    "unmute": [],
},
"vision": {
    "screenshot": ["path"],
    "read_text": ["image_path"],
    "image_size": ["image_path"],
    "image_info": ["image_path"],
    "find_template": ["image_path", "template_path"],
    "grayscale": ["image_path", "output_path"],
}
        }


        self.aliases = {

            "target": [
                "name",
                "app",
                "application",
                "program"
            ],

            "url": [
                "website",
                "link"
            ],

            "query": [
                "search",
                "keyword",
                "text"
            ],

            "index": [
                "tab",
                "tab_index"
            ]

        }

    def _normalize_parameters(self, parameters):

        normalized = dict(parameters)

        for canonical, aliases in self.aliases.items():

            if canonical in normalized:
                continue

            for alias in aliases:

                if alias in normalized:

                    normalized[canonical] = normalized[alias]
                    break

        return normalized

    def validate_step(self, step: dict):

        capability = step["capability"].lower()
        action = step["action"].lower()

        if not capability:
            raise ValueError("I couldn't understand that command.")

        if capability not in self.schemas:
            raise ValueError(f"Unknown capability '{capability}'.")
        if action not in self.schemas[capability]:
            raise ValueError(
            f"Unknown action '{action}' for capability '{capability}'."
        )

        parameters = self._normalize_parameters(
            step.get("parameters", {})
        )

        required = self.schemas[capability][action]

        for field in required:

            if field not in parameters:
                raise ValueError(
                f"Missing parameter '{field}'"
            )

        step["capability"] = capability
        step["action"] = action
        step["parameters"] = parameters

        return step
    def validate(self, command: dict):
        return self.validate_step(command)