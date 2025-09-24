import requests
import time
import os
import base64
import numpy as np
import cv2
idx = 1

def b64_to_bgr(b64_str: str) -> np.ndarray:
    """Decode base64 JPEG/PNG string to BGR image (OpenCV)."""
    try:
        buf = base64.b64decode(b64_str)
        print(buf)
        print(type(buf), len(buf))
        arr = np.frombuffer(buf, dtype=np.uint8)
        print(arr)
        print(f"arr type: {arr.dtype}, shape: {arr.shape}")
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)  # BGR
        return img
    except Exception:
        return None
    
def main():
    while True:
        try:
            response = requests.get('http://localhost:8000/v2/front')
            img_data = response.json()
        except Exception as e:
            print(f"Error fetching screenshot: {e}")
            break
        timestamp_img = img_data['timestamp']
        front_base64 = img_data['front_frame']
        img = b64_to_bgr(front_base64)
        if not os.path.exists(f'./data_{idx}'):
            os.makedirs(f'./data_{idx}')
        if img is not None:
            # print(img.shape)
            cv2.imwrite(f'./data_{idx}/front_frame_{timestamp_img}.jpeg', img)
        time.sleep(0.03333333333333333)  # ~30 FPS
    print("Exited loop.")

if __name__ == "__main__":
    main()