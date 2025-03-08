import argparse
import os

REPLACE_MAP = {
    "_Y-_": "_Y+_",
    "_Y+_": "_Y-_",
    "_X-_": "_Z+_",
    "_Z-_": "_X+_",
    "_X+_": "_Z-_"
}


def main(file_names, in_place, silent):
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

        target_file_name = ""
        if in_place:
            target_file_name = file_name

        else:
            file_name_no_ext, file_ext = os.path.splitext(file_name)
            file_base_name = os.path.basename(file_name_no_ext)
            new_file_name = os.path.join(os.path.dirname(file_name),
                                         file_base_name + "_modified" + file_ext)
            target_file_name = new_file_name

        with open(target_file_name, 'w') as target:
            target.writelines(lines_modified)
            if not silent:
                print("Went through {} lines and replaced {} occurences in {}.".
                    format(
                        len(lines_modified),
                        len(replace_positions),
                        os.path.basename(target_file_name)
                    )
                )



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_names", nargs='+')
    parser.add_argument("--in_place", action='store_true')
    parser.add_argument("--silent", action='store_true')

    args = parser.parse_args()

    main(args.file_names, args.in_place, args.silent)
    if not args.silent:
        print("Done.")
