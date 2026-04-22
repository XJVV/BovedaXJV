import os

# Archivos de entrada y salida
INPUT_FILE = "brain_v4.tflite"
OUTPUT_FILE = "model_data.h"
ARRAY_NAME = "brain_v4_tflite"

def convertir_a_hex(in_path, out_path, array_name):
    if not os.path.exists(in_path):
        print(f"❌ Error: No se encontró el archivo '{in_path}'")
        return

    with open(in_path, "rb") as f:
        datos = f.read()

    lineas_hex = []
    for i in range(0, len(datos), 12):
        chunk = datos[i:i+12]
        lineas_hex.append("  " + ", ".join([f"0x{b:02x}" for b in chunk]))
    
    # FIX: Unión de líneas corregida
    c_array = ",\n".join(lineas_hex)
    
    contenido_h = f"""// Archivo generado automáticamente
#ifndef MODEL_DATA_H
#define MODEL_DATA_H

// Alineación en memoria para mejor rendimiento en el ESP32
#ifdef __has_attribute
#define DATA_ALIGN_ATTRIBUTE __attribute__((aligned(4)))
#else
#define DATA_ALIGN_ATTRIBUTE
#endif

const unsigned char {array_name}[] DATA_ALIGN_ATTRIBUTE = {{
{c_array}
}};

const int {array_name}_len = {len(datos)};

#endif // MODEL_DATA_H
"""

    with open(out_path, "w") as f:
        f.write(contenido_h)

    print(f"✅ ¡Éxito! {in_path} convertido a {out_path}")
    print(f"   Tamaño: {len(datos)} bytes ({len(datos)/1024:.1f} KB)")

if __name__ == "__main__":
    convertir_a_hex(INPUT_FILE, OUTPUT_FILE, ARRAY_NAME)