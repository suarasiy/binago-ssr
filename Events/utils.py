from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List

from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image
from io import BytesIO


def list_no_whitespace(n) -> List:
    return [x.strip() for x in n if x.strip()]


def compress_image(request_image) -> InMemoryUploadedFile:
    with Image.open(request_image) as image:
        image = image.convert('RGB')
        bytes_io = BytesIO()
        image.save(bytes_io, format='JPEG', quality=3)

        image_compressed = InMemoryUploadedFile(
            bytes_io, None, 'compressed.jpeg', 'image/jpeg', bytes_io.tell(), None
        )

    return image_compressed
