# gl2f share

[gl2f](https://github.com/trnciii/gl2f-cli) のアドオンで、ファンクラブ記事を共有するためのSNS投稿文を作成します。
ハッシュタグやurl を簡単に追加することができます。


## インストール方法

必要なもの
* gl2f 0.3.13 以上
  * [pypi 最新版](https://pypi.org/project/gl2f/)
  * [github](https://github.com/trnciii/gl2f-cli/releases) (windows.zip または macos.zip から実行ファイルを取得できます。詳細は https://github.com/trnciii/gl2f-cli)
* python3 (3.8以上) とpip

1. pip を用いて本パッケージをインストールします。 `pip install gl2f-share`
2. `gl2f config edit` > addons > add  を選択すると追加するアドオン名の入力が求められます。
3. `gl2f_share` と入力し設定を追加します。
4. `gl2f share --help` を実行し、インストールされたコマンドのヘルプが表示されることを確認します。
5. bash 補完を使用している場合は、このコマンドも追加されているので再設定します。 `eval "$(gl2f completion)"`


## 使い方

`gl2f share <board>` のように対象となる記事を指定して投稿作成を始めます。

編集のため以下の操作をおこないます。
* `Compose a post:` 投稿の本文を入力します。
* `edit hashtags? (y/N)` メンバー名やグループ名のハッシュタグを追加します。日記などにはデフォルトで関連するハッシュタグが追加されています。

投稿の作成後の行動を選択します。
* `copy to clipboard` クリップボードに本文をコピーします。
* `continue on X` Xの投稿作成へ進みます。
* `print` ターミナル上に出力します。
