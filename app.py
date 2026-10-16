import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title='AI Financial Anomaly Detective', layout='wide')
st.title('AI Financial Anomaly Detective')
st.caption('A local AI learning prototype using Python, Streamlit, Ollama and Gemma 3 1B.')

uploaded = st.file_uploader('Upload a CSV with Date, Merchant, Amount columns', type='csv')
if uploaded is not None:
    try:
        data = pd.read_csv(uploaded)
    except Exception as exc:
        st.error(f'Unable to read CSV: {exc}')
        st.stop()
    if not {'Date', 'Merchant', 'Amount'}.issubset(data.columns):
        st.error('CSV must contain Date, Merchant, and Amount columns.')
        st.stop()
    data['Amount'] = pd.to_numeric(data['Amount'], errors='coerce')
    invalid = int(data['Amount'].isna().sum())
    if invalid:
        st.warning(f'Skipping {invalid} rows with invalid amounts.')
    data = data.dropna(subset=['Amount'])
    threshold = st.number_input('Flag transactions above (€)', min_value=0.0, value=500.0, step=50.0)
    flagged = data.loc[data['Amount'] > threshold].copy()
    flagged['Exceeds threshold by (€)'] = (flagged['Amount'] - threshold).round(2)
    left, right = st.columns(2)
    left.metric('Valid transactions', len(data))
    right.metric('Flagged transactions', len(flagged))
    st.subheader('All transactions')
    st.dataframe(data, use_container_width=True)
    st.subheader('Flagged transactions')
    st.dataframe(flagged, use_container_width=True)
    if st.button('Analyze with Gemma AI'):
        if flagged.empty:
            st.info('No transactions exceed the chosen threshold.')
        else:
            # Only the first 20 flagged rows are sent to the locally running model.
            evidence = flagged.head(20)[['Date', 'Merchant', 'Amount', 'Exceeds threshold by (€)']]
            prompt = (
                'You are assisting with a review of synthetic financial transactions. '
                'The Python calculations below are authoritative. '
                'All listed transactions exceed the threshold. '
                'Explain why each transaction merits verification, without asserting fraud. '
                'Do not contradict the numerical facts, invent details, or claim access to other records. '
                'Suggest practical verification steps.\n\n'
                f'Threshold: €{threshold:.2f}\n'
                f'Python-verified records: {evidence.to_json(orient="records")}\n'
            )
            with st.spinner('Requesting a local Gemma explanation...'):
                try:
                    result = requests.post(
                        'http://localhost:11434/api/generate',
                        json={'model': 'gemma3:1b', 'prompt': prompt, 'stream': False},
                        timeout=180,
                    )
                    result.raise_for_status()
                    st.subheader('AI-generated explanation (unverified)')
                    st.write(result.json().get('response', 'No response received.'))
                    st.warning('AI explanations can contain errors. Verify them against the transaction table before taking action.')
                except (requests.RequestException, ValueError) as exc:
                    st.error(f'Unable to contact local Ollama: {exc}. Confirm Ollama is running and gemma3:1b is installed.')
