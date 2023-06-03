import Tween, time

tween_settings = {
    "time": 2,
    "style": "linear",
}

class object:
    def __init__(self):
        self.tween_value = 0
        self.tween_value_two = 0

new_object = object()

tween_info = Tween.createTweenInfo(tween_settings)
tween = Tween.createTween(new_object, tween_info, {
    "tween_value": 1,
    "tween_value_two": 2,
})

started = time.time()

tween.Play()
tween.Finished()

print(f"Final values: {new_object.tween_value}, {new_object.tween_value_two}")
print(f"Took: {time.time()-started}s")
