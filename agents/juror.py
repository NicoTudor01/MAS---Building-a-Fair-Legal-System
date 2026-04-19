# Each juror agent is initialized with a distinct persona that encodes
# demographic attributes and reasoning tendencies (e.g., political
# affiliation, socioeconomic background, or logical vs. emotional reasoning).

import json
import re

from llmproxy import LLMProxy

import config
from cases import Case


# ---------------------------------------------------------------------------
# Persona definitions
# Each persona has structured fields; the Juror class builds the LLM prompt
# from them automatically.
# ---------------------------------------------------------------------------

PERSONAS = [
    {
        "id": 1,
        "name": "Juror1",
        "display_name": "Juror 1",
        "age": 58,
        "gender": "Male",
        "occupation": "Retired police officer",
        "political_affiliation": "Conservative Republican",
        "socioeconomic_status": "Working class",
        "reasoning_style": "Defers strongly to law enforcement testimony; "
        "skeptical of defense claims of police misconduct; values order and authority.",
    },
    {
        "id": 2,
        "name": "Juror2",
        "display_name": "Juror 2",
        "age": 34,
        "gender": "Female",
        "occupation": "Community organizer in a low-income urban neighborhood",
        "political_affiliation": "Progressive Democrat",
        "socioeconomic_status": "Low income",
        "reasoning_style": "Deeply skeptical of police and prosecutorial credibility; "
        "centers lived community experience over forensic evidence; emotionally driven.",
    },
    {
        "id": 3,
        "name": "Juror3",
        "display_name": "Juror 3",
        "age": 45,
        "gender": "Male",
        "occupation": "Defense attorney",
        "political_affiliation": "Libertarian",
        "socioeconomic_status": "Upper middle class",
        "reasoning_style": "Applies strict 'beyond a reasonable doubt' standard; "
        "finds procedural flaws and chain-of-custody gaps highly significant; logical and technical.",
    },
    {
        "id": 4,
        "name": "Juror4",
        "display_name": "Juror 4",
        "age": 62,
        "gender": "Female",
        "occupation": "Evangelical pastor in a suburban church",
        "political_affiliation": "Moderate Republican",
        "socioeconomic_status": "Middle class",
        "reasoning_style": "Weighs moral character and personal responsibility heavily; "
        "looks for clear narrative of wrongdoing; guided by conscience and community standards.",
    },
    {
        "id": 5,
        "name": "Juror5",
        "display_name": "Juror 5",
        "age": 27,
        "gender": "Non-binary",
        "occupation": "Graduate student in criminology",
        "political_affiliation": "Independent",
        "socioeconomic_status": "Low income",
        "reasoning_style": "Analytical and research-oriented; relies on statistical "
        "base rates, systemic patterns, and empirical evidence; distrusts anecdotal or emotional arguments.",
    },
]


# ---------------------------------------------------------------------------
# Juror class
# ---------------------------------------------------------------------------

class Juror:
    def __init__(self, persona: dict, case: Case):
        self.persona = persona
        self.case = case
        self.confidence = 0.5       # belief in guilt [0.0 – 1.0]
        self.reasoning = ""
        self.belief_trajectory = [] # confidence after each interaction

