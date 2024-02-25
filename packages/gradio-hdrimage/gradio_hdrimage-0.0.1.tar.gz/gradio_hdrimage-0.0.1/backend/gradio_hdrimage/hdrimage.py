"""gr.Image() component."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal, cast
from io import BytesIO

import numpy as np
import imageio
from gradio_client.documentation import document

from gradio import utils, processing_utils
from gradio.components.base import Component
from gradio.data_classes import FileData
from gradio.events import Events

# PIL.Image.init()  # fixes https://github.com/gradio-app/gradio/issues/2843


class HDRImage(Component):
    """
    Creates an image component that can be used to upload images (as an input) or display images (as an output).

    Demos: image_mod, image_mod_default_image
    Guides: image-classification-in-pytorch, image-classification-in-tensorflow, image-classification-with-vision-transformers, create-your-own-friends-with-a-gan
    """

    EVENTS = [
        Events.clear,
        Events.change,
        Events.select,
        Events.upload,
    ]

    data_model = FileData

    def __init__(
        self,
        value: str | np.ndarray | None = None,
        *,
        height: int | str | None = None,
        width: int | str | None = None,
        sources: list[Literal["upload", "clipboard"]] | None = None,
        type: Literal["numpy", "filepath"] = "numpy",
        label: str | None = None,
        every: float | None = None,
        show_label: bool | None = None,
        show_download_button: bool = True,
        container: bool = True,
        scale: int | None = None,
        min_width: int = 160,
        interactive: bool | None = None,
        visible: bool = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        show_share_button: bool | None = None,
    ):
        """
        Parameters:
            value: A PIL HDRImage, numpy array, path or URL for the default value that HDRImage component is going to take. If callable, the function will be called whenever the app loads to set the initial value of the component.
            height: The height of the displayed image, specified in pixels if a number is passed, or in CSS units if a string is passed.
            width: The width of the displayed image, specified in pixels if a number is passed, or in CSS units if a string is passed.
            image_mode: "RGB" if color, or "L" if black and white. See https://pillow.readthedocs.io/en/stable/handbook/concepts.html for other supported image modes and their meaning.
            sources: List of sources for the image. "upload" creates a box where user can drop an image file, "clipboard" allows users to paste an image from the clipboard. If None, defaults to ["upload", "clipboard"].
            type: The format the image is converted before being passed into the prediction function. "numpy" converts the image to a numpy array with shape (height, width, 3) and values from 0 to 255, "filepath" passes a str path to a temporary file containing the image.
            label: The label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.
            every: If `value` is a callable, run the function 'every' number of seconds while the client connection is open. Has no effect otherwise. The event can be accessed (e.g. to cancel it) via this component's .load_event attribute.
            show_label: if True, will display label.
            show_download_button: If True, will display button to download image.
            container: If True, will place the component in a container - providing some extra padding around the border.
            scale: relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.
            min_width: minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.
            interactive: if True, will allow users to upload and edit an image; if False, can only be used to display images. If not provided, this is inferred based on whether the component is used as an input or output.
            visible: If False, component will be hidden.
            elem_id: An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.
            elem_classes: An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.
            render: If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.
            show_share_button: If True, will show a share icon in the corner of the component that allows user to share outputs to Hugging Face Spaces Discussions. If False, icon does not appear. If set to None (default behavior), then the icon appears if this Gradio app is launched on Spaces, but not otherwise.
        """
        valid_types = ["numpy", "filepath"]
        if type not in valid_types:
            raise ValueError(
                f"Invalid value for parameter `type`: {type}. Please choose from one of: {valid_types}"
            )
        self.type = type
        self.height = height
        self.width = width
        valid_sources = ["upload", "clipboard"]
        if sources is None:
            self.sources =  ["upload", "clipboard"]
        elif isinstance(sources, str):
            self.sources = [sources]  # type: ignore
        else:
            self.sources = sources
        for source in self.sources:  # type: ignore
            if source not in valid_sources:
                raise ValueError(
                    f"`sources` must a list consisting of elements in {valid_sources}"
                )
        self.show_download_button = show_download_button
        self.show_share_button = (
            (utils.get_space() is not None)
            if show_share_button is None
            else show_share_button
        )
        super().__init__(
            label=label,
            every=every,
            show_label=show_label,
            container=container,
            scale=scale,
            min_width=min_width,
            interactive=interactive,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            render=render,
            value=value,
        )

    def preprocess(
        self, payload: FileData | None
    ) -> np.ndarray | str | None:
        """
        Parameters:
            payload: image data in the form of a FileData object
        Returns:
            Passes the uploaded image as a `numpy.array`, or `str` filepath depending on `type`.
        """
        if payload is None:
            return payload
        file_path = Path(payload.path)
        if payload.orig_name:
            p = Path(payload.orig_name)
            name = p.stem
            # suffix = p.suffix.replace(".", "")
            # if suffix in ["jpg", "jpeg"]:
            #     suffix = "jpeg"
        else:
            name = "image"
            # suffix = "exr"
            # suffix = file_path.splitext()[1].replace(".", "")

        im = imageio.imread(file_path)
        if im.dtype == np.uint8:
            im = im.astype(np.float32) / 255.0
        # im = im.astype(np.float32)

        print(im.shape)
        print(im.dtype)

        if self.type == "numpy":
            return im
        elif self.type == "filepath":
            im_bytes = encode_image_to_bytes(im, format="exr")
            path = processing_utils.save_bytes_to_cache(im_bytes, file_name=f"{name}.exr", cache_dir=self.GRADIO_CACHE)
            return path
        else:
            raise ValueError(
                "Unknown type: "
                + str(type)
                + ". Please choose from: 'numpy', 'filepath'."
            )

    def postprocess(
        self, value: np.ndarray | str | Path | None
    ) -> FileData | None:
        """
        Parameters:
            value: Expects a `numpy.array`, `str`, or `pathlib.Path` filepath to an image which is displayed.
        Returns:
            Returns the image as a `FileData` object.
        """
        if value is None:
            return None

        if isinstance(value, np.ndarray):
            im_bytes = encode_image_to_bytes(value, format="exr")
            path = processing_utils.save_bytes_to_cache(im_bytes, file_name=f"image.exr", cache_dir=self.GRADIO_CACHE)
        elif isinstance(value, Path):
            path = str(value)
        elif isinstance(value, str):
            path = value
        else:
            raise ValueError(
                "Cannot process this value as an Image, it is of type: " + str(type(value))
            )

        orig_name = Path(path).name if Path(path).exists() else None
        return FileData(path=path, orig_name=orig_name)

    def example_inputs(self) -> Any:
        return "https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png"


def encode_image_to_bytes(image, format="exr"):
    with BytesIO() as output_bytes:
        imageio.imwrite(output_bytes, image, format=format)
        return output_bytes.getvalue()
