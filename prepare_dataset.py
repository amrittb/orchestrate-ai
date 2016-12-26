from orchestrate_ai.youtube_dataset import *

def main():
	# Download and prepare datasets
	list_generator = video_list_generator.Generator("playlists.json", youtube_api_client.Client("AIzaSyD_UC-FpXbJeWzPfscLz9RhqSjKwj33q6A"))
	video_list = list_generator.get_video_list("piano","sad")
	
	downloader = youtube_video_downloader.Downloader()
	downloader.download_from_list(video_list)

if __name__ == '__main__':
	main()