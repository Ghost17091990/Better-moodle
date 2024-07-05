import base64
import requests
import pyperclip
import pyautogui
import keyboard
import ctypes
IDC_HAND = 32649
API_KEY = "YOUR_API_KEY" #!!!!!!change this with your OpenAI API Key!!!!!
def set_cursor(cursor_id):
    ctypes.windll.user32.SetSystemCursor(ctypes.windll.user32.LoadCursorW(0, cursor_id), 32512)

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')    

def take_screenshot():
    file_name = "image.png"
    screenshot = pyautogui.screenshot()
    screenshot.save(file_name)
    print(f"Screenshot saved as {file_name}")
    set_cursor(IDC_HAND)
    # OpenAI API Key
    api_key = API_KEY

    # Function to encode the image


    # Path to your image
    image_path = "image.png"

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4o",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "Please answer the questions from the image as follows (if ther's multiple good answers give them but don't write anything else): [numéro de la question]: [Réponse(s)]"
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    #print(response.json())
    texte_a_copier = response.json()['choices'][0]['message']['content']
    pyperclip.copy(texte_a_copier)
    set_cursor(IDC_HAND)
    
def on_f8_press(event):
    take_screenshot()
    
keyboard.on_press_key("F8", on_f8_press)
keyboard.wait("esc")
