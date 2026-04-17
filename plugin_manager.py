import os
import importlib.util


class PluginManager:
    def __init__(self, editor):
        self.editor = editor
        self.plugins = []

    def load_plugins_from_folder(self, folder):
        print("Plugin folder:", folder)

        if not os.path.exists(folder):
            print("Plugin folder NOT FOUND")
            return

        for file in os.listdir(folder):
            if file.endswith(".py"):
                path = os.path.join(folder, file)
                print("Loading plugin:", path)

                try:
                    spec = importlib.util.spec_from_file_location(file[:-3], path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    if hasattr(module, "Plugin"):
                        plugin_instance = module.Plugin(self.editor)

                        info = getattr(module, "PLUGIN_INFO", {
                            "name": file,
                            "description": "No description"
                        })

                        self.plugins.append({
                            "name": info["name"],
                            "description": info["description"],
                            "instance": plugin_instance,
                            "enabled": True,
                            "path": path
                        })

                        if hasattr(plugin_instance, "activate"):
                            plugin_instance.activate()

                    else:
                        print(f"{file} has no Plugin class")

                except Exception as e:
                    print(f"PLUGIN ERROR in {file}: {e}")