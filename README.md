**# Ollama Library Scraper**

A Python data-analysis pipeline that scrapes model information from the **Ollama model library**, cleans and normalizes the collected data, calculates model efficiency metrics, identifies **Pareto frontiers**, and visualizes the resulting model trade-offs in 2D or 3D.

**---**

**## Version**

****v2.0.0****

**---**

**## Features**

* Scrape model families and model variants from the Ollama model library.

* Extract model information including:

* Full model name.

* Model family.

* Model variant.

* Storage size.

* Context length.

* Capabilities.

* Modalities.

* Scrape multiple model families in parallel using `ThreadPoolExecutor`.

* Clean scraped data using configurable filtering rules.

* Remove unsupported, unwanted, and embedding models.

* Normalize model parameter counts.

* Normalize storage sizes into GB.

* Normalize context lengths into thousands of tokens.

* Calculate parameter efficiency.

* Calculate context efficiency.

* Calculate additive normalized efficiency.

* Calculate multiplicative normalized efficiency.

* Calculate a **2-variable Pareto frontier** using parameter/storage and context/storage.

* Calculate a **3-variable Pareto frontier** using parameter, context, and storage.

* Generate a 2D efficiency visualization.

* Generate a 3D Pareto-frontier visualization.

* Display accepted and rejected models using different colors.

* Display processing durations for individual pipeline stages.

* Centralize all configurable settings in `main.py`.

* Uses typed `TypedDict` structures to maintain consistent data between pipeline stages.

**---**

## Project Structure

```text
ollama-model-analyzer/
├── whole_web/
    ├── main.py
    ├── constants.py
    ├── a_scraping.py
    ├── b_cleaning.py
    ├── c_normalizing.py
    ├── d_comparing.py
    ├── e_visualizing.py
├── README.md
├── requirements.txt
└── LICENSE
```

**---**

## Explanation

The program processes Ollama model data through five main stages:

1. **Scraping** — Collect model information from the Ollama model library.

2. **Cleaning** — Remove models that do not satisfy the configured filtering rules.

3. **Normalizing** — Convert textual model information into numerical values.

4. **Comparing** — Calculate efficiency metrics and Pareto frontiers.

5. **Visualizing** — Display the resulting comparisons as 2D or 3D graphs.

The complete pipeline is:

```text
Ollama Library
      ↓
   Scraping
      ↓
   Cleaning
      ↓
 Normalizing
      ↓
  Comparing
      ↓
 Visualizing
```

### Data Collection

The scraper starts from the Ollama model library and collects the available model-family URLs.

Each model family is then scraped independently.

The collected data includes:

```text
Full Name
Family
Variant
Storage
Context
Capabilities
Modalities
```

Model families are scraped in parallel using `ThreadPoolExecutor`.

### Data Cleaning

The cleaning stage removes models that do not meet the configured requirements.

Current banned families include:

```text
bge
embed
```

Current banned variant keywords include:

```text
cloud
latest
mlx
x
q
fp
```

Models are also rejected when:

```text
Variant is missing
Storage is missing
Variant begins with "e"
Variant does not contain a parameter size
Model has embedding capability
```

Accepted and rejected models can optionally be displayed separately.

### Normalization

The normalization stage converts the scraped text values into numerical values.

#### Parameters

Parameter counts are converted into billions:

```text
7b      → 7.0
13b     → 13.0
500m    → 0.5
```

#### Storage

Storage is converted into GB:

```text
500MB   → 0.5 GB
7GB     → 7.0 GB
1TB     → 1000.0 GB
```

#### Context

Context length is converted into thousands of tokens:

```text
8K      → 8
32K     → 32
1M      → 1000
```

Parameter count and context length are then min-max normalized:

```text
Normalized Value = (Value - Minimum) / (Maximum - Minimum)
```

### Efficiency

The comparison stage calculates several efficiency metrics.

#### Parameter Efficiency

```text
Parameter Efficiency = Parameters / Storage
```

This represents the number of model parameters, in billions, per GB of storage.

#### Context Efficiency

```text
Context Efficiency = Context / Storage
```

This represents the context length, in thousands of tokens, per GB of storage.

#### Additive Normalized Efficiency

```text
(parameter_normalized + context_normalized) / storage
```

#### Multiplicative Normalized Efficiency

```text
(parameter_normalized × context_normalized) / storage
```

The additive and multiplicative metrics are additional comparison measures and do not define Pareto dominance.

### Pareto Frontier

The project uses Pareto dominance rather than reducing all objectives into a single score.

A model is dominated when another model is at least as good in every relevant objective and strictly better in at least one.

#### 2-Variable Frontier

The 2-variable frontier uses:

```text
Parameter Efficiency → Maximize
Context Efficiency   → Maximize
```

The comparison is therefore:

```text
Parameter / Storage
Context / Storage
```

#### 3-Variable Frontier

The 3-variable frontier uses:

```text
Parameters → Maximize
Context    → Maximize
Storage    → Minimize
```

This preserves the trade-off between model size, context length, and storage requirements.

The Pareto frontier is therefore a **set of non-dominated models**, rather than a single objectively best model.

### Visualization

The visualization mode is controlled through `VARIABLE_COUNT` in `main.py`.

```text
VARIABLE_COUNT = 2
```

generates a 2D plot:

```text
X = Parameter Efficiency
Y = Context Efficiency
```

Both axes use logarithmic scaling.

```text
VARIABLE_COUNT = 3
```

generates a 3D plot:

```text
X = Parameters (B)
Y = Storage (GB)
Z = Context (K)
```

The plots display both the complete model dataset and the corresponding Pareto frontier.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/ollama-library-scraper.git

cd ollama-library-scraper
```

### Requirements

Install the required packages:

```bash
pip install requests beautifulsoup4 colorama matplotlib
```

Alternatively, the project includes a `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Configuration

All configurable settings are located in `main.py`.

```python
DEBUG_SCRAPE: bool = True

DEBUG_CLEAN_ACCEPTED: bool = True
DEBUG_CLEAN_REJECTED: bool = True

DEBUG_NORMALIZE: bool = False

DEBUG_COMPARE: bool = False

VARIABLE_COUNT: int = 2
```

`VARIABLE_COUNT` accepts:

```text
2 → 2D storage-efficiency visualization
3 → 3D Pareto-frontier visualization
```

No `.env` file or additional configuration is required.

**---**

## Usage

Run the program:

```bash
python main.py
```

The program will:

1. Scrape the Ollama model library.

2. Clean the scraped model data.

3. Normalize the numerical values.

4. Calculate the selected Pareto frontier.

5. Display the frontier information.

6. Generate the selected visualization.

For example:

```python
VARIABLE_COUNT: int = 2
```

produces a 2D storage-efficiency comparison.

Changing it to:

```python
VARIABLE_COUNT: int = 3
```

produces a 3D parameter/storage/context comparison.

Debug output can be enabled or disabled independently through the configuration variables in `main.py`.

**---**

## Dependencies

* Python 3.10+

* `requests`

* `beautifulsoup4`

* `colorama`

* `matplotlib`

* Standard Library

* `typing`

* `time`

* `concurrent.futures`

* `urllib.parse`

**---**
**## Attribution**

This project is an independent tool and is not affiliated with or endorsed by Ollama.

Model information is collected from the publicly accessible Ollama model library:
https://ollama.com/library

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.
