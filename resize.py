import os
from PIL import Image

def resize_and_pad_image(target_size=(500, 500)):
    # 取得指令碼所在的資料夾路徑
    folder_path = os.path.dirname(os.path.abspath(__file__))
    
    # 支援的圖片格式
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff')
    
    # 建立輸出資料夾
    output_folder = os.path.join(folder_path, "resized_with_padding")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"已建立輸出資料夾: {output_folder}")

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(valid_extensions):
            image_path = os.path.join(folder_path, filename)
            
            try:
                with Image.open(image_path) as img:
                    # 1. 計算等比例縮小的尺寸（不超過 500x500）
                    img.thumbnail(target_size, Image.Resampling.LANCZOS)
                    
                    # 2. 根據原圖格式決定背景色
                    # 如果是 PNG 支援透明度，使用透明背景 (0,0,0,0)；其餘使用純白背景 (255,255,255)
                    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                        background_color = (0, 0, 0, 0)
                        new_img = Image.new('RGBA', target_size, background_color)
                    else:
                        background_color = (255, 255, 255)
                        new_img = Image.new('RGB', target_size, background_color)
                    
                    # 3. 將縮小後的圖片置中貼到背景上
                    offset = (
                        (target_size[0] - img.size[0]) // 2,
                        (target_size[1] - img.size[1]) // 2
                    )
                    new_img.paste(img, offset)
                    
                    # 4. 儲存圖片
                    output_path = os.path.join(output_folder, filename)
                    new_img.save(output_path)
                    print(f"成功處理並填補邊框: {filename}")
                    
            except Exception as e:
                print(f"處理 {filename} 時發生錯誤: {e}")

if __name__ == "__main__":
    print("開始調整圖片大小並加入填補...")
    resize_and_pad_image()
    print("處理完成！請查看 'resized_with_padding' 資料夾。")
