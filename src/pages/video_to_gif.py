from algorithms.video_to_gif_state_functions import convert_to_gif, select_video

import taipy.gui.builder as tgb

with tgb.Page() as video_gif_page:
    tgb.text("## Video to **Gif** Converter", mode="md")
    with tgb.part(class_name="main-section"):
        with tgb.part():
            tgb.text("### **Upload** Video:", mode="md")
            tgb.file_selector(
                "{content}",
                label="Select Video",
                on_action=select_video,
                extensions=".mp4,.avi",
                drop_message="Drop Message",
                class_name="fullwidth",
            )
            with tgb.layout("1 1 1"):
                tgb.text("#### Total duration of: {video_duration} s:", mode="md")
                tgb.text(
                    "#### Size: {file_size}",
                    mode="md",
                )
                tgb.text(
                    "#### Video File Name: {file_name}",
                    mode="md",
                )

        with tgb.part(render="{video_is_selected}"):
            tgb.text("### Select Parameters:", mode="md")
            with tgb.layout("1 1 1 1"):
                tgb.number("{start_time}", label="Start time", min=0, max=60)
                tgb.number("{duration}", label="Clip Duration", min=1, max=60)
                tgb.number(
                    "{resize_factor}", label="Resize Factor", min=0.1, max=1.0, step=0.1
                )
                with tgb.layout("1 1"):
                    tgb.text("#### FPS: ", mode="md")
                    tgb.slider("{fps}", lov=[5, 7, 10, 15, 20, 25, 30, 35])
            tgb.button(
                label="Convert to GIF!",
                on_action=convert_to_gif,
                class_name="fullwidth plain",
            )

        with tgb.part(render="{gif_is_ready}"):
            tgb.text("### Convert to GIF:", mode="md")
            with tgb.part(class_name="gif-output"):
                tgb.image("{content_download}", height="200px", class_name="gif-output")
            tgb.file_download(
                "{content_download}",
                label="Download File",
                active="{gif_is_ready}",
                class_name="fullwidth",
            )
