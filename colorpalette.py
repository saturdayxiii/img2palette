from PIL import Image
from collections import Counter
import matplotlib.pyplot as plt

# Function to bucket/round colors
def bucket_color(color, bucket_size=10):
    """Rounds the RGB values to the nearest bucket size."""
    return tuple((channel // bucket_size) * bucket_size for channel in color)

# Function to convert a color tuple to RGBA string
def rgba_string(color):
    """Converts an RGB color tuple to an RGBA string representation."""
    return f"RGBA{color}"

# Function to convert RGB to hex code
def rgb_to_hex(color):
    """Converts an RGB tuple to a hex code string."""
    return '#{:02x}{:02x}{:02x}'.format(*color)

# Function to load and process the image
def process_image(image_path, bucket_size=10, color_limit=10, chart_type='bar', exclude_top=0, label_format='rgba'):
    # Load the image
    img = Image.open(image_path)
    pixels = list(img.getdata())

    # Apply bucketing to each pixel's color
    bucketed_pixels = [bucket_color(pixel, bucket_size) for pixel in pixels]

    # Count the frequency of each bucketed color
    color_counts = Counter(bucketed_pixels)

    # Sort colors by frequency and exclude the top N most common colors
    sorted_colors = color_counts.most_common()[exclude_top: exclude_top + color_limit]

    # Get the RGB values and their frequencies
    colors, counts = zip(*sorted_colors) if sorted_colors else ([], [])

    # Normalize the RGB values for Matplotlib
    norm_colors = [(r/255, g/255, b/255) for r, g, b in colors]

    # Convert color tuples to the desired label format
    if label_format == 'rgba':
        labels = [rgba_string(color) for color in colors]
    elif label_format == 'hex':
        labels = [rgb_to_hex(color) for color in colors]

    # Show the chart based on user choice
    if chart_type == 'bar':
        # Plot the color bar
        plt.bar(range(len(counts)), counts, color=norm_colors)
        plt.xticks(range(len(labels)), labels, rotation=90)
        plt.xlabel(f"Colors ({label_format.upper()})")
        plt.ylabel("Frequency")
        plt.title(f"Top {color_limit} Colors in the Image (Bucket Size: {bucket_size}, Excluding Top {exclude_top})")
    elif chart_type == 'pie':
        # Plot the color pie chart
        plt.pie(counts, colors=norm_colors, labels=labels, startangle=90)
        plt.title(f"Top {color_limit} Colors in the Image (Bucket Size: {bucket_size}, Excluding Top {exclude_top})")
        plt.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.

    plt.show()

# Function to count unique colors in the image without bucketing
def count_unique_colors(image_path):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    unique_colors = set(pixels)  # Use a set to find unique colors
    return len(unique_colors)

# Function to count unique colors after applying the bucket size
def count_bucketed_colors(image_path, bucket_size):
    img = Image.open(image_path)
    pixels = list(img.getdata())

    # Apply bucketing
    bucketed_pixels = [bucket_color(pixel, bucket_size) for pixel in pixels]
    unique_bucketed_colors = set(bucketed_pixels)
    return len(unique_bucketed_colors)

# Function to interact with the user
def main():
    image_path = input("Enter the path to the image: ")
    
    # Count and inform the user about the number of unique colors without bucketing
    num_unique_colors = count_unique_colors(image_path)
    print(f"The image contains {num_unique_colors} unique colors.")
    
    # Loop to allow user to adjust bucket size after seeing the effect
    while True:
        bucket_size = int(input("Enter the color bucket size (e.g., 10, 20): "))
        
        # Count and display the number of colors with the chosen bucket size
        num_bucketed_colors = count_bucketed_colors(image_path, bucket_size)
        print(f"With a bucket size of {bucket_size}, the image contains {num_bucketed_colors} unique colors.")
        
        # Ask the user if they want to change the bucket size
        change_bucket = input("Would you like to change the bucket size? (yes/no): ").lower()
        if change_bucket == 'no':
            break
    
    # Ask for the number of top colors to display
    color_limit = int(input("Enter the number of top colors to display: "))

    # Ask the user if they want to exclude the most common colors
    exclude_top = int(input("How many of the most common colors would you like to exclude from the palette? (e.g., 0, 1, 2): "))

    # Ask the user for their preferred chart type (bar or pie)
    chart_type = input("Would you like to see a 'bar' chart or 'pie' chart? (bar/pie): ").lower()
    
    # Ask the user for their preferred label format (RGBA or hex)
    label_format = input("Would you like the colors labeled as 'rgba' or 'hex' codes? (rgba/hex): ").lower()

    process_image(image_path, bucket_size, color_limit, chart_type, exclude_top, label_format)

if __name__ == "__main__":
    main()
