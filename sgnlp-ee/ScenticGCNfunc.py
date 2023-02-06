from sgnlp.models.sentic_gcn import(
    SenticGCNConfig,
    SenticGCNModel,
    SenticGCNEmbeddingConfig,
    SenticGCNEmbeddingModel,
    SenticGCNTokenizer,
    SenticGCNPreprocessor,
    SenticGCNPostprocessor,
    download_tokenizer_files,
)

#from main.py import Comment

download_tokenizer_files(
    "https://storage.googleapis.com/sgnlp/models/sentic_gcn/senticgcn_tokenizer/",
    "senticgcn_tokenizer")

tokenizer = SenticGCNTokenizer.from_pretrained("senticgcn_tokenizer")

config = SenticGCNConfig.from_pretrained(
    "https://storage.googleapis.com/sgnlp/models/sentic_gcn/senticgcn/config.json"
)
model = SenticGCNModel.from_pretrained(
    "https://storage.googleapis.com/sgnlp/models/sentic_gcn/senticgcn/pytorch_model.bin",
    config=config
)

embed_config = SenticGCNEmbeddingConfig.from_pretrained(
    "https://storage.googleapis.com/sgnlp/models/sentic_gcn/senticgcn_embedding_model/config.json"
)

embed_model = SenticGCNEmbeddingModel.from_pretrained(
    "https://storage.googleapis.com/sgnlp/models/sentic_gcn/senticgcn_embedding_model/pytorch_model.bin",
    config=embed_config
)

preprocessor = SenticGCNPreprocessor(
    tokenizer=tokenizer, embedding_model=embed_model,
    senticnet="https://storage.googleapis.com/sgnlp/models/sentic_gcn/senticnet.pickle",
    device="cpu")

postprocessor = SenticGCNPostprocessor()


def has_negative_sentiment(comment):
    input = [
        {  # Single word aspect
            "aspects": ["you", "him", "she", "they", "your", "youre"],
            "sentence": comment
        },
    ]

    processed_inputs, processed_indices = preprocessor(input)
    raw_outputs = model(processed_indices)

    post_outputs = postprocessor(processed_inputs=processed_inputs, model_outputs=raw_outputs)

    print(post_outputs[0])
    if -1 in post_outputs[0]["labels"]:
        return True
    else: return False
    # {'sentence': ['To', 'sum', 'it', 'up', ':', 'service', 'varies', 'from', 'good', 'to', 'mediorce', ',',
    #               'depending', 'on', 'which', 'waiter', 'you', 'get', ';', 'generally', 'it', 'is', 'just',
    #               'average', 'ok', '.'],
    #  'aspects': [[5]],
    #  'labels': [0]}

has_negative_sentiment("You are stupid you know that?")