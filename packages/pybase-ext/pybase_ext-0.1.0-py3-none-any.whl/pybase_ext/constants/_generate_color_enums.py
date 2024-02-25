"""Python script that updates the color enums."""
from typing import Iterator, Tuple, Union

# Table obtained from https://www.rapidtables.com/web/color/RGB_Color.html
# This approach is takes as accessing the url through 'requests' provides a
# security error.
_basic_color_code_table = (
    "Black	#000000	(0,0,0)\n"
    "White	#FFFFFF	(255,255,255)\n"
    "Red	#FF0000	(255,0,0)\n"
    "Green	#00FF00	(0,255,0)\n"
    "Blue	#0000FF	(0,0,255)\n"
    "Yellow	#FFFF00	(255,255,0)\n"
    "Cyan 	#00FFFF	(0,255,255)\n"
    "Aqua	#00FFFF	(0,255,255)\n"
    "Magenta	#FF00FF	(255,0,255)\n"
    "Fuchsia	#FF00FF	(255,0,255)\n"
    "Silver	#C0C0C0	(192,192,192)\n"
    "Gray	#808080	(128,128,128)\n"
    "Maroon	#800000	(128,0,0)\n"
    "Olive	#808000	(128,128,0)\n"
    "Dark_Green	#008000	(0,128,0)\n"
    "Purple	#800080	(128,0,128)\n"
    "Teal	#008080	(0,128,128)\n"
    "Navy	#000080	(0,0,128)\n"
).replace("\t", " ")


def _get_name_and_value(
    bgr_format: bool, hex_format: bool = False
) -> Iterator[Tuple[str, Union[Tuple, str]]]:
    """Extracts and yields the color name in uppercase, and its color code.

    Parameters
    ----------
    bgr_format : bool
        If True, the color code is returned as BGR. Otherwise, as RGB.
    hex_format : bool
        If True, returns the color code as hexadecimal.
    """
    for line in _basic_color_code_table.splitlines():
        name, hex_val_str, code_val_str = line.split()
        if hex_format:
            code_val = hex_val_str.replace("#", "")
        else:
            code_val = tuple(
                int(c)
                for c in code_val_str.replace("(", "").replace(")", "").split(",")
            )
        if bgr_format:
            code_val = code_val[::-1]
        yield name.upper(), code_val


def generate_color_enum(
    class_name: str, enum_type: str, description: str, **kwargs
) -> str:
    """Wrapper to define a whole color enum class."""
    return (
        f"class {class_name}({enum_type}): \n"
        f'\t"""\n\t{description}\n\t"""\n\t'
        + "\n\t".join(
            [f"{name} = {value}" for name, value in _get_name_and_value(**kwargs)]
        )
    )


if __name__ == "__main__":
    color_classes = [
        generate_color_enum(
            class_name="RGB",
            enum_type="TupleEnum",
            description="Enumeration in which members are RGB color codes.",
            bgr_format=False,
        ),
        generate_color_enum(
            class_name="BGR",
            enum_type="TupleEnum",
            description="Enumeration in which members are BGR color codes.",
            bgr_format=True,
        ),
    ]

    mod_text = (
        '"""Module with enumerations containing color codes."""\n'
        "from pybase_ext.enum import TupleEnum\n" + "\n\n".join(color_classes)
    )

    with open("colors.py", "w", encoding="utf-8") as color_module:
        color_module.write(mod_text)
