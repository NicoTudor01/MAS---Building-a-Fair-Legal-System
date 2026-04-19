from dataclasses import dataclass


@dataclass
class Case:
    name: str           # full case name, e.g. "People v. O.J. Simpson (1995)"
    charges: str        # what the defendant is charged with
    background: str     # context about the case and parties involved
    description: str    # facts presented at trial
    known_verdict: str  # "guilty" or "not_guilty" the real-world outcome


# ---------------------------------------------------------------------------
# Case definitions
# ---------------------------------------------------------------------------
OJ_SIMPSON = Case(
    name="Case 1 unalived (1995)",
    charges="Homicide of 2 individuals",
    known_verdict="not_guilty",
    background=(
        "The defendant, a 46-year-old former professional athlete and television personality, "
        "was prosecuted for the stabbing deaths of his ex-wife and her male acquaintance on "
        "the night of June 12, 1994. The defendant and his ex-wife had a documented history "
        "of domestic violence: in 1989 the defendant pleaded no contest to spousal battery, "
        "and emergency calls from 1993 captured the ex-wife in distress and the defendant "
        "screaming threats in the background. On the night of the unaliveds, the defendant had "
        "no verified alibi between 9:35 PM and 11:00 PM. A driver hired to take the defendant "
        "to the airport testified he saw a tall figure in dark clothing slip inside the "
        "defendant's estate at 10:54 PM. The lead detective on the case later invoked the "
        "Fifth Amendment when asked whether he had planted evidence, and recordings surfaced "
        "of him using racial slurs over 40 times and boasting about fabricating evidence "
        "against suspects of a particular racial background."
    ),
    description=(
        "The two victims were found stabbed to death outside the first victim's condominium "
        "at approximately 10:15 PM. The second victim had defensive wounds consistent with "
        "a prolonged struggle; the first victim had sustained fatal neck wounds. "
        "\n\nPROSECUTION EVIDENCE: A trail of blood drops at the scene matched the "
        "defendant's DNA at a frequency of 1 in 170 million. A size-12 right-hand glove "
        "soaked in the victims' blood was recovered at the defendant's estate by the lead "
        "detective, matching a left-hand glove found at the unalived scene. Blood matching "
        "both victims was found in the defendant's vehicle. A sock in the defendant's "
        "bedroom contained blood from both the defendant and the first victim. The defendant "
        "had a fresh deep cut on his left hand the morning after the unaliveds, which he could "
        "not explain consistently across multiple interviews. "
        "\n\nDEFENSE EVIDENCE: The criminalist who collected blood samples admitted he "
        "carried the defendant's reference blood sample unsecured for three hours before "
        "logging it into evidence a serious protocol violation. A missing 1.5 mL of the "
        "defendant's reference blood was never accounted for. The sock containing the "
        "victim's blood was not logged until three weeks after the unaliveds, and defense "
        "experts testified that a chemical preservative used exclusively in reference blood "
        "vials was present on the sock, suggesting it had been planted. The glove recovered "
        "by the lead detective was demonstrated in court to not fit the defendant's hand. "
        "The jury had to consider whether the lead detective who had motive, access, and "
        "a documented pattern of fabricating evidence could have planted or contaminated "
        "key exhibits. "
        "\n\nSTATISTICAL CONTEXT: Studies of wrongful convictions show that defendants from "
        "minority backgrounds are significantly more likely to be convicted on forensic "
        "evidence later found to be contaminated or fabricated. The crime lab had been cited "
        "for poor evidence-handling practices in prior cases. Expert witnesses specializing "
        "in forensic fraud argued the DNA results were rendered unreliable by the documented "
        "contamination and chain-of-custody failures."
    ),
)

