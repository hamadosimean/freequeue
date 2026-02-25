from django.core.exceptions import ValidationError
from .constants import (
    MAX_FILE_SIZE_MB,
    ALLOWED_IMAGE_EXTENSIONS,
    ALLOWED_VIDEO_EXTENSIONS,
    ALLOWED_PDF_EXTENSIONS,
)


def validate_file_size(value):
    """Valide que la taille du fichier ne dépasse pas 5 Mo"""
    max_size = MAX_FILE_SIZE_MB * 1024 * 1024
    if value.size > max_size:
        raise ValidationError(f"Le fichier ne doit pas dépasser {MAX_FILE_SIZE_MB} Mo.")


def video_validator(video):
    allowed_extensions = ALLOWED_VIDEO_EXTENSIONS
    ext = video.name.rsplit(".", 1)[-1].lower()
    if ext not in allowed_extensions:
        raise ValidationError(
            "Seules les vidéos " + " ".join(allowed_extensions) + " sont autorisées."
        )
    validate_file_size(video)


def image_validator(image):
    allowed_extensions = ALLOWED_IMAGE_EXTENSIONS
    ext = image.name.rsplit(".", 1)[-1].lower()
    if ext not in allowed_extensions:
        raise ValidationError(
            "Seules les images " + " ".join(allowed_extensions) + " sont autorisées."
        )
    validate_file_size(image)


def pdf_validator(pdf):
    allowed_extensions = ALLOWED_PDF_EXTENSIONS
    ext = pdf.name.rsplit(".", 1)[-1].lower()
    if ext not in allowed_extensions:
        raise ValidationError(
            "Seules les PDF " + " ".join(allowed_extensions) + " sont autorisées."
        )
    validate_file_size(pdf)
