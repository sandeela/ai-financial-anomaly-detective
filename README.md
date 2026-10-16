# AI Financial Anomaly Detective

A beginner-friendly, **local AI learning prototype** built with **Python, Pandas, Streamlit, Ollama, and Google's Gemma 3 1B open-weight model**. Upload a CSV, identify transactions above a chosen amount threshold, and request a plain-language explanation from a locally running language model.

> This is **not** a validated fraud detection system. It flags amounts above a user-selected threshold; it does not infer whether a payment is fraudulent. Use **synthetic data only** for this tutorial.

## Prerequisites

- Windows with Python installed (`py --version`)
- [Ollama](https://ollama.com/download/windows) installed and running
- Gemma 3 1B downloaded using `ollama run gemma3:1b` (enter `/bye` to exit the chat)

## Run locally

Open PowerShell in this project directory:

```powershell
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

Open http://localhost:8501 and upload `transactions.csv`.

With the default €500 threshold, the synthetic sample has **6 valid transactions and 2 flagged transactions**: €2,800 and €950. Click **Analyze with Gemma AI** to request an explanation from Ollama on `http://localhost:11434/api/generate`.

## Architecture

1. **Streamlit** accepts the CSV upload and displays tables.
2. **Pandas** converts amounts to numbers and flags amounts strictly greater than the threshold.
3. **Python** calculates how much each flagged transaction exceeds the threshold.
4. **Requests** sends up to 20 flagged transaction records to the **local Ollama** API.
5. **Gemma 3 1B** generates a natural-language explanation, which is explicitly labeled unverified.

## Privacy and limitations

- The app's AI request goes to `localhost`, not an external inference provider. Running locally does **not** by itself guarantee confidentiality or security; device security, logs, network exposure, and deployment configuration still matter.
- Ollama/Gemma inference does **not** retrain the model on uploaded data in this workflow.
- The model receives only the first 20 flagged transactions, but the whole CSV is processed by the local Streamlit/Pandas app.
- Small language models can contradict verified data. The AI response is **not automatically validated** and must be reviewed by a person.
- This sample does not implement authentication, audit logging, production data governance, duplicate detection, behavioral baselines, or anomaly-scoring algorithms.
- Local use avoids paid inference API charges; you still supply your own computer and electricity. Check the licenses of each dependency/model before redistribution or commercial use.

## Example input format

```csv
Date,Merchant,Amount
2026-10-10,Supermarket,45
2026-10-12,Electronics Store,2800
```

## Troubleshooting

- **Blank Streamlit page:** Refresh the browser and inspect PowerShell for errors.
- **Cannot connect to Ollama:** Make sure Ollama is running and `ollama run gemma3:1b` has downloaded the model.
- **Missing modules:** Run `py -m pip install -r requirements.txt` again.

## Next steps

Add duplicate-transaction checks, robust anomaly detection, evidence-backed summaries, and numerical output validation before considering any serious financial use.
