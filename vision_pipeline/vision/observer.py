import importlib
import time
from vision_pipeline.tracker.lib.query import obj_query

class Observer():
    __version__ = "0.0.1"
    def __init__(self, framework):
        print("Observer:", self.__version__)
        
        # Framework instance
        self.framework  = framework
        
        # Plugin instances
        self.plugins = {}
        
        # Load the plugins
        for t in self.framework.settings["vision"]["plugins"].keys():
            for k in self.framework.settings["vision"]["plugins"][t].keys():
                plugin = self.framework.settings["vision"]["plugins"][t][k]
                print("Plugin found ["+t+"]", k, plugin["enabled"])
                if plugin["enabled"] is True:
                    lib = importlib.import_module(plugin["import"])
                    if "init" in plugin:
                        getattr(lib, plugin["init"])()
                    self.plugins[k] = {
                        "name": k,
                        "settings": plugin,
                        "type": t,
                        "fn": getattr(lib, plugin["method"])
                    }
    
    
    def see(self, frame):
        # Save the frame
        self.framework.renderer.setFrame(frame)
        self.runPipeline(frame)
        
    
    # Execute every pipleline item on a frame
    def runPipeline(self, frame):
        # Run the pipelines in order
        for item in self.framework.settings["vision"]["pipeline"]:
            if item["op"] == "box":
                # Object detection
                if item["level"] == "frame":
                    if "params" in item:
                        params = item["params"]
                    else:
                        params = None
                    objects = self.plugins[item["plugin"]]["fn"](frame, params)
                    for obj in objects:
                        self.framework.tracker.registerObject(self.plugins[item["plugin"]]["name"], obj)
            elif item["op"] == "attr":
                # Attribute inference
                if item["level"] == "object":
                    self.inferAttributes(frame, item)
    
    
    
    # Filter the objects and apply an attr plugin on them
    def inferAttributes(self, frame, pipeline_item):
        # Find matching objects
        targets = self.framework.tracker.query(pipeline_item["match"])
        for obj_id in targets:
            # Execute the plugin, infer the attributes
            attrs = self.runAttrPlugin(frame, pipeline_item, self.framework.tracker.objects[obj_id])
            # Save the last inference of that plugin
            self.framework.tracker.objects[obj_id][pipeline_item["plugin"]+"_last_inference"] = round(time.time()*1000)
            
            attr_updates = {}
            
            if "result" in pipeline_item:
                # There's a rule to pool the results
                # Start by adding the results in an array
                for attr_name in attrs.keys():
                    if "pool_"+attr_name not in self.framework.tracker.objects[obj_id]:
                        # There's no pool for that attribute, let's create it
                        #self.framework.tracker.objects[obj_id]["pool_"+attr_name] = []
                        attr_updates["pool_"+attr_name] = []
                    else:
                        attr_updates["pool_"+attr_name] = self.framework.tracker.objects[obj_id]["pool_"+attr_name]
                    #self.framework.tracker.objects[obj_id]["pool_"+attr_name].append(attrs[attr_name])
                    attr_updates["pool_"+attr_name].append(attrs[attr_name])
                    # Now we apply the pooling rule
                    pooledValue = self.getPooledAttrValue(attr_updates["pool_"+attr_name], pipeline_item["result"])
                    if pooledValue is not None:
                        attr_updates[attr_name] = pooledValue
                        attr_updates[attr_name+"_last_inference"] = round(time.time()*1000)
                        if attr_name+"_inference_count" in self.framework.tracker.objects[obj_id]:
                            attr_updates[attr_name+"_inference_count"] = self.framework.tracker.objects[obj_id][attr_name+"_inference_count"] + 1
                        else:
                            attr_updates[attr_name+"_inference_count"] = 1
            else:
                # No rule, just apply the attributes obtained
                for attr_name in attrs.keys():
                    attr_updates[attr_name] = attrs[attr_name]
                    attr_updates[attr_name+"_last_inference"] = round(time.time()*1000)
                    if attr_name+"_inference_count" in self.framework.tracker.objects[obj_id]:
                        attr_updates[attr_name+"_inference_count"] = self.framework.tracker.objects[obj_id][attr_name+"_inference_count"] + 1
                    else:
                        attr_updates[attr_name+"_inference_count"] = 1
            
            if "condition" in pipeline_item:
                # Make sure we fit the condition
                _obj = {"obj": attr_updates}
                _query_output = obj_query(_obj, pipeline_item["condition"])
                # Only apply the infered attributes if they match the condition
                if _query_output is not None and "obj" in _query_output:
                    for k in attr_updates.keys():
                        self.framework.tracker.objects[obj_id][k]   = attr_updates[k]
            else:
                for k in attr_updates.keys():
                    self.framework.tracker.objects[obj_id][k]   = attr_updates[k]
    
    
    # Get the attribute value based on an array of previous inferences, based on a pooling rule
    def getPooledAttrValue(self, attr_pool, pooling_rule):
        if pooling_rule["type"] == "max":
            _count, _val    = max([(attr_pool.count(chr),chr) for chr in set(attr_pool)])
            if "maxSize" in pooling_rule:
                attr_pool = attr_pool[pooling_rule["maxSize"]*-1:]
            if "minSize" in pooling_rule and len(attr_pool) < pooling_rule["minSize"]:
                return None
            else:
                return _val
        #return attr_pool
        return None
    
    # Run an attr plugin to infer object attributes on a specific object
    def runAttrPlugin(self, frame, pipeline_item, obj_data, returnAll=False):
        # Clip the object ouf of the frame
        rect    = self.getObjRect(frame, obj_data)
        # Infer the attributes from the plugin
        attrs   = self.plugins[pipeline_item["plugin"]]["fn"](rect)
        if returnAll is False:
            return attrs
        else:
            for a in attrs.keys():
                obj_data[a] = attrs[a]
                if a+"_inference_count" in obj_data:
                    obj_data[a+"_inference_count"] = obj_data[a+"_inference_count"] + 1
                else:
                    obj_data[a+"_inference_count"] = 1
                    
            return obj_data
    
    # Clip an object from a frame using the object coordinates
    def getObjRect(self, frame, obj_data):
        x1, x2, y1, y2 = int(min([obj_data["x1"],obj_data["x2"]])), int(max([obj_data["x1"],obj_data["x2"]])), int(min([obj_data["y1"],obj_data["y2"]])), int(max([obj_data["y1"],obj_data["y2"]]))
        return frame[y1:y2, x1:x2].copy()
    
    
    
    
    
    
    
    