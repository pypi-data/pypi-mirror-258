import os
os.environ["OPENCV_IO_ENABLE_OPENEXR"]="1"

import gradio as gr
from gradio_hdrimage import HDRImage


example = HDRImage().example_inputs()

demo = gr.Interface(
    lambda x:x,
    HDRImage(),  # interactive version of your component
    HDRImage(),  # static version of your component
    # examples=[[example]],  # uncomment this line to view the "example version" of your component
)


if __name__ == "__main__":
    demo.launch()
