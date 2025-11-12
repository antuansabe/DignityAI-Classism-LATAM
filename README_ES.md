# 🌟 DignityAI-Clasismo-LATAM

> **Parte de la [Iniciativa DignityAI](https://github.com/antonnDromundo/DignityAI)** - Protegiendo la dignidad humana mediante IA

## 📋 Descripción

**DignityAI-Clasismo-LATAM** es el primer dataset comprehensivo de discriminación clasista en español latinoamericano, diseñado para entrenar modelos de NLP que detecten y prevengan discurso de odio socioeconómico.

Este dataset documenta expresiones de clasismo en 5 países latinoamericanos, desde insultos explícitos hasta microagresiones sutiles normalizadas en el lenguaje cotidiano.

---

## 🎯 Acerca de DignityAI

**DignityAI** es una iniciativa open-source que crea datasets y modelos de IA para detectar discriminación en comunidades hispanohablantes.

### 🗂️ Familia de Datasets DignityAI:

| Dataset | Ejemplos | Enfoque | Estado |
|---------|----------|---------|--------|
| [SinOdio-LATAM](https://huggingface.co/datasets/antonn-dromundo/SinOdio-LATAM-Regional-HateSpeech) | 20,000 | Discurso de odio general | ✅ Publicado |
| [DignityAI-Machismo-LATAM](https://huggingface.co/datasets/antonn-dromundo/DignityAI-Machismo-LATAM) | 18,000 | Machismo y sexismo | ✅ Publicado |
| **DignityAI-Clasismo-LATAM** | 27,883 | **Discriminación económica** | ✅ **NUEVO** |
| DignityAI-Racism-LATAM | Por definir | Discriminación racial | 🔜 Próximamente |
| DignityAI-Xenophobia-LATAM | Por definir | Xenofobia | 🔜 Próximamente |

---

## 📊 Características del Dataset

- ✅ **27,883 ejemplos únicos de alta calidad**
- ✅ **5 países:** México, Argentina, Colombia, Chile, España
- ✅ **6 categorías** de discriminación clasista
- ✅ **18 subcategorías** cubriendo todas las formas de discriminación económica
- ✅ **Pares contrastivos:** texto clasista + alternativa inclusiva
- ✅ **Balance perfecto** entre países y categorías
- ✅ **Jerga regional auténtica** por país
- ✅ **12 contextos diferentes** (redes sociales, trabajo, espacios públicos, etc.)
- ✅ **Múltiples formatos:** CSV, JSON, Parquet
- ✅ **Splits listos:** Train (70%), Validation (15%), Test (15%)

---

## 🏷️ Categorías

### 1. **Deshumanización Directa** (20% - 5,573 ejemplos)
Ataques directos relacionados con estatus económico:
- **Insultos de pobreza:** "muerto de hambre", "limosnero", "naco", "villero", "ñero"
- **Ataques por apariencia:** "harapiento", "mugroso", "corriente", "flaite"
- **Vocabulario deshumanizante:** "plebe", "gentuza", "escoria", "lacra", "chusma"

### 2. **Estereotipos y Prejuicios** (20% - 5,573 ejemplos)
Vinculación de pobreza con rasgos negativos:
- **Asociación pobreza = crimen:** Estereotipos que vinculan estatus económico con criminalidad
- **Prejuicios de capacidad:** "no entienden", "ignorantes", suposiciones sobre inteligencia
- **Estereotipos de hábitos:** "flojos", "no quieren trabajar", "viven del estado"

### 3. **Exclusión Normalizada** (15% - 4,180 ejemplos)
Discriminación cotidiana disfrazada de normal:
- **Segregación espacial:** "no es su lugar", exclusión de espacios
- **Exclusión de servicios:** "no pueden pagarlo", negación de acceso
- **Barreras clasistas:** "código de vestimenta requerido", restricciones de membresía

### 4. **Clasismo Aspiracional** (15% - 4,180 ejemplos)
Discriminación de clase interiorizada:
- **Negación de origen:** "no soy como ellos", vergüenza de orígenes humildes
- **Adoración de estatus:** "gente bonita", "gente bien", idolatría de riqueza
- **Meritocracia tóxica:** "son pobres porque quieren", culpabilización de víctimas

### 5. **Microagresiones Cotidianas** (15% - 4,180 ejemplos)
Expresiones sutiles pero dañinas:
- **Diminutivos condescendientes:** "pobrecito", "tu trabajadora", "el chico"
- **Sorpresa por competencia:** "hablas bien para ser de...", cumplidos con doble filo
- **Invisibilización:** "el de limpieza", "la muchacha", reducir personas a sus oficios

### 6. **Violencia Simbólica** (15% - 4,180 ejemplos)
Discriminación institucional/sistémica:
- **Lenguaje de políticas:** "población vulnerable", "beneficiarios", términos paternalistas
- **Discurso mediático:** criminalización, victimización de barrios pobres
- **Lenguaje corporativo:** "recursos de bajo nivel", "personal no calificado"

---

## 🌍 Cobertura Regional

### Países y Jerga Regional Auténtica:

| País | Ejemplos | Términos Auténticos Utilizados |
|------|----------|--------------------------------|
| 🇲🇽 **México** | 5,577 | naco, prole, Tepito, Polanco, wey, pinche |
| 🇦🇷 **Argentina** | 5,577 | villero, negro, cabeza, conurbano, Palermo, boludo, che |
| 🇨🇴 **Colombia** | 5,577 | gamín, ñero, Ciudad Bolívar, Rosales, parce, gonorrea |
| 🇨🇱 **Chile** | 5,577 | flaite, roto, La Pincoya, Las Condes, weon, conchetumare |
| 🇪🇸 **España** | 5,577 | chusma, cutre, Cañada Real, Salamanca, joder, hostia |

---

## 📂 Estructura del Dataset

Cada ejemplo contiene:

```json
{
  "pais": "México",
  "categoria": "deshumanizacion_directa",
  "subcategoria": "insultos_pobreza",
  "texto_clasista": "Pinche muerto de hambre, vete a tu rancho",
  "texto_inclusivo": "Respeto tu situación, todos merecemos dignidad",
  "contexto": "comentario_redes_sociales",
  "nivel_sutileza": "explícito",
  "grupos_afectados": ["personas_bajos_recursos", "migrantes_rurales"],
  "mecanismo_discriminacion": "insulto_directo",
  "jerga_regional": true,
  "generado_en": "2025-11-09T10:30:00",
  "id": "a3f2b8c1d4e5f6g7"
}
```

### Descripción de Campos:
- **pais**: País de origen (México, Argentina, Colombia, Chile, España)
- **categoria**: Categoría principal de discriminación (6 totales)
- **subcategoria**: Tipo específico de discriminación (18 totales)
- **texto_clasista**: Texto clasista/discriminatorio
- **texto_inclusivo**: Alternativa inclusiva/respetuosa
- **contexto**: Contexto donde ocurre (12 tipos)
- **nivel_sutileza**: Nivel de sutileza (explícito, sutil, normalizado, interiorizado, sistémico)
- **grupos_afectados**: Grupos afectados (lista)
- **mecanismo_discriminacion**: Mecanismo de discriminación (18 tipos)
- **jerga_regional**: Usa jerga regional (booleano)
- **generado_en**: Timestamp de generación
- **id**: Identificador único

---

## 🚀 Inicio Rápido

### Cargar Dataset Completo

```python
from datasets import load_dataset
import pandas as pd

# Opción 1: Cargar desde CSV local
df = pd.read_csv("dataset.csv")
print(f"Total de ejemplos: {len(df):,}")

# Opción 2: Cargar desde HuggingFace (una vez publicado)
# dataset = load_dataset("antonn-dromundo/DignityAI-Clasismo-LATAM")
```

### Cargar Split Específico

```python
# Cargar splits individuales
train_df = pd.read_csv("train.csv")
val_df = pd.read_csv("validation.csv")
test_df = pd.read_csv("test.csv")

print(f"Train: {len(train_df):,} ejemplos")
print(f"Validation: {len(val_df):,} ejemplos")
print(f"Test: {len(test_df):,} ejemplos")
```

### Filtrar por País

```python
# Filtrar ejemplos de México
df_mexico = df[df['pais'] == 'México']

# Filtrar ejemplos de Argentina
df_argentina = df[df['pais'] == 'Argentina']

print(f"Ejemplos México: {len(df_mexico):,}")
print(f"Ejemplos Argentina: {len(df_argentina):,}")
```

### Filtrar por Categoría

```python
# Filtrar microagresiones
microagresiones = df[df['categoria'] == 'microagresiones_cotidianas']

# Filtrar discriminación explícita
explicito = df[df['nivel_sutileza'] == 'explícito']

print(f"Microagresiones: {len(microagresiones):,}")
print(f"Explícito: {len(explicito):,}")
```

---

## 💡 Casos de Uso

### 1. 🤖 Entrenamiento de Modelos

Fine-tune de modelos BERT para detección de clasismo:

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
import pandas as pd

# Cargar dataset
df = pd.read_csv("train.csv")

# Cargar BERT en español
model_name = "dccuchile/bert-base-spanish-wwm-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

# Preparar dataset
def tokenize_function(text):
    return tokenizer(text, padding="max_length", truncation=True, max_length=128)

# Crear etiquetas: 1 para clasista, 0 para inclusivo
texts = df['texto_clasista'].tolist() + df['texto_inclusivo'].tolist()
labels = [1] * len(df) + [0] * len(df)

# Tokenizar
encodings = tokenizer(texts, truncation=True, padding=True, max_length=128)

# Crear dataset
import torch

class ClassismDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

dataset = ClassismDataset(encodings, labels)

# Argumentos de entrenamiento
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
)

# Entrenar
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
)

trainer.train()
```

### 2. 🔍 Monitoreo de Redes Sociales

Detectar comentarios clasistas en tiempo real:

```python
from transformers import pipeline

# Cargar modelo entrenado
classifier = pipeline("text-classification", model="your-model-path")

# Analizar comentarios
comments = [
    "Pinche muerto de hambre, vete a tu barrio",
    "Respeto tu situación, todos tenemos luchas"
]

for comment in comments:
    result = classifier(comment)
    print(f"Texto: {comment}")
    print(f"Clasificación: {result[0]['label']}")
    print(f"Confianza: {result[0]['score']:.2%}\n")
```

### 3. 📊 Investigación y Análisis

Analizar patrones de discriminación:

```python
import pandas as pd
import matplotlib.pyplot as plt

# Cargar dataset
df = pd.read_csv("dataset.csv")

# Analizar por país
print("Ejemplos por país:")
print(df['pais'].value_counts())

# Analizar mecanismos más comunes
print("\nMecanismos de discriminación principales:")
print(df['mecanismo_discriminacion'].value_counts().head(10))

# Analizar distribución de sutileza
print("\nNiveles de sutileza:")
print(df['nivel_sutileza'].value_counts())

# Visualizar distribución por categoría
df['categoria'].value_counts().plot(kind='bar', figsize=(12, 6))
plt.title('Distribución por Categoría')
plt.xlabel('Categoría')
plt.ylabel('Cantidad')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('distribucion_categorias.png')
```

### 4. 🎓 Herramientas Educativas

Crear materiales de capacitación sobre conciencia:

```python
import pandas as pd
import random

df = pd.read_csv("dataset.csv")

# Obtener ejemplos para taller - clasismo sutil
sutiles = df[df['nivel_sutileza'] == 'sutil'].sample(10)

print("TALLER: Reconociendo el Clasismo Sutil\n")
print("="*70)

for i, row in sutiles.iterrows():
    print(f"\n{i+1}. Categoría: {row['subcategoria']}")
    print(f"   Clasista: {row['texto_clasista']}")
    print(f"   Mejor: {row['texto_inclusivo']}")
    print(f"   Por qué es problemático: {row['mecanismo_discriminacion']}")
    print(f"   Grupos afectados: {row['grupos_afectados']}")
```

---

## 📈 Estadísticas del Dataset

### Distribución por País

| País | Ejemplos | Porcentaje |
|------|----------|------------|
| México | 5,577 | 20.0% |
| Argentina | 5,577 | 20.0% |
| Colombia | 5,577 | 20.0% |
| Chile | 5,577 | 20.0% |
| España | 5,577 | 20.0% |

### Distribución por Categoría

| Categoría | Ejemplos | Peso |
|-----------|----------|------|
| Deshumanización Directa | 5,573 | 20.0% |
| Estereotipos y Prejuicios | 5,573 | 20.0% |
| Exclusión Normalizada | 4,180 | 15.0% |
| Clasismo Aspiracional | 4,180 | 15.0% |
| Microagresiones Cotidianas | 4,180 | 15.0% |
| Violencia Simbólica | 4,180 | 15.0% |

### Splits

| Split | Ejemplos | Porcentaje |
|-------|----------|------------|
| Train | 19,518 | 70% |
| Validation | 4,182 | 15% |
| Test | 4,183 | 15% |

### Distribución de Contextos

Los ejemplos aparecen en 12 contextos diferentes:
- Comentarios en redes sociales
- Conversaciones laborales
- Interacciones de servicio al cliente
- Discurso político
- Discusiones familiares
- Entornos educativos
- Espacios públicos
- Comunicación mediática
- Foros en línea
- Aplicaciones de citas
- Grupos de WhatsApp
- Comentarios de YouTube

---

## 🔬 Metodología

Este dataset fue generado usando **generación combinatoria basada en templates**:

```
Templates × Variables × Contextos × Países = 27,883 combinaciones únicas
```

### Ventajas:
- ⚖️ **Balance perfecto** en todas las dimensiones
- 🌎 **Expresiones regionales auténticas** de hablantes nativos
- 🔄 **Metodología reproducible**

### Aseguramiento de Calidad:
- ✅ Revisión manual de templates por hablantes nativos
- ✅ Deduplicación automática (eliminados 2,117 duplicados - 7.06%)
- ✅ Validación regional por hablantes de cada país
- ✅ Verificación de balance (<5% desviación entre países)
- ✅ Cero textos vacíos (100% contenido válido)
- ✅ Longitudes de texto realistas (11-84 caracteres)

### Estructura de Templates:

Cada subcategoría contiene:
- 10-15 **templates clasistas** con variables
- 8-10 **templates inclusivos** con variables
- 10-20 **variables** por template
- **Modismos regionales** inyectados por país (30% de probabilidad)

Ejemplo de template:
```python
"Los de {zona_pobre} son todos {estereotipo_criminal}"
# Se convierte en México: "Los de Tepito son todos rateros"
# Se convierte en Argentina: "Los de la villa son todos ladrones"
```

---

## 📚 Citar Este Dataset

Si usas este dataset en tu investigación, por favor cita:

```bibtex
@dataset{dignityai_clasismo_latam_2025,
  author = {Dromundo, Antonio},
  title = {DignityAI-Clasismo-LATAM: Dataset de Discriminación Socioeconómica en Español Latinoamericano},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/antonnDromundo/DignityAI-Clasismo-LATAM},
  note = {Parte de la Iniciativa DignityAI}
}
```

### Papers Relacionados:

Este dataset se basa en investigación sobre:
- **Aporofobia** (rechazo al pobre) - Adela Cortina
- Clasismo en América Latina
- Detección de discriminación socioeconómica
- NLP en español para justicia social

---

## 📜 Licencia

**CC BY-NC-SA 4.0** (Creative Commons Atribución-NoComercial-CompartirIgual 4.0 Internacional)

### Términos:
- ✅ **Atribución (BY)**: Debes dar crédito apropiado
- ✅ **NoComercial (NC)**: No para uso comercial sin autorización
- ✅ **CompartirIgual (SA)**: Redistribuciones bajo la misma licencia

### Usos permitidos:
- ✅ Investigación y propósitos académicos
- ✅ Materiales educativos
- ✅ Entrenamiento de modelos IA sin fines de lucro
- ✅ Aplicaciones de bien social
- ✅ Proyectos open-source

### Requiere permiso:
- ❌ Productos comerciales
- ❌ Servicios de pago
- ❌ Modelos propietarios

**Para licencia comercial, contactar:** antonio.dromundo@gmail.com

---

## 🤝 Contribuir

¡Damos la bienvenida a contribuciones! Formas de ayudar:

### Reportar Problemas
¿Encontraste errores o sesgos? [Abre un issue](https://github.com/antonnDromundo/DignityAI-Clasismo-LATAM/issues)

### Añadir Ejemplos
Sugiere nuevas expresiones o variantes regionales de tu país

### Validación
Ayuda a validar ejemplos de tu país o región

### Traducción
Ayuda a adaptar a otras variantes del español (peruano, venezolano, etc.)

### Investigación
Publica papers usando este dataset y comparte tus hallazgos

### Código
Contribuye scripts de preprocesamiento, herramientas de análisis o código de entrenamiento

---

## 🔗 Proyectos Relacionados

### Otros Datasets DignityAI:
- **[SinOdio-LATAM](https://huggingface.co/datasets/antonn-dromundo/SinOdio-LATAM-Regional-HateSpeech)** - Discurso de odio general (20K ejemplos)
- **[DignityAI-Machismo-LATAM](https://huggingface.co/datasets/antonn-dromundo/DignityAI-Machismo-LATAM)** - Detección de machismo (18K ejemplos)

### Próximamente:
- **DignityAI-Racism-LATAM** - Discriminación racial
- **DignityAI-Xenophobia-LATAM** - Detección de xenofobia
- **DignityAI-API** - API de detección en tiempo real
- **DignityAI-Models** - Modelos pre-entrenados para todos los datasets

### Datasets Similares:
- HateCheck (inglés)
- DETOXIS (toxicidad en español)
- HateEval (discurso de odio inglés/español)

---

## 👤 Autor

**Antonio Dromundo**

Creador de DignityAI - IA para justicia social en América Latina

- 💼 **LinkedIn:** [antonio-dromundo](https://linkedin.com/in/antonio-dromundo)
- 🐦 **Twitter:** [@antonnDromundo](https://twitter.com/antonnDromundo)
- 💻 **GitHub:** [antonnDromundo](https://github.com/antonnDromundo)
- 📧 **Email:** antonio.dromundo@gmail.com
- 🌐 **Sitio Web:** [dignityai.org](https://dignityai.org) *(próximamente)*

---

## ⚠️ Advertencia de Contenido

**Este dataset contiene ejemplos de lenguaje clasista y discriminatorio con fines de investigación y prevención.**

### Notas Importantes:
- ⚠️ El contenido refleja **lenguaje discriminatorio real** usado en la sociedad
- 🎯 **Propósito:** Entrenar modelos de IA para **detectar y prevenir** discriminación económica
- ❌ El contenido **no refleja** las opiniones o valores del autor
- ✅ Todos los ejemplos emparejados con **alternativas inclusivas**
- 🔬 Para **investigación, educación y bien social** únicamente

**Usar responsablemente. No usar para generar o amplificar discurso de odio.**

---

## 🙏 Agradecimientos

Este proyecto fue posible gracias a:

- **Adela Cortina** - Por su trabajo pionero sobre aporofobia (rechazo al pobre)
- **Organizaciones de justicia social latinoamericanas** - Por documentar patrones de discriminación
- **Comunidad de ética en NLP** - Por metodologías y mejores prácticas
- **Hablantes nativos** de 5 países que validaron expresiones regionales
- **Comunidad DignityAI** - Por retroalimentación y apoyo

Agradecimiento especial a comunidades que luchan contra la discriminación económica en toda América Latina.

---

## 📞 Contacto

### Para preguntas sobre el dataset:
- Abre un issue en GitHub
- Email: antonio.dromundo@gmail.com

### Para oportunidades de colaboración:
- Asociaciones de investigación
- Mejoras al dataset
- Desarrollo de modelos
- Validación regional

### Para licencia comercial:
- Email: antonio.dromundo@gmail.com
- Asunto: "Licencia Comercial DignityAI"

---

## 🌟 Apoya DignityAI

Si este dataset es útil para tu investigación o proyecto:

- ⭐ **Marca con estrella** este repositorio
- 📢 **Comparte** en redes sociales con #DignityAI
- 📝 **Cita** en tus papers
- 🤝 **Contribuye** con mejoras
- 💬 **Difunde** sobre discriminación económica

¡Juntos podemos construir IA que proteja la dignidad humana! 🌍

---

<div align="center">

**🌟 DignityAI - Protegiendo la dignidad humana mediante IA 🌟**

[Sitio Web](https://dignityai.org) • [GitHub](https://github.com/antonnDromundo/DignityAI) • [Twitter](https://twitter.com/antonnDromundo) • [LinkedIn](https://linkedin.com/in/antonio-dromundo)

Hecho con ❤️ para la justicia social en América Latina

</div>