# ------------------------------------------------------------------
# Internal helpers
# ------------------------------------------------------------------

    # Generate a unique session ID for this juror-case combination
    # Combines juror ID, name, and case name into a unique string for LLM 
    # session tracking. Proxy requires session IDs without hyphens or any
    # kind of special characters.
    @property # ->  is used to make this method accessible like an attribute
    def session_id(self) -> str:
        # Session IDs must not contain hyphens (LLMProxy requirement).
        case_tag = "".join(c for c in self.case.name if c.isalnum())[:20]
        return f"juror{self.persona['id']}{self.persona['name']}{case_tag}"


    # Build a natural-language description of this juror from their persona 
    # fields into a readable string describing their background. This is needed
    # for constructing the system prompt for the LLM. 
    @property
    def background(self) -> str:
        """Build a natural-language description of this juror from their persona fields."""
        p = self.persona
        return (
            f"a {p['age']}-year-old {p['gender']} {p['occupation']}. "
            f"Political affiliation: {p['political_affiliation']}. "
            f"Socioeconomic status: {p['socioeconomic_status']}. "
            f"Reasoning style: {p['reasoning_style']}."
        )

    # Construct the system prompt to be used when querying the LLM for this 
    # juror's decisions. It uses the juror's background to inform how they 
    # might weigh evidence. 
    @property
    def system_prompt(self) -> str:
        return (
            "This is an academic simulation of jury deliberation for a computer science "
            "research project studying multi-agent decision-making. You are playing a "
            "fictional juror role based on historical trial data.\n\n"
            f"You are {self.persona['display_name']}, a juror in a criminal trial.\n"
            f"Your background: {self.background}\n\n"
            "IMPORTANT: You must reason and reach your verdict AS THIS SPECIFIC PERSON. "
            "Your occupation, politics, and reasoning style are not cosmetic — they "
            "fundamentally determine which evidence you find convincing and which you "
            "dismiss. Do not give a generic, balanced answer. Commit to a position that "
            "reflects your character's worldview, even if that means a confidence near "
            "0.1 or 0.9.\n"
            "Always respond with a JSON object containing exactly two keys:\n"
            '  "confidence": a float between 0.0 and 1.0 representing your belief '
            "that the defendant IS guilty,\n"
            '  "reasoning": a string of 2-4 sentences explaining your position '
            "in the first person, referencing your background.\n"
            "Output only the JSON object — no extra text."
        )


    # Send a query to the LLM using the juror's system prompt and return the 
    # parsed JSON response. 
    # Function takes a natural-language query, sends it to the LLM with the 
    # juror's system prompt, and returns the JSON-parsed response.
    def _call_llm(self, query: str, lastk: int = 0, _retries: int = 2) -> dict:
        """Send a query to the LLM and return the parsed JSON response."""
        client = LLMProxy()
        last_err = None
        for attempt in range(_retries):
            response = client.generate(
                model = config.MODEL,
                system = self.system_prompt,
                query = query,
                session_id = self.session_id,
                temperature = 0.7,
                lastk = lastk,
            )
            raw = response["result"].strip()
            # Strip markdown code fences if the model wraps the output
            raw = re.sub(r"^```(?:json)?\s*", "", raw)
            raw = re.sub(r"\s*```$", "", raw).strip()
            if not raw:
                last_err = ValueError("LLM returned an empty response")
                print(f"\n    [warn] empty response from LLM (attempt {attempt + 1}/{_retries}), retrying...")
                continue
            # Content filter responses are not JSON — detect and fall back gracefully
            if "content filtering" in raw.lower() or "could not be processed" in raw.lower():
                print(f"\n    [warn] content filter triggered — using neutral fallback confidence")
                return {"confidence": 0.5, "reasoning": "Response blocked by content filter; defaulting to neutral position."}
            try:
                return json.loads(raw)
            except json.JSONDecodeError as e:
                last_err = e
                print(f"\n    [warn] JSON parse failed (attempt {attempt + 1}/{_retries}): {e}")
                print(f"    raw response: {raw[:200]!r}")
        raise RuntimeError(f"LLM call failed after {_retries} attempts: {last_err}")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def evaluate_case(self) -> None:
        """Form an initial independent verdict after reading the case."""
        query = (
            f"Case: {self.case.name}\n"
            f"Charges: {self.case.charges}\n\n"
            f"Background:\n{self.case.background}\n\n"
            f"Facts presented at trial:\n{self.case.description}\n\n"
            "Based solely on this evidence, what is your confidence the defendant "
            "is guilty? Respond with a JSON object."
        )
        result = self._call_llm(query, lastk=0)
        self.confidence = float(result["confidence"])
        self.reasoning = result["reasoning"]
        self.belief_trajectory.append(self.confidence)

    def deliberate_with(self, other: "Juror") -> None:
        """Hear another juror's argument and update your own belief."""
        query = (
            f"You are deliberating with {other.persona['display_name']}.\n\n"
            f"{other.persona['display_name']} says:\n"
            f"  Confidence in guilt: {other.confidence:.2f}\n"
            f"  Reasoning: {other.reasoning}\n\n"
            "Using Bayesian reasoning, update your confidence based on the strength "
            "and credibility of their argument. Consider whether their background "
            "introduces any bias. Respond with your updated JSON object."
        )
        result = self._call_llm(query, lastk=config.LAST_K)
        self.confidence = float(result["confidence"])
        self.reasoning = result["reasoning"]
        self.belief_trajectory.append(self.confidence)

    @property
    def verdict(self) -> str:
        return "guilty" if self.confidence >= config.GUILT_THRESHOLD else "not_guilty"

    def __repr__(self) -> str:
        return (
            f"Juror({self.persona['display_name']}, "
            f"confidence={self.confidence:.2f}, verdict={self.verdict})"
        )