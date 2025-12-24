import re

filament_usage_mm = "total estimated time"
# filament_usage_mm = "model printing time"
filament_usage_g =  "total filament length [mm]"
estimated_time = "total filament weight [g]"
# materials = 1
printer = "machine"

#keys = [filament_usage_g, filament_usage_mm, estimated_time, materials, printer]
keys = [filament_usage_g, filament_usage_mm, estimated_time, printer]

def parse_gcode(file_path, keywords = keys):
    metrics = {}
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line.startswith(";"):
                continue

            # For each keyword, search anywhere in the line
            for key in keywords:
                pattern = re.compile(re.escape(key) + r"\s*:\s*(.+?)(\s*;|$)")
                match = pattern.search(line)
                if match:
                    value = match.group(1).strip()
                    
                    # Try converting numeric list or single float
                    if "," in value:
                        try:
                            value = [float(x) for x in value.split(",")]
                        except ValueError:
                            pass
                    else:
                        try:
                            value = float(value)
                        except ValueError:
                            pass
                    
                    metrics[key] = value
                    trimmed_metrics = trim(metrics)
    return trimmed_metrics

def trim(input_dict):
    metrics = {}

    for key, value in input_dict.items():
        if isinstance(value, str):
            metric = value.replace("=", "").strip()
        else:
            metric = value
        metrics[key] = metric
    return metrics
    