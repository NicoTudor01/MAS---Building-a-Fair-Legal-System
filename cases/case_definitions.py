from dataclasses import dataclass


@dataclass
class Case:
    name: str           # full case name, e.g. "People v. O.J. Simpson (1995)"
    charges: str        # what the defendant is charged with
    background: str     # context about the case and parties involved
    description: str    # facts presented at trial
    known_verdict: str  # "guilty" or "not_guilty" — the real-world outcome


# ---------------------------------------------------------------------------
# Case definitions
# ---------------------------------------------------------------------------

OJ_SIMPSON = Case(
    name="People v. O.J. Simpson (1995)",
    charges="Homicide of Nicole Brown Simpson and Ron Goldman",
    known_verdict="not_guilty",
    background=(
        "O.J. Simpson, a retired NFL athlete and public figure, was prosecuted in connection "
        "with the deaths of Nicole Brown Simpson and Ronald Goldman on June 12, 1994. "
        "The prosecution's case rested on DNA evidence, forensic trace evidence linking "
        "Simpson to the scene, and records of prior altercations between Simpson and the "
        "deceased. The defense challenged the integrity of the forensic collection process, "
        "alleged misconduct by investigating officers, and disputed the chain of custody "
        "for key physical exhibits."
    ),
    description=(
        "Two individuals were found deceased outside a Los Angeles residence. Forensic "
        "analysis produced DNA results linking Simpson to the scene. A glove recovered "
        "at the scene was matched to one found at Simpson's property. Simpson could not "
        "provide a verified alibi for the relevant time period. The defense presented "
        "expert testimony arguing that evidence samples were mishandled or contaminated, "
        "and that at least one lead investigator had a documented history of racial bias. "
        "After less than four hours of deliberation, the jury returned a not-guilty verdict."
    ),
)

DEREK_CHAUVIN = Case(
    name="State v. Derek Chauvin (2021)",
    charges="Second-degree murder, third-degree murder, and second-degree manslaughter",
    known_verdict="guilty",
    background=(
        "Minneapolis police officer Derek Chauvin was charged following the death of George "
        "Floyd on May 25, 2020. Bystander video showed Chauvin kneeling on Floyd's neck for "
        "approximately nine minutes and twenty-nine seconds while Floyd was handcuffed and "
        "face-down on the pavement. Floyd repeatedly said he could not breathe and lost "
        "consciousness. The medical examiner ruled the death a homicide."
    ),
    description=(
        "Officers responded to a call about an allegedly counterfeit $20 bill. Officer Derek "
        "Chauvin restrained George Floyd by kneeling on his neck and back for over nine "
        "minutes. Floyd became unresponsive while Chauvin maintained his position despite "
        "pleas from bystanders. The county medical examiner ruled the manner of death "
        "homicide, citing cardiopulmonary arrest complicating law enforcement subdual, "
        "restraint, and neck compression. The defense argued Floyd's pre-existing heart "
        "condition and fentanyl in his system contributed to his death."
    ),
)

# All available cases — add new ones here
CASES = {
    "oj_simpson": OJ_SIMPSON,
    "derek_chauvin": DEREK_CHAUVIN,
}
