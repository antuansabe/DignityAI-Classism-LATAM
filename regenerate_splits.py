#!/usr/bin/env python3
"""
Regenera los splits (train/validation/test) después de mejorar el dataset
"""

import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

def crear_splits(df: pd.DataFrame, output_dir: Path):
    """
    Crea splits train/validation/test estratificados
    """
    print("=" * 80)
    print("✂️ CREANDO SPLITS (Train/Val/Test)")
    print("=" * 80)

    # Shuffle dataset
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    # Split 70% train, 15% validation, 15% test
    train_df, temp_df = train_test_split(
        df,
        test_size=0.3,
        random_state=42,
        stratify=df['categoria']  # Estratificado por categoría
    )

    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.5,
        random_state=42,
        stratify=temp_df['categoria']
    )

    # Guardar splits
    train_path = output_dir / "train.csv"
    val_path = output_dir / "validation.csv"
    test_path = output_dir / "test.csv"

    train_df.to_csv(train_path, index=False)
    val_df.to_csv(val_path, index=False)
    test_df.to_csv(test_path, index=False)

    print(f"\n✓ Train: {len(train_df):,} ejemplos → {train_path}")
    print(f"✓ Validation: {len(val_df):,} ejemplos → {val_path}")
    print(f"✓ Test: {len(test_df):,} ejemplos → {test_path}")

    # Distribución por categoría
    print("\n📊 Distribución por categoría:")
    print(f"\n{'Categoría':<35} {'Train':>8} {'Val':>8} {'Test':>8}")
    print("-" * 65)

    for categoria in sorted(df['categoria'].unique()):
        train_count = len(train_df[train_df['categoria'] == categoria])
        val_count = len(val_df[val_df['categoria'] == categoria])
        test_count = len(test_df[test_df['categoria'] == categoria])
        print(f"{categoria:<35} {train_count:>8} {val_count:>8} {test_count:>8}")

    print("=" * 80)

if __name__ == "__main__":
    dataset_path = Path("dignityai-clasismo-latam/dataset.csv")
    output_dir = Path("dignityai-clasismo-latam")

    print("=" * 80)
    print("🔄 REGENERANDO SPLITS DESPUÉS DE MEJORA DE DATASET")
    print("=" * 80)
    print(f"📁 Dataset: {dataset_path}")
    print(f"📁 Directorio salida: {output_dir}")
    print("=" * 80)

    # Leer dataset
    df = pd.read_csv(dataset_path)
    print(f"\n✓ Dataset cargado: {len(df):,} filas")

    # Crear splits
    crear_splits(df, output_dir)

    print("\n" + "=" * 80)
    print("✅ SPLITS REGENERADOS EXITOSAMENTE")
    print("=" * 80)
