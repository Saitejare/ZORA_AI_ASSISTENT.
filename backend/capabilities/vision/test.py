from backend.capabilities.vision.service import VisionService

vision = VisionService()

print("=" * 60)
print("Screenshot")
print(vision.execute(
    "screenshot",
    {
        "path": "screen.png"
    }
))

print("=" * 60)
print("Image Info")
print(vision.execute(
    "image_info",
    {
        "image_path": "screen.png"
    }
))

print("=" * 60)
print("Image Size")
print(vision.execute(
    "image_size",
    {
        "image_path": "screen.png"
    }
))

print("=" * 60)
print("OCR")
print(vision.execute(
    "read_text",
    {
        "image_path": "screen.png"
    }
))