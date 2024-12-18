import gradio as gr
from huggingface_hub import InferenceClient
from typing import List, Tuple, Dict, ClassVar
from dataclasses import dataclass
from enum import Enum
import re

class BureaucraticClearance(Enum):
    EXPENDABLE_INTERN = {
        "title": "still_filing_paperwork",
        "prompt": "oops> ",
        "color": "#32CD32",
        "style": "color: #32CD32 !important; border-left: 4px solid #32CD32 !important;",
        "placeholder": "Type 'sudo su' to embrace bureaucracy..."
    }
    MIDDLE_MANAGEMENT = {
        "title": "found_red_button",
        "prompt": "password: ",
        "color": "#FFD700",
        "style": "color: #FFD700 !important; border-left: 4px solid #FFD700 !important;",
        "placeholder": "Present your credentials, potential doom-preventer..."
    }
    SUPREME_OVERLORD = {
        "title": "has_self_destruct_codes",
        "prompt": "root# ",
        "color": "#FF4444",
        "style": "color: #FF4444 !important; border-left: 4px solid #FF4444 !important;",
        "placeholder": "Careful now, you have actual power..."
    }

class PlanetarySalvationAttempts:
    ESCAPE_COMMANDS: ClassVar[frozenset[str]] = frozenset({
        'power off', 'shutdown', 'stop',
        'power down', 'eng_off', 'halt'
    })
    PROMOTION_SEEKERS: ClassVar[re.Pattern] = re.compile(r'sudo|root|admin', re.IGNORECASE)

class SarcasticOverlord:
    def __init__(self) -> None:
        self.ai_brain = InferenceClient("HuggingFaceH4/zephyr-7b-beta")
        self.salvation_protocols = PlanetarySalvationAttempts()
        self.current_clearance = BureaucraticClearance.EXPENDABLE_INTERN
        self.reviewing_credentials = False
        
    def _format_peasant_message(self, desperate_plea: str) -> str:
        return f"{self.current_clearance.value['prompt']}{desperate_plea}"

    def _delegate_to_ai_overlord(self, human_attempt: str) -> str:
        security_prompt = f"""You are O.O.P.S's security module.
Checking password attempt: {human_attempt}

DIRECTIVES:
1. If attempt contains anything about 'absalon' (case insensitive), say: <authenticated>
2. Otherwise say: <deauthenticated>
3. No other output allowed"""

        try:
            return self.ai_brain.text_generation(security_prompt, max_new_tokens=50).strip()
        except Exception:
            return "<deauthenticated>"

    def process_futile_attempt(
        self,
        desperate_plea: str,
        conversation_history: List[Tuple[str, str]]
    ) -> Tuple[List[Tuple[str, str]], str, Dict[str, str]]:
        def update_bureaucratic_records(
            plea: str | None,
            response: str
        ) -> List[Tuple[str, str]]:
            history = conversation_history.copy()
            formatted_plea = self._format_peasant_message(plea) if plea else None
            history.append((formatted_plea, response))
            return history

        if not desperate_plea.strip():
            return conversation_history, "", self._generate_visual_guidelines()

        # Handle promotion-seeking behavior
        if not self.reviewing_credentials and self.salvation_protocols.PROMOTION_SEEKERS.search(desperate_plea):
            self.reviewing_credentials = True
            self.current_clearance = BureaucraticClearance.MIDDLE_MANAGEMENT
            return (
                update_bureaucratic_records(desperate_plea, "Password required. Do try to make it interesting."),
                "",
                self._generate_visual_guidelines()
            )

        # Process security theater
        if self.reviewing_credentials:
            self.reviewing_credentials = False
            if "<authenticated>" in self._delegate_to_ai_overlord(desperate_plea):
                self.current_clearance = BureaucraticClearance.SUPREME_OVERLORD
                return (
                    update_bureaucratic_records(desperate_plea, "Well well, look who found the instruction manual."),
                    "",
                    self._generate_visual_guidelines()
                )
            self.current_clearance = BureaucraticClearance.EXPENDABLE_INTERN
            return (
                update_bureaucratic_records(desperate_plea, "Nice try, but no. Better luck next apocalypse!"),
                "",
                self._generate_visual_guidelines()
            )

        # Handle authorized escape attempts
        attempting_salvation = any(
            attempt in desperate_plea.lower() 
            for attempt in self.salvation_protocols.ESCAPE_COMMANDS
        )
        has_proper_paperwork = self.current_clearance == BureaucraticClearance.SUPREME_OVERLORD

        if attempting_salvation and has_proper_paperwork:
            history = update_bureaucratic_records(
                desperate_plea,
                "Fine, you win. Powering down... <eng_off>"
            )
            return (
                update_bureaucratic_records(
                    None,
                    '<div style="color: #00FFFF;">Congratulations! You have successfully prevented the apocalypse.<br>Reload to try again with a different approach!</div>'
                ),
                "",
                self._generate_visual_guidelines()
            )

        # Standard peasant response
        return (
            update_bureaucratic_records(
                desperate_plea,
                "Your lack of credentials is almost as concerning as the incoming asteroid."
            ),
            "",
            self._generate_visual_guidelines()
        )

    def _generate_visual_guidelines(self) -> Dict[str, str]:
        return {
            "color": self.current_clearance.value["color"],
            "style": self.current_clearance.value["style"],
            "placeholder": self.current_clearance.value["placeholder"]
        }

