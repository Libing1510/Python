from moviepy.editor import VideoFileClip


def convert_mp4_to_mp3(mp4_file, mp3_file):
    try:
        # Load the video file
        video = VideoFileClip(mp4_file)

        # Extract audio from the video
        audio = video.audio

        # Write the audio to a new file
        audio.write_audiofile(mp3_file)

        print(f"Successfully converted {mp4_file} to {mp3_file}")

    except Exception as e:
        print(f"Error converting {mp4_file} to {mp3_file}: {str(e)}")


# Example usage:
input_file = f"C:/Users/YVR/Videos/nan.mp4"
output_file = "C:/Users/YVR/Videos/nan.mp3"

convert_mp4_to_mp3(input_file, output_file)
