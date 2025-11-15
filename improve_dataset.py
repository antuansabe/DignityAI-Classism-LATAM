#!/usr/bin/env python3
"""
DignityAI-Classism-LATAM Dataset Improver

Agrega ruido natural a los textos sintéticos para hacerlos más realistas
y similares a contenido real de internet.

Author: Antonio Dromundo
Date: 2025
License: CC BY-NC-SA 4.0
"""

import random
import pandas as pd
from pathlib import Path
import re

# ============================================================================
# FUNCIONES DE RUIDO NATURAL
# ============================================================================

def introduce_typos(text: str) -> str:
    """
    Introduce errores ortográficos comunes en español
    """
    typos = {
        # Omisión de acentos (muy común)
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',

        # Confusión b/v
        'b': 'v', 'v': 'b',

        # Confusión y/ll
        'y': 'll', 'll': 'y',

        # Confusión s/c/z
        'c': 's', 's': 'z',

        # Falta de h
        'h': '',

        # Confusión g/j
        'g': 'j', 'j': 'g',
    }

    # Aplicar 1-3 typos aleatorios
    num_typos = random.randint(1, 3)
    for _ in range(num_typos):
        if len(text) > 5:  # Solo si hay suficiente texto
            char_pairs = list(typos.items())
            old_char, new_char = random.choice(char_pairs)
            if old_char in text:
                # Reemplazar solo UNA ocurrencia aleatoria
                positions = [i for i, c in enumerate(text) if c == old_char]
                if positions:
                    pos = random.choice(positions)
                    text = text[:pos] + new_char + text[pos+1:]

    return text


def randomize_capitalization(text: str) -> str:
    """
    Aplica mayúsculas caóticas (estilo internet)
    """
    strategies = [
        lambda t: t.lower(),  # todo minúsculas
        lambda t: t.upper(),  # TODO MAYÚSCULAS
        lambda t: ''.join(c.upper() if random.random() < 0.3 else c.lower() for c in t),  # AlEaToRiO
    ]

    return random.choice(strategies)(text)


