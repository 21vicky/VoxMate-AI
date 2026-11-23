import gradio as gr

from src.speech_to_text import SpeechToText
from src.ai_brain import AIBrain
from src.text_to_speech import TextToSpeech


# ============================================================
# VOXMATE - NOVA COMMAND CENTER
# A redesigned interface; keeps the existing VoxMate engines.
# ============================================================

print("\n[VOXMATE] Booting command center...")

stt = SpeechToText()
brain = AIBrain()
tts = TextToSpeech()

print("[VOXMATE] Voice, AI and speech modules are ready.\n")


# ------------------------- BACKEND ---------------------------

def process_voice(audio_path, chat_history):
    history = chat_history or []

    if audio_path is None:
        return history, "No recording received. Press the microphone and try again.", None

    try:
        recognized_text = stt.transcribe(audio_path)

        if not recognized_text or str(recognized_text).startswith("Transcription error"):
            return history, recognized_text or "I couldn't understand the recording.", None

        answer = brain.generate_response(recognized_text)

        if not answer:
            return history, recognized_text, None

        if str(answer).startswith("Sorry, I encountered an error:"):
            return history, recognized_text, None

        response_audio = tts.generate_speech(answer)

        updated_history = history + [
            {"role": "user", "content": recognized_text},
            {"role": "assistant", "content": answer},
        ]

        return updated_history, recognized_text, response_audio

    except Exception as exc:
        print(f"[VOXMATE] Processing error: {exc}")
        return history, f"Processing error: {exc}", None


def reset_session():
    if hasattr(brain, "conversation"):
        brain.conversation.clear()
    return [], "", None, None


# --------------------------- DESIGN -------------------------

