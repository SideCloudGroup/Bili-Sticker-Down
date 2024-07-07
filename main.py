import os
import subprocess

import requests
import toml
from PIL import Image

config = toml.load("config.toml")


def calculate_new_size(original_width, original_height, config):
    if original_width == original_height:
        return config['app']['final_resolution'], config['app']['final_resolution']
    elif original_width > original_height:
        scale_factor = config['app']['final_resolution'] / original_width
        return config['app']['final_resolution'], int(original_height * scale_factor)
    else:
        scale_factor = config['app']['final_resolution'] / original_height
        return int(original_width * scale_factor), config['app']['final_resolution']


def get_stickers(session, config):
    # 从API获取表情列表，转成JSON
    api_url = f"https://api.bilibili.com/x/garb/v2/mall/suit/detail?item_id={config['app']['suit_id']}&part=suit"
    res = session.get(api_url, headers={'User-Agent': config['app']['user_agent']}).json()
    if res['data']['suit_items'] is None:
        raise ValueError("装扮不存在")
    stickers = {'name': res['data']['name']}
    for item in res['data']['suit_items']['emoji_package'][0]['items']:
        stickers[item['name'].split('_')[-1][:-1]] = item['properties']['image']
    return stickers


def process_image(img_path, config, sticker_name, name):
    if config['app']['super_resolution']:
        print(f"超分辨率优化 {sticker_name}_{name}.png")
        command = [
            config['realesrgan']['executable_file_path'],
            '-i', img_path,
            '-o', img_path,
            '-n', config['realesrgan']['model'],
            '-s', str(config['realesrgan']['scale']),
        ]
        subprocess.run(command, check=True)
    if config['app']['final_resolution'] > 0:
        print(f"调整分辨率 {sticker_name}_{name}.png")
        with Image.open(img_path) as img:
            original_width, original_height = img.size
            new_size = calculate_new_size(original_width, original_height, config)
            resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
            resized_img.save(img_path)
            print(f"{name}.png 优化完成")


def main():
    session = requests.Session()
    stickers = get_stickers(session, config)
    os.makedirs(stickers['name'], exist_ok=True)
    for name, url in stickers.items():
        if name == "name":
            continue
        img_path = os.path.join(stickers['name'], f"{name}.png")
        print(f"下载 {stickers['name']}_{name}.png")
        with open(img_path, "wb") as f:
            f.write(session.get(url).content)
        process_image(img_path, config, stickers['name'], name)

    print("表情包处理完成")


if __name__ == "__main__":
    main()
