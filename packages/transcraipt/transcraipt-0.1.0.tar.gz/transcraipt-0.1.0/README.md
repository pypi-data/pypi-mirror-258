# Audio Transcript

Audio Transcript is a powerful tool designed to transcribe audio files using OpenAI's API. It segments the audio, transcribes the segments, and then concatenates the transcriptions to provide a comprehensive transcript of the audio file. This tool is designed with efficiency in mind, allowing for rapid transcription of large audio files by breaking them down into manageable segments. It leverages the OpenAI API for accurate transcription and supports a variety of audio formats.

## Installation

To get Audio Transcript up and running, you've got two straightforward options: pip install or direct setup. Pick the one that suits you best.

### Option 1: Pip Install

Fire up your terminal and run:

```
pip install audio_transcript
```

This command fetches Audio Transcript from PyPI and installs it along with all its dependencies. Easy peasy.

### Option 2: Direct Setup

Prefer to do things manually? No problem. Here's how:

First, clone the repository to your local machine:

```
git clone https://github.com/gsusI/audio_transcript.git
```

Next, dive into the cloned directory:

```
cd audio_transcript
```

And kick off the setup script:

```
python setup.py install
```

This installs all the necessary dependencies and gets the tool ready for action.

## Post-Installation Goodies

Once you've got Audio Transcript installed, you can supercharge your command-line experience with autocomplete. Just follow the on-screen instructions post-installation. They'll walk you through setting up autocomplete for bash, zsh, or PowerShell. It's a game-changer, trust me.

## Usage

To use Audio Transcript, you need to provide the source audio file and optionally specify parameters such as the directory for audio segments, segment duration, overlap duration, and the output file for the transcript. The tool comes with a command-line interface that is fully documented. To see all available options, run:

```
transcribe-audio --help
```

A typical command might look like this:

```
transcribe-audio --source_audio_file path/to/your/audio/file.mp3 --audio_segment_dir path/to/segment/dir --segment_duration 300 --overlap_duration 30 --output_file path/to/output/transcript.txt
```
