from transformers import pipeline

# Load a pre-trained summarization model
summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6"
)

# Sample long text
text = """
Artificial Intelligence is becoming an important part of modern technology.
It is used in healthcare, education, finance, transportation, cybersecurity,
and many other areas. Machine learning allows computers to learn patterns
from data and make predictions. Natural Language Processing allows computers
to understand and process human language. With the development of powerful
pre-trained models, developers can now build useful AI applications without
training large models from scratch.
"""

# Generate summary
summary = summarizer(
    text,
    max_length=60,
    min_length=20,
    do_sample=False
)

print("\nOriginal Text:")
print(text)

print("\nAI Generated Summary:")
print(summary[0]["summary_text"])