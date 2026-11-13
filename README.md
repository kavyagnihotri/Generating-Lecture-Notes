# Generating-Lecture-Notes

A research project on automatically building lecture-note material for technical concepts. Starting from the TeKnowbase list of technical entities, we:

1. collected the Wikipedia page for each entity,
2. extracted its images, captions and summary text,
3. built a concept graph from the links between entity pages (with first- and second-hop neighbours), and
4. trained a BERT token-classification model that predicts where an image belongs in a passage of text.

> This project is archived and no longer maintained.

## Repository layout

```
starting_material/   TeKnowbaseEntities.tsv: the original entity list (name, URI)
scripts/             Data collection and preprocessing scripts (Python)
csv_files/           CSV outputs of the scripts
downloads/           Entity summaries and the two-hop concept lists
token-classification/ Training code for the image-location model (HuggingFace run_ner.py)
output.txt           Sample of the token-labelled text produced by task8
```

## Pipeline

All scripts are meant to be run from the repository root, e.g. `python scripts/task4b_wikiSummary.py`. They use `requests` + `BeautifulSoup` to scrape Wikipedia.

### 1. Entities
- **`getWikiEntities.py`**: filters `TeKnowbaseEntities.tsv` down to entities that have a Wikipedia URL → `csv_files/wikiEntities.csv` (~85.8k entities).

### 2. Images
- **`extractWikiImages.py`**: gets the main image of each page (from the infobox, or else the first right-floated thumbnail).
- **`newImages.py`** / **`task2_images.py`**: add a second and third image per page → `csv_files/wiki3Images.csv`.
- **`task6_reExtractImages.py`**: extracts up to three images per page together with their captions → `csv_files/wikiImagesWithText.csv`.
- **`extractWikiPseudoCodes.py`**: collects `<pre>` blocks (pseudo-code / code samples) from each page.

### 3. Concept graph
- **`task3_entityMap.py`**: for each entity, reads the opening paragraphs of its page and records which linked pages are also known entities → `csv_files/entity_map_complete.csv` (adjacency list).
- **`task4_twoHops.py`**: turns the adjacency list into first-hop and second-hop neighbours for every entity. The resulting concept lists are in `downloads/FullTwoHopsConcepts.csv`, where first-hop concepts are marked with `$1$`.

### 4. Summaries
- **`task4b_wikiSummary.py`**: fetches a short summary (the first few paragraphs) for each entity. It prefers Simple English Wikipedia and falls back to English Wikipedia.
- **`task5_summarize.py`**: combines the two-hop graph with the summaries, gathering the summaries of an entity and its neighbours.
- `downloads/DictSummary{2,5,10}.txt`: dictionaries mapping each entity to its summary text.

### 5. Image-location dataset
The goal is to learn where in a text an image should be placed. Each page's text is extracted with every `<img>` replaced by an `$IMG$` marker:

- **`task7_modifyExtractedPages.py`**, **`task7-2_prepare_img_data.py`**, **`task7-3_prepare_img_data.py`**: successive versions of the page-text extraction. The last one writes one file per entity to `pages/`.
- **`task8_prepareData.py`**: converts the page text to CoNLL-style token labels (sample in `output.txt`).
- **`dataset_for_token-class.py`**: the final dataset builder. It cleans the text, splits it into chunks of up to 700 words that contain an image, and labels the sentence just before each `$IMG$` with `B-IMG` / `I-IMG` (everything else is `O`). It writes JSON Lines files with `tokens` and `tags`:
  - `json_files/train.json`: 25,000 examples
  - `json_files/validation.json`: 6,000 examples
  - `json_files/test.json`: 1,500 examples
- **`helper/validate.py`**: checks that every example has the same number of tokens and tags.

### 6. Model training
`token-classification/` contains HuggingFace's token-classification example (`run_ner.py`), used to fine-tune `bert-base-uncased` on the image-location dataset.

```bash
cd token-classification
pip install -r requirements.txt
bash run_custom.sh          # local run
sbatch run_custom_job.sh    # SLURM job on a GPU node
```

The scripts expect the data in `../data/image-location/` and save the model to `../models/image-location/`. The `.out` / `.err` files are the logs from the training runs on the cluster.

## Other files
- `scripts/classify_entities.py`: an unfinished experiment to classify entities as Scientific / Technical / Other with DistilBERT.

## Dependencies
Python 3 with `requests`, `beautifulsoup4`, `pandas`, `numpy`, `tqdm`, plus `token-classification/requirements.txt` (`transformers`, `datasets`, `evaluate`, `seqeval`, `accelerate`, `torch`) for training.
