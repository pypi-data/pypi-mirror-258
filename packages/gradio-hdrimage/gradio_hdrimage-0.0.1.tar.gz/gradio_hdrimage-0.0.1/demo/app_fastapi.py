import sys
import os
os.environ["OPENCV_IO_ENABLE_OPENEXR"]="1"

import gradio as gr
from gradio_hdrimage import HDRImage
from fastapi import FastAPI
import uvicorn


example = HDRImage().example_inputs()

demo = gr.Interface(
    lambda x:x,
    HDRImage(),  # interactive version of your component
    HDRImage(),  # static version of your component
    # examples=[[example]],  # uncomment this line to view the "example version" of your component
)


if __name__ == "__main__":
    demo = demo.queue()
    app = FastAPI()
    app = gr.mount_gradio_app(app, demo, path='/diffhandles')
    try:
        uvicorn.run(app, host="0.0.0.0", port=6006)
    except KeyboardInterrupt:
        sys.exit()

