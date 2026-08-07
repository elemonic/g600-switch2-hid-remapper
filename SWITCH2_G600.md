# Switch 2 + Logitech G600 firmware

[日本語版](SWITCH2_G600.ja.md)

This branch is an unofficial HID Remapper firmware variant for this setup:

- Nintendo Switch 2
- Logitech G600 mouse
- Adafruit Feather RP2040 with USB Type A Host

It addresses a compatibility problem observed on Switch 2. The upstream combined keyboard/mouse HID interface passed the G600 keyboard usages but not its mouse input. A mouse-only diagnostic firmware passed the mouse input but intentionally omitted keyboard input.

The recommended build exposes one composite USB device containing three independent HID interfaces and three distinct interrupt IN endpoints:

1. boot-protocol mouse
2. boot-protocol keyboard
3. HID Remapper configuration and Monitor

The mouse and keyboard input reports do not use Report IDs. The recommended `mouse-first` build places the mouse on interface 0 and the keyboard on interface 1.

## Test status

Short hardware testing on Switch 2 confirmed all of the following at the same time:

- pointer movement
- left, right, and middle click
- vertical wheel
- G600 buttons that produce keyboard keys, including F4 and keypad keys
- another keyboard connected through a USB hub

The test lasted only a few minutes. Extended Final Fantasy XIV gameplay testing, suspend/resume testing, and exhaustive hot-plug testing have not been completed yet. The WebHID configuration interface is retained but has not yet been tested on hardware with this variant.

The diagnostic `keyboard-first` build has not been tested because the recommended mouse-first build already passes both input types.

## Known limitations

- Only the Adafruit Feather RP2040 USB Host build is supported here.
- The exposed mouse report has three buttons: left, right, and middle.
- The exposed keyboard uses the standard boot-keyboard layout: modifiers plus up to six simultaneous non-modifier keys.
- Consumer Control output is not exposed in this variant.
- This is an experimental pre-release with no warranty.

## Installing the UF2

Download `remapper_feather_switch2_g600.uf2` from this fork's [Releases page](https://github.com/elemonic/hid-remapper/releases).

1. Disconnect the Feather from the Switch 2.
2. Connect the Feather USB-C port to a computer.
3. Hold `BOOT`, press and release `RESET`, then release `BOOT`.
4. Copy the UF2 to the `RPI-RP2` drive.
5. Connect the G600 to the Feather USB-A host port, then connect the Feather USB-C port to the Switch 2.

No mapping backup is needed when the HID Remapper configuration is empty. If you have custom mappings, export them before flashing.

To restore the official firmware, download `remapper_feather.uf2` from the upstream [r2026-05-25 release](https://github.com/jfedor2/hid-remapper/releases/tag/r2026-05-25) and flash it with the same BOOT/RESET procedure.

## Building from source

GitHub-generated source ZIP and TAR archives do not contain submodule contents. Clone with submodules instead:

```bash
git clone --branch switch2-g600 --recurse-submodules \
  https://github.com/elemonic/hid-remapper.git
cd hid-remapper
```

Install CMake, Python 3, GNU Make, the Arm GNU embedded toolchain, Newlib, and SRecord. On Ubuntu/Debian, the package names are typically:

```bash
sudo apt install cmake git make python3 \
  gcc-arm-none-eabi libnewlib-arm-none-eabi \
  libstdc++-arm-none-eabi-newlib srecord
```

Build the recommended mouse-first firmware:

```bash
cmake -S firmware -B firmware/build-switch2-g600 \
  -DPICO_BOARD=feather_host \
  -DSWITCH2_SPLIT_HID=ON
cmake --build firmware/build-switch2-g600 \
  --target remapper --parallel 4
```

The result is `firmware/build-switch2-g600/remapper.uf2`.

Validate the USB descriptors compiled into the ELF:

```bash
python3 scripts/validate_switch2_split_elf.py \
  firmware/build-switch2-g600/remapper.elf \
  --order mouse-first
```

For diagnostic comparison only, add `-DSWITCH2_KEYBOARD_FIRST=ON` when configuring and validate with `--order keyboard-first`.

## USB identity

- VID: `0xCAFE` (unchanged from upstream)
- PID: `0xBAF2` (unchanged from upstream)
- product string: `Switch2 MFirst XXXX`, with `XXXX` derived from the Feather unique ID

## License and attribution

The upstream software is MIT-licensed. The original copyright and license notice remain in [LICENSE](LICENSE). Dependency and toolchain notices relevant to the distributed UF2 are collected in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and [LICENSES](LICENSES/).

This project is not affiliated with or endorsed by Nintendo, Logitech, Adafruit, or the upstream HID Remapper project.
