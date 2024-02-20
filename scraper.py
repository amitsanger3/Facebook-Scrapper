from facebook_scraper import get_posts
from db_process import *

import config
import time, json, os, requests, shutil
import random


class FbImgScrape:

    def __init__(self, op_dir):
        self.op_dir = op_dir
        self.options={"progress": True, "posts_per_page": 200}
        self.fb_url_db = FbDatabase()
        self.img_num = 0

    def make_dir(self, dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        return True

    def get_group_id(self, group_url):
        return group_url.strip().split('/')[-2]

    def url_uniqueness_check(self, url):
        return self.fb_url_db.gdelt_url_insert(url)

    def download_image(self, image_url, group_path):
        res = requests.get(image_url, stream=True)
        print(res.status_code, "==================", self.img_num)
        if res.status_code == 200:
            with open(os.path.join(group_path, f"{self.img_num}.jpg"), 'wb') as f:
                shutil.copyfileobj(res.raw, f)
        self.img_num += 1

    def parser(self):
        for url, group_title in config.GROUPS:
            group_path = os.path.join(self.op_dir, "_".join(group_title.strip().split()))
            self.make_dir(group_path)
            group_id = self.get_group_id(url)
            print(">"*100, "\n", group_title, group_id, ">"*100, "\n",)

            for post in get_posts(group=group_id, pages=config.PAGES, cookies="./cookie.json", options=self.options):
                # print("POST #######",post)
                group_path1 = os.path.join(group_path, "HIGH_QUALITY")
                self.make_dir(group_path1)
                try:
                    img_url = post["image"]
                    # print("@@@@@@@", img_url)
                    if img_url:
                        if self.url_uniqueness_check(img_url):
                            self.download_image(img_url, group_path1)
                except:
                    pass

                try:
                    img_urls = post["images"]
                    # print("@@@@@@@", img_urls)
                    for img_url in img_urls:
                        if self.url_uniqueness_check(img_url):
                            self.download_image(img_url, group_path1)
                except:
                    pass
                # low quality
                # group_path2 = os.path.join(group_path, "LOW_QUALITY")
                # self.make_dir(group_path2)
                # try:
                #     img_url = post['image_lowquality']
                #     # print("@@@@@@@", img_url)
                #     if img_url:
                #         self.download_image(img_url, group_path2)
                # except:
                #     pass
                #
                # try:
                #     img_urls = post['images_lowquality']
                #     # print("@@@@@@@", img_urls)
                #     for img_url in img_urls:
                #         self.download_image(img_url, group_path2)
                # except:
                #     pass
                # time.sleep(random.randint(3, 6))
            #     break
            # break


if __name__ == "__main__":
    op_dir = r"E:\Documents"
    FbImgScrape(op_dir).parser()