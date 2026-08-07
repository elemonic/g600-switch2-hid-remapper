# Switch 2＋Logitech G600用ファームウェア

[English](SWITCH2_G600.md)

初めて導入する場合は、先に[購入から接続までのガイド](START_HERE.ja.md)を参照してください。

このブランチは、次の構成向けに作成した非公式のHID Remapper派生版です。

- Nintendo Switch 2
- Logitech G600マウス
- Adafruit Feather RP2040 with USB Type A Host

Switch 2では、本家のKeyboard／Mouse複合HIDインターフェースを使うとG600のキーボード入力だけが通り、マウス入力が通らない現象がありました。原因切り分け用のMouse専用版では、反対にマウス入力だけが正常に通りました。

推奨版では、Featherを1台の複合USB機器として列挙し、その中に3つの独立したHIDインターフェースと3つの異なるInterrupt INエンドポイントを提示します。

1. Boot Protocol Mouse
2. Boot Protocol Keyboard
3. HID Remapperの設定／Monitor

MouseとKeyboardの入力レポートにはReport IDを付けません。推奨する`mouse-first`版では、Mouseをインターフェース0、Keyboardをインターフェース1に配置します。

## 実機確認状況

Switch 2での短時間試験では、次の入力が同時に通ることを確認しました。

- カーソル移動
- 左・右・中央クリック
- 縦ホイール
- F4やテンキーを含む、G600が出すキーボード入力

試験時間は数分程度です。FF14での長時間プレイ、スリープ復帰、あらゆる抜き差しパターンは未確認です。WebHID設定用インターフェースは残していますが、この派生版での実機確認はまだ行っていません。

Keyboard優先版は診断用です。Mouse優先版で両方の入力が通ったため、通常利用のための検証は行っていません。

## 既知の制限

- 対応対象はAdafruit Feather RP2040 USB Host版だけです。
- Mouse出力は左・右・中央の3ボタンです。
- Keyboard出力は標準Boot Keyboard形式で、修飾キーと最大6個の通常キーを同時出力できます。
- Consumer Control出力は提示しません。
- 実験的なpre-releaseであり、無保証です。

## UF2の書き込み

このforkの[Releasesページ](https://github.com/elemonic/g600-switch2-hid-remapper/releases)から`remapper_feather_switch2_g600.uf2`をダウンロードします。

1. FeatherをSwitch 2から外します。
2. FeatherのUSB-C側をPCへ接続します。
3. `BOOT`を押したまま`RESET`を押して離し、その後`BOOT`を離します。
4. 表示された`RPI-RP2`ドライブへUF2をコピーします。
5. G600をFeatherのUSB-A Host端子へ接続し、FeatherのUSB-C側をSwitch 2へ接続します。

HID Remapperの設定が空なら、事前のマッピング保存は不要です。独自マッピングがある場合は、書き込み前にエクスポートしてください。

公式版へ戻す場合は、本家の[r2026-05-25 Release](https://github.com/jfedor2/hid-remapper/releases/tag/r2026-05-25)から`remapper_feather.uf2`を取得し、同じBOOT／RESET手順で書き込みます。

## ソースからのビルド

GitHubが自動生成するSource ZIP／TARにはサブモジュールの中身が入りません。次のようにサブモジュール込みでcloneしてください。

```bash
git clone --branch switch2-g600 --recurse-submodules \
  https://github.com/elemonic/g600-switch2-hid-remapper.git
cd g600-switch2-hid-remapper
```

CMake、Python 3、GNU Make、Arm GNU組み込みツールチェーン、Newlib、SRecordが必要です。Ubuntu／Debian系では通常、次のパッケージを使用します。

```bash
sudo apt install cmake git make python3 \
  gcc-arm-none-eabi libnewlib-arm-none-eabi \
  libstdc++-arm-none-eabi-newlib srecord
```

推奨するMouse優先版をビルドします。

```bash
cmake -S firmware -B firmware/build-switch2-g600 \
  -DPICO_BOARD=feather_host \
  -DSWITCH2_SPLIT_HID=ON
cmake --build firmware/build-switch2-g600 \
  --target remapper --parallel 4
```

生成物は`firmware/build-switch2-g600/remapper.uf2`です。

コンパイル済みELF内のUSB記述子を検証できます。

```bash
python3 scripts/validate_switch2_split_elf.py \
  firmware/build-switch2-g600/remapper.elf \
  --order mouse-first
```

診断目的でKeyboard優先版を作る場合だけ、CMake構成時に`-DSWITCH2_KEYBOARD_FIRST=ON`を追加し、検証時は`--order keyboard-first`を指定します。

## USB識別情報

- VID: `0xCAFE`（本家から変更なし）
- PID: `0xBAF2`（本家から変更なし）
- 製品文字列: `Switch2 MFirst XXXX`（`XXXX`はFeather固有IDから生成）

## ライセンスと帰属

本家ソフトウェアはMIT Licenseです。元の著作権表示とライセンス文は[LICENSE](LICENSE)に残しています。配布UF2に関係する依存物とツールチェーンの通知は[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)および[LICENSES](LICENSES/)にまとめています。

このプロジェクトはNintendo、Logitech、Adafruit、本家HID Remapperプロジェクトによる公式提供・推奨ではありません。
