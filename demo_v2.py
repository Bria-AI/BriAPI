import io
import time
import requests
from typing import Dict, List, Optional


api_url: str = <enter api url here>
auth_headers: Dict[str, str] = {
    "api_token": <enter your api_token here>,
    "api_secret": <enter your api_secret here>,
}
source_image_url: str = <add any image url you would like to work on>

    
def upload() -> str:
    res = requests.get(source_image_url, timeout=4.0)
    if res.status_code != requests.codes.ok:
        raise Exception()
    input_image = io.BytesIO(res.content)
    response = requests.request(
        method="POST",
        url=f"{api_url}/upload",
        headers=auth_headers,
        data={},
        files=[
            (
                "file",
                (
                    "8928f232dc8bdb35.jpeg",
                    input_image,
                    "image/jpeg",
                ),
            )
        ],
    )
    res: Dict = response.json()
    code: int = res.get("code")
    visual_id: Optional[str] = None  # used this for all other reuqest
    if code == 200:  # image uploaded for the first time
        visual_id = res.get("visual_id")
    elif code == 603:  # in case the image alrady uploaded
        visual_id = res.get("response_body").get("visual_id")
    if visual_id is None:
        exit(0)
    return visual_id


def info(visual_id: str) -> Dict:
    response = requests.request(
        method="GET",
        url=f"{api_url}/{visual_id}/info",
        headers=auth_headers,
    )
    return response.json()


def create(info: Dict, visual_id: str) -> Dict:
    scene_object: Dict = info["scene"][0]
    scene_object_id: str = scene_object.get("id")
    actions: Dict = scene_object.get("actions")

    # The api support the folowiing.
    # Note that any of these can be returned null, if that is the case we dont support a action for this image
    age_action: Optional[Dict] = actions.get("age")
    diversity_actions: Optional[List[str]] = actions.get("diversity")
    glasses_actions: Optional[List[str]] = actions.get("glasses")
    expressions_actions: Optional[List[str]] = actions.get("expressions")
    hair_color_actions: Optional[List[str]] = actions.get("hair_color")
    gender_actions: Optional[List[str]] = actions.get("gender")
    makeup_actions: Optional[List[str]] = actions.get("makeup")
    hair_line_actions: Optional[List[str]] = actions.get("hair_line")

    response = requests.request(
        method="POST",
        url=f"{api_url}/{visual_id}/create",
        headers=auth_headers,
        json={
            "changes": [
                {
                    "id": scene_object_id,
                    "actions": {"diversity": diversity_actions[0]},
                }
            ],
        },
    )

    return response.json()


past = time.time()
visual_id: str = upload()
image_info: Dict = info(visual_id=visual_id)
new_created_image: Dict = create(info=image_info, visual_id=visual_id)
time_diff: int = time.time() - past

image_url: str = new_created_image.get("image_res")
confidence: str = new_created_image.get("confidence")

print(
    f"New image created with after {time_diff}-sec with confidence: {confidence}, get it from {image_url}"
)
