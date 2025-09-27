# 📃 A GUI tool to batch rename image files using WhatsApp logs or text mappings

### Goal of this project:
- Create a Python Dictionary with key-value pairs mapping original image filenames to their WhatsApp captions (captions are taken from chat logs) or even using a plain text file.
- Support custom regular expressions (RegEx)
- Copy and rename all images into a separate output folder.
- Provide a user-friendly GUI using Tkinter.
- Automate a tedious and repetitive task!

#
### The Contents:
- Launch the program and provide the WhatsApp log file (in `.txt` format), the original images folder and an output folder

<img width="496" height="328" alt="1" src="https://github.com/user-attachments/assets/46a9190a-6fcc-4c4d-883f-6869ace21018" />

- This is the original folder and names of the images

<img width="1000" alt="2" src="https://github.com/user-attachments/assets/04db5e34-3bb5-4de8-9127-9812095ac8fd" />

- When the user clicks Submit, the program first copies the image folder to the output directory (to prevent errors or corruption)
- The program matches each original image filename with its corresponding caption from the WhatsApp log using a Python Dictionary.
- The mapping is done using RegEx to find a pattern in all the original image names (think IMG-numbers.jpg)

<img width="1000" alt="3" src="https://github.com/user-attachments/assets/e3157111-533a-404c-83ee-ae0ca5fe7ff4" />

#
### Custom Regex Example:
- Here our custom regex will be “summer” since it is the common name/occurrence across all the images. Clicking the help button explains how the custom regex option works

<img height="280" alt="4" src="https://github.com/user-attachments/assets/0034c469-7031-4594-af07-605d778b67fa" />
&nbsp;
<img height="280" alt="5" src="https://github.com/user-attachments/assets/2ace5835-9359-4e6e-8d09-bd0c181d32b2" />

- Example of a text file where there must be an alternating pattern of original image name followed by a new image name the user wants at the next line. Users don’t have to worry about white space or gaps between lines as long as the pattern is being followed:

<img width="958" height="176" alt="6" src="https://github.com/user-attachments/assets/ff79706a-0f6f-4986-a01c-2ad5d45b536c" />

- Another example of this pattern:
```
original_image_1.jpg
new_name_1.jpg
original_image_2.png
new_name_2.png
```

<table>
  <tr>
    <td align="center">
      Original Image Names (Before)
      <br> <img height="139" alt="7" src="https://github.com/user-attachments/assets/e8bb5a26-11bc-4940-858b-1790b0cfae68" />
    </td>
    <td align="center">
      Renamed Images (After)
      <br> <img height="139" alt="8" src="https://github.com/user-attachments/assets/422e9572-588e-4b0f-8643-92129744e9b8" />
    </td>
  </tr>

  <tr>
    <td align="center">
      Error if you Provide the wrong text file
      <br><br> <img height="143" alt="9" src="https://github.com/user-attachments/assets/d6138c3f-fdf9-49ca-9949-873a8ba2524d" />
    </td>
    <td align="center">
      Error if you Provide the wrong folder path
      <br><br> <img height="143" alt="10" src="https://github.com/user-attachments/assets/f8438c1b-3436-4e1c-9e3c-73c0068ae4aa" />
    </td>
  </tr>
</table>
