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

inputs = [
    {  # Single word aspect
        "aspects": ["service"],
        "sentence": "To sum it up : service varies from good to mediorce , depending on which waiter you get ; generally it is just average ok .",
    },
    {  # Single-word, multiple aspects
        "aspects": ["service", "decor"],
        "sentence": "Everything is always cooked to perfection , the service is excellent, the decor cool and understated.",
    },
    {  # Multi-word aspect
        "aspects": ["grilled chicken", "chicken"],
        "sentence": "the only chicken i moderately enjoyed was their grilled chicken special with edamame puree .",
    },
]

processed_inputs, processed_indices = preprocessor(inputs)
raw_outputs = model(processed_indices)

post_outputs = postprocessor(processed_inputs=processed_inputs, model_outputs=raw_outputs)

print(post_outputs[0])
# {'sentence': ['To', 'sum', 'it', 'up', ':', 'service', 'varies', 'from', 'good', 'to', 'mediorce', ',',
#               'depending', 'on', 'which', 'waiter', 'you', 'get', ';', 'generally', 'it', 'is', 'just',
#               'average', 'ok', '.'],
#  'aspects': [[5]],
#  'labels': [0]}

print(post_outputs[1])
# {'sentence': ['Everything', 'is', 'always', 'cooked', 'to', 'perfection', ',', 'the', 'service',
#               'is', 'excellent,', 'the', 'decor', 'cool', 'and', 'understated.'],
#  'aspects': [[8], [12]],
#  'labels': [1, 1]}

print(post_outputs[2])
# {'sentence': ['the', 'only', 'chicken', 'i', 'moderately', 'enjoyed', 'was', 'their', 'grilled',
#               'chicken', 'special', 'with', 'edamame', 'puree', '.'],
#  'aspects': [[8, 9], [2], [9]],
#  'labels': [1, 1, 1]}