from flask import Blueprint
import importlib
import pkgutil
import inspect


def register_blueprints(app, package_name, package_path):
    """Автоматическая регистрация всех Blueprint-ов в указанном пакете."""
    for _, name, _ in pkgutil.iter_modules([package_path]):
        module = importlib.import_module(f"{package_name}.{name}")

        for obj_name, obj in inspect.getmembers(module):
            if isinstance(obj, Blueprint):
                app.register_blueprint(obj)
