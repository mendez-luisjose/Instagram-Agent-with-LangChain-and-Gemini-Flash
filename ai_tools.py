from pydantic.v1 import BaseModel, Field
from langchain.tools import tool
from instagram_tools import generate_ig_post, generate_ig_story, publish_ig_note, modify_ig_pic_profile, modify_ig_bio

class PostCaptionTopicInput(BaseModel):
    topic: str = Field(description="Instagram Caption Topic in the user's request.", default="", exclude=None)

class NoteMessageInput(BaseModel):
    message: str = Field(description="Message in the user's request.", default="", exclude=None)
    

@tool("generate_ig_post", return_direct=True, args_schema=PostCaptionTopicInput) 
def tool_generate_ig_post(topic) :
    """
    Use this tool when a user wants to create or generate a new instagram post.
    You will need to identify the topic of the instagram post from the user's request.
    Usually, the requests will look like 'create an instagram post about {topic}'. 
    The parameter must be of type string.
    """
    return generate_ig_post(topic)

@tool("generate_ig_story", return_direct=True, args_schema=PostCaptionTopicInput) 
def tool_generate_ig_story(topic) :
    """
    Use this tool when a user wants to create or generate a new instagram story.
    You will need to identify the topic of the instagram story from the user's request.
    Usually, the requests will look like 'create an instagram story about {topic}'. 
    The parameter must be of type string.
    """
    return generate_ig_story(topic)

@tool("publish_ig_note", return_direct=True, args_schema=NoteMessageInput) 
def tool_publish_ig_note(message) :
    """
    Use this tool when a user wants to create or publish a new instagram note.
    You will need to identify the message or note from the user's request.
    Usually, the requests will look like 'create an instagram note that says {message}' or 'publish a note that says {message}'. 
    The parameter must be of type string.
    """
    return publish_ig_note(message)

@tool("modify_ig_pic_profile", return_direct=True, args_schema=NoteMessageInput) 
def tool_modify_ig_pic_profile(topic) :
    """
    Use this tool when a user wants to modify or create a new picture for their instagram profile.
    You will need to identify the topic of the new instagram profile picture from the user's request.
    Usually, the requests will look like 'modify my instagram picture profile with a new one about {topic}' or 'modify my picture profile with an image about {topic}'. 
    The parameter must be of type string.
    """
    return modify_ig_pic_profile(topic)

@tool("modify_ig_bio", return_direct=True, args_schema=NoteMessageInput) 
def tool_modify_ig_bio(message) :
    """
    Use this tool when a user wants to create, publish or modify their instagram bio or biography.
    You will need to identify the message, note or the new biography from the user's request.
    Usually, the requests will look like 'modify my instagram biography with a new one that says {message}', 'change my bio that says {message}' or 'modify my biography that says {message}'. 
    The parameter must be of type string.
    """
    return modify_ig_bio(message)

ig_tools = [
    tool_generate_ig_post,
    tool_generate_ig_story,
    tool_publish_ig_note,
    tool_modify_ig_pic_profile,
    tool_modify_ig_bio
]