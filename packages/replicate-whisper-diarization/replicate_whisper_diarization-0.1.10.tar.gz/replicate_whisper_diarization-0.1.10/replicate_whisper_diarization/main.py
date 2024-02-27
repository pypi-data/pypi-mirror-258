from replicate_whisper_diarization.whisper import transcribe
from replicate_whisper_diarization.diarization import run_diarization, run_segmentation


def extract_word_timestamps(segments: list[dict]) -> list[dict]:
    word_timestamps = []

    for segment in segments:
        for word in segment["words"]:
            word_timestamps.append(word.update({"text": word["word"]}) or word)
    return word_timestamps


def run_transcript_with_diarization(
    audio_url: str,
    whisper_model: str = "base",
    language: str | None = None,
    num_speakers: int | None = None,
    min_speakers: int | None = None,
    max_speakers: int | None = None,
    use_cache: bool = False,
) -> list[dict]:
    transcript = transcribe(
        audio_url=audio_url,
        model=whisper_model,
        language=language,
        use_cache=use_cache,
    )
    transcript_segments = transcript["segments"]
    language = transcript["detected_language"]
    word_timestamps = extract_word_timestamps(transcript_segments)
    segments = run_segmentation(
        audio_url,
        num_speakers=num_speakers,
        min_speakers=min_speakers,
        max_speakers=max_speakers,
        use_cache=use_cache,
    )
    segments = segments["output"]["segments"]
    return run_diarization(segments, word_timestamps, language)
