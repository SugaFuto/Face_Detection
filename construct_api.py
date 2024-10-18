
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse
import shutil
from PIL import Image
import io
# from ultralytics import YOLO
import cv2

app = FastAPI()
# YOLOv8モデルをロード
# model = YOLO('yolov8s.pt')
@app.post("/uploadimage/")
#################################################画像をそのまま返すtestOK
# async def upload_image(file: UploadFile):
#     try:
#         # 画像ファイルを保存
#         with open(f"uploaded_{file.filename}", "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)
        
#         # 画像の保存に成功した場合のレスポンス
#         return JSONResponse(content={"message": "File uploaded successfully!"})
#     except Exception as e:
#         return JSONResponse(content={"message": str(e)}, status_code=500)
##################################################################
##cv2で描画し，保存する→OK
# async def upload_image(file: UploadFile):
    try:
        # 画像ファイルを保存
        file_path = f"uploaded_{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 画像を読み込んでOpenCVで編集
        img = cv2.imread(file_path)
        height, width, _ = img.shape

        # ランダムな四角形を挿入
        start_point = (50, 50)
        end_point = (width-50, height-50)
        color = (0, 255, 0) # 緑色の四角形
        thickness = 3
        img = cv2.rectangle(img, start_point, end_point, color, thickness)

        # 編集された画像を保存
        edited_image_path = f"edited_{file.filename}"
        cv2.imwrite(edited_image_path, img)

        # 編集された画像を返す
        return StreamingResponse(open(edited_image_path, "rb"), media_type="image/png")
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)

# async def upload_image(file: UploadFile):
#     try:

        
#         # 画像ファイルを保存
#         file_path = f"uploaded_{file.filename}"
#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)
        
#         # 物体検出
#         results = model(file_path)
#         result_img = results[0].plot()

#         # 検出された画像をファイルに保存
#         detected_image_path = f"detected_{file.filename}"
#         result_img.save(detected_image_path)

#         return FileResponse(detected_image_path, media_type="image/png", filename=detected_image_path)
#     except Exception as e:
#         return JSONResponse(content={"message": str(e)}, status_code=500)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
