import yt_dlp

URLS = ['https://www.youtube.com/watch?v=BaW_jenozKc']

# ℹ️ See help(yt_dlp.postprocessor.PostProcessor)
class MyCustomPP(yt_dlp.postprocessor.PostProcessor):
    def run(self, info):
        self.to_screen('Doing stuff')
        return [], info


with yt_dlp.YoutubeDL() as ydl:
    # ℹ️ "when" can take any value in yt_dlp.utils.POSTPROCESS_WHEN
    ydl.add_post_processor(MyCustomPP(), when='pre_process')
    ydl.download(URLS)