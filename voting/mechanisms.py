# Voting mechanisms that aggregate juror confidence scores into a final verdict.
# Each function takes a list of Juror objects and returns "guilty" or "not_guilty".

import itertools
import config


def plurality_vote(jurors) -> str:
    # Each juror casts a binary vote; majority wins.
    guilty = sum(1 for j in jurors if j.verdict == "guilty")
    return "guilty" if guilty > len(jurors) - guilty else "not_guilty"


def social_welfare_vote(jurors) -> str:
    # Average all confidence scores; if mean >= threshold  guilty.
    avg = sum(j.confidence for j in jurors) / len(jurors)
    return "guilty" if avg >= config.GUILT_THRESHOLD else "not_guilty"


def tournament_vote(jurors) -> str:
    # Round-robin: juror i beats juror j if confidence_i > confidence_j.
    # The juror with the most wins sets the final verdict.
    wins = {j.persona["id"]: 0 for j in jurors}
    for j_a, j_b in itertools.combinations(jurors, 2):
        if j_a.confidence > j_b.confidence:
            wins[j_a.persona["id"]] += 1
        elif j_b.confidence > j_a.confidence:
            wins[j_b.persona["id"]] += 1
    winner_id = max(wins, key=lambda pid: wins[pid])
    winner = next(j for j in jurors if j.persona["id"] == winner_id)
    return winner.verdict


def slater_ranking(jurors) -> str:
    # Find the linear ordering that minimises pairwise disagreements (Kemeny-style).
    # The mean confidence of the top half in that ordering determines the verdict.
    n = len(jurors)
    pref = [[0] * n for _ in range(n)]
    for i, j_a in enumerate(jurors):
        for k, j_b in enumerate(jurors):
            if i != k and j_a.confidence > j_b.confidence:
                pref[i][k] = 1

    best_score = float("inf")
    best_order = list(range(n))
    for perm in itertools.permutations(range(n)):
        score = sum(
            1
            for pos_a, i in enumerate(perm)
            for pos_b, k in enumerate(perm)
            if pos_a < pos_b and pref[k][i] == 1
        )
        if score < best_score:
            best_score = score
            best_order = list(perm)

    top_half = best_order[: n // 2]
    top_avg = sum(jurors[i].confidence for i in top_half) / len(top_half)
    return "guilty" if top_avg >= config.GUILT_THRESHOLD else "not_guilty"
