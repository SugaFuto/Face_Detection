from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse, FileResponse
import shutil
import cv2
from ultralytics import YOLO
import logging

logging.basicConfig(level=logging.INFO)
face_cascade_path = "opencv/haarcascade_frontalface_alt.xml"
eye_cascade_path = "opencv/haarcascade_eye.xml"
app = FastAPI()

# YOLOv8モデルをロード
#model = YOLO('yolov8s.pt')
model = YOLO('weights/1st_best.pt')

@app.post("/uploadimage/")
# async def upload_image(file: UploadFile):
#     try:
#         # 画像ファイルを保存
#         file_path = f"uploaded_{file.filename}"
#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         # 物体検出
#         results = model.predict(file_path)
#         result_img = results[0].plot()

#         # 検出された画像をファイルに保存
#         detected_image_path = f"detected_{file.filename}"
#         cv2.imwrite(detected_image_path, result_img)

#         return FileResponse(detected_image_path, media_type="image/png", filename=detected_image_path)
#     except Exception as e:
#         return JSONResponse(content={"message": str(e)}, status_code=500)

async def upload_image(file: UploadFile):
    try:
        # 画像ファイルを保存
        file_path = f"uploaded_{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # カスケード分類器を読み込む
        face_cascade = cv2.CascadeClassifier(face_cascade_path)
        eye_cascade = cv2.CascadeClassifier(eye_cascade_path)
        
        # ファイルパスの検証
        if not face_cascade.load(face_cascade_path):
            raise ValueError(f"Failed to load face cascade from {face_cascade_path}")
        if not eye_cascade.load(eye_cascade_path):
            raise ValueError(f"Failed to load eye cascade from {eye_cascade_path}")
        
        # 画像を読み込む
        src = cv2.imread(file_path)
        if src is None:
            raise ValueError(f"Failed to read image from {file_path}")
        
        # グレースケールに変換
        src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        
        # 顔を検出
        faces = face_cascade.detectMultiScale(src_gray)
        for (x, y, w, h) in faces:
            cv2.rectangle(src, (x, y), (x + w, y + h), (0, 0, 255), 2)
            face = src[y: y + h, x: x + w]
            face_gray = src_gray[y: y + h, x: x + w]
            eyes = eye_cascade.detectMultiScale(face_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(face, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
        
        # 検出された画像を保存
        detected_image_path = f"detected_{file.filename}"
        cv2.imwrite(detected_image_path, src)
        
        return FileResponse(detected_image_path, media_type="image/png", filename=detected_image_path)
    except Exception as e:
        logging.error(f"Error: {e}")
        return JSONResponse(content={"message": str(e)}, status_code=500)








if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)





