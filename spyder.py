# import requests
# from bs4 import BeautifulSoup
#
#
# def get_page_title(url):
#     # 发送HTTP GET请求获取网页内容
#     response = requests.get(url)
#
#     # 检查请求是否成功
#     if response.status_code == 200:
#         # 使用BeautifulSoup解析网页内容
#         soup = BeautifulSoup(response.text, 'html.parser')
#
#         # 获取网页的标题
#         title = soup.title.string
#
#         return title
#     else:
#         return "请求失败，状态码：" + str(response.status_code)
#
#
# # 使用函数
# url = "https://baike.baidu.com/item/娜塔莎·罗曼诺夫/472746?fr=ge_ala"  # 替换为你想抓取的网页的URL
# title = get_page_title(url)
# print("网页标题：", title)
import tkinter as tk
from tkinter import filedialog
import requests
import re
import os
from threading import Thread


def find_media_urls(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
            media_urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+/\S+\.(?:jpg|png|mp4)', html_content)
            return media_urls
        else:
            print(f"无法访问网页，状态码：{response.status_code}")
            return []
    except Exception as e:
        print(f"发生错误：{e}")
        return []


def download_file(url, save_folder):
    try:
        file_name = url.split('/')[-1]
        file_path = os.path.join(save_folder, file_name)
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
            print(f"下载完成：{file_path}")
        else:
            print(f"下载失败，状态码：{response.status_code}，URL：{url}")
    except Exception as e:
        print(f"下载时发生错误：{e}")


def download_media():
    url = url_entry.get()
    save_folder = folder_path.get()
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    media_urls = find_media_urls(url)
    for media_url in media_urls:
        Thread(target=download_file, args=(media_url, save_folder)).start()


def select_folder():
    directory = filedialog.askdirectory()
    folder_path.set(directory)


app = tk.Tk()
app.title("Media Downloader")

tk.Label(app, text="URL:").pack(padx=10, pady=5)
url_entry = tk.Entry(app, width=50)
url_entry.pack(padx=10, pady=5)

tk.Label(app, text="Download Folder:").pack(padx=10, pady=5)
folder_path = tk.StringVar()
folder_entry = tk.Entry(app, textvariable=folder_path, width=50)
folder_entry.pack(padx=10, pady=5)
folder_button = tk.Button(app, text="Select Folder", command=select_folder)
folder_button.pack(padx=10, pady=5)

download_button = tk.Button(app, text="Download", command=download_media)
download_button.pack(padx=10, pady=10)

app.mainloop()
