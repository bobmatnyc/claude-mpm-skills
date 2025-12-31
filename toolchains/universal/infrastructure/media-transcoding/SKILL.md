---
name: media-transcoding
description: FFmpeg-based media transcoding workflows with preset-driven conversions, batch processing, and safe backups for web/mobile/archive outputs.
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Use FFmpeg presets to convert videos for web/mobile/archive with batch scripts, backups, and faststart MP4s."
    when_to_use: "Optimizing video files for web delivery, compressing large media libraries, or standardizing outputs with repeatable presets."
    quick_start: "1. Run ./ffmpeg_convert.sh check 2. Convert one file with web_standard 3. Batch convert with batch_web_standard"
tags:
  - ffmpeg
  - media
  - video
  - transcoding
  - encoding
---

# Media Transcoding (FFmpeg)

## Overview

Use FFmpeg presets to normalize video outputs for web streaming, mobile delivery, or archival quality. Your `hf-videos` repo already includes a simple bash script and a more advanced Python script with presets, backups, and logging.

## Quick Start (hf-videos)

```bash
./ffmpeg_convert.sh check
./ffmpeg_convert.sh web_standard "My Video.mp4"
./ffmpeg_convert.sh batch_web_standard
```

Outputs are written to `converted/` with backups in `backup/` and logs in `conversion.log`.

## Preset Summary (hf-videos)

- **web_standard**: 1080p max, CRF 23, 128k audio, `+faststart`
- **web_high**: 1080p max, CRF 20, 192k audio
- **mobile**: 720p max, CRF 25, 96k audio
- **ultra_compact**: 480p max, CRF 28, 64k audio
- **archive**: original res, CRF 18, 256k audio

All presets use H.264 + AAC with `+faststart` for streaming-friendly MP4s.

## Batch Workflow

1. Run a single-file conversion first to validate output.
2. Run batch conversion once the preset is confirmed.
3. Verify output sizes and playback.

Batch commands:

```bash
./ffmpeg_convert.sh batch_web_standard
./ffmpeg_convert.sh batch_mobile
./ffmpeg_convert.sh batch_ultra_compact
```

## Advanced Script (convert_video.py)

Use `convert_video.py` when you need:

- Progress monitoring
- Metadata inspection
- Overwrite control
- Preset listing and batch automation

```bash
python3 convert_video.py --list-presets
python3 convert_video.py --file "My Video.mp4" --preset web_standard
python3 convert_video.py --preset mobile --overwrite
```

## Output Conventions

- Converted files use suffixes like `_web_standard`.
- Backups preserve original filenames.
- Logs go to `conversion.log` for audit and troubleshooting.

## Troubleshooting

- **FFmpeg missing**: `brew install ffmpeg` (macOS) or install from ffmpeg.org.
- **Permission errors**: `chmod +x ffmpeg_convert.sh`.
- **Disk pressure**: clean `converted/` and `backup/` after validation.

## Related Skills

- `toolchains/universal/infrastructure/docker`
