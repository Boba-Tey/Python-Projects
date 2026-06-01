from bs4 import BeautifulSoup
import requests, os, time

def get_links():
    url = "your url"
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    post_links = soup.find_all("a", { "rel": "bookmark" })

    page_builder([link["href"] for link in post_links])

def page_builder(links):
    count = 1

    for link in links:
        try:
            response = requests.get(link, timeout = 10)
            soup = BeautifulSoup(response.text, "html.parser")

            page_title = soup.find("h3", class_ = "entry-title")
            page_meta = soup.find("div", class_ = "entry-meta")
            page_content = soup.find("div", class_ = "entry-content")
            image_links = soup.find_all("img", class_ = "aligncenter")

            if os.path.exists(f"post{count}"):
                print(f"Skipped post{count}")
                count += 1
                continue

            os.mkdir(f"post{count}")

            if image_links:
                image_count = 1

                for image in image_links:
                    response = requests.get(image["src"], timeout = 10)

                    if response.status_code == 200:
                        with open(os.path.join(f"post{count}", f"image{image_count}.png"), "wb") as file:
                            file.write(response.content)

                        print(f"Image downloaded successfully as image{image_count}.png")

                    else:
                        print(f"Failed to download image. Status code: {response.status_code}")
                    
                    image_count += 1

            with open(os.path.join(f"post{count}", f"post{count}.html"), "w", encoding = "utf-8") as file:
                file.write(f"{page_title.text.strip()}\n\n{str(page_meta.text.strip())}\n\n{str(page_content)}")

            print(f"Saved page content as post{count}.html\n")
            count += 1
            time.sleep(2)

        except Exception as e:
            print(e)
            count += 1
            time.sleep(2)