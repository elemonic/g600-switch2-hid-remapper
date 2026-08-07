# Switch 2版FF14でLogitech G600を使う

G600をSwitch 2版FF14で使いたくて、個人が趣味で少し手を入れた[HID Remapper](https://www.remapper.org/)用のファームウェアです。Logitech G600のマウス操作とサイドボタンのキー入力を、Nintendo Switch 2へ同時に送ります。

必要なのは、USB-A端子付きの小さな基板1枚とUSBケーブルです（私は半田付けが苦手なのでUSB-A実装済み基板を購入）。Switch 2との繋ぎ方には、動作未チェックの項目もあります。

> [!CAUTION]
> これは非公式の実験的な方法です。Nintendo、スクウェア・エニックス、Logitech、Adafruit、本家HID Remapperとは関係ありません。
>
> ソースコード、ファームウェア、文書は、すべて現状有姿（AS IS）で公開します。動作、互換性、安全性、継続利用を保証せず、更新、修正、個別サポートを続ける義務も負いません。利用するかどうかは、ご自身で判断してください。
>
> 適用法令で認められる範囲において、作者およびコントリビューターは、機器の故障、データ損失、本プロジェクトの利用または利用不能から生じた損害を補償しません。詳しくは[MIT License](LICENSE)を確認してください。
>
> この派生版で起きた問題を、本家HID Remapperへ報告しないでください。

このページへのリンクや、実際に試した結果の共有は歓迎します。**アフィリエイト記事への利用はご遠慮ください。** 注意書きを省いて商品リンクを並べ、「これで動く」などと購入を促すような紹介をされると困ります。そういう目的の方は、ここでお帰りください。

## 買う前に

- 動作確認したのは、下に書いた機器の組み合わせだけです。
- Switch 2側やFF14側の更新で動かなくなる可能性があります。反対に、将来の更新で変換基板なしでもG600を使えるようになる可能性もあります。
- 数分程度の実機試験では動きましたが、長時間プレイ、スリープ復帰、すべての抜き差し手順までは確認していません。
- 基板やケーブルを買う場合は、以上を了承したうえで判断してください。

## 用意するもの

### 基本の機材

1. **Logitech G600 MMO Gaming Mouse**
2. **Adafruit Feather RP2040 with USB Type A Host**（[スイッチサイエンス](https://www.switch-science.com/products/8956) / [Adafruit公式](https://www.adafruit.com/product/5723)）
3. **データ通信対応のUSBケーブル** — Feather側はUSB-Cです。Switch 2側は接続方法に合わせます。私の構成ではドック相当機器のUSB-A端子へ挿すため、USB-A―USB-Cケーブルを使いました。[^cable]

> [!NOTE]
> Raspberry Pi Picoを使った本家HID Remapperや自作基板へ、この変更を移植できる可能性はあります。ただし、今回配布しているUF2はFeather RP2040 USB Host専用です。ほかの基板では動作確認していませんし、このUF2を書き込まないでください。本家の候補は[ハードウェア資料](HARDWARE.md)で確認できます。

## 1. ファームウェアをダウンロードする

[`remapper_feather_switch2_g600.uf2`](https://github.com/elemonic/g600-switch2-hid-remapper/releases/download/switch2-g600-v0.1.0-rc.1/remapper_feather_switch2_g600.uf2) をダウンロード

<details>
<summary>ハッシュの確認、ソースの確認・ビルド</summary>

ハッシュを確認する場合、正しいSHA-256は次の値です。

```text
7b1f4a3cee5a9f6f8d9e4aa0793f46ff40b2480d48f85bb394dfc93ec5aa811f
```

Windows PowerShellでは、ダウンロードしたフォルダーで次を実行します。

```powershell
Get-FileHash .\remapper_feather_switch2_g600.uf2 -Algorithm SHA256
```

macOSでは次を実行します。

```bash
shasum -a 256 remapper_feather_switch2_g600.uf2
```

Linuxでは次を実行します。

```bash
sha256sum remapper_feather_switch2_g600.uf2
```

Releaseにある`SHA256SUMS.txt`でも同じ値を確認できます。ソースを読んだり自分でビルドしたりする場合は、[この版のソースとビルド手順](https://github.com/elemonic/g600-switch2-hid-remapper/blob/switch2-g600-v0.1.0-rc.1/SWITCH2_G600.ja.md#ソースからのビルド)へ進んでください。

</details>

## 2. Featherへ書き込む

1. G600とSwitch 2からFeatherを外します。
2. FeatherのUSB-C端子とPCを、データ通信対応ケーブルでつなぎます。
3. Featherの`BOOT`ボタンを押したまま、`RESET`ボタンを一度押して離します。
4. `RPI-RP2`というドライブがPCに表示されたら、`BOOT`を離します。
5. `RPI-RP2`へ`remapper_feather_switch2_g600.uf2`をコピーします。
6. コピー後にドライブが消えたら書き込み完了です。

Featherは裸の基板です。通電中に金属や水分へ触れない場所へ置き、端子やケーブルへ無理な力がかからないようにしてください。ケースへ入れる場合も、`BOOT`と`RESET`を押せるものが便利です。

## 3. Switch 2へつなぐ

現在、動作を確認できているのは次の構成です。

```text
Logitech G600
    ↓ USB-A
Feather RP2040 USB Host
    ↓ USB-C
USB-A―USB-Cケーブル（データ通信対応）
    ↓ USB-A
非純正のドック相当機器
    ↓ USB-C
Nintendo Switch 2 本体下部のUSB-C端子
```

これで接続完了です。追加ドライバーやSwitch 2側の専用設定はありません。

### 未確認の構成

- 純正Nintendo Switch 2ドックのUSB-A端子へFeatherを接続し、TVモードで使う
- 現在の非純正ドック相当機器から映像を出し、TVモードで使う
- FeatherをSwitch 2本体上部のUSB-C端子へ直接接続する

TVモードは、適合するHDMIケーブルが手元にないため未確認です。[^hdmi]

## G600のサイドボタンを変更したい場合

Switch 2上ではLogitechの設定ソフトが動きません。G600のボタン割り当てを変える場合は、先にPCで設定し、G600の**オンボードメモリ**へ保存してください。PC上のゲームを検出して切り替わるプロファイルは、Switch 2へ持っていけません。

オンボードメモリについては、[Logicool公式サポート](https://support.logi.com/hc/ja/articles/360023411353)も参照してください。

## うまく動かないとき

- `RPI-RP2`が出ない：充電専用ではなく、データ通信対応ケーブルか確認します。`BOOT`を押したまま`RESET`を押し、ドライブが出るまで`BOOT`を押し続けます。
- Featherの電源は入るがSwitch 2で反応しない：ケーブルがデータ通信対応か、UF2のファイル名、各コネクターが奥まで挿さっているかを確認します。一度すべて外してからつなぎ直します。
- マウスは動くがサイドボタンが想定と違う：G600のオンボードメモリに保存された割り当てをPCで確認します。
- 別のマウスや基板で動かない：今回の実機確認対象はG600とFeather RP2040 USB Hostだけです。

詳しい動作確認範囲、既知の制限、USBの構成は[技術情報](SWITCH2_G600.ja.md)にまとめています。

[^cable]: 実機試験では、スイッチサイエンスで購入したUSB-A―USB-Cケーブルを使いました。製品名は未確認です。充電専用ではなく、データ通信対応のものが必要です。高価なUSB4ケーブルは必要ありません。
[^hdmi]: 任天堂はSwitch 2のTVモードに、同梱の[ウルトラ ハイスピードHDMIケーブル](https://support.nintendo.com/jp/switch2/play/use/playmode/tvmode/index.html)を案内しています。このファームウェアの確認だけを目的に、新しいHDMIケーブルを購入する必要はありません。
