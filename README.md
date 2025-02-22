# JSON to SRT Converter

This Python script converts a JSON transcript (e.g., from Google Speech-to-Text API) into an SRT (SubRip Subtitle) file. It processes timestamps, segments text into appropriate chunks, and formats the subtitles correctly.

## Features
- Parses JSON transcripts containing words and timestamps
- Groups words into sentences based on punctuation
- Splits long sentences into smaller subtitle chunks
- Formats timestamps in SRT format (`HH:MM:SS,ms`)
- Outputs a properly formatted `.srt` file

## Requirements
- Python 3.x

## Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/musayko/json-to-srt.git
   cd json-to-srt
   ```
2. Ensure you have a `transcript.json` file in the project directory.
3. Run the script:
   ```sh
   python main.py
   ```

## JSON Format Example
The script expects a JSON file structured like this:
```json
{
  "results": [
    {
      "alternatives": [
        {
          "words": [
            {"word": "Hello", "startTime": "0.0s", "endTime": "0.5s"},
            {"word": "world", "startTime": "0.6s", "endTime": "1.0s"}
          ]
        }
      ]
    }
  ]
}
```

## Output Format (SRT)
The generated `output.srt` file will look like this:
```
1
00:00:00,000 --> 00:00:00,500
Hello

2
00:00:00,600 --> 00:00:01,000
world
```

## Notes
- Ensure the `transcript.json` file is correctly formatted before running the script.
- You can modify `split_text()` to adjust subtitle length.

## License
This project is open-source and available under the MIT License.

