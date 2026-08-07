#!/usr/bin/env python3

"""Validate the compiled USB descriptors in a Switch 2 mouse-only ELF."""

import argparse
import re
import subprocess
import sys
from pathlib import Path


EXPECTED_CONFIGURATION = bytes.fromhex(
    "09 02 22 00 01 01 00 a0 32 "
    "09 04 00 00 01 03 01 02 00 "
    "09 21 11 01 00 01 22 34 00 "
    "07 05 81 03 40 00 01"
)

EXPECTED_REPORT = bytes.fromhex(
    "05 01 09 02 a1 01 09 01 a1 00 "
    "05 09 19 01 29 03 15 00 25 01 95 03 75 01 81 02 "
    "95 01 75 05 81 03 "
    "05 01 09 30 09 31 09 38 15 81 25 7f 75 08 95 03 81 06 "
    "c0 c0"
)


def run(command: list[str]) -> str:
    return subprocess.run(command, check=True, text=True, capture_output=True).stdout


def find_symbol(nm: str, elf: Path, name: str) -> tuple[int, int]:
    output = run([nm, "-S", "--defined-only", str(elf)])
    for line in output.splitlines():
        fields = line.split()
        if len(fields) == 4 and fields[3] == name:
            return int(fields[0], 16), int(fields[1], 16)
    raise ValueError(f"ELF symbol not found: {name}")


def extract_symbol(nm: str, objdump: str, elf: Path, name: str) -> bytes:
    address, size = find_symbol(nm, elf, name)
    output = run(
        [
            objdump,
            "-s",
            f"--start-address={address:#x}",
            f"--stop-address={address + size:#x}",
            str(elf),
        ]
    )
    result = bytearray()
    for line in output.splitlines():
        fields = line.split()
        if not fields or not re.fullmatch(r"[0-9a-fA-F]+", fields[0]):
            continue
        for field in fields[1:]:
            if not re.fullmatch(r"(?:[0-9a-fA-F]{2}){1,4}", field):
                break
            result.extend(bytes.fromhex(field))
            if len(result) >= size:
                return bytes(result[:size])
    raise ValueError(f"Could not extract all {size} bytes for ELF symbol: {name}")


def validate(elf: Path, tool_prefix: str) -> str:
    nm = f"{tool_prefix}nm"
    objdump = f"{tool_prefix}objdump"
    configuration = extract_symbol(
        nm, objdump, elf, "configuration_descriptor_switch2_mouse_only"
    )
    report = extract_symbol(
        nm, objdump, elf, "our_report_descriptor_switch2_mouse_only"
    )

    if configuration != EXPECTED_CONFIGURATION:
        raise ValueError(
            "Configuration descriptor mismatch\n"
            f"expected: {EXPECTED_CONFIGURATION.hex(' ')}\n"
            f"actual:   {configuration.hex(' ')}"
        )
    if report != EXPECTED_REPORT:
        raise ValueError(
            "HID report descriptor mismatch\n"
            f"expected: {EXPECTED_REPORT.hex(' ')}\n"
            f"actual:   {report.hex(' ')}"
        )

    return "\n".join(
        [
            "PASS: compiled Switch 2 mouse-only USB descriptors match the expected bytes.",
            "",
            "Configuration descriptor:",
            "- Total length: 34 bytes",
            "- HID interfaces: 1",
            "- Interface 0 class: HID (0x03)",
            "- Interface 0 subclass: Boot Interface (0x01)",
            "- Interface 0 protocol: Mouse (0x02)",
            "- Interrupt IN endpoint: 0x81, 64-byte maximum packet, 1 ms interval",
            "- HID report descriptor length: 52 bytes",
            "",
            "HID report descriptor:",
            "- Application collections: 1 (Mouse)",
            "- Report ID items: none",
            "- Input report: 4 bytes (3 buttons, X, Y, vertical wheel)",
            "- X/Y/wheel: signed 8-bit relative values (-127..127)",
            "- Keyboard, Consumer Control, vendor-defined config, and Monitor: absent",
            "",
            f"Configuration bytes: {configuration.hex(' ')}",
            f"Report bytes: {report.hex(' ')}",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("elf", type=Path)
    parser.add_argument(
        "--tool-prefix",
        default="arm-none-eabi-",
        help="prefix including an optional path, ending before nm/objdump",
    )
    args = parser.parse_args()
    try:
        print(validate(args.elf, args.tool_prefix))
    except (OSError, subprocess.CalledProcessError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
