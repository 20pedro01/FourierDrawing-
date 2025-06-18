# FourierDrawing
Gato dibujado con DFT en Python 
# Animación con Transformada Discreta de Fourier en Python

Este proyecto convierte el contorno de una imagen en una animación usando **series de Fourier**. Utiliza **números complejos**, **Transformada Discreta de Fourier (DFT)** y animaciones con `matplotlib` para crear una reconstrucción visual del dibujo original a partir de círculos giratorios (*epiciclos*).

https://www.tiktok.com/@[tu_usuario]/video/[id_del_video]

---

## ¿Qué es esto?

La idea se basa en que cualquier curva cerrada puede expresarse como la suma de muchas ondas senoidales (eso es lo que hace la transformada de Fourier).  
Cada onda se representa como un círculo girando, y al sumar todas, se reconstruye el dibujo.

---

## ¿Qué hace el código?

1. **Carga una imagen** (`cat.jpg`) y detecta su contorno.
2. Convierte los puntos a **números complejos**.
3. Aplica una **DFT personalizada** para obtener frecuencias, fases y amplitudes.
4. Dibuja **círculos animados** con `matplotlib` donde el último punto traza el dibujo original.
5. Exporta la animación como `cat_animation.mp4`.

---

## 🛠️ Requisitos

Instala las librerías necesarias:

```bash
pip install opencv-python numpy matplotlib

brew install ffmpeg

