import os
import asyncio
import json
import logging
from helper.utils import metadata_text

logger = logging.getLogger(__name__)


async def change_metadata(input_file, output_file, metadata):
    """
    ✅ Fully async FFmpeg metadata change.
    Uses asyncio.create_subprocess_exec() so the bot NEVER freezes.
    """
    author, title, video_title, audio_title, subtitle_title = await metadata_text(metadata)
    
    # ✅ Async ffprobe — get video metadata without blocking
    try:
        probe_process = await asyncio.create_subprocess_exec(
            'ffprobe', '-v', 'error', '-show_streams', '-print_format', 'json', input_file,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await asyncio.wait_for(probe_process.communicate(), timeout=60)
        
        if probe_process.returncode != 0:
            logger.error(f"ffprobe error: {stderr.decode()}")
            return False
            
        data = json.loads(stdout.decode())
        streams = data.get('streams', [])
    except asyncio.TimeoutError:
        logger.error(f"ffprobe timed out for: {input_file}")
        return False
    except Exception as e:
        logger.error(f"ffprobe failed: {e}")
        return False

    # Build FFmpeg command
    cmd = [
        'ffmpeg', '-y',
        '-i', input_file,
        '-map', '0',
        '-c:v', 'copy',
        '-c:a', 'copy',
        '-c:s', 'copy',
    ]
    
    if title:
        cmd.extend(['-metadata', f'title={title}'])
    if author:
        cmd.extend(['-metadata', f'author={author}'])

    # Add per-stream metadata
    for stream in streams:
        stream_index = stream.get("index", 0)
        codec_type = stream.get('codec_type', '')
        
        if codec_type == 'video' and video_title:
            cmd.extend([f'-metadata:s:{stream_index}', f'title={video_title}'])
        elif codec_type == 'audio' and audio_title:
            cmd.extend([f'-metadata:s:{stream_index}', f'title={audio_title}'])
        elif codec_type == 'subtitle' and subtitle_title:
            cmd.extend([f'-metadata:s:{stream_index}', f'title={subtitle_title}'])

    cmd.extend(['-metadata', 'comment=Added by @SenpaiLabs'])
    cmd.extend(['-f', 'matroska'])
    cmd.append(output_file)
    
    logger.info(f"FFmpeg cmd: {' '.join(cmd)}")
    
    # ✅ Async FFmpeg execution — bot stays responsive
    try:
        ffmpeg_process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await asyncio.wait_for(
            ffmpeg_process.communicate(), 
            timeout=600  # 10 min max per file
        )
        
        if ffmpeg_process.returncode != 0:
            logger.error(f"FFmpeg error: {stderr.decode()}")
            return False
            
        return True
        
    except asyncio.TimeoutError:
        logger.error(f"FFmpeg timed out (10min) for: {input_file}")
        try:
            ffmpeg_process.kill()
        except Exception:
            pass
        return False
    except Exception as e:
        logger.error(f"FFmpeg failed: {e}")
        return False
