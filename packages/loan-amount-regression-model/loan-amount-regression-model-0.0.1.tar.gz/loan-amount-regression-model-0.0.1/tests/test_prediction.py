import numpy as np

from regression.predict import make_prediction


def test_make_prediction(sample_input_data):
    # Given
    expected_first_prediction_value = 115.75994497049246
    expected_no_predictions = 338

    # When
    result = make_prediction(input_data=sample_input_data)

    # Then
    predictions = result.get("predictions")
    assert isinstance(predictions, list)
    assert isinstance(predictions[0], np.float64)
    assert result.get("errors") is None
    assert len(predictions) == expected_no_predictions
    assert predictions[0] == expected_first_prediction_value
