[English](BUILD.md) | 日本語

# GOTOKU-55 のつくりかた

![top](topview.jpg)

## 必要なパーツ

### 電子部品
- [Ploopy Adept PCB](https://github.com/ploopyco/adept-trackball/tree/master/hardware/electronics)
- [ファームウェア](https://github.com/ploopyco/qmk_firmware)
- PMW3360 光学センサ
  - LM19-LSI レンズ
- USB-Cケーブル

電子部品についてはAdeptのキットを買えば揃います。


### 機械部品
- 55mm球
- 皿ネジ x4
  - 横ねじ版の筐体：M2x10mm
  - 縦ねじ版の筐体：M2x7mm
- SMR63ZZ ボールベアリング x3
- （任意）粘着ゴム足 直径8mm 高さ1.6mm x4

筐体の版によってネジの長さが違うので注意してください。なお、記載より多少短いネジでも問題ありません。

いきなり高価な55mm球を買うのを躊躇する場合は55mmの卓球練習用ボールが安価です。

ボールベアリングはステンレス製でないとすぐ錆びます。日本精工製がおすすめです。

### 3Dプリント品
- [ベアリング軸](https://github.com/ploopyco/classic-2-trackball/tree/master/hardware/mechanicals)
- [ベアリングはめこみ治具](https://github.com/ploopyco/classic-2-trackball/tree/master/hardware/mechanicals)
- [GOTOKU 腕](../3d-model/)（どちらか1つ）
  - 一体版：PLAでプリント
    - `gotoku-v4-slim-55mm-smr63-65deg-trackball-support`
  - 分割版：金属の腕とPLAの床
    - `gotoku-v4-slim-55mm-smr63-65deg-trackball-support-split-metal`（金属）
    - `gotoku-v4-slim-55mm-smr63-65deg-trackball-support-split-floor-disc`（PLA）
- 筐体トップとボトム（どれか1組）
  - [small-btu v4 筐体トップとボトム](https://github.com/adept-anyball/ploopy-adept-small-btu/tree/main/v4)
  - [GOTOKU 筐体 横ねじ版](../3d-model/)
    - `gotoku-v4-slim-top-side-screw`、`gotoku-v4-slim-bottom-side-screw`
  - [GOTOKU 筐体 縦ねじ版](../3d-model/)
    - `gotoku-v4-slim-top-vertical-screw`、`gotoku-v4-slim-bottom-vertical-screw`

3Dプリントは適切な向きで行う必要があります。基本的に大きな平面がプレート側です。

腕とボトムには、金属プリントや切削加工に使えるSTEPデータもあります。GOTOKU筐体のトップはSTLのみです。

### 金属部品
腕は分割版をSLM（金属3Dプリント）で金属にすることを推奨します。PLAの腕は55mm球の重さと手のひらの力で外側にたわみますが、金属ならたわみません。私はステンレス316Lでプリントしました。

ボトムの金属化は任意です。重くなって安定するだけです。金属にする場合は、タップ加工を避けるため縦ねじ版を使ってください。

## 組立手順

### ベアリングの組立
治具を使ってベアリングに軸を押し込みます。このとき完全に中央に位置していなくても動作上おそらく影響はないです。

GOTOKU腕パーツにベアリングを押し込みます。押し込みには治具を使うと便利です。押し込んだ後滑らかに回転することを確認してください。

腕の各支柱の外側には直径3mmの穴があります。もし失敗した場合は、この穴につまようじを差し込んでベアリングを後ろから押し出せばやり直せます。

### ケースの組立
分割版の腕を使う場合は、先にPLAの床を金属の腕へ下から入れます。床の縁の小さな突起を前側の支柱に向けてください。床はセンサーレンズで支えられるので、腕を筐体から取り出すと床は落ちます。

筐体トップにGOTOKU腕をはめ込みます。

![trim](need_trim.jpg)

嵌合がきつい場合はプリント時に底面が薄く突き出していないか確認してください。少しヤスリやカッターで整える必要があるかもしれません。

ボールの読み取りやボタンの押下に問題があればケースの調整が必要かもしれません。
3Dプリント品は何度もネジ止めできるほど強度が高くないのでネジ止め前に動作確認をしておきましょう。

縦ねじ版では、ネジは底面から入れてPLAのトップにねじ山を切りながら締まります。締めすぎないでください。

### 結果報告
高価なトラックボール球は部屋の風景やあなたの顔が映り込む可能性があります。
SNSなどに製作したトラックボールの写真を投稿する際は事前に確認しておきましょう。