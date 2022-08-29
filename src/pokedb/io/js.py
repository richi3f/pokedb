__all__ = ["read_js", "to_js"]

import json

from pokedb.core.typing import PathLike

JS_PREFIX = "export default "
JS_SUFFIX = ";"


def read_js(file_path: PathLike, **kwargs) -> dict:
    with open(file_path, "r", encoding="utf-8") as file:
        file.seek(len(JS_PREFIX))
        json_str = file.read()[: -len(JS_SUFFIX)]
    return json.loads(json_str, **kwargs)


def to_js(data: dict, file_path: PathLike, **kwargs) -> None:
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(JS_PREFIX + json.dumps(data, **kwargs) + JS_SUFFIX)
