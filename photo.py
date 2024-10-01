import Metashape as ms
from PIL import Image
import os

count = 0
max_images = 50
doc = ms.app.document
doc.open("project.psz")

def main():
    photos()
    Image_Processing()
    Image_Masking()
    Photos_Allignment()
    Scale_Bar()
    final_product()

def photos():
    global count
    with open("filename.txt", "r") as file:
        for filename in file:
            if count != max_images:
                image_path = filename.strip()
                if os.path.exists(image_path):
                    try:
                        img = Image.open(image_path)
                        output_file = os.path.splitext(image_path)[0] + ".jpeg"






                        img.convert("RGB").save(output_file, "JPEG")
                        print(f"Image {image_path} saved as {output_file}")
                    except Exception as e:
                        print(f"Error processing {image_path}: {e}")
                else:
                    print(f"Image {image_path} not found.")
                count += 1
            else:
                break

# Metashape API Processing Functions
def Image_Processing():
    print("Adding photos to the chunk and processing...")
    chunk = doc.addChunk()
    photo_paths = []  # Replace with a list of your photo paths
    for filename in os.listdir("path_to_photos_folder"):  # Use your path here
        if filename.endswith(".jpeg"):
            photo_paths.append(os.path.join("path_to_photos_folder", filename))

    chunk.addPhotos(photo_paths)
    print(f"{len(photo_paths)} photos added.")

def Image_Masking():
    print("Applying masks to the images...")
    chunk = doc.chunk
    for camera in chunk.cameras:
        # Assuming all images have the same mask (or mask logic applied here)
        mask_path = os.path.join("masks_folder", camera.label + "_mask.png")
        if os.path.exists(mask_path):
            mask_image = ms.Image()
            mask_image.load(mask_path)
            camera.setMask(mask_image)
            print(f"Mask applied to {camera.label}")
        else:
            print(f"Mask not found for {camera.label}")

def Scale_Bar():
    print("Setting up scale bars...")
    chunk = doc.chunk
    markers = chunk.markers  # Assuming markers have been placed in the scene manually or by a script
    if len(markers) >= 2:
        scale_bar = chunk.addScalebar(markers[0], markers[1])
        scale_bar.reference.distance = 1.0  # Set the actual scale in meters or the unit you're using
        print(f"Scale bar added between {markers[0].label} and {markers[1].label}.")

def Photos_Allignment():
    print("Aligning photos...")
    chunk = doc.chunk
    chunk.matchPhotos(accuracy=ms.HighAccuracy, generic_preselection=True, reference_preselection=False)
    chunk.alignCameras()
    print("Photos aligned.")

def final_product():
    print("Building final product...")
    chunk = doc.chunk
    chunk.buildDenseCloud(quality=ms.MediumQuality, filtering=ms.AggressiveFiltering)
    chunk.buildModel(surface_type=ms.Arbitrary, interpolation=ms.EnabledInterpolation)
    chunk.buildUV(mapping_mode=ms.GenericMapping)
    chunk.buildTexture(blending_mode=ms.MosaicBlending)
    chunk.exportModel("final_model.obj", texture_format=ms.ImageFormatJPEG)
    print("Final model exported as 'final_model.obj'.")

# Call the main function to execute
if __name__ == "__main__":
    main()
