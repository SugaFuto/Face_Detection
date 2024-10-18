from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse, FileResponse
import shutil
import cv2
from ultralytics import YOLO

app = FastAPI()

# YOLOv8モデルをロード
model = YOLO('yolov8s.pt')

@app.post("/uploadimage/")
async def upload_image(file: UploadFile):
    try:
        # 画像ファイルを保存
        file_path = f"uploaded_{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 物体検出
        results = model.predict(file_path)
        result_img = results[0].plot()

        # 検出された画像をファイルに保存
        detected_image_path = f"detected_{file.filename}"
        cv2.imwrite(detected_image_path, result_img)

        return FileResponse(detected_image_path, media_type="image/png", filename=detected_image_path)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
