# 🕷️ ScrapeGraphAI: You Only Scrape Once

ScrapeGraphAI is a *web scraping* python library based on LangChain which uses LLM and direct graph logic to create scraping pipelines.
Just say which information you want to extract and the library will do it for you!

<p align="center">
  <img src="https://raw.githubusercontent.com/VinciGit00/Scrapegraph-ai/main/docs/assets/scrapegraphai_logo.png" alt="Scrapegraph-ai Logo" style="width: 50%;">
</p>


## 🚀 Quick install

The reference page for Scrapegraph-ai is avaible on the official page of pypy: [pypi](https://pypi.org/project/scrapegraphai/).

```bash
pip install scrapegraphai
```
## 🔍 Demo

Try out ScrapeGraphAI in your browser:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1sEZBonBMGP44CtO6GQTwAlL0BGJXjtfd?usp=sharing)

## 📖 Documentation

The documentation for ScrapeGraphAI can be found [here](https://scrapegraph-ai.readthedocs.io/en/latest/).
Behind this there is also the docusaurus documentation [here](https://scrapegraph-doc.onrender.com/)).

## Setup the api keys

Follow the procedure on the following link to setup your OpenAI API key: [link](https://scrapegraph-ai.readthedocs.io/en/latest/index.html).

## 💻 Usage

### Case 1: Extracting information using a prompt

You can use the `SmartScraper` class to extract information from a website using a prompt.

The `SmartScraper` class is a direct graph implementation that uses the most common nodes present in a web scraping pipeline. For more information, please see the [documentation](https://scrapegraph-ai.readthedocs.io/en/latest/).

```python
from scrapegraphai.graphs import SmartScraper

OPENAI_API_KEY = "YOUR_API_KEY"

llm_config = {
    "api_key": OPENAI_API_KEY,
    "model_name": "gpt-3.5-turbo",
}

smart_scraper = SmartScraper("List me all the titles and project descriptions",
                             "https://perinim.github.io/projects/", llm_config)

answer = smart_scraper.run()
print(answer)
```

The output will be a dictionary with the extracted information, for example:

```bash
{
    'titles': [
        'Rotary Pendulum RL'
        ],
    'descriptions': [
        'Open Source project aimed at controlling a real life rotary pendulum using RL algorithms'
        ]
}
```

## 🤝 Contributing

Scrapegraph-ai is [MIT LICENSED](https://github.com/VinciGit00/Scrapegraph-ai/blob/main/LICENSE).

Contributions are welcome! Please check out the todos below, and feel free to open a pull request.

For more information, please see the [contributing guidelines](https://github.com/VinciGit00/Scrapegraph-ai/blob/main/CONTRIBUTING.md).

Join our Discord server to discuss with us improvements and give us suggestions!

[![Join Discord Server](https://img.shields.io/badge/Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/DujC7HG8)
 

## Contributors
[![Contributors](https://contrib.rocks/image?repo=VinciGit00/Scrapegraph-ai)](https://github.com/VinciGit00/Scrapegraph-ai/graphs/contributors)

## Authors

<p align="center">
  <img src="https://raw.githubusercontent.com/VinciGit00/Scrapegraph-ai/main/docs/assets/logo_authors.png" alt="Authors Logos">
</p>

## 📜 License

ScrapeGraphAI is licensed under the Apache 2.0 License. See the [LICENSE](https://github.com/VinciGit00/Scrapegraph-ai/blob/main/LICENSE) file for more information.

## Acknowledgements

- We would like to thank all the contributors to the project and the open-source community for their support.
- ScrapeGraphAI is meant to be used for data exploration and research purposes only. We are not responsible for any misuse of the library.

## Thanks to: 
- [nicolapiazzalunga](https://github.com/nicolapiazzalunga) for having inspired us to the functions: scrapegraph/convert_to_json.py and scrapegraph/convert_to_csv.py
