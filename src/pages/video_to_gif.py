import taipy.gui.builder as tgb

import taipy_utilities.builder_extension as tgb_ext
from callbacks.video_to_gif_callbacks import (
    convert_to_gif_callback,
    select_video_callback,
)

with tgb.Page() as video_gif_page:
    tgb_ext.mdtext("## Video to **GIF** Converter")
    with tgb.part(class_name="main-section"):
        with tgb.part():
            tgb_ext.mdtext("### **Upload** Video:")
            tgb.file_selector(
                "{content}",
                label="Select Video",
                on_action=select_video_callback,
                extensions=".mp4,.avi",
                drop_message="Upload!",
                class_name="fullwidth",
            )
            with tgb.layout("1 1 1"):
                tgb_ext.mdtext("#### Total duration of: {video_duration} s:")
                tgb_ext.mdtext(
                    "#### Size: {file_size}",
                )
                tgb_ext.mdtext(
                    "#### Video File Name: {file_name}",
                )

        with tgb.part(render="{video_is_selected}"):
            tgb_ext.mdtext("### Select Parameters:")
            with tgb.layout("1 1 1 1"):
                tgb.number("{start_time}", label="Start time", min=0, max=60)
                tgb.number("{duration}", label="Clip Duration", min=1, max=60)
                tgb.number(
                    "{resize_factor}", label="Resize Factor", min=0.1, max=1.0, step=0.1
                )
                with tgb.layout("1 1"):
                    tgb_ext.mdtext("#### FPS: ")
                    tgb.slider("{fps}", lov=[5, 7, 10, 15, 20, 25, 30, 35])
            tgb_ext.fullwidth_button(
                label="Convert to GIF!",
                on_action=convert_to_gif_callback,
            )

        with tgb.part(render="{gif_is_ready}"):
            tgb_ext.mdtext("### Convert to GIF:")
            with tgb.part(class_name="image-output"):
                tgb.image("{content_download}", height="200px", class_name="gif-output")
            tgb.file_download(
                "{content_download}",
                label="Download File",
                active="{gif_is_ready}",
                class_name="fullwidth",
            )
