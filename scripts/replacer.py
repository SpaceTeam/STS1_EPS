import argparse
import os

REPLACE_MAP = {
    "Panel_Y-_": "Panel_Y+_",
    "Panel_Y+_": "Panel_Y-_",
    "Panel_X-_": "Panel_Z+_",
    "Panel_Z-_": "Panel_X+_",
    "Panel_X+_": "Panel_Z-_"
}


def main(file_names, in_place):
    for file_name in file_names:
        with open(file_name, 'r') as f:
            lines = f.readlines()
        replace_positions = []
        for line_number, line_str in enumerate(lines):
            for key, value in REPLACE_MAP.items():
                if key in line_str:
                    replace_positions.append({"line": line_number, "from": key, "to": value})

        lines_modified = lines
        for replace_position in replace_positions:
            at = replace_position["line"]
            from_str = replace_position["from"]
            to_str = replace_position["to"]
            lines_modified[at] = lines_modified[at].replace(from_str, to_str)

        if in_place:
            with open(file_name, 'w') as target:
                target.writelines(lines_modified)

        else:
            file_name_no_ext, file_ext = os.path.splitext(file_name)
            file_base_name = os.path.basename(file_name_no_ext)
            new_file_name = os.path.join(os.path.dirname(file_name),
                                         file_base_name + "_modified" + file_ext)

            with open(new_file_name, 'w') as target:
                target.writelines(lines_modified)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_names", nargs='+')
    parser.add_argument("--in_place", action='store_true')

    args = parser.parse_args()

    main(args.file_names, args.in_place)
