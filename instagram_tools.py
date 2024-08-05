from instagrapi import Client
from dotenv import load_dotenv
import os
import google.generativeai as genai
import requests
from PIL import Image
from io import BytesIO
from requests.exceptions import Timeout
from utils import text_to_speech
import time
from playsound import playsound
import base64
import streamlit as st

load_dotenv()


ACCOUNT_USERNAME = os.getenv("ACCOUNT_USERNAME")
ACCOUNT_PASSWORD = os.getenv("ACCOUNT_PASSWORD")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')

cl = Client()             
cl.login(st.session_state.instagram_user, st.session_state.instagram_password)

API_URL_ENDPOINT = st.session_state.api_url_endpoint

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)

def generate_ig_caption(query) :
    query_post = f"Generate a Instagram Caption Post about {query}. Just generate the caption without any extra information so i can just copy and paste it into the Instagram Post."
    response = model.generate_content(query_post)
    return response.text

def generate_post_ig_img(query, img_type="post") :
    query_img = f"ghibli style {query}"
    resp = requests.post(API_URL_ENDPOINT, data={"query": query_img, "story": False})
    img_post_content = resp.content
    pillow_img = Image.open(BytesIO(img_post_content)).convert('RGB')

    if img_type == "post":
        pillow_img.save("./imgs/ig_post.png")
    else :
        pillow_img.save("./imgs/ig_pic_profile.png")

def generate_story_ig_img(query) :
    query_img = f"ghibli style {query}"
    resp = requests.post(API_URL_ENDPOINT, data={"query": query_img, "story": True})
    img_post_content = resp.content
    pillow_img = Image.open(BytesIO(img_post_content)).convert('RGB')
    pillow_img.save("./imgs/ig_story.png")

def generate_ig_post(query) :
    """
    Generate a new Instagram Post, with a new AI Caption and a new AI Image Generated.
    """  
    try :
        file_path = text_to_speech("Sure… let me create the instagram post… I am going to generate a new image and a new caption for the post… Please wait a few seconds… I will let you know when the post is available and published")
        autoplay_audio(file_path)
        #playsound(file_path)
        #os.remove(file_path)

        #time.sleep(5)
        generate_post_ig_img(query)
        ig_post_caption = generate_ig_caption(query)

        media = cl.photo_upload(
            "./imgs/ig_post.png",
            ig_post_caption,
            extra_data={
                "custom_accessibility_caption": "alt text example",
                "like_and_view_counts_disabled": 1,
                "disable_comments": 1,
            }
        )
        
        file_path = text_to_speech("The Instagram post was created and published successfully… you can check it in your Instagram account")
        autoplay_audio(file_path)
        #playsound(file_path)
        #os.remove(file_path)
        #time.sleep(3)

        return "Instagram Post Created Successfully!"
    except Timeout as e:
        return f"An unexpected Timeout error occurred. {e} Try Again."
    except Exception as e:
        return f"An unexpected error occurred. {e} Try Again."
    except :
        return f"An unexpected error occurred. Try Again."
    
def generate_ig_story(query) :
    """
    Generate a new Instagram Story, with a new AI Image Generated.
    """  
    try :
        file_path = text_to_speech("Sure… let me create the instagram story… I am going to generate a new image for the story… Please wait a few seconds… I will let you know when the story is available and published")
        autoplay_audio(file_path)
        #playsound(file_path)
        #os.remove(file_path)

        #time.sleep(5)
        generate_story_ig_img(query)

        media = cl.photo_upload_to_story(
            "./imgs/ig_story.png"
        )

        
        file_path = text_to_speech("The Instagram Story was created and published successfully… you can check it in your Instagram account")
        autoplay_audio(file_path)
        #playsound(file_path)
        #os.remove(file_path)
        #time.sleep(3)

        return "Instagram Story Created Successfully!"
    except Timeout as e:
        return f"An unexpected Timeout error occurred. {e} Try Again."
    except Exception as e:
        return f"An unexpected error occurred. {e} Try Again."
    except :
        return f"An unexpected error occurred. Try Again."
    
def publish_ig_note(query) :
    """
    Publish a new Instagram Note.
    """  
    try :
        file_path = text_to_speech("Sure… Please wait a few seconds… I will let you know when the note is available and published")
        autoplay_audio(file_path)
        #playsound(file_path)
        #os.remove(file_path)
        time.sleep(3)

        cl.create_note(query)
        
        file_path = text_to_speech("The Instagram Note was published successfully… you can check it in your Instagram account")
        autoplay_audio(file_path)
        #playsound(file_path)
        #os.remove(file_path)

        return "Instagram Note Published Successfully!"
    except Timeout as e:
        return f"An unexpected Timeout error occurred. {e} Try Again."
    except Exception as e:
        return f"An unexpected error occurred. {e} Try Again."
    except :
        return f"An unexpected error occurred. Try Again."
    

def modify_ig_pic_profile(query) :
    """
    Generate a new Instagram Pic Profile, with a new AI Image Generated.
    """  
    try :
        file_path = text_to_speech("Sure… let me modify your instagram picture profile… Please wait a few seconds… I will let you know when its done")
        autoplay_audio(file_path)
        #playsound(file_path)
        #os.remove(file_path)

        #time.sleep(5)
        generate_post_ig_img(query, img_type="profile_picture")

        cl.account_change_picture("./imgs/ig_pic_profile.png")
        
        file_path = text_to_speech("Your Instagram Picture Profile was Modified successfully")
        autoplay_audio(file_path)
        #playsound(file_path)
        #os.remove(file_path)
        #time.sleep(3)

        return "Instagram Picture Profile Modified Successfully!"
    except Timeout as e:
        return f"An unexpected Timeout error occurred. {e} Try Again."
    except Exception as e:
        return f"An unexpected error occurred. {e} Try Again."
    except :
        return f"An unexpected error occurred. Try Again."
    
def modify_ig_bio(query) :
    """
    Publish a new Instagram Biography.
    """  
    try :
        file_path = text_to_speech("Sure… Please wait a few seconds… I will let you know when your bio is modified")
        autoplay_audio(file_path)
        #playsound(file_path)
        #os.remove(file_path)

        cl.account_set_biography(query)

        time.sleep(3)
        
        file_path = text_to_speech("Your instagram bio was modified successfully… you can check it in your Instagram account")
        autoplay_audio(file_path)
        #playsound(file_path)
        #os.remove(file_path)
        #time.sleep(3)

        return "Instagram Bio Modified Successfully!"
    except Timeout as e:
        return f"An unexpected Timeout error occurred. {e} Try Again."
    except Exception as e:
        return f"An unexpected error occurred. {e} Try Again."
    except :
        return f"An unexpected error occurred. Try Again."
    


