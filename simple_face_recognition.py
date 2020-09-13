#from vision_pipeline.framework import VisionFramework
from vision_pipeline import framework

visionPipeline = framework.VisionFramework(settings="settings/face_recognition.json")

visionPipeline.capture(src=0, fps=30)