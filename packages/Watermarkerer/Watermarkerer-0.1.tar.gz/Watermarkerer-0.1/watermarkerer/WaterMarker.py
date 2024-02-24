import os
import typing
from concurrent.futures import ProcessPoolExecutor

from PIL import Image

import moviepy.editor as mp


WATERMARK_IMG: str = "assets/wm.png"

PADDING: int = 5

ALLOWED_EXT = ['jpg', 'jpeg', 'png', 'mp4']


class WaterMarker:
    def __init__(
            self,
            obj: str,
            output: str,
            position: typing.Literal["bottom_right", "bottom_right", "top_left", "top_right"] = "bottom_right"
    ):
        """
        Put watermark on file

        :param obj: file to be watermarked
        :param output: output file with watermark
        :param position: position of watermark spawn
        """
        # validations
        if not os.path.isfile(obj):
            raise FileNotFoundError("obj path is invalid")

        if not any([obj.endswith(ext) for ext in ALLOWED_EXT]):
            raise Exception("This extension of obj is not allowed")

        if not any([output.endswith(ext) for ext in ALLOWED_EXT]):
            raise Exception("This extension of output is not allowed")

        obj_ext = obj.split(".")[1]
        output_ext = output.split(".")[1]

        # type of processing
        self.processing_type: str = "video" if obj_ext == "mp4" else "image"

        if obj_ext in ALLOWED_EXT[:3]:
            if output_ext not in ALLOWED_EXT[:3]:
                raise Exception("Extension of output differ from obj extension")

        if obj_ext == "mp4" and output_ext != "mp4":
            raise Exception("Extension of output differ from obj extension")

        self.obj = obj
        self.output = output

        if self.processing_type == "image":
            self.watermark: Image = Image.open(WATERMARK_IMG)
            self.target: Image = Image.open(obj)

            # convert image to support opacity
            self.watermark.convert("RGBA")
        else:
            self.target = mp.VideoFileClip(obj)

            self.watermark = (mp.ImageClip(WATERMARK_IMG)
                                .set_duration(self.target.duration)
                                .set_position(
                                    (position.split("_")[1], position.split("_")[0])
                                ))

        # position of wm spawning in text form
        self.position = position

        if isinstance(self.target, Image.Image):
            self.target_width = self.target.width
            self.target_height = self.target.height

            self.watermark_width = self.watermark.width
            self.watermark_height = self.watermark.height

        else:
            self.target_width = self.target.w
            self.target_height = self.target.h

            self.watermark_width = self.watermark.w
            self.watermark_height = self.watermark.h

        # available places to spawn
        self.positions: dict = {
            "top_left": (PADDING, PADDING),
            "top_right": (self.target_width - self.watermark_width - PADDING, PADDING),
            "bottom_right": (
                self.target_width - self.watermark_width - PADDING,
                self.target_height - self.watermark_height - PADDING
            ),
            "bottom_left": (PADDING, self.target_height - self.watermark_height - PADDING)
        }

    def put(self) -> str:
        """
        Put watermark on the image or video (obj)

        :return: str path of result file
        """
        # image processing
        if self.processing_type == "image":
            self.watermark.thumbnail((int(self.target_width * 0.2), int(self.target_height * 0.2)))

            self.target.paste(self.watermark, self.positions[self.position], mask=self.watermark)

            self.target.save(self.output)

        # video processing
        elif self.processing_type == "video":

            final = mp.CompositeVideoClip([self.target, self.watermark])
            final.write_videofile(self.output, logger=None)

        else:
            raise Exception

        return self.output

    def process(self):
        # self.put()
        with ProcessPoolExecutor() as executor:
            return executor.submit(self.put).result()