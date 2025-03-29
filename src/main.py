import cv2
import mediapipe as mp
import numpy as np
from PIL import Image, ImageDraw
import time
from enum import Enum
import json
from get_hand_angles import get_hand_angles
from get_hand_distances import get_hand_distances
from check_pose import check_pose
from hands import mp_hands, hands
from deserialize_poses import deserialize_poses
import psutil
import sys
from dynamic_screen import DynamicScreen

screen = DynamicScreen()

mp_drawing = mp.solutions.drawing_utils

cam = cv2.VideoCapture(0)

class State(Enum):
  WAITING_TO_TAKE = 1
  MATCHING_POSE = 2
  WAITING_FOR_EXIT = 3

state = State.MATCHING_POSE
ms_till_snapshot = 5000
start_ns = time.time_ns()
process = psutil.Process()

fps_cache = []

#uncomment to make window resizable
cv2.namedWindow('Hand Tracking', cv2.WINDOW_NORMAL)

def process_hands(frame):
  rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
  results = hands.process(rgb_frame)
  return results

pose_data = deserialize_poses()
if not pose_data and state == State.MATCHING_POSE:
  print('Exiting: no poses to match!')
  exit()

def serialize_hand(hand_landmarks):
  angles = get_hand_angles(hand_landmarks)
  distances = get_hand_distances(hand_landmarks)
  return { 'angles': angles, 'distances': distances }

def take_snapshot(multi_hand_landmarks):
  serialized_hands = {
    i: hand for i, hand_landmarks in enumerate(multi_hand_landmarks) 
    if (hand := serialize_hand(hand_landmarks)) is not None
  }

  if not serialized_hands:
    return None

  with open("poses/crip.json", "w") as file:
    json.dump(serialized_hands, file, indent=2)

last_loop_time = time.perf_counter()
while True:
  ret, frame = cam.read()

  screen.adjust(frame)

  if not ret:
      break
  
  frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
  frame_pil = frame_pil.transpose(Image.FLIP_LEFT_RIGHT)
  #draw = ImageDraw.Draw(frame_pil)
  frame = cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGB2BGR)
  results = process_hands(frame)
  key = cv2.waitKey(1)
  status_text = str(state)

  if state == State.WAITING_TO_TAKE:
    ms_till_snapshot = 5000 - (time.time_ns() - start_ns) / 1_000_000
    if (ms_till_snapshot > 0):
      if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
          mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    else:
      #Take snapshot
      if results.multi_hand_landmarks is None: continue
      take_snapshot(results.multi_hand_landmarks)
      state = State.WAITING_FOR_EXIT
  elif state == State.MATCHING_POSE:
    if results.multi_hand_landmarks is not None:
      for hand_landmarks in results.multi_hand_landmarks:
        angles = get_hand_angles(hand_landmarks)
        distances = get_hand_distances(hand_landmarks)
        for connection_name, distance in distances.items():
          index = mp_hands.HandLandmark[connection_name.split('-')[0] + '_TIP']
          landmark = hand_landmarks.landmark[index]
        matched_pose_name = None
        for pose_name, data in pose_data.items():
          matched = check_pose(data, angles, results)
          if matched:
            matched_pose_name = pose_name
            status_text = f'throwing up {pose_name}'
            break
        drawing_spec = mp_drawing.DrawingSpec(
          color=(0, 255, 0) if matched_pose_name else (0, 0, 255),
          thickness=2,
          circle_radius=5
        )
        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS, landmark_drawing_spec=drawing_spec)
    
    if key == ord('q'):
      break
  else:
    if key == ord('q'):
      break

  cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
  cv2.imshow("Hand Tracking", frame)

  current_time = time.perf_counter()
  fps = 1 / (current_time - last_loop_time)
  fps_cache.append(fps)
  if len(fps_cache) > 50: fps_cache.pop(0)
  memory_info = process.memory_info()
  #sys.stdout.write(f'\rFPS: {sum(fps_cache) / len(fps_cache):.2f} | RSS: {memory_info.rss / 1024 / 1024:.2f} MB | VMS: {memory_info.vms / 1024 / 1024:.2f} MB')
  last_loop_time = current_time

cam.release()
cv2.destroyAllWindows()