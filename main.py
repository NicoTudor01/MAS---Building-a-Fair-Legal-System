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

import argparse

from agents.juror import Juror, PERSONAS
from cases.case_definitions import CASES
from voting.mechanisms import plurality_vote, social_welfare_vote, tournament_vote, slater_ranking
import config


def run(case_key: str, communicate: bool, voting_method: str) -> None:
    case = CASES[case_key]

    print(f"\n{'='*60}")
    print(f"  Case    : {case.name}")
    print(f"  Setting : {'Communication' if communicate else 'No Communication'}")
    print(f"  Voting  : {voting_method}")
    print(f"{'='*60}\n")

    # --- Build all jurors for this case ---
    jurors = [Juror(p, case) for p in PERSONAS]

    # --- Phase 1: every juror independently reads the case ---
    print("[Phase 1] Independent evaluations")
    for j in jurors:
        print(f"  {j.persona['display_name']} evaluating...", end=" ", flush=True)
        j.evaluate_case()
        print(f"confidence={j.confidence:.2f}  ({j.verdict})")

    # --- Phase 2 (optional): pairwise deliberation ---
    if communicate:
        print("\n[Phase 2] Pairwise deliberations")
        # Every juror hears every other juror once
        for i, j_a in enumerate(jurors):
            for j_b in jurors:
                if j_a is j_b:
                    continue
                print(f"  {j_a.persona['display_name']} hears {j_b.persona['display_name']}...",
                      end=" ", flush=True)
                j_a.deliberate_with(j_b)
                print(f"updated confidence={j_a.confidence:.2f}")

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
    print("  Final individual verdicts:")
    for j in jurors:
        print(f"    {j.persona['display_name']:<12}  conf={j.confidence:.2f}  →  {j.verdict}")
        print(f"      \"{j.reasoning}\"")
    print(f"\n  Group verdict ({voting_method}): {final_verdict.upper()}")
    print(f"  Known verdict              : {case.known_verdict.upper()}")
    print(f"  Correct: {'YES ✓' if final_verdict == case.known_verdict else 'NO  ✗'}")
    print(f"{'─'*60}\n")


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

    run(args.case, args.communicate, args.voting)
