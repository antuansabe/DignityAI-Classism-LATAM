# DignityAI-Clasismo-LATAM

> Parte de [DignityAI](https://sin-odio.vercel.app/dignityai): recursos abiertos para detectar y estudiar discriminación en el español de América Latina.

**Advertencia de contenido.** Este dataset contiene lenguaje de discriminación socioeconómica (clasismo) explícito y sutil. Existe para entrenar y evaluar sistemas que **detectan** discriminación, nunca para generarla.

**Estado:** 🛑 datos sintéticos · 🛑 sin validación comunitaria · versión recomendada **1.1**

*English summary: synthetic, template-based Spanish dataset on socioeconomic discrimination (classism) across 5 countries, with contrastive non-discriminatory alternatives. Version 1.1 removes duplicates and near-duplicates and provides leakage-free splits. Best used for stress-testing and taxonomy work, not as the sole training source for a detector. License CC BY-NC-SA 4.0.*

## Qué contiene

Textos discriminatorios escritos a partir de plantillas combinatorias, cada uno etiquetado con país, categoría, subcategoría, nivel de sutileza y contexto (redes sociales, trabajo, apps de citas, etc.), más un conjunto de textos de contraste no discriminatorios.

- **Países:** México, Argentina, Colombia, Chile, España
- **Taxonomía:** 6 categorías, 18 subcategorías, niveles de sutileza: sutil, explícito, interiorizado, sistémico, normalizado

| Categoría | Subcategorías | Textos únicos |
|---|---|---:|
| `clasismo_aspiracional` | `adoracion_estatus`, `desprecio_origenes`, `meritocracia_toxica` | 2,845 |
| `deshumanizacion_directa` | `ataques_apariencia`, `insultos_pobreza`, `vocabulario_deshumanizante` | 3,579 |
| `estereotipos_prejuicios` | `asociar_pobreza_crimen`, `estereotipos_habitos`, `prejuicios_capacidades` | 3,957 |
| `exclusion_normalizada` | `barreras_clasistas`, `exclusion_servicios`, `segregacion_espacial` | 2,879 |
| `microagresiones_cotidianas` | `diminutivos_condescendientes`, `invisibilizacion`, `sorpresa_competencia` | 2,464 |
| `violencia_simbolica` | `discurso_corporativo`, `lenguaje_institucional`, `medios_comunicacion` | 2,596 |

## Versiones

| Versión | Carpeta | Formato | Recomendación |
|---|---|---|---|
| **1.1** | [`v1.1/`](v1.1/) | Una fila por texto: `texto`, `etiqueta` (1 discriminatorio, 0 contraste), `tipo`, `pais`, `categoria`, `subcategoria`, `nivel_sutileza`, `contexto` | **Usar esta** |
| 1.0 | [`dignityai-clasismo-latam/`](dignityai-clasismo-latam/) | Pares (texto discriminatorio + alternativa) con metadatos extendidos | Solo para consultar los pares; **no uses sus splits** |

## Cifras medidas (noviembre 2026)

Calculadas con [`scripts/build_v1_1.py`](scripts/build_v1_1.py); el detalle está en [`v1.1/reporte_v1_1.json`](v1.1/reporte_v1_1.json).

| Medida | Valor |
|---|---:|
| Filas en v1.0 (pares) | 27,883 |
| Textos en formato largo | 55,766 |
| Tras quitar duplicados exactos | 22,305 |
| **Tras quitar casi-duplicados (v1.1)** | **19,187** |
| Discriminatorios / contraste | 18,320 / 867 |
| Train / validación / prueba | 13,430 / 2,878 / 2,879 |
| Fuga entre train y prueba (v1.1) | 0.0% |

Textos discriminatorios únicos por país:

| País | Textos |
|---|---:|
| México | 4,481 |
| Argentina | 3,679 |
| Colombia | 3,480 |
| Chile | 3,344 |
| España | 3,336 |

### Qué tan difícil es (baselines TF-IDF + regresión logística, F1 macro)

| Tarea | F1 |
|---|---:|
| Discriminatorio vs. contraste, partición v1.1 | 0.998 |
| Discriminatorio vs. contraste, **subcategorías no vistas** | **0.913** |
| Clasificar la categoría | 0.998 |

Que un modelo tan simple llegue a ~0.99 significa que los textos se distinguen por el estilo de la plantilla, no por comprensión. **La fila de subcategorías no vistas es la cifra honesta de generalización.**

## Limitaciones medidas

- **Es sintético.** Las plantillas no capturan la variedad del lenguaje real. El ruido (typos, abreviaturas, risas) se añadió con un script solo al lado discriminatorio, así que un modelo puede aprender que "escribir informal" = discriminación.
- **Los contrastes son pocos.** Solo 867 textos de contraste únicos frente a 18,320 discriminatorios (longitud mediana 38 vs. 39 caracteres).
- **La v1.0 tenía fuga.** Sus splits repetían en prueba casi el 100% de los textos de contraste de entrenamiento. Por eso existe la v1.1.
- **Sin validación comunitaria.** Ninguna organización ni comunidad afectada ha revisado los ejemplos todavía.

### Qué no cubre

- Perú, Centroamérica y el Caribe hispanohablante.
- Clasismo que solo se entiende con contexto (tono, imagen, conversación previa).
- Intersecciones con racismo y género, que en la práctica casi siempre van juntas.
- Ojo: incluye España, aunque el nombre diga LATAM.

## Cómo usarlo

```python
import pandas as pd

base = "https://raw.githubusercontent.com/antuansabe/DignityAI-Classism-LATAM/main/v1.1"
train = pd.read_csv(f"{base}/train.csv")
test = pd.read_csv(f"{base}/test.csv")
print(train.groupby(["pais", "categoria"]).size())
```

**Usos recomendados:** pruebas de estrés de detectores y LLMs, estudio de la taxonomía, materiales de formación con advertencia de contenido, aumento de datos **junto con** corpus reales (ver el [directorio de datos reales](https://sin-odio.vercel.app/dignityai#directorio)).

**No lo uses para:** generar contenido discriminatorio, entrenar un detector solo con estos datos, tomar decisiones automáticas sobre personas o fines comerciales sin autorización.

## Licencia

[CC BY-NC-SA 4.0](LICENSE). Uso libre para investigación, educación, organizaciones civiles y periodismo. Para uso comercial, escribe a antuansabe@gmail.com.

## Cómo citar

Usa el archivo [`CITATION.cff`](CITATION.cff) (GitHub muestra el botón "Cite this repository") o:

```bibtex
@misc{dromundo2025clasismo,
  author = {Dromundo, Antonio},
  title  = {DignityAI-Clasismo-LATAM: dataset sintético de discriminación socioeconómica (clasismo) en español},
  year   = {2025},
  note   = {Versión 1.1 (2026)},
  url    = {https://github.com/antuansabe/DignityAI-Classism-LATAM}
}
```

## Contacto y contribuciones

- Errores, sesgos o ejemplos que deban retirarse: abre un [issue](https://github.com/antuansabe/DignityAI-Classism-LATAM/issues) o escribe a antuansabe@gmail.com.
- Si eres parte de una comunidad afectada, tu revisión tiene prioridad sobre cualquier métrica.

Proyecto independiente de Antonio Dromundo ([GitHub](https://github.com/antuansabe), [Hugging Face](https://huggingface.co/antonn-dromundo)). No está afiliado a ninguna organización mencionada en este repositorio.
