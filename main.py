from framework import VisionFramework

visionPipeline = VisionFramework(settings="settings/gender_age.json")

visionPipeline.capture(src=0, fps=30)