import io
from typing import Tuple

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from PIL import Image, ImageEnhance


app = FastAPI(title="Virtual Try-On Engine", version="0.1.0")


@app.get("/health")
def health():
    return {"ok": True}


def _open_image(file_bytes: bytes) -> Image.Image:
    im = Image.open(io.BytesIO(file_bytes))
    # Always work in RGBA to support transparency in dress images (PNG).
    return im.convert("RGBA")


def _fit_dress_to_person(person_size: Tuple[int, int], dress: Image.Image) -> Tuple[Image.Image, Tuple[int, int]]:
    """
    MVP placement heuristic:
    - scale dress to ~65% of person's width
    - place at ~22% from top (approx shoulder/chest area)
    """
    pw, ph = person_size
    target_w = int(pw * 0.65)
    # preserve aspect ratio
    scale = target_w / max(1, dress.width)
    target_h = int(dress.height * scale)

    dress_resized = dress.resize((target_w, target_h), resample=Image.Resampling.LANCZOS)

    x = (pw - target_w) // 2
    y = int(ph * 0.22)
    return dress_resized, (x, y)


def _make_alpha(dress_rgba: Image.Image) -> Image.Image:
    """
    If the dress already has alpha, use it.
    Otherwise create a soft alpha from brightness to reduce harsh edges.
    """
    r, g, b, a = dress_rgba.split()
    if a.getextrema() != (255, 255):
        # has some transparency already
        return a

    # Create alpha based on luminance: treat near-white background as transparent-ish.
    gray = dress_rgba.convert("L")
    # Invert so bright areas become low alpha.
    inv = Image.eval(gray, lambda px: 255 - px)
    alpha = ImageEnhance.Contrast(inv).enhance(1.7)
    alpha = ImageEnhance.Brightness(alpha).enhance(1.15)
    return alpha


def tryon_compose(person_rgba: Image.Image, dress_rgba: Image.Image) -> Image.Image:
    base = person_rgba.copy()

    dress_resized, (x, y) = _fit_dress_to_person(base.size, dress_rgba)
    alpha = _make_alpha(dress_resized)

    # Slightly reduce opacity for more natural blending on photos.
    alpha = ImageEnhance.Brightness(alpha).enhance(0.82)

    # Composite: paste dress onto person using alpha mask.
    base.paste(dress_resized, (x, y), mask=alpha)
    return base


@app.post("/tryon")
async def tryon(person_image: UploadFile = File(...), dress_image: UploadFile = File(...)):
    person_bytes = await person_image.read()
    dress_bytes = await dress_image.read()

    person = _open_image(person_bytes)
    dress = _open_image(dress_bytes)

    out = tryon_compose(person, dress)
    buf = io.BytesIO()
    out.save(buf, format="PNG")
    return Response(content=buf.getvalue(), media_type="image/png")

