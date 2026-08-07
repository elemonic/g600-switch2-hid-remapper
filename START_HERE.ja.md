# Switch 2版FF14でLogitech G600を使う

G600をSwitch 2版FF14で使いたくて、個人が趣味で少し手を入れたファームウェアです。Logitech G600のマウス操作とサイドボタンのキー入力を、Nintendo Switch 2へ同時に送ります。

必要なのは、USB-A端子付きの小さな基板1枚とUSBケーブルです。はんだ付けはしません。ただし、Switch 2とのつなぎ方には、まだ確認中の構成があります。

> [!CAUTION]
> これは非公式の実験的な方法です。Nintendo、スクウェア・エニックス、Logitech、Adafruit、本家HID Remapperとは関係ありません。
>
> 突然使えなくなる、最初から環境によっては動かない、公式の更新によってこの基板自体が不要になる、といった可能性があります。購入費用、故障、データ損失、そのほか使用によって生じた損害の責任は負えません。

このページへのリンクや、実際に試した結果の共有は歓迎します。ただし、注意書きを省いて商品リンクだけ並べ、「これを買えば必ず動く」と誘導するアフィリエイト記事への利用は遠慮してください。そういう目的の方は、ここでお帰りください。

## 買う前に

- 動作確認したのは、下に書いた機器の組み合わせだけです。
- Switch 2側やFF14側の更新で動かなくなる可能性があります。反対に、将来の更新で変換基板なしでもG600を使えるようになる可能性もあります。
- 数分程度の実機試験では動きましたが、長時間プレイ、スリープ復帰、すべての抜き差し手順までは確認していません。
- 基板やケーブルを買う場合は、以上を了承したうえで判断してください。

## 用意するもの

### 基本の機材

1. **Logitech G600 MMO Gaming Mouse**
2. **[Adafruit Feather RP2040 with USB Type A Host（Product ID 5723）](https://www.adafruit.com/product/5723)**
3. **データ通信対応のUSBケーブル**

実機試験では、スイッチサイエンスで購入したUSB-A―USB-Cケーブルを使いました。製品名は未確認です。充電専用ではなく、データ通信に対応したケーブルが必要です。高価なUSB4ケーブルは必要ありません。

PCへの書き込みとSwitch 2への接続にUSB-A―USB-Cケーブルを使う場合、PCやドック相当機器のUSB-A側へ挿し、FeatherのUSB-C側へつなぎます。

Switch 2本体へ直接つなぐ場合はUSB-C―USB-Cケーブルを使う想定です。Switch 2に付属するUSB-C充電ケーブル`BEE-011`は、[任天堂の案内](https://support.nintendo.com/jp/switch2/mastery/screenshot/manage/index.html)でもデータ転送対応とされています。ただし、この直結方法は今回まだ試していません。

筆者ははんだ付けが苦手なので、最初からUSB-A端子が付いているFeather RP2040 USB Hostを選びました。この基板ならG600をそのまま挿せます。

> [!NOTE]
> Raspberry Pi Picoを使った本家HID Remapperや自作基板へ、この変更を移植できる可能性はあります。ただし、今回配布しているUF2はFeather RP2040 USB Host専用です。ほかの基板では動作確認していませんし、このUF2を書き込まないでください。本家の候補は[ハードウェア資料](HARDWARE.md)で確認できます。

## 1. ファームウェアをダウンロードする

[v0.1.0-rc.1のReleaseページ](https://github.com/elemonic/hid-remapper/releases/tag/switch2-g600-v0.1.0-rc.1)を開き、Assetsから次のファイルをダウンロードします。

[`remapper_feather_switch2_g600.uf2`をダウンロード](https://github.com/elemonic/hid-remapper/releases/download/switch2-g600-v0.1.0-rc.1/remapper_feather_switch2_g600.uf2)

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

Releaseにある`SHA256SUMS.txt`でも同じ値を確認できます。ソースを読んだり自分でビルドしたりする場合は、[この版のソースとビルド手順](https://github.com/elemonic/hid-remapper/blob/switch2-g600-v0.1.0-rc.1/SWITCH2_G600.ja.md#ソースからのビルド)へ進んでください。

## 2. Featherへ書き込む

1. G600とSwitch 2からFeatherを外します。
2. FeatherのUSB-C端子とPCを、データ通信対応ケーブルでつなぎます。
3. Featherの`BOOT`ボタンを押したまま、`RESET`ボタンを一度押して離します。
4. `RPI-RP2`というドライブがPCに表示されたら、`BOOT`を離します。
5. `RPI-RP2`へ`remapper_feather_switch2_g600.uf2`をコピーします。
6. コピー後にドライブが消えたら書き込み完了です。

初期状態のHID Remapperでマッピングを追加していなければ、設定のバックアップは不要です。独自のマッピングがある場合だけ、先に設定をJSONへエクスポートしてください。

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

非純正のドック相当機器とFeatherの間は、直接接続した場合と、USBハブを挟んだ場合の両方を短時間だけ確認しています。使用したドック相当機器、ケーブル、ハブの製品名は確認中です。

この構成では、追加ドライバーやSwitch 2側の専用設定は使いませんでした。短時間の試験では、カーソル移動、左右・中央クリック、縦ホイール、F4やテンキーを含むG600のキー入力を同時に確認しました。USBハブへ別のキーボードも接続できましたが、ハブの機種を含めて保証はできません。

次の構成はまだ試していません。導入に必要な手順とは分け、今後の確認事項として残しています。

- 純正Nintendo Switch 2ドックのUSB-A端子へFeatherを接続し、TVモードで使う
- 現在の非純正ドック相当機器から映像を出し、TVモードで使う
- FeatherをSwitch 2本体上部のUSB-C端子へ直接接続する

TVモードは、適合するHDMIケーブルが手元にないため未確認です。任天堂はSwitch 2のTVモードに、同梱の[ウルトラ ハイスピードHDMIケーブル](https://support.nintendo.com/jp/switch2/play/use/playmode/tvmode/index.html)を案内しています。このファームウェアを試すためだけに、新しいHDMIケーブルを購入する必要はありません。

## G600のサイドボタンを変更したい場合

Switch 2上ではLogitechの設定ソフトが動きません。G600のボタン割り当てを変える場合は、先にPCで設定し、G600の**オンボードメモリ**へ保存してください。PC上のゲームを検出して切り替わるプロファイルは、Switch 2へ持っていけません。

オンボードメモリについては、[Logicool公式サポート](https://support.logi.com/hc/ja/articles/360023411353)も参照してください。

## うまく動かないとき

- `RPI-RP2`が出ない：充電専用ではなく、データ通信対応ケーブルか確認します。`BOOT`を押したまま`RESET`を押し、ドライブが出るまで`BOOT`を押し続けます。
- Featherの電源は入るがSwitch 2で反応しない：ケーブルがデータ通信対応か、UF2のファイル名、各コネクターが奥まで挿さっているかを確認します。一度すべて外してからつなぎ直します。
- マウスは動くがサイドボタンが想定と違う：G600のオンボードメモリに保存された割り当てをPCで確認します。
- 別のマウスや基板で動かない：今回の実機確認対象はG600とFeather RP2040 USB Hostだけです。

## 元へ戻す

本家HID Remapperの[r2026-05-25 Release](https://github.com/jfedor2/hid-remapper/releases/tag/r2026-05-25)から`remapper_feather.uf2`をダウンロードし、同じBOOT／RESET手順で書き込みます。

詳しい動作確認範囲、既知の制限、USBの構成は[技術情報](SWITCH2_G600.ja.md)にまとめています。