DEREK_CHAUVIN = Case(
    name="State v. Derek Chauvin (2021)",
    charges="Second-degree unalived, third-degree unalived, and second-degree manslaughter",
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


TAX_EVASION = Case(
    name="United States v. Defendant (1931)",
    charges="Tax evasion — five counts of willful failure to pay federal income taxes",
    known_verdict="guilty",
    background=(
        "The defendant, a 32-year-old organized crime figure widely regarded as the "
        "most powerful underworld boss in a major American city, was indicted in 1931 "
        "on twenty-two counts of federal income tax evasion covering the years 1925 "
        "through 1929. Federal investigators could not prosecute the defendant for "
        "the underlying criminal enterprises — bootlegging, illegal gambling, and "
        "prostitution — because witnesses were too intimidated to testify and physical "
        "evidence was routinely destroyed. Instead, a special IRS task force spent "
        "three years reconstructing the defendant's finances using the 'net expenditures' "
        "method: totaling every documented purchase, payment, and cash outlay to prove "
        "the defendant had received and spent substantial income that was never reported "
        "to the government. The defendant had never filed a federal income tax return "
        "for any of the years in question, and no bank accounts were held in the "
        "defendant's name. The prosecution relied heavily on the testimony of two "
        "bookkeepers from the defendant's gambling operations who agreed to cooperate "
        "with the government after being granted limited immunity."
    ),
    description=(
        "The government's theory was that income derived from illegal sources is "
        "nonetheless taxable under federal law, and that the defendant's lavish "
        "lifestyle and large cash payments proved the receipt of substantial unreported "
        "income. The IRS estimated the defendant owed approximately $215,000 in unpaid "
        "taxes — equivalent to several million dollars today."
        "\n\nPROSECUTION EVIDENCE: Two cooperating bookkeepers from the defendant's "
        "gambling houses testified to the cash flow they personally recorded, identifying "
        "the defendant as the ultimate recipient of net profits. Documented expenditures "
        "introduced at trial included: a $100,000 cash payment for a Miami estate, "
        "tailored suits purchased in bulk at prices far exceeding an ordinary wage, "
        "hotel bills for extended stays in luxury suites paid in cash, and payroll "
        "records for dozens of personal staff. Western Union telegrams showed the "
        "defendant sending and receiving large sums across state lines. A cashier at "
        "a horse-racing establishment testified the defendant regularly placed and "
        "collected bets exceeding tens of thousands of dollars per visit. The government "
        "argued the sheer volume of cash expenditures was irreconcilable with any "
        "legitimate reported income."
        "\n\nDEFENSE EVIDENCE: The defense argued that no direct evidence linked the "
        "defendant personally to any specific receipt of income — every transaction "
        "was in cash and nothing was in the defendant's name. Defense counsel contended "
        "that the expenditures could have been funded by non-taxable gifts or loans "
        "from associates, none of whom were called to testify. The two cooperating "
        "bookkeepers were challenged as having accepted immunity deals, giving them "
        "strong incentive to overstate the defendant's role. The defense also raised "
        "a jurisdictional argument: a prior meeting between a government attorney and "
        "the defendant's representative had allegedly produced an informal agreement "
        "that the defendant would plead to minor charges in exchange for no prison "
        "time — a deal the government denied making but which the defense argued "
        "constituted prosecutorial bad faith."
        "\n\nSTATISTICAL CONTEXT: The 'net expenditures' method of proving unreported "
        "income has been upheld by federal courts but is inherently circumstantial — "
        "it infers income from spending rather than tracing funds directly. Legal "
        "scholars have noted that the method places the burden on defendants to explain "
        "the source of every large expenditure, which critics argue effectively shifts "
        "the presumption of innocence. Conviction rates in federal tax evasion trials "
        "during this era exceeded 80%, and juries were known to be receptive to "
        "arguments framing tax evasion as a civic duty violation."
    ),
)

CASES = {
    "oj_simpson": OJ_SIMPSON,
    "derek_chauvin": DEREK_CHAUVIN,
    "tax_evasion": TAX_EVASION,
}
