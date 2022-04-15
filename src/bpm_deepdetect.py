from essentia.standard import MonoLoader, TempoCNN

def deep_bpm(audio_file, model_path):

    audio = MonoLoader(filename=audio_file)()
    model = TempoCNN(graphFilename=model_path)
    global_tempo, local_tempo, local_tempo_probabilities = model(audio)

    return global_tempo, local_tempo, local_tempo_probabilities
