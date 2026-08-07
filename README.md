# Logitech G600をNintendo Switch 2で使う

Logitech G600のマウス操作とサイドボタンのキー入力を、Nintendo Switch 2版FF14へ同時に送るための非公式HID Remapper派生ファームウェアです。

## [購入・書き込み・接続の手順はこちら](START_HERE.ja.md)

> [!CAUTION]
> 個人が趣味で作った実験的なファームウェアです。Nintendo、スクウェア・エニックス、Logitech、Adafruit、本家HID Remapperによる公式提供・推奨ではありません。
>
> この派生版で起きた問題を、本家HID Remapperへ報告しないでください。

## 現在の状態

Adafruit Feather RP2040 with USB Type A HostとG600を使った短時間の実機試験で、次の入力が同時に動くことを確認しました。

- カーソル移動
- 左・右・中央クリック
- 縦ホイール
- F4やテンキーを含むG600のキー入力

長時間プレイ、純正Nintendo Switch 2ドックでのTVモード、本体上部USB-Cへの直結などは未確認です。対応範囲と注意点は[導入ガイド](START_HERE.ja.md)を確認してください。

## ダウンロードと技術情報

- [v0.1.0-rc.1 Release](https://github.com/elemonic/hid-remapper/releases/tag/switch2-g600-v0.1.0-rc.1)
- [日本語の技術情報・ビルド手順](SWITCH2_G600.ja.md)
- [Technical notes and build instructions](SWITCH2_G600.md)
- [第三者ライセンス・通知](THIRD_PARTY_NOTICES.md)

## 本家プロジェクトとの関係

このリポジトリは、[jfedor2/hid-remapper](https://github.com/jfedor2/hid-remapper)の`r2026-05-25`を基準にしたforkです。Switch 2とG600向けの変更や配布物に関する責任は、このfork側にあります。

本家HID Remapperの通常版、対応ハードウェア、設定方法については、[remapper.org](https://www.remapper.org/)と[本家リポジトリ](https://github.com/jfedor2/hid-remapper)を参照してください。

## ライセンス

ソフトウェアは、個別に記載がある場合を除き[MIT License](LICENSE)です。元の著作権表示とライセンス文はそのまま残しています。

このリポジトリに含まれるハードウェア設計は、個別に記載がある場合を除き[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)です。配布UF2に関係する依存物とツールチェーンの通知は[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)および[LICENSES](LICENSES/)にまとめています。