def add_natural_noise(text: str, probability: float = 0.7) -> str:
    """
    Agrega ruido realista a texto sintético

    Args:
        text: Texto original
        probability: Probabilidad de aplicar ruido (0.0-1.0)

    Returns:
        Texto con ruido natural aplicado
    """
    # Aplicar ruido con cierta probabilidad global
    if random.random() > probability:
        return text

    # 1. Typos/errores ortográficos (30% probabilidad)
    if random.random() < 0.3:
        text = introduce_typos(text)

    # 2. Abreviaciones internet (25% probabilidad - aumentado de 20%)
    abreviaciones = {
        'porque': ['xq', 'pq', 'porque', 'xk', 'pk'],
        'que': ['q', 'ke', 'que', 'k'],
        'para': ['pa', 'para', 'pa\''],
        'por': ['x', 'por'],
        'esto': ['sto', 'esto'],
        'también': ['tb', 'tmb', 'tambien', 'también'],
        'todo': ['td', 'todo'],
        'bien': ['bn', 'bien'],
        'más': ['mas', 'más', '+'],
        'no': ['no', 'nop', 'nel'],
        'sí': ['si', 'sí', 'sep', 'sip'],
        'de': ['de', 'd'],
        'tú': ['tu', 'tú'],
    }

    for palabra, alternativas in abreviaciones.items():
        if palabra in text.lower():
            # Reemplazar algunas ocurrencias (no todas)
            words = text.split()
            for i, word in enumerate(words):
                if palabra in word.lower() and random.random() < 0.5:
                    # Preservar mayúsculas iniciales si las hay
                    replacement = random.choice(alternativas)
                    if word[0].isupper() and replacement[0].isalpha():
                        replacement = replacement.capitalize()
                    words[i] = word.replace(palabra, replacement)
            text = ' '.join(words)

    # 3. Eliminar puntuación formal (40% probabilidad)
    if random.random() < 0.4:
        text = text.replace('.', '')
        text = text.replace(',', '')

    # 4. Mayúsculas caóticas (15% probabilidad)
    if random.random() < 0.15:
        text = randomize_capitalization(text)

    # 5. Emojis contextualmente apropiados (10% probabilidad)
    if random.random() < 0.1:
        sufijos = [
            ' jaja', ' jajaja', ' jeje', ' xD', ' XD',
            ' lol', ' jajaj', ' jajajaj',
            ' 😂', ' 🤣', ' 🤷‍♂️', ' 🤷', ' 💀',
            ' 😏', ' 😎', ' 🙄', ' 😤'
        ]
        text += random.choice(sufijos)

    # 6. Repetición de letras para énfasis (8% probabilidad)
    if random.random() < 0.08:
        words = text.split()
        if words:
            word_idx = random.randint(0, len(words) - 1)
            word = words[word_idx]
            if len(word) > 2:
                # Repetir una letra aleatoria 2-4 veces
                char_idx = random.randint(0, len(word) - 1)
                char = word[char_idx]
                repetitions = random.randint(2, 4)
                words[word_idx] = word[:char_idx] + char * repetitions + word[char_idx+1:]
                text = ' '.join(words)

    # 7. Espacios inconsistentes (5% probabilidad)
    if random.random() < 0.05:
        # Eliminar espacios después de comas/puntos a veces
        text = re.sub(r'([,.])\s', lambda m: m.group(1) if random.random() < 0.5 else m.group(0), text)
        # Agregar espacios extra a veces
        text = re.sub(r'\s', lambda m: '  ' if random.random() < 0.1 else ' ', text)

    # Limpiar espacios múltiples excesivos
    text = re.sub(r'\s{3,}', '  ', text)

    return text.strip()


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def improve_dataset(
    input_path: str,
    output_path: str,
    column_name: str = 'texto_clasista',
    probability: float = 0.7,
    replace_original: bool = False
):
    """
    Mejora un dataset aplicando ruido natural a una columna específica

    Args:
        input_path: Ruta al CSV de entrada
        output_path: Ruta al CSV de salida
        column_name: Nombre de la columna a mejorar
        probability: Probabilidad de aplicar ruido (0.0-1.0)
        replace_original: Si True, reemplaza la columna original. Si False, crea una nueva columna
    """
    print("=" * 80)
    print("🔧 MEJORANDO DATASET CON RUIDO NATURAL")
    print("=" * 80)
    print(f"📁 Archivo entrada: {input_path}")
    print(f"📁 Archivo salida: {output_path}")
    print(f"📊 Columna a mejorar: {column_name}")
    print(f"🎲 Probabilidad de ruido: {probability * 100:.1f}%")
    print(f"🔄 Reemplazar original: {'Sí' if replace_original else 'No'}")
    print("=" * 80)

    # Leer dataset
    df = pd.read_csv(input_path)
    print(f"\n✓ Dataset cargado: {len(df):,} filas")

    # Verificar que la columna existe
    if column_name not in df.columns:
        raise ValueError(f"La columna '{column_name}' no existe en el dataset")

    # Aplicar ruido natural
    print(f"\n🔄 Aplicando ruido natural a '{column_name}'...")

    if replace_original:
        new_column_name = column_name
    else:
        new_column_name = f"{column_name}_ruidoso"

    # Aplicar transformación con barra de progreso simple
    improved_texts = []
    total = len(df)
    noise_applied_count = 0

    for idx, text in enumerate(df[column_name], 1):
        improved = add_natural_noise(str(text), probability)
        improved_texts.append(improved)

        # Contar cuántos fueron modificados
        if improved != str(text):
            noise_applied_count += 1

        # Mostrar progreso cada 1000 registros
        if idx % 1000 == 0 or idx == total:
            percentage = (idx / total) * 100
            print(f"  Procesando: {idx:,}/{total:,} ({percentage:.1f}%)", end='\r')

    print()  # Nueva línea después del progreso

    # Asignar resultados
    df[new_column_name] = improved_texts

    # Guardar
    df.to_csv(output_path, index=False)

    # Estadísticas
    print("\n" + "=" * 80)
    print("✅ PROCESO COMPLETADO")
    print("=" * 80)
    print(f"✓ Archivo guardado: {output_path}")
    print(f"✓ Total de filas: {len(df):,}")
    print(f"✓ Textos con ruido aplicado: {noise_applied_count:,} ({noise_applied_count/total*100:.1f}%)")
    print(f"✓ Textos sin cambios: {total - noise_applied_count:,} ({(total - noise_applied_count)/total*100:.1f}%)")

    if replace_original:
        print(f"\n✓ Columna reemplazada y guardada en: {output_path}")
    else:
        print(f"\n✓ Nueva columna creada: '{new_column_name}'")

    print("=" * 80)

    return df


# ============================================================================
# CLI
# ============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Mejora un dataset agregando ruido natural a textos sintéticos"
    )
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Ruta al CSV de entrada'
    )
    parser.add_argument(
        '--output', '-o',
        required=True,
        help='Ruta al CSV de salida'
    )
    parser.add_argument(
        '--column', '-c',
        default='texto_clasista',
        help='Nombre de la columna a mejorar (default: texto_clasista)'
    )
    parser.add_argument(
        '--probability', '-p',
        type=float,
        default=0.7,
        help='Probabilidad de aplicar ruido (0.0-1.0)'
    )
    parser.add_argument(
        '--replace', '-r',
        action='store_true',
        help='Reemplazar columna original en lugar de crear una nueva'
    )

    args = parser.parse_args()

    improve_dataset(
        input_path=args.input,
        output_path=args.output,
        column_name=args.column,
        probability=args.probability,
        replace_original=args.replace
    )
