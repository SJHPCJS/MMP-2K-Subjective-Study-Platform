import os
import json
import random
import re

def create_user_directory(user_id):
    base_path = os.getcwd()
    user_path = os.path.join(base_path, user_id)

    if not os.path.exists(user_path):
        os.makedirs(user_path)
    return user_path

def check_and_add_user_id(user_id, id_file='id.txt'):
    if os.path.exists(id_file):
        with open(id_file, 'r', encoding='utf-8') as file:
            ids = file.read().splitlines()
    else:
        ids = []

    if user_id not in ids:
        with open(id_file, 'a', encoding='utf-8') as file:
            file.write(user_id + '\n')
        return False
    return True

def distribute_images(image_base_path):
    images = [img for img in os.listdir(image_base_path) if img.endswith(('.png', '.jpg', '.jpeg'))]
    images.sort(key=natural_sort_key)  # 保证顺序一致

    golden_questions = images[-50:]  # 最后50张作为 golden question
    normal_images = images[:-50]  # 剩余图片

    # 将 normal images 随机分配到4个 batch 中
    random.shuffle(normal_images)
    image_batches = {str(batch): [] for batch in range(1, 5)}
    for i, image in enumerate(normal_images):
        batch_name = str((i % 4) + 1)
        image_batches[batch_name].append(image)

    # 每个 batch 插入 golden questions，保持间隔一致
    golden_per_batch = [12, 12, 13, 13]  # 50张分配到4个批次，两个12张两个13张
    golden_index = 0
    for batch_name, count in zip(image_batches, golden_per_batch):
        batch = image_batches[batch_name]
        golden_interval = len(batch) // count  # 间隔位置
        for i in range(count):  # 每个 batch 插入对应数量的 golden question
            insert_position = i * golden_interval + i  # 插入位置
            batch.insert(insert_position, golden_questions[golden_index])
            golden_index += 1

    return image_batches

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)', s)]

def create_json(user_id, image_batches, user_path, image_base_path):
    image_data = []
    for batch_name, images in image_batches.items():
        for image in images:
            image_id, ext = os.path.splitext(image)
            image_info = {
                "image_id": image_id,
                "url": os.path.join(image_base_path, image),
                "batch": batch_name,
                "rate": "NULL",
                "tagList": [],
                "description": "NULL"
            }
            image_data.append(image_info)

    random.shuffle(image_data)

    json_path = os.path.join(user_path, f'{user_id}_result.json')
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(image_data, json_file, ensure_ascii=False, indent=4)

def main():
    user_id = input("Please enter new user ID: ")

    if check_and_add_user_id(user_id):
        print(f"User ID {user_id} already exists.")
    else:
        user_path = create_user_directory(user_id)
        image_base_path = os.path.join(os.getcwd(), 'image_base')
        image_batches = distribute_images(image_base_path)
        create_json(user_id, image_batches, user_path, image_base_path)
        print(f"User {user_id} has been created and images have been assigned.")

if __name__ == "__main__":
    main()
