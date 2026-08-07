#!/usr/bin/env python3

"""Validate compiled USB descriptors in a Switch 2 split-HID ELF."""

import argparse
import subprocess
import sys
from pathlib import Path

from validate_switch2_mouse_only import EXPECTED_REPORT as EXPECTED_MOUSE_REPORT
from validate_switch2_mouse_only import extract_symbol


EXPECTED_KEYBOARD_REPORT = bytes.fromhex(
    "05 01 09 06 a1 01 "
    "05 07 19 e0 29 e7 75 01 95 08 81 02 "
    "75 08 95 01 81 03 "
    "05 07 19 00 2a 91 00 15 00 26 ff 00 95 06 81 00 "
    "05 08 19 01 29 03 15 00 25 01 75 01 95 03 91 02 "
    "95 05 91 03 c0"
)

EXPECTED_CONFIG_REPORT = bytes.fromhex(
    "06 00 ff 09 20 a1 01 09 20 85 64 75 08 95 20 b1 02 c0 "
    "09 21 a1 01 09 21 85 65 75 08 95 3f 81 02 c0"
)


def hid_interface(
    number: int,
    endpoint: int,
    protocol: int,
    report_descriptor_length: int,
) -> bytes:
    return bytes(
        [
            0x09,
            0x04,
            number,
            0x00,
            0x01,
            0x03,
            0x01 if protocol else 0x00,
            protocol,
            0x00,
            0x09,
            0x21,
            0x11,
            0x01,
            0x00,
            0x01,
            0x22,
            report_descriptor_length,
            0x00,
            0x07,
            0x05,
            endpoint,
            0x03,
            0x40,
            0x00,
            0x01,
        ]
    )


def expected_configuration(order: str) -> bytes:
    mouse = lambda number, endpoint: hid_interface(
        number, endpoint, 0x02, len(EXPECTED_MOUSE_REPORT)
    )
    keyboard = lambda number, endpoint: hid_interface(
        number, endpoint, 0x01, len(EXPECTED_KEYBOARD_REPORT)
    )
    config = lambda number, endpoint: hid_interface(
        number, endpoint, 0x00, len(EXPECTED_CONFIG_REPORT)
    )

    first_two = (
        mouse(0, 0x81) + keyboard(1, 0x82)
        if order == "mouse-first"
        else keyboard(0, 0x81) + mouse(1, 0x82)
    )
    return bytes.fromhex("09 02 54 00 03 01 00 a0 32") + first_two + config(2, 0x83)


def require_equal(label: str, actual: bytes, expected: bytes) -> None:
    if actual != expected:
        raise ValueError(
            f"{label} mismatch\n"
            f"expected: {expected.hex(' ')}\n"
            f"actual:   {actual.hex(' ')}"
        )


def validate(elf: Path, tool_prefix: str, order: str) -> str:
    nm = f"{tool_prefix}nm"
    objdump = f"{tool_prefix}objdump"
    configuration = extract_symbol(
        nm, objdump, elf, "configuration_descriptor_switch2_split"
    )
    mouse = extract_symbol(
        nm, objdump, elf, "our_report_descriptor_switch2_mouse_only"
    )
    keyboard = extract_symbol(nm, objdump, elf, "boot_kb_report_descriptor")
    config = extract_symbol(nm, objdump, elf, "config_report_descriptor")

    require_equal(
        "Configuration descriptor", configuration, expected_configuration(order)
    )
    require_equal("Mouse report descriptor", mouse, EXPECTED_MOUSE_REPORT)
    require_equal("Keyboard report descriptor", keyboard, EXPECTED_KEYBOARD_REPORT)
    require_equal("Config report descriptor", config, EXPECTED_CONFIG_REPORT)

    first = "Mouse" if order == "mouse-first" else "Keyboard"
    second = "Keyboard" if order == "mouse-first" else "Mouse"
    return "\n".join(
        [
            f"PASS: compiled Switch 2 {order} split-HID descriptors match the expected bytes.",
            "",
            "Configuration descriptor:",
            "- Total length: 84 bytes",
            "- HID interfaces: 3, each with a distinct interrupt IN endpoint",
            f"- Interface 0 / endpoint 0x81: {first}",
            f"- Interface 1 / endpoint 0x82: {second}",
            "- Interface 2 / endpoint 0x83: vendor config and Monitor",
            "",
            "Input report descriptors:",
            "- Mouse: 4 bytes, no Report ID (3 buttons, X, Y, vertical wheel)",
            "- Keyboard: 8-byte boot layout, no Report ID (modifiers and 6 keys)",
            "- Config/Monitor remains isolated on interface 2 with Report IDs 100/101",
            "",
            f"Configuration bytes: {configuration.hex(' ')}",
            f"Mouse report bytes: {mouse.hex(' ')}",
            f"Keyboard report bytes: {keyboard.hex(' ')}",
            f"Config report bytes: {config.hex(' ')}",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("elf", type=Path)
    parser.add_argument("--order", required=True, choices=("mouse-first", "keyboard-first"))
    parser.add_argument(
        "--tool-prefix",
        default="arm-none-eabi-",
        help="prefix including an optional path, ending before nm/objdump",
    )
    args = parser.parse_args()
    try:
        print(validate(args.elf, args.tool_prefix, args.order))
    except (OSError, subprocess.CalledProcessError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
