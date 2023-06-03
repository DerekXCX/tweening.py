import time, threading, math

_acceptedInfo = {
    "time": (int, float),
    "style": (str),
}

_defaults = {
    "style": "linear",
}

_requiredParameters = ["time"]

def _searchDict(dict : dict, searching_key : str):
    found = None
    try:
        found = dict[searching_key]
    except:
        pass
    return found

def _formatTypeTuple(tuple):
    returning_string = ""
    if isinstance(tuple, type):
        returning_string = str(tuple).split("'")[1]
        return returning_string
    for value in tuple:
        type_as_string = str(value)
        split_string = type_as_string.split("'")
        returning_string += f", {split_string[1]}"
    returning_string = returning_string.replace(", ", "", 1)
    return returning_string

def _formatInfoDictionary(info_dictionary):
    returning = {}
    issues = []
    
    for index in info_dictionary:
        value = info_dictionary[index]
        found_index_in_accepted = _searchDict(_acceptedInfo, index)
        
        if not found_index_in_accepted: 
            issues.append(f"TWEEN INFO: Invalid setting: {index}")
            continue
        
        accepted_value_types = _acceptedInfo[index]
        
        if not isinstance(value, accepted_value_types):
            accepted_value_types_to_string = _formatTypeTuple(accepted_value_types).upper()
            value_type_to_string = _formatTypeTuple(type(value)).upper()
            issues.append(f"TWEEN INFO: Invalid value type for '{index}', expected {accepted_value_types_to_string} not {value_type_to_string}")
            continue
   
        returning[index] = value
    for value in _defaults:
        if not _searchDict(returning, value):
            returning[value] = _defaults[value]
    for value in _requiredParameters:
        if not _searchDict(returning, value):
            issues.append(f"TWEEN INFO: Missing required setting: {value}")
            returning = None
            
    return returning, issues
    pass

def _linearFormula(time_elapsed, time_to_take, starting_value, final_value):
    slope_one = (final_value - starting_value)
    slope_two = 1/time_to_take
    return (time_elapsed * slope_one * slope_two) + starting_value
    
_getKeyPointFunctions = {
    "linear": _linearFormula
}

def _moveAlongKeyPoints(tween, value_to_update):
    object = tween.object
    starting_value = getattr(object, value_to_update)
    resolution = tween.resolution
    tween_info = tween.info
    time_to_take = tween_info.time
    final_value = tween.values_to_update[value_to_update]
    
    last_looped = time.time()
    time_elapsed = 0
    loop_number = 0
    
    while (1):
        if tween.paused: continue
        last_looped = time.time()
        value = _getKeyPointFunctions[tween_info.style](time_elapsed, time_to_take, starting_value, final_value)
        setattr(object, value_to_update, value)
        if (value >= final_value) or (time_elapsed >= time_to_take) or (loop_number >= resolution + 1):
            setattr(object, value_to_update, final_value)
            break
        loop_number += 1
        time.sleep(time_to_take/resolution)
        time_elapsed += (time.time() - last_looped)
        
class createTweenInfo:
    def __init__(self, info : dict):
        self.invalid = False
        get_accepted_parameters, issues = _formatInfoDictionary(info)

        if not _searchDict(_getKeyPointFunctions, get_accepted_parameters["style"]):
            issues.append("TWEEN INFO: Invalid style provided")
            get_accepted_parameters = None
        if not get_accepted_parameters:
            for value in issues:
                print(value)
            self.invalid = True
            return
        for index in get_accepted_parameters:
            setattr(self, index, get_accepted_parameters[index])
    
class createTween:
    def __init__(self, object : object, info : dict, values : dict):
        if not info.invalid:
            self.info = info
            self.values_to_update = {}
            self.threads = {}
            self.object = object
            self.paused = False
            self.playing = False
            self.times_played = 0
            
            self.resolution = 1000
        
            for index in values:
                index_value = values[index]
                value_type_to_string = _formatTypeTuple(type(index_value)).upper()
                if not isinstance(index_value, (float, int)): print(f"TWEEN: Tweening values must be a FLOAT or INT, not {value_type_to_string}"); continue
                if hasattr(object, index):
                    self.values_to_update[index] = index_value
                else:
                    print(f"TWEEN: Object does not have attribute {index.upper} to tween")
        else:
            print("TWEEN: Invalid tween info provided"); del(self); return
                
    def Play(self):
        if self.playing:
            print("TWEEN: Already playing a tween, please cancel or wait for finish before playing again")
            return
        
        self.playing = True
        self.threads = []
        for value_to_update in self.values_to_update:
            update_thread = threading.Thread(target = _moveAlongKeyPoints, args = (self, value_to_update))
            update_thread.start()
            
            self.threads.append(update_thread)
        def waitForThreadsToFinish():
            for thread in self.threads:
                thread.join()
            self.times_played += 1
            self.Playing = False
            self.threads.clear()
        threading.Thread(target = waitForThreadsToFinish).start()
    def Pause(self):
        self.paused = True
    def Resume(self):
        self.paused = False  
    def Finished(self):
        times_played_when_started = self.times_played
        while (1):
            if times_played_when_started != self.times_played:
                break
    def Cancel():
        pass
