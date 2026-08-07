# Using Logitech G600 on Nintendo Switch 2

[日本語](README.md)

This unofficial HID Remapper firmware variant uses an [Adafruit Feather RP2040 with USB Type A Host](https://www.adafruit.com/product/5723) to make both Logitech G600 mouse input and side-button keyboard input available in FINAL FANTASY XIV on Nintendo Switch 2.

## [Installation and technical guide](SWITCH2_G600.md)

> [!CAUTION]
> This is an experimental personal project. It is not provided or endorsed by Nintendo, Square Enix, Logitech, Adafruit, or the upstream HID Remapper project.
>
> Operation is not guaranteed. Updates to Nintendo Switch 2 or FINAL FANTASY XIV may make this firmware stop working; conversely, future updates may make this firmware unnecessary.
>
> Do not report problems with this variant to the upstream HID Remapper project.

## Current status

Short hardware testing with a Logitech G600 and an Adafruit Feather RP2040 with USB Type A Host confirmed all of the following at the same time:

- pointer movement
- left, right, and middle click
- vertical wheel
- G600 keyboard input, including function keys (F1-F12) and keypad keys

Extended gameplay, TV mode with the official Nintendo Switch 2 dock, and a direct connection to the console's top USB-C port have not been tested. See the [installation and technical guide](SWITCH2_G600.md) for the tested scope and limitations.

## Reporting a problem

If a problem is reproducible with this variant, please use the [bug report form](https://github.com/elemonic/g600-switch2-hid-remapper/issues/new?template=bug_report.yml) to let us know. The form is currently in Japanese. Because this is a personal hobby project, no response, investigation, or fix is guaranteed. Do not report problems with this variant to the upstream HID Remapper project.

## Downloads and documentation

- [v0.1.0-rc.1 Release](https://github.com/elemonic/g600-switch2-hid-remapper/releases/tag/switch2-g600-v0.1.0-rc.1)
- [Japanese setup guide](START_HERE.ja.md)
- [Technical notes and build instructions](SWITCH2_G600.md)
- [Third-party notices](THIRD_PARTY_NOTICES.md)

## Relationship to upstream

This repository is a fork of [jfedor2/hid-remapper](https://github.com/jfedor2/hid-remapper), based on `r2026-05-25`. The Switch 2 and G600 changes and release assets are maintained independently in this fork and are not supported by the upstream project.

For the regular HID Remapper firmware, supported hardware, and configuration instructions, see [remapper.org](https://www.remapper.org/) and the [upstream repository](https://github.com/jfedor2/hid-remapper).

## Disclaimer

All source code, firmware, and documentation in this project are provided as is, without any warranty of operation, compatibility, safety, or continued availability. You are responsible for deciding whether to use them.

To the extent permitted by applicable law, the authors and contributors are not liable for damage to a Nintendo Switch 2, G600, Feather, or any other equipment; loss or corruption of data; loss caused by inability to use the project; or any other direct or indirect damages arising from use of or inability to use the project. There is no obligation to provide continued updates, fixes, or individual support. See the [MIT License](LICENSE) for the license terms.

## License

The software is licensed under the [MIT License](LICENSE), unless stated otherwise. The original copyright and license notice are retained.

Hardware designs in this repository are licensed under the [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/), unless stated otherwise. Dependency and toolchain notices relevant to the distributed UF2 are collected in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and [LICENSES](LICENSES/).
