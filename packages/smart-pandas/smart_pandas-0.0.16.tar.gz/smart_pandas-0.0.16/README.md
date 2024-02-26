# SMART_PANDAS 🤖 [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1imiAh-Q8iuAA4q4L7GLAPG-_IMOg9VoL?usp=sharing)

### Supercharge your data science workflows with 🐐 Ollama models.

---

`smart-pandas` is a Python library highly inspired by the pandas-gpt, to perform the diverse operations on a [pandas](https://pandas.pydata.org/) DataFrame using llama 2 model.

## Installation

### First install the ollama from 🐐[ollama](https://ollama.com/download). Ollama is required and need to be installed must.


```bash
pip install smart-pandas
```

## Examples

```python
import pandas as pd
import smart_pandas

df = pd.DataFrame('https://raw.githubusercontent.com/owid/covid-19-data/master/scripts/input/un/handwashing_facilities.csv')

# Data transformation
df = df.ask('Remove iso_code')

# Queries
top_10 = df.ask('what are the top 10 most locations having handwashing_facilities, as a table')

# Plotting
top_10=top_10.ask("Reset index")
top_10.ask('horizontal bar plot, seaborn colors with width 700')

```

### Aurthor

***Muntakimur Rahaman***

Senior Data Scientist,

Innova-analytics.ai

Contact: [muntakim.cse@gmail.com](mailto:muntakim.cse@gmail.com)


## Alternatives

- [pandas-gpt](https://github.com/rvanasa/pandas-gpt): OpenAI based pandas auto-completion (Paid api key)
- [GitHub Copilot](https://github.com/features/copilot): General-purpose code completion (paid subscription)
- [Sketch](https://github.com/approximatelabs/sketch): AI-powered data summarization and code suggestions (works without an API key)

## Disclaimer

Please note that the [limitations](https://github.com/ollama/gpt-3/blob/master/model-card.md#limitations) of llama 2 also apply to this library. I would recommend using `smart-pandas` in a sandboxed environment such as [Google Colab](https://colab.research.google.com), [Kaggle](https://www.kaggle.com/docs/notebooks), or [GitPod](https://www.gitpod.io/).