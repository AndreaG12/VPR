#Mio
#URLS = {
 #   "tokyo_xs": "https://drive.google.com/file/d/15QB3VNKj93027UAQWv7pzFQO1JDCdZj2/view?usp=share_link",
  #  "sf_xs": "https://drive.google.com/file/d/10ZVF3BzNNmNfDX5oPce_7SUZNwijqpvQ/view?usp=sharing",
   # "gsv_xs": "https://drive.google.com/file/d/1ozI-r1V5sTvFaA-7UBIyfk0WvKfH0NRL/view?usp=sharing"
#}
Nico
URLS = {
    "tokyo_xs": "https://drive.google.com/file/d/1AWCDdwwU4wHG7h1dbD8_j45uWGw4XuVd/view?usp=sharing",
    "sf_xs": "https://drive.google.com/file/d/1ZHji6-20BvwhlGA_XilIg2VOYFOvyUez/view?usp=sharing",
    "gsv_xs": "https://drive.google.com/file/d/1Z-_7suk2_273hHE8COG9MLzRhDW8qCK7/view?usp=sharing"
}
#Berton
#URLS = {
 #   "tokyo_xs": "https://drive.google.com/file/d/15QB3VNKj93027UAQWv7pzFQO1JDCdZj2/view?usp=share_link",
  #  "sf_xs": "https://drive.google.com/file/d/1tQqEyt3go3vMh4fj_LZrRcahoTbzzH-y/view?usp=share_link",
   # "gsv_xs": "https://drive.google.com/file/d/1q7usSe9_5xV5zTfN-1In4DlmF5ReyU_A/view?usp=share_link"
#}
import os
import gdown
import shutil

os.makedirs("data", exist_ok=True)
for dataset_name, url in URLS.items():
    print(f"Downloading {dataset_name}")
    zip_filepath = f"data/{dataset_name}.zip"
    gdown.download(url, zip_filepath, fuzzy=True)
    shutil.unpack_archive(zip_filepath, extract_dir="data")
    os.remove(zip_filepath)

