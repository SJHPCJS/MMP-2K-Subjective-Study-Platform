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
    random.shuffle(images)

    image_batches = {str(batch): [] for batch in range(1, 5)}
    for i, image in enumerate(images):
        batch_name = str((i % 4) + 1)
        image_batches[batch_name].append(image)

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

    # 随机打乱image_data
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
