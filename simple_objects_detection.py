from vision_pipeline import framework

visionPipeline = framework.VisionFramework(settings="settings/objects.json")

visionPipeline.capture(src=0, fps=30)