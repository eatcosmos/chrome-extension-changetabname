from PIL import Image
import os
import glob

def resize_image(image_path, size=(640, 400)):
    """调整图片大小并保持宽高比"""
    try:
        with Image.open(image_path) as img:
            # 计算新的尺寸，保持宽高比
            width, height = img.size
            ratio = min(size[0]/width, size[1]/height)
            new_size = (int(width * ratio), int(height * ratio))
            
            # 调整大小，使用高质量的重采样
            resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # 创建新的白色背景图像
            final_img = Image.new('RGB', size, (255, 255, 255))
            
            # 将调整大小的图像粘贴到中心
            x = (size[0] - new_size[0]) // 2
            y = (size[1] - new_size[1]) // 2
            final_img.paste(resized_img, (x, y))
            
            # 保存图片，在文件名中添加 _resized
            filename, ext = os.path.splitext(image_path)
            new_path = f"{filename}_resized{ext}"
            final_img.save(new_path, quality=95)
            print(f"已处理: {os.path.basename(image_path)} -> {os.path.basename(new_path)}")
            return new_path
    except Exception as e:
        print(f"处理 {image_path} 时出错: {e}")
        return None

def main():
    # 获取当前目录下所有的截图文件
    image_patterns = ['屏幕截图*.png', '屏幕截图*.jpg', '屏幕截图*.jpeg']
    image_files = []
    
    for pattern in image_patterns:
        image_files.extend(glob.glob(pattern))
    
    if not image_files:
        print("没有找到符合条件的截图文件")
        return
    
    print(f"找到 {len(image_files)} 个截图文件")
    
    # 创建 screenshots 目录（如果不存在）
    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')
    
    # 处理每个图片
    for image_file in image_files:
        resized_path = resize_image(image_file)
        if resized_path:
            # 移动处理后的图片到 screenshots 目录
            final_path = os.path.join('screenshots', os.path.basename(resized_path))
            os.rename(resized_path, final_path)
            print(f"已移动到: {final_path}")

if __name__ == "__main__":
    main()
    print("\n处理完成！所有调整大小的图片都保存在 screenshots 目录中") 