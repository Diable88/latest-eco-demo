from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
from PIL import Image
import io
import base64

app = FastAPI()

# Cấu hình static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Cấu hình templates
templates = Jinja2Templates(directory="templates")

# Lưu đường dẫn ảnh chân dung đã xoá nền
image_path = ""

# Hàm gọi API Remove.bg để xoá nền ảnh
def remove_background(image):
    api_key = 'aT27DhgMkcEWQkkNbVabUqeK'

    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        headers={'X-Api-Key': api_key},
        files={'image_file': image}
    )

    if response.status_code == requests.codes.ok:
        return response.content
    else:
        return None

# Hàm xử lý khi người dùng nhấn nút "Chọn ảnh"
def select_image():
    global image_path
    # TODO: Xử lý lấy đường dẫn file ảnh chân dung

@app.post("/upload-image/")
async def upload_image(image: UploadFile = File(...)):
    try:
        # Xoá nền ảnh sử dụng API Remove.bg
        removed_bg_image = remove_background(image.file)

        if removed_bg_image:
            # Resize ảnh đã xoá nền về kích thước 450x650
            img_portrait = Image.open(io.BytesIO(removed_bg_image)).convert("RGBA")
            img_portrait_resized = img_portrait.resize((450, 650))

            # TODO: Tiếp tục xử lý tạo ảnh merged và trả về template HTML

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)