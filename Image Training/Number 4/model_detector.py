import cv2
import glob
import polars as pl
from ultralytics import YOLO

model = YOLO('best-1300-images.pt')

png_files = glob.glob('Puzzle Numbers/*.png')
jpg_files = glob.glob('Puzzle Numbers/*.jpg')

image_files = jpg_files + png_files

all_results = []

for img_path in image_files:
    #print(f"Processing {img_path}")
    img = cv2.imread(img_path)

    results = model(img)
    result = results[0]

    df = result.to_df()

    if df.height > 0:  # Only add non-empty DataFrames
        df = df.with_columns(pl.lit(img_path).alias('image'))
        all_results.append(df)
    else:
        print(f"No detections in {img_path}")

    #img_with_boxes = result.plot()
    #img_with_boxes = cv2.cvtColor(img_with_boxes, cv2.COLOR_RGB2BGR)

    #cv2.imshow('YOLO Detection', img_with_boxes)
    if cv2.waitKey(0) & 0xFF == 27:  # Press ESC to exit early
        break

cv2.destroyAllWindows()

if all_results:
    combined_df = pl.concat(all_results)
    print("\nCombined results from all images:")
    print(combined_df)

    #combined_df.write_csv('combined_results.csv')
    #print("\nResults saved to combined_results.csv")
else:
    print("No results found.")