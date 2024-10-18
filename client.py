# import requests

# url = "http://127.0.0.1:8000/uploadimage/"
# files = {"file": open("imagesdog.jpg", "rb")}
# response = requests.post(url, files=files)

# print(response.status_code)
# print(response.json())
import requests

# APIエンドポイント
url = "http://127.0.0.1:8000/uploadimage/"
# 送信する画像のパス
image_path = "imagesdog."

# 画像をPOSTして検出結果を取得
files = {"file": open(image_path, "rb")}
response = requests.post(url, files=files)

# 画像を保存する
if response.status_code == 200:
    print("画像が保存されました: detected_image.png")
else:
    print("画像の取得に失敗しました")
