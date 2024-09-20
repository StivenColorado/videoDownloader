import yt_dlp
import streamlit as st
import os

class YoutubeDownloader:
    def __init__(self, url, output_path):
        self.url = url
        self.output_path = output_path
        self.title = ""
        self.duration = 0
        self.thumbnail_url = ""

    def fetch_video_info(self):
        ydl_opts = {
            'cookiefile': './cookies.txt',  # Asegúrate de tener las cookies de YouTube exportadas
            'format': 'best',
            'quiet': True,  # Cambia a True para silenciar la salida
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(self.url, download=False)
                self.title = info_dict.get('title', 'Título no disponible')
                self.duration = info_dict.get('duration', 0)
                self.thumbnail_url = info_dict.get('thumbnail', '')
        except Exception as e:
            st.error(f"Error al obtener información del video: {str(e)}")

    def download(self, progress_callback):
        ydl_opts = {
            'cookiefile': './cookies.txt',  # Utiliza las cookies para autenticación
            'format': 'best',
            'progress_hooks': [progress_callback],
            'quiet': True,
            'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
        except Exception as e:
            st.error(f"Error al descargar el video: {str(e)}")

def on_progress(d):
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes', 0)
        downloaded_bytes = d.get('downloaded_bytes', 0)
        if total_bytes > 0:
            progress = downloaded_bytes / total_bytes
            st.session_state.progress = progress

if __name__ == "__main__":
    st.title("Descargador de Videos de Youtube 📸")
    url = st.text_input("Ingrese la URL del video: ")
    output_path = './downloads'  # Ruta de salida predeterminada

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    if 'progress' not in st.session_state:
        st.session_state.progress = 0.0

    if url:
        downloader = YoutubeDownloader(url, output_path)
        downloader.fetch_video_info()

        st.write(f"**Título**: {downloader.title}")
        st.write(f"**Duración**: {downloader.duration // 60} minutos y {downloader.duration % 60} segundos")
        if downloader.thumbnail_url:
            st.image(downloader.thumbnail_url)

        if 'is_downloading' not in st.session_state:
            st.session_state.is_downloading = False

        if st.button("Descargar", disabled=st.session_state.is_downloading):
            st.session_state.is_downloading = True
            st.write("Descargando video, por favor espera...")
            downloader.download(on_progress)
            st.success("¡Descarga completada! 😃")
            st.session_state.is_downloading = False

    st.progress(st.session_state.progress)
