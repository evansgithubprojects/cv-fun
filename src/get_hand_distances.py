from hands import tracked_landmark_roots, tracked_landmarks, get_landmark
from dynamic_screen import DynamicScreen

def get_hand_distances(hand_landmarks):
  distances = {}
  tips = []
  for root_name in tracked_landmark_roots:
    tip_name = tracked_landmarks[root_name][-1]
    tips.append((tip_name, get_landmark(tip_name, hand_landmarks)))

  for i, (tip_name, tip) in enumerate(tips):
    if i + 1 == len(tips): break
    (next_name, next_tip) = tips[i + 1]
    distances[tip_name + '-' + next_name] = DynamicScreen.instance.get_static_distance((tip.x, tip.y), (next_tip.x, next_tip.y))

  return distances