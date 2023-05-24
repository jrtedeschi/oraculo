import whisper



def audio_to_text(path: str, language: str = "en-US", model: str = "base", output: str = None):

    model = whisper.load_model(model)
    result = model.transcribe(path, language=language, word_timestamps=True)
    
    # if output is None get filename from path 
    if output is None:
        output = path.split(".")[0] + ".txt"

    with open(output, "w") as f:
            f.write(result["text"])


