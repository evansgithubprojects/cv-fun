import json

pose_names = [
  'blood',
  #'crip',
  'west side'
]

def deserialize_poses():
  pose_data = {}
  for pose_name in pose_names:
    try:
      with open(f'poses/{pose_name}.json', "r") as poseFile:
        deserialized = None
        try:
          deserialized = json.loads(poseFile.read())
        except ValueError as error:
          print('Failed to deserialize pose data: ')
          print(error)
          return

        if deserialized:
            pose_data[pose_name] = deserialized
    except OSError as error:
      print('Failed to open pose file: ')
      print(error)
      return
  
  return pose_data