from apiflask import APIBlueprint

api_v1 = APIBlueprint('api_v1', __name__)

from your_recording.api.v1 import resources
