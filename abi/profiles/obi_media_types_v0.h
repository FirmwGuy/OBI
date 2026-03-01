/* SPDX-License-Identifier: CC-BY-SA-4.0 */
/* SPDX-FileCopyrightText: © 2026–present Victor M. Barrientos <firmw.guy@gmail.com> */

#ifndef OBI_MEDIA_TYPES_V0_H
#define OBI_MEDIA_TYPES_V0_H

#include "../obi_core_v0.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef enum obi_color_space_v0 {
    OBI_COLOR_SPACE_UNKNOWN = 0,
    OBI_COLOR_SPACE_SRGB    = 1,
    OBI_COLOR_SPACE_LINEAR  = 2,
} obi_color_space_v0;

typedef enum obi_alpha_mode_v0 {
    OBI_ALPHA_UNKNOWN        = 0,
    OBI_ALPHA_STRAIGHT       = 1,
    OBI_ALPHA_PREMULTIPLIED  = 2,
    OBI_ALPHA_OPAQUE         = 3,
} obi_alpha_mode_v0;

typedef enum obi_pixel_format_v0 {
    OBI_PIXEL_FORMAT_RGBA8 = 0,
    OBI_PIXEL_FORMAT_BGRA8 = 1,
    OBI_PIXEL_FORMAT_RGB8  = 2,
    OBI_PIXEL_FORMAT_A8    = 3,
} obi_pixel_format_v0;

typedef enum obi_audio_sample_format_v0 {
    OBI_AUDIO_SAMPLE_S16 = 0,
    OBI_AUDIO_SAMPLE_F32 = 1,
} obi_audio_sample_format_v0;

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif /* OBI_MEDIA_TYPES_V0_H */

