from vision_pipeline import framework

visionPipeline = framework.VisionFramework(settings="settings/age_detection.json")

visionPipeline.capture(src=0, fps=30)