from framework import VisionFramework

visionPipeline = VisionFramework(settings="settings/emotions.json")
visionPipeline.capture(src=1, fps=30)