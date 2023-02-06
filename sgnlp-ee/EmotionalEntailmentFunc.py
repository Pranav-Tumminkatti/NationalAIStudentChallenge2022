from sgnlp.models.emotion_entailment import (
    RecconEmotionEntailmentConfig,
    RecconEmotionEntailmentTokenizer,
    RecconEmotionEntailmentModel,
    RecconEmotionEntailmentPreprocessor,
    RecconEmotionEntailmentPostprocessor,
)

# Load model
config = RecconEmotionEntailmentConfig.from_pretrained(
    "https://storage.googleapis.com/sgnlp/models/reccon_emotion_entailment/config.json"
)
tokenizer = RecconEmotionEntailmentTokenizer.from_pretrained("roberta-base")
model = RecconEmotionEntailmentModel.from_pretrained(
    "https://storage.googleapis.com/sgnlp/models/reccon_emotion_entailment/pytorch_model.bin",
    config=config,
)
preprocessor = RecconEmotionEntailmentPreprocessor(tokenizer)
postprocessor = RecconEmotionEntailmentPostprocessor()


def checkemotionalentailment(target_utterance,evidence_utterance,conversation_history):
    input_batch = {
        "emotion": ["anger" for i in range(len(target_utterance))],
        "target_utterance": target_utterance,
        "evidence_utterance": evidence_utterance,
        "conversation_history": conversation_history
    }

    tensor_dict = preprocessor(input_batch)
    raw_output = model(**tensor_dict)
    output = postprocessor(raw_output)
    print(output)
    return 1 in output

