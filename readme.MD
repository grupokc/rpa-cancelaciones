# BI: Disminuciones Cancelaciones
Proceso ETL automatizado.

Este proyecto automatiza la extracción de datos desde una GUI, toma capturas de pantalla, transforma las imágenes en texto usando OCR (Tesseract) y retorna toda la información cargada en un archivo `.xlsx`.

## Uso

### Crear entorno virtual

```bash
python -m venv .venv
.\.venv\scripts\activate
pip install -r requirements.txt
```

### Instalar Tesseract OCR

Debes descargar e instalar Tesseract OCR desde [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract).  
Luego, agrega la ruta de instalación de Tesseract al PATH de tu sistema.


### Agregar el Modelo Hermes 
En la ruta: `C:\Program Files\Tesseract-OCR\tessdata` pegar el modelo ocr Hermes_v3.traineddata para que tesseract lo reconozca. 

