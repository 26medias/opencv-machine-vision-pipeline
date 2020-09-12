#from vision_pipeline.framework import VisionFramework
from vision_pipeline import framework

visionPipeline = framework.VisionFramework(settings="settings/face_detection.json")

visionPipeline.capture(src=0, fps=30)