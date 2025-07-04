import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

load_dotenv(".env")

user = os.getenv("WP_USERNAME", "").strip()
app_pass = os.getenv("WP_APP_PASS", "").strip()
cred = HTTPBasicAuth(user, app_pass)

def upload_media(img):
    url = "https://firsteducationnews.com/wp-json/wp/v2/media"
    headers = {"Content-Disposition": f'attachment; filename="{img}"'}
    img_file = {"file": open(img, "rb")}

    response = requests.post(url, headers=headers, auth=cred, files=img_file)
    if response.status_code == 201:
        img_id = response.json()["id"]
        print("Image uploaded successfully:", response.status_code)
        return img_id
    else:
        print("Failed to upload image:", response.status_code, response.text)
        return None

def post_automation():
    content_list = []
    wp_body = {
        "Title": ["Test", "Hello World", "Food"],
        "Desc": ["texting 123", "Hru globe?", "Is delicious"],
        "Image": ["1.jpg", "2.jpg", "3.jpg"]
    }
    for title, desc, image in zip(wp_body["Title"], wp_body["Desc"], wp_body["Image"]):
        image_id = upload_media(image)
        contents = {
            "title": title,
            "content": desc,
            "status": "publish"
        }
        if image_id:
            contents["featured_media"] = image_id  

        content_list.append(contents)
    return content_list

def create_post():
    url = "https://firsteducationnews.com/wp-json/wp/v2/posts"
    headers = {"Content-Type": "application/json"}
    post_data = post_automation()
    
    for post in post_data:
        response = requests.post(url, headers=headers, auth=cred, json=post)
        if response.status_code == 201:
            print("Post created successfully:", response.status_code)
        else:
            print("Failed to create post:", response.status_code, response.text)

if __name__ == "__main__":
    create_post()