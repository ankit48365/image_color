import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import tkinter as tk
from tkinter import filedialog
from sklearn.cluster import KMeans

# Configuration
NUM_COLORS = 6  # Number of main colors for the bar chart (3 to 10)

def load_image():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
    )
    if not file_path:
        raise ValueError("No image selected")
    return Image.open(file_path)

def get_dominant_colors(image, num_colors):
    # Convert image to RGB if it has an alpha channel
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    
    # Resize image to speed up processing
    image = image.resize((150, 150))
    
    # Convert image to numpy array
    pixels = np.array(image).reshape(-1, 3)
    
    # Use KMeans clustering to find dominant colors
    kmeans = KMeans(n_clusters=num_colors, random_state=42)
    kmeans.fit(pixels)
    
    # Get colors and their counts
    colors = kmeans.cluster_centers_.astype(int)
    labels = kmeans.labels_
    counts = np.bincount(labels)
    
    # Calculate percentages
    percentages = (counts / counts.sum()) * 100
    
    return colors, percentages

def plot_color_chart(colors, percentages):
    # Create figure
    plt.figure(figsize=(10, 6))
    
    # Create bar chart
    bars = plt.bar(range(len(colors)), percentages, color=[colors/255 for colors in colors])
    
    # Customize plot
    plt.title('Color Distribution in Image')
    plt.xlabel('Colors')
    plt.ylabel('Percentage (%)')
    plt.xticks([])  # Hide x-axis labels since we're showing colors
    
    # Add percentage labels on top of bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{percentages[i]:.1f}%', ha='center', va='bottom')
    
    # Save the plot
    plt.savefig('color_distribution.png')
    plt.close()

def main():
    try:
        # Validate configuration
        if not 3 <= NUM_COLORS <= 10:
            raise ValueError("NUM_COLORS must be between 3 and 10")
        
        # Load image
        image = load_image()
        
    #     # Get dominant colors and their percentages
    #     colors, percentages = get_dominant_colors(image, NUM_COLORS)
        
    #     # Plot the bar chart
    #     plot_color_chart(colors, percentages)
        
    #     print(f"Color distribution chart saved as 'color_distribution.png'")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 