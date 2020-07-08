# click-warp-perspective
click-warp-perspectiveはマウスクリックで指定した座標を矩形に射影変換するプログラムです。<br>
このプログラムを単体で使うというよりは、抜き出した矩形の画像を更に別の処理にかけるような使い方を想定しています。 

## 動作例
![loz2q-f546w](https://user-images.githubusercontent.com/37477845/86814717-bf0e6e00-c0bc-11ea-85e8-ef41a4f534e0.gif)

# Requirement
 
* OpenCV 3.4.2(or later)
 
# Installation
 
ディレクトリを丸ごとコピーして実行してください。
 
# Usage
 
サンプルの実行方法は以下です。
 
```bash
python main.py
```

以下のコマンドラインオプションがあります。

--device：OpenCVのVideoCapture()で開くカメラデバイスorファイル

--width：カメラキャプチャサイズ(幅)

--height：カメラキャプチャサイズ(高さ)

--crop_width：射影変換後の矩形のサイズ(幅)

--crop_height：射影変換後の矩形のサイズ(高さ)

ウィンドウの任意のポイント4点をマウス左クリックすることで対象を指定します。

キーボードの「0」～「9」を押すことでIDを指定できます。

また、「C」を押すことで、現在選択中のIDのポイントをリセットします。


# Author
高橋かずひと(https://twitter.com/KzhtTkhs)
 
# License 
click-warp-perspective is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).

