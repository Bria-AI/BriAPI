import io
from typing import Dict, List, Optional
import time
import requests

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
                    "foo.jpeg",
                    input_image,
                    "image/jpeg",
                ),
            )
        ],
    )
    res: Dict = response.json()
    code: int = res.get("code")
    v_hash: Optional[str] = None  # used this for all other reuqest
    if code == 200:  # image uploaded for the first time
        v_hash = res.get("vhash")
    elif code == 603:  # in case the image alrady uploaded
        v_hash = res.get("response_body").get("vhash")
    if v_hash is None:
        exit(0)
    return v_hash


def info(v_hash: str) -> Dict:
    response = requests.request(
        method="GET",
        url=f"{api_url}/info?vhash={v_hash}",
        headers=auth_headers,
    )
    return response.json()


def create(info: Dict, v_hash: str) -> Dict:
    scene_object: Dict = info["scene"][0]
    scene_object_id: str = scene_object.get("id")
    actions: Dict = scene_object.get("actions")

    # The api support the folowiing.
    # Note that any of these can be returned null, if that is the case we dont support a action for this image
    age_action: Optional[Dict] = actions.get("age")
    diversify_actions: Optional[List[str]] = actions.get("diversify")
    glasses_actions: Optional[List[str]] = actions.get("glasses")
    smile_actions: Optional[List[str]] = actions.get("smile")

    response = requests.request(
        method="POST",
        url=f"{api_url}/create?vhash={v_hash}",
        headers=auth_headers,
        json={
            "vhash": v_hash,
            "changes": [
                {
                    "id": scene_object_id,
                    "actions": {"diversify": diversify_actions[3]},
                }
            ],
        },
    )

    return response.json()


past = time.time()
v_hash: str = upload()
image_info: Dict = info(v_hash=v_hash)
new_created_image: Dict = create(info=image_info, v_hash=v_hash)
time_diff: int = time.time() - past

image_url: str = new_created_image.get("image_res")
confidence: str = new_created_image.get("confidence")

print(
    f"New image created with after {time_diff}-sec with confidence: {confidence}, get it from {image_url}"
)
