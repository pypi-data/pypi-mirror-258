"""
methods for frame rendering and message handling
"""

# lib
import json
from importlib import resources
from typing import Literal
from flask import render_template, request, make_response, Response

# src
from .models import FrameMessage

# enum types
ButtonActions = Literal['post', 'post_redirect', 'mint', 'link']


def render_frame(
        title: str = None,
        image: str = None,
        content: str = None,
        post_url: str = None,
        button1: str = None,
        button1_action: ButtonActions = None,
        button1_target: str = None,
        button2: str = None,
        button2_action: ButtonActions = None,
        button2_target: str = None,
        button3: str = None,
        button3_action: ButtonActions = None,
        button3_target: str = None,
        button4: str = None,
        button4_action: ButtonActions = None,
        button4_target: str = None,
        input_text: str = None
) -> Response:
    # TODO support cache age, aspect ratio, state data

    try:
        print(resources.files('templates'))
    except Exception as e:
        print(e)
    try:
        print(resources.files('templates') / 'frame.html')
    except Exception as e:
        print(e)
    try:
        print(resources.path('framelib', 'templates'))
    except Exception as e:
        print(e)
    try:
        print(resources.path('templates', 'frame.html'))
    except Exception as e:
        print(e)

    # render frame template
    html = render_template(
        'frame.html',
        title=title,
        image=image,
        content=content,
        post_url=post_url,
        button1=button1,
        button1_action=button1_action,
        button1_target=button1_target,
        button2=button2,
        button2_action=button2_action,
        button2_target=button2_target,
        button3=button3,
        button3_action=button3_action,
        button3_target=button3_target,
        button4=button4,
        button4_action=button4_action,
        button4_target=button4_target,
        input_text=input_text
    )

    # response
    res = make_response(html)
    res.status_code = 200
    return res


def message() -> FrameMessage:
    # parse action message
    body = json.loads(request.data)
    msg = FrameMessage(**body)
    return msg
