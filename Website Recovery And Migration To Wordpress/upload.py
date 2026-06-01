import requests, random, string, os, re
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv(".env")

wp_username = os.getenv("WP_USER")
wp_password = os.getenv("WP_PASS")

# Creating Users:
def create_users():
    user_url = "your url"
    symbol_select = string.ascii_letters + string.digits + string.punctuation

    for name in os.listdir("./Contributors"):
        password = "".join(random.choice(symbol_select) for _ in range(10))

        data = {
            "username":  name,
            "password":  password,
            "email":     f"{name.lower().split()[0]}@gmail.in",
            "roles":     "author"
        }

        response = requests.post(user_url, auth = (wp_username, wp_password), json = data)

        if response.ok:
            with open(os.path.join("Credentials", f"{name}.txt"), "w", encoding = "utf-8") as file:
                file.write(f"Username: {data["username"]}\nPassword: {data["password"]}")
                print(f"User for {name} created!")

        else:
            print(response.text)

# Creating Categories:
def create_categories(categories):
    category_url = "https://sitename/wp-json/wp/v2/categories"

    for category in categories:
        data = { "name": category }
        response = requests.post(category_url, auth = (wp_username, wp_password), json = data)
        print(f"Category {category} added!") if response.ok else print(response.text)

# Creating Pages:
def create_page(name, dir_path):
    html_file = None
    image_file = None

    for file in os.listdir(dir_path):
        if os.path.splitext(file)[1] == ".html":
            html_file = file

        elif os.path.splitext(file)[1] == ".png":
            image_file = file

    if html_file:
        with open(os.path.join(dir_path, html_file), "r", encoding = "utf-8") as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, "html.parser")
        entry_div = soup.find("div", class_ = "entry-content")

        bio_parts = []

        for child in entry_div.children:
            if getattr(child, "name", None) == "hr":
                break

            if getattr(child, "name", None) == "div" and "thumbnail-holder" in child.get("class", []):
                continue

            bio_parts.append(child.get_text(" ", strip = True) if hasattr(child, "get_text") else str(child).strip())

        bio_text = " ".join(bio_parts).strip()

        data = { 
            "title":     name, 
            "content":   bio_text, 
            "status":    "publish" 
        }
    
        if image_file:
            media_url = "https://sitename/wp-json/wp/v2/media"
            media_file = { "file": open(os.path.join(dir_path, image_file), "rb") }

            response = requests.post(media_url, auth = (wp_username, wp_password), files = media_file)
            data["featured_media"] = response.json()["id"]
            print("Image uploaded!")

        page_url = "https://sitename/wp-json/wp/v2/pages"
        response = requests.post(page_url, auth = (wp_username, wp_password), json = data)

        if response.ok:
            print(f"Page for {name} created!")
            page_link = response.json()["link"]

            with open("Contributor Page.txt", "a", encoding = "utf-8") as file:
                file.write(f'\n<h4><a href="{page_link}">{name}</a></h4>')

# Parsing File Conetents:
def get_post_files(dir_path):
    print(f"Now at: {dir_path}")
    media_list = []

    for file in os.listdir(dir_path):
        if os.path.splitext(file)[1] == ".html":
            html_file = file

        else:
            media_list.append(file)

    with open(os.path.join(dir_path, html_file), "r", encoding = "utf-8") as file:
        html_content = file.read()
    
    info = {
        "path":    dir_path,
        "title":   re.search(r"\S.+", html_content).group(),
        "author":  re.search(r"By\s(.+)\s\[", html_content).group(1),
        "month":   re.search(r"\[(.+[a-zA-Z])", html_content).group(1),
        "year":    re.search(r"\[(?:[A-Za-z]+\s+)?(\d{4})\]", html_content).group(1),
        "body":    re.search(r'<div class="entry-content">.+', html_content, re.DOTALL).group()
    }

    post_to_wordpress(info, media_list)

# Posting To Wordpress:
def post_to_wordpress(info, media_list):
    soup = BeautifulSoup(info["body"], "html.parser")

    if media_list:
        media_url = "https://sitename/wp-json/wp/v2/media"
        media_dictionary = {}
       
        for media in media_list:
            media_file = { "file": open(os.path.join(info["path"], media), "rb") }
            response = requests.post(media_url, auth = (wp_username, wp_password), files = media_file)

            if response.ok:
                if "image" in media:
                    match = re.search(r"\d+", media)

                    if match:
                        media_dictionary[int(match.group())] = response.json()["source_url"]
              
                else: 
                    media_dictionary[media] = response.json()["source_url"]

                print(f"{media} added!")
                
            else: 
                print(response.text)

        if media_dictionary:
            image_tags = soup.find_all("img")
            original_urls = {number: image_tag for number, image_tag in enumerate(image_tags, start = 1)}

            for key in original_urls.keys():
                photo_name = re.search(r'([^/]+)$', str(original_urls[key]["src"])).group(1)

                if key in media_dictionary:
                    original_urls[key]["src"] = media_dictionary[key]

                elif photo_name in media_dictionary:
                    original_urls[key]["src"] = media_dictionary[photo_name]
                
    post_url = "https://sitename/wp-json/wp/v2/posts"

    month = f"{datetime.strptime(info["month"], '%B').month:02d}"
    day = f"{random.randint(1, 28):02d}"

    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    post_date = datetime(int(info["year"]), int(month), int(day), hour, minute, second).isoformat()

    post = { 
        "title":    info["title"], 
        "content":  str(soup) if media_list else info["body"], 
        "date":     post_date,
        "author":   25,
        "status":   "publish" 
    }

    df = pd.read_excel("essayist.xlsx")
    categories = list(df.columns[df.isin([info["title"]]).any()])
    
    if categories:
        get_categories = "https://sitename/wp-json/wp/v2/categories"
        category_json = requests.get(get_categories, auth = (wp_username, wp_password)).json()

        category_ids = [c["id"] for c in category_json if c["name"] in categories]
        post["categories"] = category_ids

    response = requests.post(post_url, auth = (wp_username, wp_password), json = post)
    print("Post uploaded!\n") if response.ok else print(response.text + "\n")