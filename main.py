import json
import re

def format_time(seconds):
    """Convert seconds to SRT time format (HH:MM:SS,ms)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

def split_text(text, max_length):
    """Split text into chunks of max_length characters or less."""
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        if len(' '.join(current_chunk + [word])) <= max_length:
            current_chunk.append(word)
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

# Load the JSON data
with open("transcript.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Initialize variables
all_words = []
subtitle_segments = []

# Collect all words from all results
for result in data["results"]:
    for alternative in result["alternatives"]:
        if "words" in alternative:
            all_words.extend(alternative["words"])

# Sort words by start time
all_words.sort(key=lambda x: float(x["startTime"].rstrip("s")))

# Initialize variables for sentence grouping
current_sentence = []
sentence_start_time = float(all_words[0]["startTime"].rstrip("s"))

# Define sentence-ending punctuation
sentence_endings = [".", "!", "?"]

for word in all_words:
    word_text = word["word"]
    start_time = float(word["startTime"].rstrip("s"))
    end_time = float(word["endTime"].rstrip("s"))

    current_sentence.append(word_text)

    # Check if the word ends with sentence-ending punctuation
    if any(word_text.endswith(ending) for ending in sentence_endings):
        subtitle_segments.append({
            "text": " ".join(current_sentence),
            "start_time": sentence_start_time,
            "end_time": end_time
        })
        current_sentence = []
        if word != all_words[-1]:  # If not the last word
            sentence_start_time = float(all_words[all_words.index(word) + 1]["startTime"].rstrip("s"))

# Add any remaining words as the last segment
if current_sentence:
    subtitle_segments.append({
        "text": " ".join(current_sentence),
        "start_time": sentence_start_time,
        "end_time": float(all_words[-1]["endTime"].rstrip("s"))
    })

# Generate SRT content
srt_content = ""
for i, segment in enumerate(subtitle_segments, start=1):
    text_chunks = split_text(segment["text"], 45)
    chunk_duration = (segment["end_time"] - segment["start_time"]) / len(text_chunks)

    for j, chunk in enumerate(text_chunks):
        chunk_start_time = segment["start_time"] + j * chunk_duration
        chunk_end_time = segment["start_time"] + (j + 1) * chunk_duration

        srt_content += f"{i}\n"
        srt_content += f"{format_time(chunk_start_time)} --> {format_time(chunk_end_time)}\n"
        srt_content += f"{chunk}\n\n"
        i += 1

# Save the SRT file
with open("output.srt", "w", encoding="utf-8") as srt_file:
    srt_file.write(srt_content)

print("SRT file created successfully!")