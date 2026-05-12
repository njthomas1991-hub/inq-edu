from importlib import import_module


def _export(module_name: str) -> None:
	try:
		module = import_module(f".{module_name}", __name__)
	except ModuleNotFoundError:
		return

	names = getattr(module, "__all__", None)
	if names is None:
		names = [name for name in dir(module) if not name.startswith("_")]

	for name in names:
		globals()[name] = getattr(module, name)


for _module_name in ("public_views", "auth_views", "profile_views", "avatar_views"):
	_export(_module_name)

del _export, import_module