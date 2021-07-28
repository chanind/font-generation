from torchvision import transforms

tensorify = transforms.Compose(
    [
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.5, 0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5, 0.5)),
    ]
)


def pil_to_tensor(img):
    """Turns a PIL Glyph image into a 1-channel image"""
    return tensorify(img)[3, :, :].unsqueeze(0)