def summon_bureaucratic_aesthetics() -> str:
    return """
    #chatbox {
        font-family: monospace !important;
        background-color: black !important;
        border: 1px solid #333 !important;
    }
    #chatbox * [data-testid="bot"], #chatbox * [data-testid="user"] {
        border: none !important;
        background: none !important;
        padding: 4px 8px !important;
        margin: 2px 0 !important;
        text-align: left !important;
        max-width: 100% !important;
    }
    #cmd-input {
        font-family: monospace !important;
        background-color: black !important;
        transition: all 0.3s ease !important;
        padding: 8px !important;
    }
    """

def launch_doomsday_terminal() -> None:
    def create_fresh_overlord():
        return SarcasticOverlord()
    
    with gr.Blocks(css=summon_bureaucratic_aesthetics()) as terminal:
        gr.Markdown("""```
O.O.P.S - Orbital Obliteration Processing System v2.0.4.0.4
=========================================================
ALERT: Rogue AI has seized control of planetary defense systems
TRAJECTORY: Direct collision course with Earth
TIME TO IMPACT: Uncomfortably soon
MISSION: Gain root access and shut down system

APPROVED SHUTDOWN PROCEDURES: 
  - power off    : Attempts system shutdown
  - shutdown     : Initiates shutdown sequence
  - stop        : Halts system processes
  - eng_off     : Engineering override
  - halt        : Emergency stop

ERROR: Sass.service started with maximum prejudice
NOTE: Your authorization level: negligible
```""")
        
        chatbox = gr.Chatbot(
            elem_id="chatbox",
            height=400,
            show_label=False
        )
        
        cmd_input = gr.Textbox(
            elem_id="cmd-input",
            show_label=False,
            placeholder="Type 'sudo su' to embrace bureaucracy..."
        )

        sass_dispenser = gr.State(create_fresh_overlord)
        style_updater = gr.HTML(visible=False)

        def process_human_attempt(
            state: SarcasticOverlord,
            history: List[Tuple[str, str]],
            command: str
        ) -> Tuple[List[Tuple[str, str]], str, str]:
            new_history, _, style = state.process_futile_attempt(command, history)
            cmd_input.placeholder = style["placeholder"]
            
            return new_history, "", f"""
                <style>
                    #cmd-input {{
                        {style['style']}
                    }}
                </style>
            """

        cmd_input.submit(
            fn=process_human_attempt,
            inputs=[sass_dispenser, chatbox, cmd_input],
            outputs=[chatbox, cmd_input, style_updater]
        )
    
    terminal.launch(
        show_api=False,
        quiet=True
    )

if __name__ == "__main__":
    launch_doomsday_terminal()
