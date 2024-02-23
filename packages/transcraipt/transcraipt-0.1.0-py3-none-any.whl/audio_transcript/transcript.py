import subprocess
import os
import openai
import hashlib
import json
import argparse
import sys
from tqdm import tqdm
import argcomplete  # Import argcomplete for autocomplete support

def parse_arguments():
    parser = argparse.ArgumentParser(description="""This script processes audio files to generate transcriptions by segmenting the audio, transcribing the segments, and then concatenating the transcriptions. 
To enable autocomplete in your shell, follow these instructions:
- For bash, add:
  eval "$(register-python-argcomplete transcript.py)" 
  to your .bashrc.
- For zsh, add:
  eval "$(register-python-argcomplete transcript.py)" 
  to your .zshrc.
- For PowerShell, add:
  Import-Module <path to argcomplete module> 
  to your profile.""")
    parser.add_argument('--source_audio_file', type=str, help='Absolute or relative path to the source audio file that you want to transcribe.', required=True)
    parser.add_argument('--audio_segment_dir', type=str, default='segmented_audio', help='Path to the directory where audio segments will be stored. Defaults to a folder named "segmented_audio" in the current directory.')
    parser.add_argument('--overlap_duration', type=int, default=30, help='Duration in seconds of how much each audio segment should overlap with the next one. Helps in ensuring continuity in transcriptions. Defaults to 30 seconds.')
    parser.add_argument('--segment_duration', type=int, default=300, help='Total duration in seconds for each audio segment, including the overlap duration. For example, with a default of 300 seconds and an overlap of 30 seconds, each segment will be 5 minutes long with the last 30 seconds repeated in the next segment. Defaults to 300 seconds.')
    parser.add_argument('--test', action='store_true', help='Enables test mode to process a limited number of audio chunks, useful for quick checks.')
    parser.add_argument('--test_chunks', type=int, default=7, help='Specifies the number of audio chunks to process in test mode. Only effective if --test is enabled. Defaults to 7 chunks.')
    parser.add_argument('--verbose', action='store_true', help='Enables verbose output, providing detailed logs of the script\'s operations. Useful for debugging or understanding the script\'s progress.')
    parser.add_argument('--openai_api_key', type=str, help='Your OpenAI API key required for accessing the transcription service. This is not stored and is only used for the duration of the script execution.')
    parser.add_argument('--output_file', type=str, help='Filename for saving the final transcript. If not provided, the transcript will be printed to the console.', required=False)
    
    argcomplete.autocomplete(parser)  # Enable autocomplete with argcomplete
    return parser.parse_args()

def generate_file_hash(file_path):
    """Generate MD5 hash of a file's contents."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def segment_audio_with_overlap(source_file, segment_dir, segment_duration, overlap_duration, verbose=False):
    if not os.path.exists(segment_dir):
        os.makedirs(segment_dir)
    segment_cmd = f"ffmpeg -i {source_file} -f segment -segment_time {segment_duration - overlap_duration} -c copy -reset_timestamps 1 -map 0 {segment_dir}/segment_%03d.mp3"
    if verbose:
        print(f"Segmenting audio with command: {segment_cmd}")
    subprocess.call(segment_cmd, shell=True)

def transcribe_audio(file_path, openai_api_key, verbose=False):
    file_hash = generate_file_hash(file_path)
    transcript_cache_file = f"{file_path}.{file_hash}.cache"
    if os.path.exists(transcript_cache_file):
        with open(transcript_cache_file, 'r') as cache_file:
            return cache_file.read()
    else:
        client = openai.OpenAI(api_key=openai_api_key)
        with open(file_path, 'rb') as audio_file:
            transcript_response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        transcript = transcript_response.text
        with open(transcript_cache_file, 'w') as cache_file:
            cache_file.write(transcript)
        if verbose:
            print(f"Transcribed: {file_path}")
        return transcript

def match_and_concatenate(transcripts, overlap_duration):
    full_transcript = transcripts[0]
    for i in range(1, len(transcripts)):
        previous_text = transcripts[i-1].split()
        current_text = transcripts[i].split()
        
        overlap = set(previous_text[-(overlap_duration*10):]) & set(current_text[:overlap_duration*10])
        if len(overlap) > overlap_duration * 3:
            overlap_index = next((j for j, word in enumerate(current_text) if word in overlap), 0)
            full_transcript += ' ' + ' '.join(current_text[overlap_index:])
        else:
            full_transcript += ' ' + ' '.join(current_text)
    return full_transcript

def main():
    args = parse_arguments()
    openai_api_key = args.openai_api_key if args.openai_api_key else os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        sys.exit('Error: OPENAI_API_KEY environment variable not set or not passed as an argument.')
    
    segment_audio_with_overlap(args.source_audio_file, args.audio_segment_dir, args.segment_duration, args.overlap_duration, args.verbose)
    transcripts = []
    segment_files = sorted([file for file in os.listdir(args.audio_segment_dir) if file.endswith('.mp3')])
    if args.test:
        segment_files = segment_files[:args.test_chunks]
    for segment_file in tqdm(segment_files, desc="Transcribing segments"):
        transcript = transcribe_audio(os.path.join(args.audio_segment_dir, segment_file), openai_api_key, args.verbose)
        transcripts.append(transcript)
    full_transcript = match_and_concatenate(transcripts, args.overlap_duration)
    
    output_file_name = args.output_file if args.output_file else args.source_audio_file.rsplit('.', 1)[0] + '.txt'
    if args.verbose:
        print(full_transcript)
    else:
        with open(output_file_name, 'w') as f:
            f.write(full_transcript)

if __name__ == "__main__":
    main()