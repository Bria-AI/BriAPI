
# Script 
# Intro to bria

# Act 1:
# TODO: ask yoav 4 prompts of politition trademarks and 2 for quality 
# Generate images via text prompts, talk about about safety (the fact we are unable to generate trademarks) 
# and diversity.
# Act 2:
# TODO: sketch to image, add brad colors,  
# Start working on the real campaign, using CN to emphasize the controllability Bria offers.
# Generate multiple options based on the provided text.
# Act 3:
# TODO: a bowel 
# Use lifestyle_shot_by_text to focus on ideation or specific requirements by experimenting with placements and backgrounds.
# Act 4:
# Image editing: enhance your image shoot by applying fine-grain touches.
# Use tools like Eraser, Expand, and Increase Resolution.
# Act 5:
# Tailored generation, use icons 

headers = {
  "Content-Type": "application/json",
  "api_token": "<Your API token here...>"
}

#%% init
import requests
import base64
from PIL import Image, ImageOps
from IPython.display import Image as IPyImage, display
from io import BytesIO
import numpy as np
from diffusers.utils import make_image_grid
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import os
import io
import json
from PIL import ImageDraw, ImageFont


def add_text_on_image(_image, text):
    draw = ImageDraw.Draw(_image)
    font = ImageFont.load_default(size=40)  # Use the default font or specify a custom font
    
    # Get the text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)  # (left, top, right, bottom)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    # Calculate position for centered text
    position = ((_image.width - text_width) // 2, _image.height - text_height - 20)
    
    # Draw the text on the image
    draw.text(position, text, fill="white", font=font)
    return _image

def download_img(result_url: str):

    img_response = requests.get(result_url)
    if img_response.ok:
        return Image.open(BytesIO(img_response.content))

# Function to concatenate an array of PIL images horizontally
def concatenate_images_horizontally(images):
    # Ensure all images have the same height by resizing them
    min_height = min(image.height for image in images)
    resized_images = [image.resize((int(image.width * min_height / image.height), min_height)) for image in images]
    
    # Convert each resized image to a numpy array
    arrays = [np.array(img) for img in resized_images]
    
    # Concatenate arrays horizontally
    concatenated_array = np.concatenate(arrays, axis=1)
    
    # Convert back to a PIL Image and return
    return Image.fromarray(concatenated_array)

# Helper function to load and display images
def load_and_display_image(path):
    image = Image.open(path).convert("RGB")
    image = ImageOps.exif_transpose(image)

    # display(IPyImage(path))
    return image

# Function to convert a PIL Image to a base64-encoded string
def pil_image_to_base64(pill_image):
    buffered = BytesIO()
    pill_image.save(buffered, format="JPEG")  # You can change the format if needed
    encoded_string = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return encoded_string

def display_local_image(image_name: str):
    # Get the current working directory
    current_dir = os.getcwd()

    # Specify the path to the image relative to the current directory
    image_path = os.path.join(current_dir, image_name)

    # Display the image
    im = IPyImage(image_path)
    display(im)

width = 128
text_to_image_bria_website_url = "https://bria.ai/hs-fs/hubfs/ai%20image%20gen%20header.png?width=3363&height=2262&name=ai%20image%20gen%20header.png"
eracer_bria_website_url = "https://bria.ai/hs-fs/hubfs/ERASER_API_blog20-30.gif?width=3630&height=2220&name=ERASER_API_blog20-30.gif"

#%% Into to bria
display(IPyImage("./assets/bria-hl.png")) 
display(IPyImage("./assets/bria.png")) 
#%% ######### /text_to_image 
print("Text-to-Image")
print("""
Quickly convert textual descriptions into high-quality images with our Text-to-Image API. 
This feature allows you to embed dynamic image generation into your applications, 
enabling users to create visuals based on simple text inputs. 
Ideal for enhancing user experiences in creative platforms, e-commerce, gaming, and more,
the Text-to-Image API brings versatile, on-demand image creation to your products.
""")

display(IPyImage(url=text_to_image_bria_website_url))

#%% Generate images
# Generate images for diffrerant usecases
model_version = "2.3"
base_url = f"https://engine.prod.bria-api.com/v1/text-to-image/base/{model_version}"

# Generation prompts
prompts = [
    "White nike sport shoe, show product shoot", 
    "Green lantern ring", 
    "R2-D2", 
    "Gucci bag"
]
seeds = [0,1,2,3]

prompts = zip(prompts, seeds)

# Function to handle API requests and fetch images
def fetch_image(prompt):

    _prompt, _seed = prompt

    # Set up the request payload for the API call
    _payload = {
        "prompt": _prompt, 
        "seed": _seed, 
        "num_results": 1,
        "sync": True, 
    }
    
    # Send a POST request to generate an image based on the prompt
    response = requests.post(base_url, json=_payload, headers=headers)
    _image_url = response.json().get("result", [{}])[0].get("urls", [None])[0]        
    img_response = requests.get(_image_url)

    return (Image.open(BytesIO(img_response.content)), _prompt, _seed)

# Use ThreadPoolExecutor to fetch images concurrently
gen_images = []
with ThreadPoolExecutor(max_workers=len(seeds)) as executor:
    # Submit fetch_image tasks for each prompt
    future_to_prompt = {executor.submit(fetch_image, prompt): prompt for prompt in prompts}
    
    # Collect results as they complete
    for future in as_completed(future_to_prompt):
        res_image = future.result()
        if res_image:
            gen_images.append(res_image)

# Display images in a grid
num_columns = 2
only_images = [_image[0] for _image in gen_images]
grid = make_image_grid(only_images, rows=len(gen_images) // num_columns, cols=num_columns)
display(grid)

#%% Generate by controle
display(IPyImage("./assets/controle_info.png"))

model_version = "2.3"
base_url = f"https://engine.prod.bria-api.com/v1/text-to-image/fast/{model_version}"

controle = [
    # (download_img("https://static.vecteezy.com/system/resources/thumbnails/002/897/817/small/cartoon-car-trees-clouds-and-sun-flat-design-environment-free-vector.jpg"), "controlnet_color_grid", "Car driving on the roade serounded by trees"),
    (download_img("https://cdna.artstation.com/p/assets/images/images/048/280/462/large/ra-i-img-20210512-001226-111-copy-3369x2399.jpg?1649670948"), "controlnet_recoloring", "Butifull vibrent mountain landscape in summer"),
    (download_img("https://images.immediate.co.uk/production/volatile/sites/2/2017/02/nutella-pancakes-1.jpg?quality=90&webp=true&crop=646px,3217px,3608px,2403px&resize=2200,1465"), "controlnet_depth", "Food photography of a vanilla cake with strawberry frosting, in the background a blurry interior of a restaurant, warm red and orange hues, sunrays"),
]

num_columns = 2
cn_grid = make_image_grid([img[0].copy().resize((512,512)) for img in controle], rows=1, cols=len(controle))
display(cn_grid)

images = []
for t in tqdm(controle):
    cn_img, guidance_method, prompt = t
    print(f"Generating by - {guidance_method}, with prompt: {prompt}")
    _payload = {
        "prompt": prompt, 
        "seed": 100, 
        "num_results": 1,
        "sync": True, 
        "guidance_method_1": guidance_method, 
        "guidance_method_1_image_file": pil_image_to_base64(cn_img)
    }

    response = requests.post(base_url, json=_payload, headers=headers)
    _image_url = response.json().get("result", [{}])[0].get("urls", [None])[0]
    img_response = requests.get(_image_url)
    res = Image.open(BytesIO(img_response.content))
    images.append(res)

gen_by_cn_grid = make_image_grid(images, rows=1, cols=len(images))
display(gen_by_cn_grid)

# # Finding the tuple with "sport shoe" in the prompt

#%% ######### /lifestyle_shot_by_text
# Create dynamic content from the selected image

url = "https://engine.prod.bria-api.com/v1/product/lifestyle_shot_by_text"

my_object = download_img("https://thejapaneseshop.co.uk/cdn/shop/products/green-wabi-sabi-premium-small-japanese-bowl-5.jpg?v=1673358282")

display(my_object.resize((512, 512)))

instructions = [
    ("bottom_right", "On towels, in a spa environment, pastel colors, warm sunlight, high-contrast image, purple photo filter"),
    ("right_center", "Studio shot, a perfect setting for a product placement on a rock with moss, surrounded by tropical vegetation, ferns and flowers, with visible moisture in the air, water drops, over a blurry jungle backgound, drama, high contrast image, cooling photo filter"), 
    ("center_horizontal", "A low angle 3d rendered image of a splash of golden honey water in mid-air, floating, splash drops in mid-air over a circular white podium in an empty white studio, symmetry cooling photo filter, high contrast image"), 
    ("bottom_center", "on a circular marble pedestal, lemons, solid light blue background")
]
placement_seed = 87676456

images_placements = []
for t in instructions:
    print(t)
    placement, scene_description = t
    payload = {
        "file": pil_image_to_base64(my_object),
        "seed": placement_seed,
        "placement_type": "manual_placement",
        "manual_placement_selection": placement,
        "num_results": 1,
        "original_quality": True,
        "optimize_description": False,
        "sync": True,
        "scene_description": scene_description
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()["result"][0][0]
    images_placements.append((download_img(data), placement_seed, scene_description))

num_columns = 2
only_images = [image[0] for image in images_placements]
grid = make_image_grid(only_images, rows=len(only_images) // num_columns, cols=num_columns)
display(grid)
selected_placement_image = only_images[0]
selected_placement_image.save("./selected_placement_image.jpg")

#%% ######### /eraser 
# The Bria Eraser Tool"
print("""
Scale object removal capabilities and reduce operational costs with 
Bria’s Eraser APIs, SDKs, and iFrames. 
Effortlessly remove unwanted elements from images and fill the space with authentic,
high-fidelity AI-generated content.
""")

display(IPyImage(url=eracer_bria_website_url))

#%% erase Elements from an image
# Scale object removal capabilities
im = images_placements[0][0]

image_after_remove_by_mask = None
for mask_path in ['./assets/mask.png']:
    mask_im = load_and_display_image(mask_path)

    con = concatenate_images_horizontally(images=[im, mask_im])
    display(con)

    url = "https://engine.prod.bria-api.com/v1/eraser"
    payload = {
        "file": pil_image_to_base64(im),
        "mask_file": pil_image_to_base64(mask_im),
        "seed": 29837923784
    }
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    image_after_remove_by_mask = download_img(data["result_url"])
    con = concatenate_images_horizontally(images=[im, image_after_remove_by_mask])
    display(con)

#%% ######### /image_expansion
# Expend images to differant asspect retios 

# display(image_after_remove_by_mask)

url = "https://engine.prod.bria-api.com/v1/image_expansion"

ratios = [
    [1280, 720],  # 16:9 - Standard for social videos, cinema, and web embeds
    [1024, 768],  # 4:3 - Legacy media, older TV shows, and document viewers
    [1024, 1024], # 1:1 - Square aspect ratio, used for social media posts, profile pictures, and some mobile interfaces
    [2000, 1000]  # 2:1 - Ultrawide banners, panoramas, and immersive web design
]

def add_aspect_ratio_text(image, ratio):
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default(size=40)  # Use the default font or specify a custom font
    text = f"{ratio[0]}:{ratio[1]}"
    
    # Get the text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)  # (left, top, right, bottom)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    # Calculate position for centered text
    position = ((image.width - text_width) // 2, image.height - text_height - 20)
    
    # Draw the text on the image
    draw.text(position, text, fill="white", font=font)
    return image

def add_margin(img):
    img_with_margin = Image.new("RGB", (1024, 1024), color="black")
    img.thumbnail((1024, 1024), Image.LANCZOS)  # Maintain aspect ratio
    img_with_margin.paste(img, ((1024 - img.width) // 2, (1024 - img.height) // 2))

    # Add a fine purple frame
    frame_padding = ImageOps.expand(img_with_margin, border=10, fill="black")
    return frame_padding

# Define the function to process each image with the API
def process_image(ratio):
    image, prompt, seed = images_placements[-1][0], instructions[1][1], placement_seed
    w, h = image.size
    payload = {
        "prompt": "on a cirar marble pedestal, solid light blue background", 
        "seed": seed,
        "file": pil_image_to_base64(image),
        "canvas_size": ratio,
        "original_image_size": [512, 512],
        "original_image_location": [445, 250]
    }

    # Send POST request to the API
    response = requests.post(url, json=payload, headers=headers)
    
    if response.ok:
        # Extract result URL from response
        result_url = response.json().get("result_url")
    
        # Verify that the image URL was retrieved successfully
        if result_url:
            img_response = requests.get(result_url)
            if img_response.ok:
                img = Image.open(BytesIO(img_response.content))
                frame_padding = add_margin(img)
                # img_with_text = add_aspect_ratio_text(frame_padding, ratio)

                return (frame_padding, prompt, seed)
            else:
                print(f"Failed to download image for prompt: '{prompt}'")
    else:
        print(response)
        return None

# Use ThreadPoolExecutor to handle requests concurrently
expended_images = []
with ThreadPoolExecutor(max_workers=len(ratios)) as executor:
    # Submit tasks for each image in the images list
    futures = {executor.submit(process_image, t): t for t in ratios}
    
    # Collect results as they complete
    for future in as_completed(futures):
        image = future.result()
        if image:
            expended_images.append(image)

only_images = [image[0] for image in expended_images]
num_columns = 2
grid = make_image_grid(only_images, rows=len(only_images) // num_columns, cols=num_columns)
display(grid)
#%% ######### /increase-res

image_to_increase = only_images[0]

# Convert the PIL image to a BytesIO object
buffer = io.BytesIO()
image_to_increase.save(buffer, format="JPEG")
buffer.seek(0)  

buffered_reader = io.BufferedReader(buffer)

url = "https://engine.prod.bria-api.com/v1/image/increase_resolution?desired_increase=4"

payload = {}
files=[
  ('file',('4e3395aa-a0e8-11ef-bbcf-9a02f96319b1.png', buffered_reader, 'image/png'))
]
_headers = {
  'API_TOKEN': headers["api_token"]
}

response = requests.request("POST", url, headers=_headers, data=payload, files=files)
increased = download_img(response.json()["result_url"])
con = concatenate_images_horizontally([image_to_increase, increased])
increased.save("./4x_increase.png")
image_to_increase.save("original_res.png")
display(con)

# %% TG exsamples

import requests
import json

tg_models = [] # Add model ids you trained here e.g 100, 200, 300 etc.

gens = []
cn_img = download_img("https://img.freepik.com/premium-photo/there-is-llama-eating-noodles-out-bowl-generative-ai_955884-30578.jpg")

for models_id in tqdm(tg_models):

    _url = f"https://engine.prod.bria-api.com/v1/text-to-image/tailored/{models_id}"

    _payload = json.dumps({
        "prompt": "lama eating ramen icon",
        "num_results": 1,
        "sync": True,
        "prompt_enhancement": True,
        "fast": True,
        "seed": 100,
        "guidance_method_1": "controlnet_canny", 
        "guidance_method_1_image_file": pil_image_to_base64(cn_img),
    })

    response = requests.request("POST", _url, headers=headers, data=_payload)
    try:
        re_image = download_img(response.json()["result"][0]["urls"][0])
        gens.append(re_image)
    except:
        print(response)
        pass
if len(gens) > 0:
    grid = make_image_grid(gens, rows=len(gens) // 2, cols=2)
    cn_img = add_text_on_image(cn_img, "ORIGINAL")
    con = concatenate_images_horizontally([cn_img, grid])
    display(con)
# %% Links
models_qr = Image.open("./assets/models_qr.png")
demo_qr = Image.open("./assets/demo_qr.png")
con = concatenate_images_horizontally([models_qr, demo_qr])
display(con) 
# %%
