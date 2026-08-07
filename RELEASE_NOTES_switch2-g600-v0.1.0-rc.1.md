# Switch 2 + Logitech G600 firmware v0.1.0-rc.1

> Experimental, unofficial pre-release for Adafruit Feather RP2040 with USB Type A Host.

This firmware exposes mouse, keyboard, and HID Remapper configuration/Monitor as separate HID interfaces. It is intended to let a Logitech G600 pass both mouse and keyboard-style button input to Nintendo Switch 2.

## Hardware test status

Short Switch 2 testing confirmed pointer movement, left/right/middle click, vertical wheel, G600 F4/keypad input, and an additional keyboard through a USB hub. Extended Final Fantasy XIV gameplay testing has not yet been completed.

## Assets

- `remapper_feather_switch2_g600.uf2` — recommended mouse-first firmware
- `SHA256SUMS.txt` — SHA-256 integrity check
- `THIRD_PARTY_LICENSES.tar.gz` — license notices accompanying the firmware

See the [English guide](https://github.com/elemonic/hid-remapper/blob/switch2-g600/SWITCH2_G600.md) or [Japanese guide](https://github.com/elemonic/hid-remapper/blob/switch2-g600/SWITCH2_G600.ja.md) before flashing.

To restore official firmware, use `remapper_feather.uf2` from the upstream [r2026-05-25 release](https://github.com/jfedor2/hid-remapper/releases/tag/r2026-05-25).

---

# Switch 2＋Logitech G600用ファームウェア v0.1.0-rc.1

Adafruit Feather RP2040 with USB Type A Host向けの、非公式・実験的なpre-releaseです。

Mouse、Keyboard、HID Remapper設定／Monitorを別々のHIDインターフェースとして提示し、G600のマウス入力とキーボード形式のボタン入力をSwitch 2へ同時に通します。

短時間のSwitch 2試験では、カーソル、左右・中央クリック、縦ホイール、G600のF4／テンキー入力、USBハブ上の別キーボードが動作しました。FF14での長時間試験は未実施です。

書き込み前に[日本語ガイド](https://github.com/elemonic/hid-remapper/blob/switch2-g600/SWITCH2_G600.ja.md)を確認してください。
