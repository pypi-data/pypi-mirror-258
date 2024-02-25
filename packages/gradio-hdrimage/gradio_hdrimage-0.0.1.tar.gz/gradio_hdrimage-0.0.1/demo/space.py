
import gradio as gr
from app import demo as app
import os

_docs = {'HDRImage': {'description': 'Creates an image component that can be used to upload images (as an input) or display images (as an output).\n', 'members': {'__init__': {'value': {'type': 'str | np.ndarray | None', 'default': 'None', 'description': 'A PIL HDRImage, numpy array, path or URL for the default value that HDRImage component is going to take. If callable, the function will be called whenever the app loads to set the initial value of the component.'}, 'height': {'type': 'int | str | None', 'default': 'None', 'description': 'The height of the displayed image, specified in pixels if a number is passed, or in CSS units if a string is passed.'}, 'width': {'type': 'int | str | None', 'default': 'None', 'description': 'The width of the displayed image, specified in pixels if a number is passed, or in CSS units if a string is passed.'}, 'sources': {'type': 'list[Literal["upload", "clipboard"]] | None', 'default': 'None', 'description': 'List of sources for the image. "upload" creates a box where user can drop an image file, "clipboard" allows users to paste an image from the clipboard. If None, defaults to ["upload", "clipboard"].'}, 'type': {'type': 'Literal["numpy", "filepath"]', 'default': '"numpy"', 'description': 'The format the image is converted before being passed into the prediction function. "numpy" converts the image to a numpy array with shape (height, width, 3) and values from 0 to 255, "filepath" passes a str path to a temporary file containing the image.'}, 'label': {'type': 'str | None', 'default': 'None', 'description': 'The label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.'}, 'every': {'type': 'float | None', 'default': 'None', 'description': "If `value` is a callable, run the function 'every' number of seconds while the client connection is open. Has no effect otherwise. The event can be accessed (e.g. to cancel it) via this component's .load_event attribute."}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will display label.'}, 'show_download_button': {'type': 'bool', 'default': 'True', 'description': 'If True, will display button to download image.'}, 'container': {'type': 'bool', 'default': 'True', 'description': 'If True, will place the component in a container - providing some extra padding around the border.'}, 'scale': {'type': 'int | None', 'default': 'None', 'description': 'relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.'}, 'min_width': {'type': 'int', 'default': '160', 'description': 'minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.'}, 'interactive': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will allow users to upload and edit an image; if False, can only be used to display images. If not provided, this is inferred based on whether the component is used as an input or output.'}, 'visible': {'type': 'bool', 'default': 'True', 'description': 'If False, component will be hidden.'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.'}, 'show_share_button': {'type': 'bool | None', 'default': 'None', 'description': 'If True, will show a share icon in the corner of the component that allows user to share outputs to Hugging Face Spaces Discussions. If False, icon does not appear. If set to None (default behavior), then the icon appears if this Gradio app is launched on Spaces, but not otherwise.'}}, 'postprocess': {'value': {'type': 'np.ndarray | str | Path | None', 'description': 'Expects a `numpy.array`, `str`, or `pathlib.Path` filepath to an image which is displayed.'}}, 'preprocess': {'return': {'type': 'np.ndarray | str | None', 'description': 'Passes the uploaded image as a `numpy.array`, or `str` filepath depending on `type`.'}, 'value': None}}, 'events': {'clear': {'type': None, 'default': None, 'description': 'This listener is triggered when the user clears the HDRImage using the X button for the component.'}, 'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the HDRImage changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'select': {'type': None, 'default': None, 'description': 'Event listener for when the user selects or deselects the HDRImage. Uses event data gradio.SelectData to carry `value` referring to the label of the HDRImage, and `selected` to refer to state of the HDRImage. See EventData documentation on how to use this event data'}, 'upload': {'type': None, 'default': None, 'description': 'This listener is triggered when the user uploads a file into the HDRImage.'}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'HDRImage': []}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_hdrimage`

<div style="display: flex; gap: 7px;">
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.0.1%20-%20orange">  
</div>

Component to load and display HDR images
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_hdrimage
```

## Usage

```python
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

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `HDRImage`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["HDRImage"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["HDRImage"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, passes the uploaded image as a `numpy.array`, or `str` filepath depending on `type`.
- **As output:** Should return, expects a `numpy.array`, `str`, or `pathlib.Path` filepath to an image which is displayed.

 ```python
def predict(
    value: np.ndarray | str | None
) -> np.ndarray | str | Path | None:
    return value
```
""", elem_classes=["md-custom", "HDRImage-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          HDRImage: [], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()