css = r"""
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --base: #0b0d0c;
    --surface: #121714;
    --surface-2: #171e19;
    --surface-3: #202a23;
    --line: rgba(190, 220, 190, .12);
    --text: #edf3e9;
    --muted: #89958a;
    --accent: #c6f36a;
    --accent-dark: #8bbd35;
    --orange: #ffb86b;
}

* { box-sizing: border-box; }

html, body {
    background: var(--base) !important;
    color: var(--text) !important;
    font-family: 'Manrope', sans-serif !important;
}

.gradio-container {
    max-width: 1600px !important;
    margin: 0 auto !important;
    padding: 0 !important;
    min-height: 100vh;
    background:
      radial-gradient(circle at 75% 0%, rgba(145, 185, 75, .08), transparent 28%),
      linear-gradient(135deg, #0b0d0c, #0d120e 60%, #0a0d0b) !important;
}

footer { display: none !important; }
.gradio-container, .gradio-container * { scrollbar-color: #485540 #111612; }

#app-shell {
    padding: 24px 30px 20px;
}

#topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 18px;
    padding: 3px 0 21px;
    border-bottom: 1px solid var(--line);
    margin-bottom: 23px;
}
.brand {
    display: flex;
    align-items: center;
    gap: 13px;
}
.brand-mark {
    width: 42px;
    height: 42px;
    display: grid;
    place-items: center;
    border-radius: 13px;
    background: var(--accent);
    color: #17200e;
    font-size: 21px;
    font-weight: 800;
    box-shadow: 0 0 24px rgba(198,243,106,.15);
}
.brand-name {
    color: var(--text);
    font-size: 16px;
    font-weight: 800;
    letter-spacing: 2px;
}
.brand-sub {
    color: var(--muted);
    font: 10px 'DM Mono', monospace;
    letter-spacing: 1.2px;
    margin-top: 4px;
}
.top-right {
    display: flex;
    align-items: center;
    gap: 18px;
    color: var(--muted);
    font: 10px 'DM Mono', monospace;
    letter-spacing: .8px;
}
.live-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 11px;
    border: 1px solid rgba(198,243,106,.25);
    border-radius: 99px;
    color: var(--accent);
    background: rgba(198,243,106,.06);
}
.live-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--accent);
    box-shadow: 0 0 9px var(--accent);
}

#main-grid {
    display: grid;
    grid-template-columns: minmax(275px, .82fr) minmax(500px, 1.8fr);
    gap: 20px;
    align-items: stretch;
}

#left-column, #right-column {
    display: flex;
    flex-direction: column;
    gap: 18px;
    min-width: 0;
}
.panel {
    background: linear-gradient(145deg, rgba(23,30,25,.96), rgba(15,20,17,.98)) !important;
    border: 1px solid var(--line) !important;
    border-radius: 16px !important;
    padding: 19px !important;
    box-shadow: 0 16px 40px rgba(0,0,0,.18);
}
.section-kicker {
    color: var(--muted);
    font: 10px 'DM Mono', monospace;
    letter-spacing: 1.7px;
    text-transform: uppercase;
    margin-bottom: 15px;
}
#identity-card {
    position: relative;
    overflow: hidden;
    min-height: 265px;
    background:
      radial-gradient(circle at 50% 45%, rgba(198,243,106,.12), transparent 39%),
      linear-gradient(145deg, #1b241c, #111713) !important;
}
#identity-card:after {
    content: "V";
    position: absolute;
    right: -13px;
    bottom: -83px;
    color: rgba(198,243,106,.035);
    font-size: 260px;
    line-height: 1;
    font-weight: 800;
    pointer-events: none;
}
.identity-label {
    color: var(--accent);
    font: 10px 'DM Mono', monospace;
    letter-spacing: 2px;
}
.identity-title {
    margin: 9px 0 0;
    color: #f0f5eb;
    font-size: 25px;
    font-weight: 800;
    letter-spacing: -1px;
}
.identity-copy {
    max-width: 270px;
    margin-top: 8px;
    color: #9ba99a;
    font-size: 12px;
    line-height: 1.7;
}
.voice-visual {
    width: 100%;
    height: 94px;
    margin: 18px 0 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 5px;
}
.voice-visual span {
    width: 4px;
    border-radius: 5px;
    background: var(--accent);
    opacity: .82;
    box-shadow: 0 0 12px rgba(198,243,106,.28);
}
.voice-visual span:nth-child(1), .voice-visual span:nth-child(13) { height: 15px; opacity: .35; }
.voice-visual span:nth-child(2), .voice-visual span:nth-child(12) { height: 27px; opacity: .5; }
.voice-visual span:nth-child(3), .voice-visual span:nth-child(11) { height: 42px; }
.voice-visual span:nth-child(4), .voice-visual span:nth-child(10) { height: 57px; }
.voice-visual span:nth-child(5), .voice-visual span:nth-child(9) { height: 72px; }
.voice-visual span:nth-child(6), .voice-visual span:nth-child(8) { height: 48px; }
.voice-visual span:nth-child(7) { height: 85px; }

.status-list {
    display: flex;
    flex-direction: column;
    gap: 13px;
}
.status-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
    color: #b4c0b3;
    font-size: 12px;
}
.status-row strong {
    color: var(--accent);
    font: 10px 'DM Mono', monospace;
    font-weight: 500;
}
.status-line {
    height: 1px;
    background: var(--line);
    margin: 1px 0;
}

#voice-panel .section-kicker { margin-bottom: 12px; }
#microphone, #transcript, #audio-output {
    background: #0c120e !important;
    border: 1px solid rgba(198,243,106,.14) !important;
    border-radius: 12px !important;
}
#transcript textarea {
    background: #0c120e !important;
    color: #e6f5d6 !important;
    border-color: rgba(198,243,106,.16) !important;
}
label, .label {
    color: #a9b6a7 !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase;
}
input, textarea {
    background: #0c120e !important;
    color: var(--text) !important;
    border-color: rgba(198,243,106,.17) !important;
}
#conversation-panel {
    min-height: 690px;
    display: flex;
    flex-direction: column;
}
.conversation-heading {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    padding-bottom: 15px;
    border-bottom: 1px solid var(--line);
    margin-bottom: 14px;
}
.conversation-title {
    color: var(--text);
    font-size: 14px;
    font-weight: 800;
    letter-spacing: .4px;
}
.conversation-sub {
    color: var(--muted);
    font: 10px 'DM Mono', monospace;
    margin-top: 5px;
}
.terminal-tag {
    color: var(--accent);
    background: rgba(198,243,106,.07);
    border: 1px solid rgba(198,243,106,.17);
    border-radius: 6px;
    padding: 7px 9px;
    font: 9px 'DM Mono', monospace;
    letter-spacing: 1px;
}
#chatbot {
    flex: 1;
    background: rgba(7,11,8,.55) !important;
    border: 1px solid rgba(198,243,106,.12) !important;
    border-radius: 12px !important;
}
#chatbot .message {
    border: 1px solid rgba(198,243,106,.12) !important;
    border-radius: 12px !important;
}
#clear-button {
    align-self: flex-end;
    min-width: 190px;
    margin-top: 13px;
    background: transparent !important;
    color: #c5d1c1 !important;
    border: 1px solid rgba(198,243,106,.24) !important;
    border-radius: 9px !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
}
#clear-button:hover {
    background: rgba(198,243,106,.08) !important;
    border-color: var(--accent) !important;
}
#footer {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    border-top: 1px solid var(--line);
    padding-top: 15px;
    margin-top: 22px;
    color: #69756a;
    font: 9px 'DM Mono', monospace;
    letter-spacing: 1px;
}

@media (max-width: 900px) {
    #app-shell { padding: 17px 14px; }
    #main-grid { grid-template-columns: 1fr; }
    #conversation-panel { min-height: 560px; }
}
@media (max-width: 560px) {
    #topbar { align-items: flex-start; }
    .top-right { flex-direction: column; align-items: flex-end; gap: 8px; }
    .brand-name { font-size: 13px; }
    .identity-title { font-size: 22px; }
    #footer { flex-direction: column; }
}
"""


