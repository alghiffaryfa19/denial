#!/usr/bin/env python3
import sys
import re

FUCHSIA_VAR_OLD = "'download_fuchsia_deps': 'host_os == \"linux\"',\n"
FUCHSIA_VAR_NEW = "'download_fuchsia_deps': False,\n"


def main():
    path = sys.argv[1]
    with open(path, encoding="utf-8") as f:
        s = f.read()

    # Use regex to match the openjdk block robustly
    openjdk_pattern = re.compile(r"^[ \t]*'engine/src/flutter/third_party/java/openjdk': \{.*?\n[ \t]*\},\n", re.MULTILINE | re.DOTALL)
    if not openjdk_pattern.search(s):
        sys.exit(f"patch-deps: openjdk anchor not found in {path}")
    
    s = openjdk_pattern.sub("", s, count=1)

    if FUCHSIA_VAR_OLD not in s:
        sys.exit(f"patch-deps: fuchsia var anchor not found in {path}")
    s = s.replace(FUCHSIA_VAR_OLD, FUCHSIA_VAR_NEW, 1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(s)
    print("patch-deps: removed openjdk cipd, disabled download_fuchsia_deps")


if __name__ == "__main__":
    main()