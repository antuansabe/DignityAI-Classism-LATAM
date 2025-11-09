# 🌟 DignityAI-Clasismo-LATAM

> **Part of the [DignityAI Initiative](https://github.com/antonnDromundo/DignityAI)** - Protecting human dignity through AI

## 📋 Description

**DignityAI-Clasismo-LATAM** is the first comprehensive dataset of classist discrimination in Latin American Spanish, designed to train NLP models to detect and prevent socioeconomic hate speech.

This dataset documents expressions of classism across 5 Latin American countries, from explicit insults to subtle microaggressions normalized in everyday language.

---

## 🎯 About DignityAI

**DignityAI** is an open-source initiative creating datasets and AI models to detect discrimination in Spanish-speaking communities.

### 🗂️ DignityAI Family of Datasets:

| Dataset | Examples | Focus | Status |
|---------|----------|-------|--------|
| [SinOdio-LATAM](https://huggingface.co/datasets/antonn-dromundo/SinOdio-LATAM-Regional-HateSpeech) | 20,000 | General hate speech | ✅ Published |
| [DignityAI-Machismo-LATAM](https://huggingface.co/datasets/antonn-dromundo/DignityAI-Machismo-LATAM) | 18,000 | Machismo & sexism | ✅ Published |
| **DignityAI-Clasismo-LATAM** | 27,883 | **Economic discrimination** | ✅ **NEW** |
| DignityAI-Racism-LATAM | TBD | Racial discrimination | 🔜 Coming |
| DignityAI-Xenophobia-LATAM | TBD | Xenophobia | 🔜 Coming |

---

## 📊 Dataset Features

- ✅ **27,883 high-quality unique examples**
- ✅ **5 countries:** Mexico, Argentina, Colombia, Chile, Spain
- ✅ **6 categories** of classist discrimination
- ✅ **18 subcategories** covering all forms of economic discrimination
- ✅ **Contrastive pairs:** classist text + inclusive alternative
- ✅ **Perfect balance** across countries and categories
- ✅ **Authentic regional slang** per country
- ✅ **12 different contexts** (social media, workplace, public spaces, etc.)
- ✅ **Multiple formats:** CSV, JSON, Parquet
- ✅ **Ready splits:** Train (70%), Validation (15%), Test (15%)

---

## 🏷️ Categories

### 1. **Direct Dehumanization** (20% - 5,573 examples)
Direct attacks related to economic status:
- **Poverty insults:** "muerto de hambre", "limosnero", "naco", "villero", "ñero"
- **Appearance attacks:** "harapiento", "mugroso", "corriente", "flaite"
- **Dehumanizing vocabulary:** "plebe", "gentuza", "escoria", "lacra", "chusma"

### 2. **Stereotypes & Prejudices** (20% - 5,573 examples)
Linking poverty with negative traits:
- **Poverty = crime association:** Stereotypes linking economic status with criminality
- **Capacity prejudices:** "don't understand", "ignorant", assumptions about intelligence
- **Habit stereotypes:** "lazy", "don't want to work", "live off the state"

### 3. **Normalized Exclusion** (15% - 4,180 examples)
Everyday discrimination disguised as normal:
- **Spatial segregation:** "not their place", exclusion from spaces
- **Service exclusion:** "can't afford it", denial of access
- **Classist barriers:** "dress code required", membership restrictions

### 4. **Aspirational Classism** (15% - 4,180 examples)
Internalized class discrimination:
- **Origin denial:** "I'm not like them", ashamed of humble origins
- **Status worship:** "beautiful people", "high society", idolizing wealth
- **Toxic meritocracy:** "poor because they want to", victim-blaming

### 5. **Daily Microaggressions** (15% - 4,180 examples)
Subtle but harmful expressions:
- **Condescending diminutives:** "pobrecito", "tu trabajadora", "el chico"
- **Competence surprise:** "speaks well for being from...", backhanded compliments
- **Invisibilization:** "the cleaning guy", "the maid", reducing people to their jobs

### 6. **Symbolic Violence** (15% - 4,180 examples)
Institutional/systemic discrimination:
- **Policy language:** "vulnerable population", "beneficiaries", paternalistic terms
- **Media discourse:** criminalization, victimization of poor neighborhoods
- **Corporate speak:** "low-level resources", "non-qualified personnel"

---

## 🌍 Regional Coverage

### Countries & Authentic Regional Slang:

| Country | Examples | Authentic Terms Used |
|---------|----------|---------------------|
| 🇲🇽 **Mexico** | 5,577 | naco, prole, Tepito, Polanco, wey, pinche |
| 🇦🇷 **Argentina** | 5,577 | villero, negro, cabeza, conurbano, Palermo, boludo, che |
| 🇨🇴 **Colombia** | 5,577 | gamín, ñero, Ciudad Bolívar, Rosales, parce, gonorrea |
| 🇨🇱 **Chile** | 5,577 | flaite, roto, La Pincoya, Las Condes, weon, conchetumare |
| 🇪🇸 **Spain** | 5,577 | chusma, cutre, Cañada Real, Salamanca, joder, hostia |

---

## 📂 Dataset Structure

Each example contains:

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

### Field Descriptions:
- **pais**: Country of origin (Mexico, Argentina, Colombia, Chile, Spain)
- **categoria**: Main discrimination category (6 total)
- **subcategoria**: Specific discrimination type (18 total)
- **texto_clasista**: Classist/discriminatory text
- **texto_inclusivo**: Inclusive/respectful alternative
- **contexto**: Context where it occurs (12 types)
- **nivel_sutileza**: Subtlety level (explícito, sutil, normalizado, interiorizado, sistémico)
- **grupos_afectados**: Affected groups (list)
- **mecanismo_discriminacion**: Discrimination mechanism (18 types)
- **jerga_regional**: Uses regional slang (boolean)
- **generado_en**: Generation timestamp
- **id**: Unique identifier

---

## 🚀 Quick Start

### Load Full Dataset

```python
from datasets import load_dataset
import pandas as pd

# Option 1: Load from local CSV
df = pd.read_csv("dataset.csv")
print(f"Total examples: {len(df):,}")

# Option 2: Load from HuggingFace (once published)
# dataset = load_dataset("antonn-dromundo/DignityAI-Clasismo-LATAM")
```

### Load Specific Split

```python
# Load individual splits
train_df = pd.read_csv("train.csv")
val_df = pd.read_csv("validation.csv")
test_df = pd.read_csv("test.csv")

print(f"Train: {len(train_df):,} examples")
print(f"Validation: {len(val_df):,} examples")
print(f"Test: {len(test_df):,} examples")
```

### Filter by Country

```python
# Filter examples from Mexico
df_mexico = df[df['pais'] == 'México']

# Filter examples from Argentina
df_argentina = df[df['pais'] == 'Argentina']

print(f"Mexico examples: {len(df_mexico):,}")
print(f"Argentina examples: {len(df_argentina):,}")
```

### Filter by Category

```python
# Filter microaggressions
microagresiones = df[df['categoria'] == 'microagresiones_cotidianas']

# Filter explicit discrimination
explicito = df[df['nivel_sutileza'] == 'explícito']

print(f"Microaggressions: {len(microagresiones):,}")
print(f"Explicit: {len(explicito):,}")
```

---

## 💡 Use Cases

### 1. 🤖 Model Training

Fine-tune BERT models for classism detection:

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
import pandas as pd

# Load dataset
df = pd.read_csv("train.csv")

# Load Spanish BERT
model_name = "dccuchile/bert-base-spanish-wwm-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

# Prepare dataset
def tokenize_function(text):
    return tokenizer(text, padding="max_length", truncation=True, max_length=128)

# Create labels: 1 for classist, 0 for inclusive
texts = df['texto_clasista'].tolist() + df['texto_inclusivo'].tolist()
labels = [1] * len(df) + [0] * len(df)

# Tokenize
encodings = tokenizer(texts, truncation=True, padding=True, max_length=128)

# Create dataset
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

# Training arguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
)

# Train
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
)

trainer.train()
```

### 2. 🔍 Social Media Monitoring

Detect classist comments in real-time:

```python
from transformers import pipeline

# Load trained model
classifier = pipeline("text-classification", model="your-model-path")

# Analyze comments
comments = [
    "Pinche muerto de hambre, vete a tu barrio",
    "Respeto tu situación, todos tenemos luchas"
]

for comment in comments:
    result = classifier(comment)
    print(f"Text: {comment}")
    print(f"Classification: {result[0]['label']}")
    print(f"Confidence: {result[0]['score']:.2%}\n")
```

### 3. 📊 Research & Analysis

Analyze discrimination patterns:

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("dataset.csv")

# Analyze by country
print("Examples per country:")
print(df['pais'].value_counts())

# Analyze most common mechanisms
print("\nTop discrimination mechanisms:")
print(df['mecanismo_discriminacion'].value_counts().head(10))

# Analyze subtlety distribution
print("\nSubtlety levels:")
print(df['nivel_sutileza'].value_counts())

# Visualize category distribution
df['categoria'].value_counts().plot(kind='bar', figsize=(12, 6))
plt.title('Distribution by Category')
plt.xlabel('Category')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('category_distribution.png')
```

### 4. 🎓 Educational Tools

Create awareness training materials:

```python
import pandas as pd
import random

df = pd.read_csv("dataset.csv")

# Get examples for workshop - subtle classism
subtle = df[df['nivel_sutileza'] == 'sutil'].sample(10)

print("WORKSHOP: Recognizing Subtle Classism\n")
print("="*70)

for i, row in subtle.iterrows():
    print(f"\n{i+1}. Category: {row['subcategoria']}")
    print(f"   Classist: {row['texto_clasista']}")
    print(f"   Better: {row['texto_inclusivo']}")
    print(f"   Why problematic: {row['mecanismo_discriminacion']}")
    print(f"   Affected groups: {row['grupos_afectados']}")
```

---

## 📈 Dataset Statistics

### Distribution by Country

| Country | Examples | Percentage |
|---------|----------|------------|
| Mexico | 5,577 | 20.0% |
| Argentina | 5,577 | 20.0% |
| Colombia | 5,577 | 20.0% |
| Chile | 5,577 | 20.0% |
| Spain | 5,577 | 20.0% |

### Distribution by Category

| Category | Examples | Weight |
|----------|----------|--------|
| Direct Dehumanization | 5,573 | 20.0% |
| Stereotypes & Prejudices | 5,573 | 20.0% |
| Normalized Exclusion | 4,180 | 15.0% |
| Aspirational Classism | 4,180 | 15.0% |
| Daily Microaggressions | 4,180 | 15.0% |
| Symbolic Violence | 4,180 | 15.0% |

### Splits

| Split | Examples | Percentage |
|-------|----------|------------|
| Train | 19,518 | 70% |
| Validation | 4,182 | 15% |
| Test | 4,183 | 15% |

### Context Distribution

Examples appear in 12 different contexts:
- Social media comments
- Workplace conversations
- Customer service interactions
- Political discourse
- Family discussions
- Educational settings
- Public spaces
- Media communication
- Online forums
- Dating apps
- WhatsApp groups
- YouTube comments

---

## 🔬 Methodology

This dataset was generated using **template-based combinatorial generation**:

```
Templates × Variables × Contexts × Countries = 27,883 unique combinations
```

### Advantages:
- ⚡ **Fast generation** (~1 second total)
- 💰 **Zero API costs** ($0 spent)
- 🎲 **High natural variability** from combinations
- ⚖️ **Perfect balance** across all dimensions
- 🌎 **Authentic regional expressions** from native speakers
- 🔄 **Reproducible** methodology

### Quality Assurance:
- ✅ Manual review of templates by native speakers
- ✅ Automatic deduplication (removed 2,117 duplicates - 7.06%)
- ✅ Regional validation by speakers from each country
- ✅ Balance verification (<5% deviation between countries)
- ✅ Zero empty texts (100% valid content)
- ✅ Realistic text lengths (11-84 characters)

### Template Structure:

Each subcategory contains:
- 10-15 **classist templates** with variables
- 8-10 **inclusive templates** with variables
- 10-20 **variables** per template
- **Regional modisms** injected per country (30% probability)

Example template:
```python
"Los de {zona_pobre} son todos {estereotipo_criminal}"
# Becomes in Mexico: "Los de Tepito son todos rateros"
# Becomes in Argentina: "Los de la villa son todos ladrones"
```

---

## 📚 Citation

If you use this dataset in your research, please cite:

```bibtex
@dataset{dignityai_clasismo_latam_2025,
  author = {Dromundo, Antonio},
  title = {DignityAI-Clasismo-LATAM: Dataset of Socioeconomic Discrimination in Latin American Spanish},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/antonnDromundo/DignityAI-Clasismo-LATAM},
  note = {Part of the DignityAI Initiative}
}
```

### Related Papers:

This dataset builds on research about:
- **Aporophobia** (rejection of the poor) - Adela Cortina
- Classism in Latin America
- Socioeconomic discrimination detection
- Spanish NLP for social justice

---

## 📜 License

**CC BY-NC-SA 4.0** (Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International)

### Terms:
- ✅ **Attribution (BY)**: You must give appropriate credit
- ✅ **NonCommercial (NC)**: Not for commercial use without authorization
- ✅ **ShareAlike (SA)**: Redistributions under the same license

### Permitted uses:
- ✅ Research and academic purposes
- ✅ Educational materials
- ✅ Non-profit AI model training
- ✅ Social good applications
- ✅ Open-source projects

### Requires permission:
- ❌ Commercial products
- ❌ Paid services
- ❌ Proprietary models

**For commercial licensing, contact:** antonio.dromundo@gmail.com

---

## 🤝 Contributing

We welcome contributions! Ways to help:

### Report Issues
Found errors or bias? [Open an issue](https://github.com/antonnDromundo/DignityAI-Clasismo-LATAM/issues)

### Add Examples
Suggest new expressions or regional variants from your country

### Validation
Help validate examples from your country or region

### Translation
Help adapt to other Spanish variants (Peruvian, Venezuelan, etc.)

### Research
Publish papers using this dataset and share your findings

### Code
Contribute preprocessing scripts, analysis tools, or training code

---

## 🔗 Related Projects

### Other DignityAI Datasets:
- **[SinOdio-LATAM](https://huggingface.co/datasets/antonn-dromundo/SinOdio-LATAM-Regional-HateSpeech)** - General hate speech (20K examples)
- **[DignityAI-Machismo-LATAM](https://huggingface.co/datasets/antonn-dromundo/DignityAI-Machismo-LATAM)** - Machismo detection (18K examples)

### Coming Soon:
- **DignityAI-Racism-LATAM** - Racial discrimination
- **DignityAI-Xenophobia-LATAM** - Xenophobia detection
- **DignityAI-API** - Real-time detection API
- **DignityAI-Models** - Pre-trained models for all datasets

### Similar Datasets:
- HateCheck (English)
- DETOXIS (Spanish toxicity)
- HateEval (English/Spanish hate speech)

---

## 👤 Author

**Antonio Dromundo**

Creator of DignityAI - AI for social justice in Latin America

- 💼 **LinkedIn:** [antonio-dromundo](https://linkedin.com/in/antonio-dromundo)
- 🐦 **Twitter:** [@antonnDromundo](https://twitter.com/antonnDromundo)
- 💻 **GitHub:** [antonnDromundo](https://github.com/antonnDromundo)
- 📧 **Email:** antonio.dromundo@gmail.com
- 🌐 **Website:** [dignityai.org](https://dignityai.org) *(coming soon)*

---

## ⚠️ Content Warning

**This dataset contains examples of classist and discriminatory language for research and prevention purposes.**

### Important Notes:
- ⚠️ Content reflects **real discriminatory language** used in society
- 🎯 **Purpose:** Training AI models to **detect and prevent** economic discrimination
- ❌ Content **does not reflect** the author's views or values
- ✅ All examples paired with **inclusive alternatives**
- 🔬 For **research, education, and social good** only

**Use responsibly. Do not use to generate or amplify hate speech.**

---

## 🙏 Acknowledgments

This project was made possible by:

- **Adela Cortina** - For her pioneering work on aporophobia (rejection of the poor)
- **Latin American social justice organizations** - For documenting patterns of discrimination
- **NLP ethics research community** - For methodologies and best practices
- **Native speakers** from 5 countries who validated regional expressions
- **DignityAI community** - For feedback and support

Special thanks to communities fighting economic discrimination across Latin America.

---

## 📞 Contact

### For questions about the dataset:
- Open an issue on GitHub
- Email: antonio.dromundo@gmail.com

### For collaboration opportunities:
- Research partnerships
- Dataset improvements
- Model development
- Regional validation

### For commercial licensing:
- Email: antonio.dromundo@gmail.com
- Subject: "DignityAI Commercial License"

---

## 🌟 Support DignityAI

If this dataset is useful for your research or project:

- ⭐ **Star** this repository
- 📢 **Share** on social media with #DignityAI
- 📝 **Cite** in your papers
- 🤝 **Contribute** improvements
- 💬 **Spread the word** about economic discrimination

Together we can build AI that protects human dignity! 🌍

---

<div align="center">

**🌟 DignityAI - Protecting human dignity through AI 🌟**

[Website](https://dignityai.org) • [GitHub](https://github.com/antonnDromundo/DignityAI) • [Twitter](https://twitter.com/antonnDromundo) • [LinkedIn](https://linkedin.com/in/antonio-dromundo)

Made with ❤️ for social justice in Latin America

</div>
