
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse
import shutil
import torch
from PIL import Image
import io
from ultralytics import 

app = FastAPI()
# YOLOv8モデルをロード
model = YOLO('yolov8s.pt')
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
###################################################################

async def upload_image(file: UploadFile):
    try:

        
        # 画像ファイルを保存
        file_path = f"uploaded_{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 物体検出
        results = model(file_path)
        result_img = results[0].plot()

        # 検出された画像をファイルに保存
        detected_image_path = f"detected_{file.filename}"
        result_img.save(detected_image_path)

        return FileResponse(detected_image_path, media_type="image/png", filename=detected_image_path)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
