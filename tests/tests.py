import unittest
from unittest.mock import patch, Mock
from oraculo.cli import app


class TestTranscribe(unittest.TestCase):
    def setUp(self):
        self.runner = app.test_cli_runner()

    @patch("typer.prompt")
    @patch("oraculo.functions.audio.audio_to_text")
    @patch("oraculo.functions.data.get_collections")
    @patch("chromadb.Client")
    def test_transcribe_without_embeddings(
        self, mock_client, mock_get_collections, mock_audio_to_text, mock_prompt
    ):
        # Given
        input_params = ["transcribe", "--embeddings=False"]
        mock_prompt.side_effect = ["path/to/audio.mp3", "pt", "base", None]

        # When
        result = self.runner.invoke(app, input=input_params)

        # Then
        assert "Transcribing... :floppy_disk:" in result.output
        assert mock_audio_to_text.called_with(
            path="path/to/audio.mp3",
            language="pt",
            model="base",
            output=None,
            embeddings=False,
            metadata=None,
            client=None,
        )
        assert result.exit_code == 0

    @patch("typer.prompt")
    @patch("oraculo.functions.audio.audio_to_text")
    @patch("oraculo.functions.data.get_collections")
    @patch("chromadb.Client")
    def test_transcribe_with_embeddings_and_existing_collection(
        self, mock_client, mock_get_collections, mock_audio_to_text, mock_prompt
    ):
        # Given
        input_params = ["transcribe", "--embeddings=True", "--collection=my_collection"]
        mock_prompt.side_effect = ["path/to/audio.mp3", "pt", "base", None]
        mock_get_collections.return_value = {"my_collection": {}}

        # When
        result = self.runner.invoke(app, input=input_params)

        # Then
        assert "Transcribing... :floppy_disk:" in result.output
        assert mock_audio_to_text.called_with(
            path="path/to/audio.mp3",
            language="pt",
            model="base",
            output=None,
            embeddings=True,
            metadata={"collection_name": "my_collection"},
            client=mock_client(),
        )
        assert result.exit_code == 0

    @patch("typer.prompt")
    @patch("oraculo.functions.audio.audio_to_text")
    @patch("oraculo.functions.data.get_collections")
    @patch("chromadb.Client")
    def test_transcribe_with_embeddings_and_new_collection(
        self, mock_client, mock_get_collections, mock_audio_to_text, mock_prompt
    ):
        # Given
        input_params = [
            "transcribe",
            "--embeddings=True",
            "--collection=new_collection",
        ]
        mock_prompt.side_effect = [
            "path/to/audio.mp3",
            "pt",
            "base",
            None,
            "new_collection",
        ]
        mock_get_collections.return_value = {}

        # When
        result = self.runner.invoke(app, input=input_params)

        # Then
        assert "Transcribing... :floppy_disk:" in result.output
        assert mock_audio_to_text.called_with(
            path="path/to/audio.mp3",
            language="pt",
            model="base",
            output=None,
            embeddings=True,
            metadata={"collection_name": "new_collection"},
            client=mock_client(),
        )
        assert result.exit_code == 0
