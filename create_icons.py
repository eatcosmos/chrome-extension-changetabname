from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size):
    """创建指定尺寸的图标"""
    # 创建一个正方形图像，使用 RGBA 模式支持透明度
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 设置颜色
    primary_color = (25, 118, 210)     # 深蓝色
    secondary_color = (66, 165, 245)   # 浅蓝色
    
    # 计算圆的大小和位置
    padding = size // 8
    circle_size = size - (2 * padding)
    
    # 绘制主圆形
    draw.ellipse(
        [padding, padding, padding + circle_size, padding + circle_size],
        fill=primary_color
    )
    
    # 绘制字母 "T"
    font_size = size // 2
    try:
        # 尝试使用 Arial 字体，如果不可用则使用默认字体
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # 获取文字大小以居中显示
    text = "T"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    # 绘制文字
    draw.text((x, y), text, fill="white", font=font)
    
    return img

def main():
    # 创建 icons 目录
    if not os.path.exists('icons'):
        os.makedirs('icons')
    
    # 生成不同尺寸的图标
    sizes = {
        16: 'icon16.png',
        48: 'icon48.png',
        128: 'icon128.png'
    }
    
    for size, filename in sizes.items():
        icon = create_icon(size)
        icon.save(os.path.join('icons', filename))
        print(f"已创建图标: {filename}")

if __name__ == "__main__":
    main() 