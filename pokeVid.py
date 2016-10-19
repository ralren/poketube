class PokeVid:
    def __init__(self, title, video_id):
        self.title = title
        self.video_id = video_id

    def get_url(self):
        base_url = "https://www.youtube.com/watch?v="
        return base_url + self.video_id
