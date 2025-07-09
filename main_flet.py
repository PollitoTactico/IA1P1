# main_flet.py

import flet as ft
import os
import shutil
import platform
import subprocess
from analizar_video import analizar_video

def main(page: ft.Page):
    page.title = "Detector de Golpes de Voleibol"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_width = 600
    page.window_height = 850

    # Variables visuales
    resultado_text = ft.Text("", size=18)
    subida_text = ft.Text("", size=16, color="green", visible=False)
    grafico = ft.Column()
    cargando = ft.ProgressBar(width=400, visible=False)

    # Almacena la ruta del último video subido
    page.ultimo_video_guardado = ""

    def al_subir_video(e: ft.FilePickerResultEvent):
        if not e.files:
            return

        archivo = e.files[0]
        ruta_original = archivo.path
        nombre_archivo = os.path.basename(ruta_original)

        try:
            os.makedirs("subidos", exist_ok=True)
            ruta_guardada = os.path.join("subidos", nombre_archivo)
            shutil.copy(ruta_original, ruta_guardada)

            page.ultimo_video_guardado = ruta_guardada

            subida_text.value = f"📤 Video subido correctamente: {nombre_archivo}"
            subida_text.visible = True
            page.update()
        except Exception as ex:
            subida_text.value = f"❌ Error al subir el video: {str(ex)}"
            subida_text.visible = True
            page.update()

    def analizar_click(e):
        if not page.ultimo_video_guardado or not os.path.exists(page.ultimo_video_guardado):
            resultado_text.value = "❌ No hay video para analizar. Sube uno primero."
            page.update()
            return

        cargando.visible = True
        resultado_text.value = "⏱ Procesando video, esto puede tardar unos minutos..."
        page.update()

        try:
            conteo, ruta_video_salida, ruta_csv = analizar_video(page.ultimo_video_guardado)

            # Copiar CSV a carpeta Descargas del usuario
            user_downloads = os.path.join(
                os.path.expanduser("~"),
                "Downloads" if platform.system() == "Windows" else "Descargas"
            )
            os.makedirs(user_downloads, exist_ok=True)
            ruta_csv_usuario = os.path.join(user_downloads, os.path.basename(ruta_csv))
            shutil.copy(ruta_csv, ruta_csv_usuario)

            # Mostrar resultados
            resultado_text.value = "🎉 Análisis completado exitosamente:\n"
            for golpe, cantidad in conteo.items():
                resultado_text.value += f"✔ {golpe.capitalize()}: {cantidad}\n"

            grafico.controls = [
                ft.Text("📊 Golpes detectados:", size=18, weight="bold"),
            ] + [
                ft.Row([
                    ft.Text(f"{golpe.capitalize()}: {cantidad}"),
                    ft.Container(
                        width=min(cantidad * 10, 300),
                        height=20,
                        bgcolor="#90CAF9",
                        border_radius=10
                    )
                ]) for golpe, cantidad in conteo.items()
            ]

        except Exception as ex:
            resultado_text.value = f"❌ Error durante el análisis: {str(ex)}"
        finally:
            cargando.visible = False
            page.update()

    def ver_en_ventana_externa(e):
        try:
            subprocess.Popen(["python", "main.py"], shell=True)
        except Exception as ex:
            resultado_text.value = f"❌ No se pudo abrir el visor externo: {str(ex)}"
            page.update()

    # Selector de archivo
    subir_archivo = ft.FilePicker(on_result=al_subir_video)
    page.overlay.append(subir_archivo)

    # Botones
    subir_btn = ft.ElevatedButton(
        text="Subir video",
        icon=ft.Icons.UPLOAD_FILE,
        on_click=lambda e: subir_archivo.pick_files(
            allow_multiple=False,
            allowed_extensions=["mp4"]
        )
    )

    analizar_btn = ft.ElevatedButton(
        text="Analizar video",
        icon=ft.Icons.PLAY_ARROW,
        on_click=analizar_click
    )

    abrir_main_btn = ft.ElevatedButton(
        text="🧿 Ver en ventana externa",
        icon=ft.Icons.MONITOR,
        on_click=ver_en_ventana_externa
    )

    # Interfaz visual
    page.add(
        ft.Text("🎯 Detección de Golpes de Voleibol", size=24, weight="bold"),
        ft.Divider(),
        subir_btn,
        analizar_btn,
        abrir_main_btn,
        subida_text,
        cargando,
        resultado_text,
        grafico
    )

ft.app(target=main)
