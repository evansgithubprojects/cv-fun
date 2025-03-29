import cv2
import time
import numpy as np

frame = np.random.randint(0, 256, (720, 1280, 3), dtype=np.uint8)  # 1280x720 random image

num_frames = 100
start_time = time.time()

for _ in range(num_frames):
    cv2.imshow("Test Window", frame)
    cv2.waitKey(1)  # Adjust this value to see FPS changes

end_time = time.time()
fps = num_frames / (end_time - start_time)

print(f"Approximate FPS: {fps:.2f}")
cv2.destroyAllWindows()