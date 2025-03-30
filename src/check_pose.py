import numpy as np
from get_hand_angles import get_hand_angles
from get_hand_distances import get_hand_distances
from hands import get_landmark

def check_pose(pose_data, results):
  for handIndex, hand_landmarks in enumerate(results.multi_hand_landmarks):
    if not str(handIndex) in pose_data: continue
    hand_data = pose_data[str(handIndex)]
    goal_angles = hand_data['angles']
    goal_distances = hand_data['distances']
    angles = get_hand_angles(hand_landmarks)
    distances = get_hand_distances(hand_landmarks)
    if angles is None:
      return False, None
    for root_name in goal_angles:
      root_angles = angles[root_name]
      for landmark_name, goal_angle in goal_angles[root_name].items():
        angle_diff = goal_angle - root_angles[landmark_name]
        if np.abs(angle_diff) > 40:
          return False, {'type': 'angle', 'landmark': get_landmark(landmark_name, hand_landmarks)}
      root_distances = [(connection_name, distance) for connection_name, distance in distances.items() if connection_name.startswith(root_name)]
      for connection_name, distance in root_distances:
        if np.abs(goal_distances[connection_name] - distance) > .05:
          connected_landmark_names = connection_name.split('-')
          return False, {'type': 'distance', 'landmarks': [get_landmark(connected_landmark_names[0], hand_landmarks), get_landmark(connected_landmark_names[1], hand_landmarks)]}
  return True, None