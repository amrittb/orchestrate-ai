import subprocess

class Downloader:

	"""Downloads videos from given video list
	
	Uses youtube-dl tool to download videos
	"""
	def download_from_list(self, video_ids):
		for i, id in enumerate(video_ids):
			print("\n Downloading ", i + 1, " out of ", len(video_ids) ," files\n")

			subprocess.run(["youtube-dl","-f 140","--no-part","-o","music/%(id)s.%(ext)s",id])
