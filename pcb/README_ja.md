[English](README.md) | 日本語

# GOTOKU PCB v1

Ploopy Adept トラックボールのメイン基板 Ploopy Madromys（R1.001）の改変版です。
JLCPCB の部品実装（PCBA）付きで発注し、小さな部品を手はんだしなくて済むようにすることが目的です。

**これは Ploopy の公式製品ではありません。Ploopy へ問い合わせないでください。**

まだ製造も動作確認もしていません。

## 2つの版

USB-C コネクタだけが違う2つの版があります。

| フォルダ | USB-C コネクタ | 備考 |
|---|---|---|
| [original](original/) | JAE DX07S016JA1R1500（LCSC C3197885） | 元の基板と同じコネクタ・配線です。 |
| [hro](hro/) | HRO TYPE-C-31-M-12（LCSC C165948） | JLCPCB で少し安くなります。コネクタ周りの配線を手作業で変更しています。 |

各フォルダの中身は次のとおりです。

- `*.kicad_pcb` は KiCad 用の基板データです。
- `*-gerber.zip` はガーバーとドリルのデータです。
- `*-BOM-JLC.csv` と `*-CPL-JLC.csv` は JLCPCB の部品実装用の部品表と配置ファイルです。
- `*-gerber-preview.png` はガーバーのプレビュー画像です。

## JLCPCB での発注

- 4層、板厚 0.8 mm
- Assemble top side（上面実装）
- 同じ版の BOM と CPL をアップロードします。

BOM で LCSC 番号が空欄の部品は JLCPCB では実装されません。
スイッチ（D2LS-21）と光学センサ（PMW3360DM-T2QU）がこれにあたります。手はんだしてください。

## 元データからの変更点

元データは [ploopyco/adept-trackball](https://github.com/ploopyco/adept-trackball) の Altium プロジェクトです（`hardware/electronics/PCBs/Madromys`、コミット `2ec4576`）。
変換したのは基板だけで、回路図は変換していません。回路は元の回路図 PDF を見てください。

### Altium から KiCad への変換

KiCad 7 の Altium インポータで変換しました。変換後に次の修正が必要でした。

- 光学センサ用の四角い穴を、基板外形の切り欠きにしました。
- USB-C コネクタの位置決め穴2つを、メッキなし穴にしました。
- 銅箔の中の、ごく短く壊れた円弧10か所を直線に置き換えました。
- 板厚を 0.8 mm に設定しました。値は Altium の層構成から求めました。

### 実装しない部品

次の部品は「DNP（未実装）」にしています。BOM と CPL からは外していますが、パッドは基板に残っています。

| 部品番号 | 部品 | 理由 |
|---|---|---|
| LED.D.1, LED.D.3 | アドレス指定可能な RGB LED | Ploopy のファームウェアが使っていません。多くの場合、外から光が見えません。 |
| LED.C.20, LED.C.23, LED.R.9, LED.R.16 | LED 用のコンデンサと抵抗 | LED がないので不要です。 |
| USB.R.12, USB.R.14 | CC1・CC2 の 10k 抵抗 | 元は各 CC 線に 10k を2本並列にしています。この基板では 5.1k を1本にしました。 |
| MCU.J.1 | 2ピンヘッダ | 元の製品と同じく、ヘッダは付けません。2つの穴はブートローダの起動に使います（後述）。 |

### 値の変更と代替部品

| 部品番号 | 元 | この基板 |
|---|---|---|
| USB.R.13, USB.R.15 | 10k 1% | 5.1k 1%（各 CC 線に1本） |
| USB.Z.1 | IP4220CZ6（ESD 保護） | SRV05-4（LCSC C384887）。ピン配置は同じです。 |
| REG.U.4 | AP2204K-1.8 | AP2112K-1.8（LCSC C176944）。ピン配置は同じです。 |
| MCU.Y.1 | RH100-12.000-16-3030（12 MHz、16 pF） | X322512MSB4SI（12 MHz、20 pF、LCSC C9002）。負荷コンデンサは 18 pF のままです。 |

REG.C.15（100 pF）は、元プロジェクトの BoM バリアントでは「未実装」になっています。
この基板では実装します。

その他の受動部品は、同じ値・同じサイズの一般的な LCSC 部品に置き換えました。

### シルク

- 基板名「Madromys R1.001 / August 2023」を「GOTOKU PCB v1」に変更しました。
- 「MCH.FID.1」の表示を消しました。
- 上面にロゴと改変の表示を追加しました。

### HRO 版のみの変更

HRO のコネクタはパッドの配置が違うため、`hro` 版だけ次の変更をしています。

- コネクタのフットプリントを KiCad ライブラリの `USB_C_Receptacle_HRO_TYPE-C-31-M-12` に置き換えました。位置と向きは元のコネクタと同じです。
- コネクタ付近の D+、D-、CC1、CC2、VBUS の配線を新しいパッドに合わせて変更しました。
- VBUS のビアを1つ移動し、コネクタ下の GND ビアを1つ削除しました。
- 新しい配線とパッドの周りのベタを削りました。

コネクタ付近の接続とクリアランスはスクリプトで確認しました。
**基板全体の DRC はまだ実行していません。この版を発注する前に、KiCad 8 以降で DRC を実行してください。**
`Madromys-usb-area-orig-vs-hro.png` で、両方の版のコネクタ周りを比較できます。

## ブートローダの起動

最初のファームウェア書き込みでは必要ありません。
新しい基板はフラッシュメモリが空なので、RP2040 が自動でブートローダ（BOOTSEL モード）で起動します。

あとでファームウェアを更新するときは、左下のボタン（matrix [0,0]）を押したまま USB ケーブルを挿します。

ファームウェアが壊れていてボタンが効かない場合は、LED.D.3 の近くにある MCU.J.1 の2つの穴を使います。
金属のピンセットで2つの穴をつないだまま、USB ケーブルを挿してください。
片方の穴は GND です。もう片方は 1k 抵抗を通してフラッシュメモリのチップセレクト線につながっています。

## ライセンス

このフォルダのファイルは CERN Open Hardware Licence Version 2 - Strongly Reciprocal（CERN-OHL-S-2.0）で公開しています。
[LICENSE](LICENSE) を見てください。
GPL-3.0 であるこのリポジトリの他の部分とはライセンスが異なります。

- 元の設計: Ploopy Corporation による Ploopy Madromys R1.001（Ploopy Adept）。CERN-OHL-S-2.0。
  ソース: https://github.com/ploopyco/adept-trackball
- 改変: Copyright (C) 2026 Kotaro WAJIKI。2026-10-11 に改変。変更内容は上の「元データからの変更点」のとおりです。
- この改変版のソースの所在（Source Location）: https://github.com/beatenavenue/hw_gotoku55-trackball/tree/main/pcb

この設計は無保証で提供されます。ライセンスの第6節を見てください。
