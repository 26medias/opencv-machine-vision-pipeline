from vision_pipeline import framework

visionPipeline = framework.VisionFramework(settings="settings/traffic.json")

# Increase the distance threshold for object permanence, cars are moving fast between frames
visionPipeline.tracker.dist_threshold   = 100
visionPipeline.tracker.deactivateAfter  = 10
visionPipeline.tracker.deleteAfter      = 30

visionPipeline.capture(src="traffic.mp4", fps=30)