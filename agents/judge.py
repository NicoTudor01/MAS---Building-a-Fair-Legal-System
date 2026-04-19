# The Judge agent presides over the deliberation process.
# It opens each pairwise session between jurors, frames the discussion, and
# ensures every juror hears every other juror exactly once per direction.
# Sleeps are inserted between API calls to stay within the 10 call/sec limit.

import json
import re
import time

from llmproxy import LLMProxy

import config
from cases import Case


class Judge:
    def __init__(self, case: Case, api_key: str = "", api_key_label: str = "", run_id: str = ""):
        self.case = case
        self.api_key = api_key
        self.api_key_label = api_key_label
        self._run_id = run_id
        self.summary = ""
        print(f"  [Judge] using API key: {api_key_label or '(none)'}")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @property
    def session_id(self) -> str:
        case_tag = "".join(c for c in self.case.name if c.isalnum())[:20]
        return f"judge{case_tag}{self._run_id}"

    @property
    def system_prompt(self) -> str:
        return (
            "You are the presiding Judge in a criminal trial.\n"
            "Your role is to ensure a fair and orderly deliberation process. "
            "You are impartial, authoritative, and precise. "
            "You guide jurors through structured discussion and ensure every voice is heard.\n\n"
            "Always respond with a JSON object containing exactly one key:\n"
            '  "statement": a 1-2 sentence instruction or framing directed at the two jurors.\n'
            "Output only the JSON object with no extra text."
        )

    def _call_llm(self, query: str, lastk: int = 0, _retries: int = 2) -> dict:
        """Send a query to the LLM and return the parsed JSON response."""
        client = LLMProxy(api_key=self.api_key or None)
        last_err = None
        for attempt in range(_retries):
            response = client.generate(
                model=config.MODEL,
                system=self.system_prompt,
                query=query,
                session_id=self.session_id,
                temperature=0.4,
                lastk=lastk,
            )
            raw = response["result"].strip()
            raw = re.sub(r"^```(?:json)?\s*", "", raw)
            raw = re.sub(r"\s*```$", "", raw).strip()
            if not raw:
                last_err = ValueError("LLM returned an empty response")
                print(f"\n    [warn] empty response from LLM (attempt {attempt + 1}/{_retries}), retrying...")
                continue
            if "content filtering" in raw.lower() or "could not be processed" in raw.lower():
                print(f"\n    [warn] content filter triggered, using fallback statement")
                return {"statement": "Please proceed with your deliberation."}
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

    def open_deliberation(self, juror_a: object, juror_b: object) -> str:
        """
        Frame the deliberation between two jurors and return the judge's statement.
        """
        query = (
            f"You are presiding over a deliberation in the case: {self.case.name}\n\n"
            f"Two jurors are about to discuss the case:\n"
            f"  - {juror_a.persona['display_name']}: confidence in guilt = {juror_a.confidence:.3f}\n"
            f"    Reasoning: {juror_a.reasoning}\n"
            f"  - {juror_b.persona['display_name']}: confidence in guilt = {juror_b.confidence:.3f}\n"
            f"    Reasoning: {juror_b.reasoning}\n\n"
            "Provide a brief opening statement instructing these two jurors on what to discuss."
        )
        result = self._call_llm(query, lastk=0)
        return result.get("statement", "Please proceed with your deliberation.")

    def run_all_deliberations(self, jurors: list) -> None:
        """
        Host every unique juror pair in a structured two-way deliberation.
        Each pair is introduced by the judge, then both jurors update their
        beliefs after hearing each other.

        Unique pairs: C(n, 2) = n*(n-1)/2   10 pairs for 5 jurors.
        Sleep of 0.15 s between each API call keeps us well under 10 calls/sec.
        """
        pairs = [
            (jurors[i], jurors[j])
            for i in range(len(jurors))
            for j in range(i + 1, len(jurors))
        ]

        for j_a, j_b in pairs:
            print(
                f"\n  [Judge] Opening deliberation: "
                f"{j_a.persona['display_name']}  {j_b.persona['display_name']}"
            )

            statement = self.open_deliberation(j_a, j_b)
            print(f"  [Judge] \"{statement}\"")
            time.sleep(0.15)

            # j_a hears j_b
            print(
                f"    {j_a.persona['display_name']} hears {j_b.persona['display_name']}...",
                end=" ",
                flush=True,
            )
            j_a.deliberate_with(j_b)
            print(f"updated confidence={j_a.confidence:.3f}")
            time.sleep(0.15)

            # j_b hears j_a (using j_a's freshly updated position)
            print(
                f"    {j_b.persona['display_name']} hears {j_a.persona['display_name']}...",
                end=" ",
                flush=True,
            )
            j_b.deliberate_with(j_a)
            print(f"updated confidence={j_b.confidence:.3f}")
            time.sleep(0.15)

    def __repr__(self) -> str:
        return f"Judge(case={self.case.name!r})"
