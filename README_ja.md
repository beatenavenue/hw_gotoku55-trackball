[English](README.md) | 日本語

> トラックボールはKensington SlimBlade ProとElecom Comfyを買えばゴールであるとされている。  
> しかしもっと小さい筐体は実現できないものだろうか。

![overview](docs/gotoku55.jpg)

# GOTOKU-55 トラックボール

## これは何？
これは、55mmトラックボールの**部品**です。順に知る必要があります。

### Ploopy Adept
カナダの小さな会社Ploopyが開発した、44mm玉(1.75in ≒ 44.5mm)のトラックボールがAdeptです。設計データとファームウェアはオープンソースで公開されていますが、部品を自分で揃えると寸法が合わないことがあるため、Ploopy公式ストアでキットか組み立て済み品を買うことが推奨されています。

- リンク: [Adept Trackball](https://ploopy.co/adept-trackball/)

#### 日本在住者向けの特記事項
最も入手難と思われる光学センサPixArt PMW3360が遊舎工房で販売されているため、PCB作成や3Dプリントに明るい人は自作したほうが早い可能性があります。レンズはLM19-LSIを使用することに注意してください。

### Anyball
Adept Anyballは、Adeptのケースを作り替えて、ボールの支持をBTU（ボールトランスファユニット）に変える改造のプロジェクトです。ケースの種類を選ぶことで、34mmの小玉から68mmのビリヤード球まで使えます。データはGitHubで公開されていて、3Dプリンタで出力して組み立てます。

もちろん55mm版もあるのですが、支える部分が低い位置となるため操作球は筐体から大きく飛び出しておりあまり操作性はよくありません。

- リンク: [Adept Anyball](https://github.com/adept-anyball/)

### small-btu v4 (Slim)
Anyballのプロジェクト内で公開されている、Fabricio Bastian氏による34mm/38mm玉用の小型ケースです。分割キーボードの間に配置するため極限まで低背化されていて、デザインも非常に美しく洗練されています。  
おそらくボタン部の高さだけでいえば市販最小級のKeychron Nape Proよりも低いと思われます。薄型キーボードを好むなら魅力的です。

- リンク: [adept-anyball/ploopy-adept-small-btu](https://github.com/adept-anyball/ploopy-adept-small-btu)

### GOTOKU-55
small-btu v4に55mm球を乗せるのはかなり厳しいです。球自体が大きい上に、BTU対応のため腕もかなり巨大なので、ほとんど操作不能でしょう。  
ですからより小型化できるようPloopy版と同じボールベアリングを使う前提で55mmを支える腕部品を作成しました。これがGOTOKU-55です。五徳、見ての通りです。

![handling](docs/handling.jpg)

基本的には腕部品のみでよいです。small-btu v4筐体は完成されていて美しいのでそのまま利用できます。  
ただし私の持ち方のような場合はv4のままでは支障があります。親指を寝かせて手前のボタンを操作すると、筐体の角が指にぶつかってしまうからです。

ですからこの持ち方をする人向けに、手前のボタンを縁まで拡張した改造版も作成しました。  
ネジ穴などはv4のままですからトップだけプリントすればよいですが、前縁の壁部分が消失して寂しい見た目になるためボトムも作っています。

## 互換性
small-btu v4 のみ対応。

v5も形状が似ているので利用できる可能性がありますが、試算ではおそらくボールが少し干渉します。

## つくりかた
[製作方法](docs/BUILD_ja.md)を参照

## ライセンス
Copyright (C) 2026 Kotaro WAJIKI  
Based on ploopy-adept-small-btu v4, Copyright (C) Fabricio Bastian  
Licensed under the GNU General Public License v3.0
