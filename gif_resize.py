from PIL import Image
import tkinter as tk

gif_name = "space.gif"
NEW_WIDTH = 400
NEW_HEIGHT = 400

'''-------------  FUNCTIONS --------------'''
def resizeGif(img: tk.PhotoImage, new_width, new_height):
    old_width = img.width()
    old_height = img.height()
    photo = tk.PhotoImage(width= new_width, height= new_height)
    for x in range(new_width):
        for y in range(new_height):
            x_old = int(x * old_width / new_width)
            y_old = int(y * old_height / new_height)
            rgb = '#%02x%02x%02x' % img.get(x_old, y_old)
            photo.put(rgb, (x,y))
    return photo

def animate(count):
    gif_lbl.configure(image= resized_frames[count])
    count += 1
    if count == frame_count:
        count = 0
    root.after(100,animate,count)


'''------------- RESIZING GIF FRAMES ------------------'''
with Image.open(gif_name) as im:
    frame_count = im.n_frames

frames = [tk.PhotoImage(file= gif_name, format= f"gif -index {i}") for i in range(frame_count)]
resized_frames = [resizeGif(frames[i],NEW_WIDTH,NEW_HEIGHT) for i in range(frame_count)]

'''------------------ SAVING RESIZED GIF ------------------'''
import imageio, base64, io
def PhotoImageToPILImage(photoimage):
    width = photoimage.width()
    height = photoimage.height()
    pil_img = Image.new("RGB", (width, height))
    img_data = [photoimage.get(x,y) for y in range(height) for x in range(width)]
    pil_img.putdata(img_data)
            
    return pil_img

output_file = "resized.gif"
# Convert tkinter.PhotoImage frames to PIL Image objects
pil_frames = [PhotoImageToPILImage(frame) for frame in resized_frames]

# Save the frames as a GIF using imageio
imageio.mimsave(
    output_file,
    [frame.convert("RGB") for frame in pil_frames],  # Convert to RGB mode
    duration=100,  # Frame duration in milliseconds (adjust as needed)
    loop=0,  # 0 means an infinite loop, or specify the number of loops
)


if __name__ == "__main__":

    '''----------------GUI HANDLING ---------------'''
    root = tk.Tk()
    root.title("GIF RESIZE")
    root.geometry("800x800")
    root.config(bg="red")

    gif_lbl = tk.Label(root, image="", bg= "blue")
    gif_lbl.pack(fill= "both", expand= True)
    animate(0)
    root.mainloop()