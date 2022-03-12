from os import listdir, path, mkdir
from PIL import Image

root_path = 'source'
thumbnail_path = 'thumbnails'
original_path = 'originals'

Point = tuple[int, int]
full_hd = 1080, 1080
thumbnail = 300, 300

def read_image(path : str) -> Image:
    return Image.open(path).convert('RGBA')

def watermark(image: Image) -> Image:
    watermark = Image.open('./watermark.png').convert('RGBA')
    w_wm, h_wt = watermark.size
    width, height = image.size
    transparent = Image.new('RGBA', (width, height), (0,0,0,0))
    transparent.paste(image, (0,0))
    transparent.paste(watermark, (width - w_wm, height - h_wt), mask=watermark)
    return transparent.convert('RGB')

def scale_large(image: Image) -> Image:
    return scale(image, full_hd)

def scale_thumbnail(image: Image) -> Image:
    return scale(image, thumbnail)

def scale(image: Image, size: Point) -> Image:
    image2 = image.copy()
    image2.thumbnail(size, Image.ANTIALIAS)
    return image2

def get_all_images_recursive(directory_path: str = '') -> list:
    
    for dir_or_file_name in listdir(path.join(root_path, directory_path)):
        if path.isfile(path.join(root_path, directory_path, dir_or_file_name)):
            
            if dir_or_file_name[0] == '.':
                continue
            
            image_original = read_image(path.join(root_path, directory_path, dir_or_file_name))
            image_large = scale_large(image_original)
            image_large = watermark(image_large)
            image_thumbnail = scale_thumbnail(image_large)
            
            if not path.isdir(path.join(original_path, directory_path)):
                mkdir(path.join(original_path, directory_path))
            image_large.save(path.join(original_path, directory_path, dir_or_file_name))
            if not path.isdir(path.join(thumbnail_path, directory_path)):
                mkdir(path.join(thumbnail_path, directory_path))
            image_thumbnail.save(path.join(thumbnail_path, directory_path, dir_or_file_name))
            
        else:
            get_all_images_recursive(path.join(directory_path, dir_or_file_name))
            

get_all_images_recursive()