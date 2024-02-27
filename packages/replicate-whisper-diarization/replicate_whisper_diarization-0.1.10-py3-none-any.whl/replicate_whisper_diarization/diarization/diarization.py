import os
import time

import replicate

from replicate_whisper_diarization.logger import get_logger
from replicate_whisper_diarization.utils.cache import (
    set_to_cache,
    get_cache_key,
    get_from_cache,
)
from replicate_whisper_diarization.diarization.utils import (
    language_mapping,
    convert_to_miliseconds,
    get_words_speaker_mapping,
    get_sentences_speaker_mapping,
)

logger = get_logger(__name__)

MODEL_NAME = os.getenv(
    "DIARIZATION_MODEL_NAME",
    "collectiveai-team/speaker-diarization-3",
)
MODEL_VERSION = os.getenv(
    "DIARIZATION_MODEL_VERSION",
    "6e29843b8c1b751ec384ad96d3566af2392046465152fef3cc22ad701090b64c",
)


def parse_diarization_segments(segments: list[dict]) -> list:
    speaker_ts = []
    for segment in segments:
        speaker_ts.append(
            [
                convert_to_miliseconds(segment["start"]),
                convert_to_miliseconds(segment["stop"]),
                segment["speaker"],
            ]
        )
    return speaker_ts


def run_segmentation(
    audio_url: str,
    webhook_url: str | None = None,
    replicate_model_name: str | None = None,
    replicate_model_version: str | None = None,
    num_speakers: int | None = None,
    min_speakers: int | None = None,
    max_speakers: int | None = None,
    use_cache: bool = False,
) -> dict:
    """
    Run diarization on audio file

    Args:
        audio_url (str): url of audio file
        webhook_url (str, optional): url to send webhook. Defaults to None.
        replicate_model_name (str, optional): name of model. Defaults to None.
        replicate_model_version (str, optional): version of model. Defaults to None.
        num_speakers (int, optional): number of speakers. Defaults to None.
        min_speakers (int, optional): minimum number of speakers. Defaults to None.
        max_speakers (int, optional): maximum number of speakers. Defaults to None.
        use_cache (bool, optional): use cache. Defaults to False.

    """

    model_name = replicate_model_name or MODEL_NAME
    model_version = replicate_model_version or MODEL_VERSION
    model = replicate.models.get(model_name)
    version = model.versions.get(model_version)

    replicate_input = {
        "audio": audio_url,
        "num_speakers": num_speakers,
        "min_speakers": min_speakers,
        "max_speakers": max_speakers,
    }

    # remove None values
    replicate_input = {k: v for k, v in replicate_input.items() if v is not None}

    if use_cache:
        cache_key = get_cache_key("segmentation", **replicate_input)
        cached_output = get_from_cache(cache_key)
        if cached_output:
            logger.info(f"loading from cache ({cache_key})")
            return cached_output

    if webhook_url:
        prediction = replicate.predictions.create(
            version=version,
            input=replicate_input,
            webhook=webhook_url,
        )
    else:
        prediction = replicate.predictions.create(
            version=version,
            input=replicate_input,
        )

    while prediction.status not in ["failed", "succeeded"] and not webhook_url:
        time.sleep(5)
        prediction.reload()
    if prediction.status == "failed":
        logger.error("Diarization failed")

    output = prediction.__dict__
    if use_cache and prediction.status == "succeeded":
        # save prediction to cache
        set_to_cache(cache_key, output)

    return output


def run_diarization(
    segments: list[dict],
    word_timestamps: list[dict[str, float]],
    language: str,
    use_cache: bool = False,
):
    if use_cache:
        cache_key = get_cache_key("diarization", segments, word_timestamps, language)
        cached_output = get_from_cache(cache_key)
        if cached_output:
            logger.info(f"loading from cache ({cache_key})")
            return cached_output

    language = language_mapping.get(language, "en")
    segments = parse_diarization_segments(segments)
    wsm = get_words_speaker_mapping(word_timestamps, segments, "start")
    ssm = get_sentences_speaker_mapping(wsm, segments)

    if use_cache:
        set_to_cache(cache_key, ssm)
    return ssm
