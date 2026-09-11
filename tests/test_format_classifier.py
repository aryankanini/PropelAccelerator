from app.intake.domain.format_classifier import DetectedFormat, FormatClassifier


def classifier() -> FormatClassifier:
    return FormatClassifier(
        {
            DetectedFormat.FORMAT_1: frozenset({"format-one"}),
            DetectedFormat.FORMAT_2: frozenset({"format-two"}),
            DetectedFormat.OPEN_SOURCE: frozenset({"open-source"}),
        }
    )


def test_classify_returns_one_supported_format_for_one_matching_marker() -> None:
    result = classifier().classify("CMS survey format-one")

    assert result.detected_format == DetectedFormat.FORMAT_1
    assert result.processing_state == "classified"


def test_classify_rejects_conflicting_format_markers() -> None:
    result = classifier().classify("format-one and format-two")

    assert result.detected_format is None
    assert result.processing_state == "classification_error"