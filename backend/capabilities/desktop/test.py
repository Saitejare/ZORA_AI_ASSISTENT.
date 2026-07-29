import time

from backend.capabilities.desktop.service import DesktopService


desktop = DesktopService()


print("=" * 60)
print("Screen Size")
print(desktop.execute("screen_size", {}))

print("=" * 60)
print("Mouse Position")
print(desktop.execute("position", {}))

print("=" * 60)
print("Waiting 3 seconds...")
desktop.execute("wait", {"seconds": 3})

print("=" * 60)
print("Move Mouse")
print(desktop.execute("move_mouse", {
    "x": 500,
    "y": 300
}))

time.sleep(1)

print("=" * 60)
print("Click")
print(desktop.execute("click", {}))

time.sleep(1)

print("=" * 60)
print("Type Text")
print(desktop.execute("type_text", {
    "text": "Hello from ZORA!"
}))

time.sleep(1)

print("=" * 60)
print("Press Enter")
print(desktop.execute("press_key", {
    "key": "enter"
}))

time.sleep(1)

print("=" * 60)
print("Take Screenshot")
print(desktop.execute("screenshot", {
    "path": "desktop_test.png"
}))

print("=" * 60)
print("Desktop capability test completed.")