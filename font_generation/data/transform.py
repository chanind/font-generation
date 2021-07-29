import numpy as np
import albumentations as A
from albumentations.pytorch.transforms import ToTensorV2

BASE_TRANSFORMS = [
    A.Normalize(
        mean=[0.5],
        std=[0.5],
    ),
    ToTensorV2(p=1.0),
]

base_transform = A.Compose(
    BASE_TRANSFORMS,
    p=1.0,
)


def pil_to_norm_tensor(img):
    """Turn a PIL Glyph image into a 1-chennal normalized tensor"""
    return base_transform(image=pil_to_numpy(img))["image"]


def pil_to_numpy(img):
    """Turns a PIL Glyph image into a 1-channel numpy array"""
    return np.expand_dims(np.asarray(img)[:, :, 3], axis=-1)
