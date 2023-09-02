import logging

from PIL import Image, ImageOps

from ...appconfig import CollageStageConfig
from ...utils.exceptions import PipelineError
from .pipelinestages_utils import get_user_file, rotate

logger = logging.getLogger(__name__)


def merge_collage_stage(
    captured_images: list[Image.Image],
    collage_merge_definition: list[CollageStageConfig],
) -> Image.Image:
    """ """

    target_image_size = (1500, 1000)  # TODO: need to find out how to handle this.
    total_images_in_collage = len(collage_merge_definition)

    collage_images: list[Image.Image] = []
    for _definition in collage_merge_definition:
        if _definition.predefined_image:
            try:
                collage_images.append(Image.open(get_user_file(_definition.predefined_image)))
            except FileNotFoundError as exc:
                raise PipelineError(f"error getting predefined file {exc}") from exc
        else:
            collage_images.append(captured_images.pop(0))

    if len(collage_images) != total_images_in_collage:
        raise PipelineError("collage images no not equal to total_images_in_collage requested!")

    new_image = Image.new("RGBA", target_image_size, color=None)

    for index, _definition in enumerate(collage_merge_definition):
        logger.debug(_definition)
        _image = collage_images[index]
        _image = ImageOps.fit(
            _image,
            (_definition.width, _definition.height),
            method=Image.Resampling.LANCZOS,
        )  # or contain?
        _image, offset_x, offset_y = rotate(_image, _definition.rotate)

        new_image.paste(_image, (_definition.pos_x - offset_x, _definition.pos_y - offset_y))

    return new_image
