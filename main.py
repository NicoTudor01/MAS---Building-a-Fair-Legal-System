# Main entry point for the Fair Legal System simulation.
#
# Run with:
#   /usr/bin/python3 main.py                   
#   /usr/bin/python3 main.py --case oj_simpson 
#   /usr/bin/python3 main.py --case oj_simpson --voting plurality
#   /usr/bin/python3 main.py --case oj_simpson --voting social_welfare
#   /usr/bin/python3 main.py --case oj_simpson --voting tournament
#   /usr/bin/python3 main.py --case oj_simpson --voting slater
#   /usr/bin/python3 main.py --case derek_chauvin
#   /usr/bin/python3 main.py --case tax_evasion --communicate --voting plurality


import argparse
import random
import time

from agents.juror import Juror, PERSONAS
from agents.judge import Judge
from cases.case_definitions import CASES
from voting.mechanisms import plurality_vote, social_welfare_vote, tournament_vote, slater_ranking
import config

from results.plotting import plot_multi_sentiment


counter = 1
data = [[0 for _ in range(5)] for _ in range(4)]

def run(case_key: str, communicate: bool, voting_method: str, data: list[list [int]]) -> None:
    global counter
    case = CASES[case_key]

    print(f"\n{'='*60}")
    print(f"  Case    : {case.name}")
    print(f"  Setting : {'Communication' if communicate else 'No Communication'}")
    print(f"  Voting  : {voting_method}")
    print(f"{'='*60}\n")

    # --- Build all jurors for this case ---
    # Jurors 1-4 each get a dedicated API key; juror 5 gets a random one.
    # A unique run_id is generated once per run so every agent starts with
    # a fresh server-side session (clearing the LLM's conversation cache).
    run_id = str(int(time.time()))

    def _key_for(juror_index: int) -> tuple:
        if juror_index < 4:
            return config.API_KEYS[juror_index], config.API_KEY_LABELS[juror_index]
        idx = random.randrange(len(config.API_KEYS))
        return config.API_KEYS[idx], config.API_KEY_LABELS[idx]

    jurors = [Juror(p, case, api_key=_key_for(i)[0], api_key_label=_key_for(i)[1], run_id=run_id) for i, p in enumerate(PERSONAS)]

    # Judge gets the first available API key
    judge = Judge(case, api_key=config.API_KEYS[0], api_key_label=config.API_KEY_LABELS[0], run_id=run_id)

    # --- Phase 1: every juror independently reads the case (first run only) ---
    if counter == 1:
        print("[Phase 1] Independent evaluations")
        for i, j in enumerate(jurors):
            print(f"  {j.persona['display_name']} evaluating...", end=" ", flush=True)
            j.evaluate_case()
            j.initial_confidence = j.confidence
            j.initial_reasoning = j.reasoning
            print(f"confidence={j.confidence:.2f}  ({j.verdict})")
            time.sleep(0.15)
            data[0][i] = j.confidence
        
    print(data)
    # --- Phase 2 (optional): judge-hosted pairwise deliberations ---
    if communicate:
        print("\n[Phase 2] Judge-hosted pairwise deliberations")
        judge.run_all_deliberations(jurors)

        print("\n[Phase 3] Final individual verdicts after deliberation")
        for i, j in enumerate(jurors):
            print(f"  {j.persona['display_name']} deliberating final verdict...", end=" ", flush=True)
            j.final_statement()
            print(f"confidence={j.confidence:.3f}  ({j.verdict})")
            print(f"    \"{j.reasoning}\"")
            time.sleep(0.15)
            data[counter][i] = j.confidence
        counter += 1

    # --- Voting ---
    if voting_method == "plurality":
        final_verdict = plurality_vote(jurors)
    elif voting_method == "social_welfare":
        final_verdict = social_welfare_vote(jurors)
    elif voting_method == "tournament":
        final_verdict = tournament_vote(jurors)
    elif voting_method == "slater":
        final_verdict = slater_ranking(jurors)

    # --- Results ---
    print(f"\n{'─'*60}")
    if communicate and any(j.initial_confidence is not None for j in jurors):
        print("  Verdict comparison (before → after deliberation):")
        for j in jurors:
            pre_conf = j.initial_confidence
            pre_v = "guilty" if pre_conf >= config.GUILT_THRESHOLD else "not_guilty"
            print(f"    {j.persona['display_name']:<12}  "
                  f"{pre_conf:.3f} ({pre_v})  →  {j.confidence:.3f} ({j.verdict})")
            print(f"      Before: \"{j.initial_reasoning}\"")
            print(f"      After:  \"{j.reasoning}\"")
    else:
        print("  Final individual verdicts:")
        for j in jurors:
            print(f"    {j.persona['display_name']:<12}  conf={j.confidence:.3f}  →  {j.verdict}")
            print(f"      \"{j.reasoning}\"")
    print(f"\n  Group verdict ({voting_method}): {final_verdict.upper()}")
    print(f"  Known verdict              : {case.known_verdict.upper()}")
    print(f"  Correct: {'YES ✓' if final_verdict == case.known_verdict else 'NO  ✗'}")
    print(f"{'-'*60}\n")    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fair Legal System MAS")
    parser.add_argument("--case",        required=True, choices=list(CASES.keys()),
                        help="Which case to simulate")
    parser.add_argument("--communicate", action="store_true",
                        help="Enable pairwise juror deliberation")
    parser.add_argument("--voting",      required=True,
                        choices=["plurality", "social_welfare", "tournament", "slater"],
                        help="Voting mechanism to determine final verdict")
    args = parser.parse_args()

    if (args.communicate == True):
        for i in range(3):
            run(args.case, args.communicate, args.voting, data)   
    else:
        run(args.case, args.communicate, args.voting, data)

    plot_multi_sentiment(data)
