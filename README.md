# Spectrum

Spectrum is a teen-first conversation safety companion. A teen can paste a conversation they choose to review, see possible risk patterns with plain-language explanations, and prepare a summary they control. It does not monitor accounts or send messages to adults.

## Project files

```text
spectrum/
├── app.py
├── demo_conversations.json
├── requirements.txt
├── README.md
├── prompts/
│   └── risk_analysis.txt
└── project_materials/
    ├── demo_video_script.md
    ├── project_overview.md
    └── pitch_narrative.md
```

## Setup

1. Install Python 3.10 or newer.
2. Open a terminal in the `spectrum` directory.
3. Create and activate a virtual environment if desired:

   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

4. Install the dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Set an API key for your shell session. PowerShell:

   ```powershell
   $env:OPENAI_API_KEY = "your-api-key"
   ```

   Optional model override (defaults to `gpt-4.1-mini`):

   ```powershell
   $env:OPENAI_MODEL = "gpt-4.1-mini"
   ```

6. Start the app:

   ```powershell
   streamlit run app.py
   ```

## Use

- Choose one of the synthetic examples and click **Load selected demo**, or paste text you choose to analyze. Consider removing names and personal details first.
- Click **Check this conversation**. Spectrum returns a rough risk indicator, excerpts that support any identified flags, explanations, possible boundaries, and optional next steps.
- Use **Prepare a shareable summary** to create a draft. Review and edit it before downloading or copying it to share. Spectrum never sends it for you.
- Open **Learn more** for short explanations of grooming, red flags, and boundaries.

The benign example is intentionally ordinary; the model should not invent concerns in it. The score is a model-generated aid, not a calibrated probability or verdict. If a teen feels in immediate danger, the app encourages contacting a trusted adult or local emergency services.

## Privacy and safety notes

This MVP has no database and does not persist transcripts to app storage. Text submitted for analysis is sent to the configured model provider, so only paste content you are comfortable sending to that service. Do not use real intimate images or identifying details in a demo. The app is educational support, not an emergency service or a replacement for a trusted adult.

## Demo and pitch materials

See `project_materials/` for a two-minute demo script, a one-page overview, and a judge-facing pitch narrative. The exact prompt sent to the model is in `prompts/risk_analysis.txt`.
