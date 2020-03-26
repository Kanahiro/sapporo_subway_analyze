このスクリプトを実行するにはrequirements.txtに記載のモジュールのほか、popplerをインストールしPATHを通しておく必要があります。

## Scheduling
毎日11時に、札幌市ウェブサイトからPDFを取得してCSVファイルに変換します。

## API Specification
以下のURLで個別のデータを直接取得出来ます。
https://kanahiro.github.io/sapporo_subway_analyze/api/data/{路線名}/{データ時点}/{PDFで右の表か左の表か}/{データのインデックス}/

例1：南北線、3月2週、右表の全データ
https://kanahiro.github.io/sapporo_subway_analyze/api/data/namboku/3gatsu2shu/right/

例2：東豊線、3月3週の全データ
https://kanahiro.github.io/sapporo_subway_analyze/api/data/toho/3gatsu3shu/