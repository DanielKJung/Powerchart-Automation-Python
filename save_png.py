from PIL import Image
from io import BytesIO



# Read the text file as a string
with open("test_image.txt", "r") as f:
    text = f.read().strip()
    
    
# Evaluate the bytes literal safely
binary_data = eval(text)  # This turns the string b'...' into actual bytes




# Convert binary data to image
image = Image.open(BytesIO(binary_data))

# Save to file
output_path = "output.png"
image.save(output_path)

# Optionally open it (will launch default image viewer)
image.show()

print(f"✅ Image saved as {output_path}")