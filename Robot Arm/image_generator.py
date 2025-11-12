from PIL import Image, ImageOps
import os
import random

def augment_images(input_folder, output_folder, num_augmented):
    os.makedirs(output_folder, exist_ok=True)
    image_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder)
                   if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not image_files:
        print("No images found in input folder.")
        return

    for i in range(num_augmented):
        img_path = image_files[i % len(image_files)]
        img = Image.open(img_path).convert("RGB")  # ensure 3 channels

        # Random horizontal flip
        if random.random() < 0.5:
            img = ImageOps.mirror(img)

        # Random vertical flip
        if random.random() < 0.5:
            img = ImageOps.flip(img)

        # Random rotation between -30 and 30 degrees
        angle = random.uniform(-30, 30)
        img = img.rotate(angle, resample=Image.BICUBIC, expand=True)

        # Random skew (slant) using affine transform
        width, height = img.size
        xshift = random.uniform(-0.2, 0.2) * width
        new_width = width + abs(xshift)
        img = img.transform(
            (int(new_width), height),
            Image.AFFINE,
            (1, xshift/height, 0, 0, 1, 0),
            resample=Image.BICUBIC
        )

        # Save augmented image
        out_path = os.path.join(output_folder, f"aug_{i+1:03d}.jpg")
        img.save(out_path)

        if (i+1) % 20 == 0:
            print(f"Generated {i+1}/{num_augmented} images")

    print("Done! Augmented images saved to:", output_folder)


# Example usage
augment_images("input_images_base", "augmented_images", num_augmented=200)
