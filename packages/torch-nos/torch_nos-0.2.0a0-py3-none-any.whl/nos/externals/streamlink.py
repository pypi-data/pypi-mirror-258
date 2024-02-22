import subprocess
import threading

import ffmpeg
import streamlink


def open_audio_stream(stream: str, preferred_quality: str = None, sample_rate: int = 16000):
    """Open the streamlink stream as an ffmpeg stdout process.

    Args:
        stream (str): The streamlink stream name.
        preferred_quality (str): The streamlink preferred quality.
    """
    stream_options = streamlink.streams(stream)
    if not stream_options:
        raise Exception(f"No playable streams found on this URL: {stream}")

    # Select the stream quality
    option = None
    for quality in [preferred_quality, "audio_only", "audio_mp4a", "audio_opus", "best"]:
        if quality in stream_options:
            option = quality
            break
    if option is None:
        try:
            option = next(iter(stream_options.values()))
        except StopIteration:
            raise Exception(f"No playable streams found on this URL: {stream}")

    # Setup the writer to read from the streamlink stdout and write
    # to the ffmpeg stdin.
    def _writer(streamlink_proc, ffmpeg_proc, chunk_size: int = 1024):
        """Write the streamlink stdout to the ffmpeg stdin."""
        while (not streamlink_proc.poll()) and (not ffmpeg_proc.poll()):
            try:
                chunk = streamlink_proc.stdout.read(chunk_size)
                ffmpeg_proc.stdin.write(chunk)
            except (BrokenPipeError, OSError):
                pass

    cmd = ["streamlink", stream, option, "-O"]
    streamlink_process = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    # Open the ffmpeg process and pipe audio from streamlink to ffmpeg with pcm encoding
    try:
        streamlink_input = ffmpeg.input("pipe:", loglevel="panic")
        ffmpeg_process = streamlink_input.output(
            "pipe:", format="s16le", acodec="pcm_s16le", ac=1, ar=sample_rate
        ).run_async(pipe_stdin=True, pipe_stdout=True)
    except ffmpeg.Error as e:
        raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

    # Keep the audio stream and ffmpeg processes alive
    thread = threading.Thread(target=_writer, args=(streamlink_process, ffmpeg_process))
    thread.start()
    return ffmpeg_process, streamlink_process