# ---------------------------- UI ----------------------------

with gr.Blocks(
    title="VoxMate | Command Center",
) as demo:

    with gr.Column(elem_id="app-shell"):
        gr.HTML("""
            <div id="topbar">
                <div class="brand">
                    <div class="brand-mark">V</div>
                    <div>
                        <div class="brand-name">VOXMATE</div>
                        <div class="brand-sub">PERSONAL AI / COMMAND CENTER</div>
                    </div>
                </div>
                <div class="top-right">
                    <span>LOCAL SESSION</span>
                    <span class="live-pill"><i class="live-dot"></i> SYSTEM ONLINE</span>
                </div>
            </div>
        """)

        with gr.Row(elem_id="main-grid"):
            with gr.Column(elem_id="left-column"):
                gr.HTML("""
                    <div id="identity-card" class="panel">
                        <div class="identity-label">YOUR AI ASSISTANT</div>
                        <div class="identity-title">Ready when<br>you are.</div>
                        <div class="identity-copy">
                            Speak naturally. VoxMate will listen, understand your request
                            and respond with a generated voice.
                        </div>
                        <div class="voice-visual">
                            <span></span><span></span><span></span><span></span><span></span>
                            <span></span><span></span><span></span><span></span><span></span>
                            <span></span><span></span><span></span>
                        </div>
                    </div>
                """)

                with gr.Column(elem_id="voice-panel", elem_classes=["panel"]):
                    gr.HTML('<div class="section-kicker">01 / Voice input</div>')

                    microphone = gr.Audio(
                        sources=["microphone"],
                        type="filepath",
                        label="RECORD A COMMAND",
                        elem_id="microphone",
                    )

                    transcript = gr.Textbox(
                        label="TRANSCRIPTION",
                        placeholder="Your recognized words will appear here...",
                        interactive=False,
                        lines=3,
                        elem_id="transcript",
                    )

                    audio_output = gr.Audio(
                        label="SPOKEN RESPONSE",
                        autoplay=True,
                        elem_id="audio-output",
                    )

                with gr.Column(elem_classes=["panel"]):
                    gr.HTML("""
                        <div class="section-kicker">02 / System status</div>
                        <div class="status-list">
                            <div class="status-row"><span>Speech recognition</span><strong>READY</strong></div>
                            <div class="status-line"></div>
                            <div class="status-row"><span>AI response engine</span><strong>READY</strong></div>
                            <div class="status-line"></div>
                            <div class="status-row"><span>Speech synthesis</span><strong>READY</strong></div>
                            <div class="status-line"></div>
                            <div class="status-row"><span>Session mode</span><strong>LOCAL</strong></div>
                        </div>
                    """)

            with gr.Column(elem_id="right-column"):
                with gr.Column(elem_id="conversation-panel", elem_classes=["panel"]):
                    gr.HTML("""
                        <div class="conversation-heading">
                            <div>
                                <div class="conversation-title">Conversation</div>
                                <div class="conversation-sub">VOICE COMMAND LOG / LIVE SESSION</div>
                            </div>
                            <div class="terminal-tag">SECURE SESSION</div>
                        </div>
                    """)

                    chatbot = gr.Chatbot(
                        label="CHAT HISTORY",
                        height=585,
                        placeholder="Your conversation will appear here.\n\nStart by recording a voice command.",
                        elem_id="chatbot",
                    )

                    clear_button = gr.Button(
                        "↺  CLEAR SESSION",
                        variant="secondary",
                        elem_id="clear-button",
                    )

        gr.HTML("""
            <div id="footer">
                <span>VOXMATE PERSONAL AI</span>
                <span>WHISPER · AI BRAIN · EDGE TTS</span>
                <span>COMMAND CENTER / V1.0</span>
            </div>
        """)

    microphone.stop_recording(
        fn=process_voice,
        inputs=[microphone, chatbot],
        outputs=[chatbot, transcript, audio_output],
    )

    clear_button.click(
        fn=reset_session,
        inputs=[],
        outputs=[chatbot, transcript, audio_output, microphone],
    )


if __name__ == "__main__":
    demo.queue()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        inbrowser=True,
        theme=gr.themes.Base(
            primary_hue="lime",
            secondary_hue="green",
            neutral_hue="slate",
        ),
        css=css,
    )
