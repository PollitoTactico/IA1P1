
---

## README 

### Lenguaje
- **Python 3.12**

### Librerías utilizadas

| Librería         | Uso |
|------------------|-----|
| `OpenCV`         | Lectura, escritura y visualización de videos |
| `MediaPipe`      | Detección de pose humana por frame |
| `NumPy`          | Vectorización de poses |
| `scikit-learn`   | Entrenamiento y predicción con SVM |
| `pandas`         | Creación y exportación de datasets |
| `Flet`           | Interfaz de usuario moderna en Python |

### ⚙️ Algoritmo de ML
- **SVM (Support Vector Machine)** con kernel lineal (`sklearn.svm.SVC(kernel="linear")`)
- Ideal para clasificación supervisada de 3 clases: `mancheta`, `voleo`, `remate`

### Flujo del sistema

1. **Entrenamiento (`entrenamiento.py`)**
   - Detecta landmarks con MediaPipe y los convierte a vectores.
   - Asigna etiquetas y entrena modelo SVM.
   - Guarda `modelo.pkl` para reuso.

2. **Análisis (`analizador_video.py`)**
   - Usa el modelo entrenado para analizar un nuevo video.
   - Crea un archivo `.csv` con predicciones por frame.
   - Genera un video anotado con texto superpuesto.

3. **Interfaz gráfica (`main_flet.py`)**
   - Permite al usuario subir videos.
   - Ejecuta el análisis y muestra estadísticas.
   - Copia automáticamente el CSV a la carpeta `Descargas`.
   - Botón opcional para abrir `main.py` y visualizar el video.

---

## Cómo usar

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```
### 2. Entrenar una sola vez
```bash
python entrenamiento.py
```
### 3. Ejecutar interfaz
```bash
python main_flet.py
```


