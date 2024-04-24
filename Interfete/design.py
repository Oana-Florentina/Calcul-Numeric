from __future__ import annotations
from typing import Iterable
from gradio.themes.base import Base
from gradio.themes.utils import colors, fonts, sizes


class PurpleTriangle(Base):
    def __init__(
            self,
            *,
            primary_hue: colors.Color | str = colors.purple,
            secondary_hue: colors.Color | str = colors.violet,
            neutral_hue: colors.Color | str = colors.violet,
            spacing_size: sizes.Size | str = sizes.spacing_md,
            radius_size: sizes.Size | str = sizes.radius_md,
            text_size: sizes.Size | str = sizes.text_lg,
            font: fonts.Font
                  | str
                  | Iterable[fonts.Font | str] = (
                    fonts.GoogleFont("Quicksand"),
                    "ui-sans-serif",
                    "sans-serif",
            ),
            font_mono: fonts.Font
                       | str
                       | Iterable[fonts.Font | str] = (
                    fonts.GoogleFont("IBM Plex Mono"),
                    "ui-monospace",
                    "monospace",
            ),
    ):
        super().__init__(
            primary_hue=primary_hue,
            secondary_hue=secondary_hue,
            neutral_hue=neutral_hue,
            spacing_size=spacing_size,
            radius_size=radius_size,
            text_size=text_size,
            font=font,
            font_mono=font_mono,
        )
        super().set(
            body_background_fill="""
                radial-gradient(circle at 10% 20%, *primary_200 0%, transparent 5%),
                radial-gradient(circle at 30% 40%, *primary_300 0%, transparent 5%),
                radial-gradient(circle at 50% 60%, *primary_400 0%, transparent 5%),
                radial-gradient(circle at 70% 80%, *primary_500 0%, transparent 5%),
                radial-gradient(circle at 90% 90%, *primary_600 0%, transparent 5%)
            """,
            body_background_fill_dark="""
                radial-gradient(circle at 10% 20%, *primary_800 0%, transparent 5%),
                radial-gradient(circle at 30% 40%, *primary_700 0%, transparent 5%),
                radial-gradient(circle at 50% 60%, *primary_600 0%, transparent 5%),
                radial-gradient(circle at 70% 80%, *primary_500 0%, transparent 5%),
                radial-gradient(circle at 90% 90%, *primary_400 0%, transparent 5%)
            """,
            button_primary_background_fill="linear-gradient(90deg, *primary_300, *secondary_400)",
            button_primary_background_fill_hover="linear-gradient(90deg, *primary_200, *secondary_300)",
            button_primary_text_color="white",
            button_primary_background_fill_dark="linear-gradient(90deg, *primary_600, *secondary_800)",
            slider_color="*secondary_300",
            slider_color_dark="*secondary_600",
            block_title_text_weight="600",
            block_border_width="3px",
            block_shadow="*shadow_drop_lg",
            button_shadow="*shadow_drop_lg",
            button_large_padding="32px",
        )

purple_triangle = PurpleTriangle()