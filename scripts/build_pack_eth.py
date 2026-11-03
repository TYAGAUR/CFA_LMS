"""Ethical and Professional Standards content pack.  python scripts/build_pack_eth.py, then re-seed."""

from packlib import EX, FUN, OL, WO, H, L, P, T, fc, q, sheet, topic, write_pack

LMS = []

# ---------------------------------------------------------------- LM1
LMS.append(
    dict(
        lm_no=1,
        title="Ethics and Trust in the Investment Profession",
        summary="Why trust matters in finance, what makes a profession, and a framework for ethical decisions.",
        los=[
            ("1.a", "explain", "Explain ethics and the role of a code of ethics in a profession."),
            ("1.b", "identify", "Identify challenges to ethical behaviour."),
            (
                "1.c",
                "describe",
                "Describe the features of a profession and the need for trust in investment management.",
            ),
            ("1.d", "distinguish", "Distinguish between ethical and legal standards."),
            ("1.e", "describe", "Describe and apply a framework for ethical decision-making."),
        ],
        topics=[
            topic(
                "Ethics, trust and professions",
                P(
                    "**Ethics** is a set of moral principles that guide behaviour: deciding what is right when no one "
                    "is "
                    "checking. A **code of ethics** writes those principles down so that members, clients and "
                    "regulators all know the standard expected."
                ),
                P(
                    "Clients hand investment professionals their savings and cannot easily judge the quality of the "
                    "advice. That information gap is why **trust** is the product the profession really sells."
                ),
                H("What makes a profession"),
                L(
                    "A body of **specialist knowledge** and high entry standards (exams, experience).",
                    "A **code of ethics** and standards of conduct that members agree to follow.",
                    "**Monitoring and enforcement**: members who break the code can be disciplined.",
                    "Commitment to **continuing education** and to serving clients and society, not just oneself.",
                ),
                FUN(
                    "Imagine a dentist who says 'Trust me, that tooth has to go' and also owns the tooth-pulling "
                    "franchise. You would want a code of ethics too."
                ),
            ),
            topic(
                "Challenges to ethical behaviour",
                L(
                    "**Overconfidence**: 'I am a good person, so whatever I decide must be ethical.'",
                    "**Situational influences**: money, prestige, deadlines, loyalty to a boss or team.",
                    "**Short-term focus**: chasing this quarter's bonus at the cost of long-term reputation.",
                ),
                P(
                    "**Legal is not the same as ethical.** Laws set a minimum, lag behind new products and differ "
                    "between countries. Some legal acts are unethical (exploiting a loophole to mislead clients), and "
                    "occasionally an ethical act can break a bad rule (whistle-blowing on fraud)."
                ),
                WO(
                    "Exam questions often describe an action that is legal and ask if it is acceptable. Being legal "
                    "is **not enough**; the Code and Standards may still be breached."
                ),
            ),
            topic(
                "A framework for ethical decisions",
                OL(
                    "**Identify**: the facts, the stakeholders and duties owed, the ethical principles and any "
                    "conflicts of interest.",
                    "**Consider**: situational influences, alternative actions, and seek guidance (compliance, "
                    "a trusted colleague, the Standards).",
                    "**Decide and act**.",
                    "**Reflect**: was the outcome as expected? What would you do differently?",
                ),
                EX(
                    "Riya, an analyst, is asked by her manager to raise a target price because the bank is pitching "
                    "for the company's bond issue. Identify: duty to clients relying on the research; conflict with "
                    "the banking team. Consider: pressure from her boss; options are to refuse, escalate to "
                    "compliance, or disclose. Act: keep the target her analysis supports and escalate. Reflect: "
                    "propose a firewall between research and banking."
                ),
                WO("The framework is a loop, not a checklist. Reflection feeds the next decision."),
            ),
        ],
        revision=sheet(
            "Ethical decision framework: Identify → Consider → Decide and act → Reflect",
            ("Ethics", "Moral principles guiding behaviour"),
            ("Code of ethics", "Written principles that members commit to"),
            ("Trust", "The core product in investment management"),
            ("Profession", "Knowledge, entry standards, code, enforcement, CPD, service"),
            ("Overconfidence", "Assuming your own choices are ethical"),
            ("Situational influence", "Money, prestige, pressure from others"),
            ("Legal vs ethical", "Law is the minimum; ethics often asks for more"),
        ),
        questions=[
            q(
                "E",
                "A written set of moral principles that members of a profession agree to follow is best called a:",
                ["Code of ethics", "Regulatory filing", "Service-level agreement"],
                0,
                "A code of ethics communicates the principles and conduct expected of members.",
                "1.a",
            ),
            q(
                "E",
                "Which is a feature of a profession?",
                [
                    "No entry requirements",
                    "Monitoring and enforcement of a code of conduct",
                    "Members serve only their own interests",
                ],
                1,
                "Professions set entry standards, adopt a code and discipline members who breach it.",
                "1.c",
            ),
            q(
                "M",
                "An analyst believes that because she has always been honest, any decision she makes is ethical. "
                "This is an example of:",
                ["A situational influence", "Short-termism", "Overconfidence bias"],
                2,
                "Overestimating one's own morality is overconfidence, a common barrier to ethical decisions.",
                "1.b",
            ),
            q(
                "M",
                "Which statement about legal and ethical standards is most accurate?",
                [
                    "Any legal action is ethical",
                    "Laws often set a minimum and ethical conduct can require more",
                    "Ethical standards never conflict with the law",
                ],
                1,
                "Laws lag, vary across countries and set only minimum conduct; ethics often demands more.",
                "1.d",
            ),
            q(
                "E",
                "The first step in the ethical decision-making framework is to:",
                ["Identify the facts, stakeholders and duties", "Act immediately", "Reflect on the outcome"],
                0,
                "The framework runs Identify, Consider, Decide and act, Reflect.",
                "1.e",
            ),
            q(
                "M",
                "A portfolio manager is offered a large bonus if she sells a high-fee fund to all her clients this "
                "quarter. The bonus is best described as a:",
                ["Situational influence", "Professional standard", "Regulatory requirement"],
                0,
                "Money and incentives are situational influences that can bias decisions.",
                "1.b",
            ),
            q(
                "H",
                "Trust is especially important in investment management mainly because:",
                [
                    "Fees are always fixed",
                    "Regulators guarantee returns",
                    "Clients find it hard to judge the quality of advice they receive",
                ],
                2,
                "Information asymmetry means clients rely on the professional's integrity.",
                "1.c",
            ),
            q(
                "M",
                "In the 'Consider' step of the framework, a member would most likely:",
                ["Publish the decision", "Seek guidance and weigh alternative actions", "Record lessons learned"],
                1,
                "Considering means evaluating influences and alternatives, and seeking advice where useful.",
                "1.e",
            ),
            q(
                "H",
                "An action is permitted in the country where a member works but is prohibited by the Code and "
                "Standards. The member should:",
                [
                    "Follow the local law because it is legal",
                    "Follow the stricter standard, the Code",
                    "Choose whichever is more profitable for clients",
                ],
                1,
                "Members follow the stricter of applicable law and the Code and Standards.",
                "1.d",
            ),
            q(
                "E",
                "Which is the last step of the ethical decision-making framework?",
                ["Identify", "Consider", "Reflect"],
                2,
                "Reflecting on the outcome closes the loop and improves future decisions.",
                "1.e",
            ),
        ],
        flashcards=[
            fc("Ethics", "Moral principles that guide behaviour, even when no one is watching."),
            fc(
                "Why trust matters in investing",
                "Clients cannot easily judge advice quality, so they rely on integrity.",
            ),
            fc("Features of a profession", "Specialist knowledge, entry standards, code, enforcement, CPD, service."),
            fc("Two big barriers to ethics", "Overconfidence and situational influences."),
            fc("Legal vs ethical", "Law is a minimum; ethical conduct may require more."),
            fc("Ethical decision framework", "Identify → Consider → Decide and act → Reflect."),
        ],
    )
)

# ---------------------------------------------------------------- LM2
LMS.append(
    dict(
        lm_no=2,
        title="Code of Ethics and Standards of Professional Conduct",
        summary="The six components of the Code, the seven Standards, and the professional conduct process.",
        los=[
            ("2.a", "describe", "Describe the structure of the CFA Institute professional conduct programme."),
            ("2.b", "identify", "Identify the six components of the Code of Ethics and the seven Standards."),
            ("2.c", "explain", "Explain the ethical responsibilities required by the Code and Standards."),
        ],
        topics=[
            topic(
                "The Code of Ethics",
                P("Members and candidates must:"),
                OL(
                    "Act with **integrity, competence, diligence, respect** and in an ethical manner with the public, "
                    "clients, employers, colleagues and others in the markets.",
                    "Place the **integrity of the profession and the interests of clients above their own** "
                    "personal interests.",
                    "Use **reasonable care and independent professional judgement**.",
                    "Practise and encourage others to practise in a **professional and ethical** manner.",
                    "Promote the **integrity and viability of global capital markets**.",
                    "**Maintain and improve** their professional competence and that of others.",
                ),
                FUN(
                    "The six-part Code is the 'be a good human' list. The Standards are the fine print that tells "
                    "you what 'good' means when your boss, your client and your bonus all want different things."
                ),
            ),
            topic(
                "The seven Standards",
                T(
                    ["Standard", "Covers"],
                    [
                        "I Professionalism",
                        "Knowledge of the law, independence and objectivity, misrepresentation, misconduct, competence",
                    ],
                    ["II Integrity of capital markets", "Material non-public information, market manipulation"],
                    [
                        "III Duties to clients",
                        "Loyalty, prudence and care; fair dealing; suitability; performance "
                        "presentation; confidentiality",
                    ],
                    ["IV Duties to employers", "Loyalty, additional compensation, supervisors' responsibilities"],
                    [
                        "V Investment analysis, recommendations and actions",
                        "Diligence and reasonable basis, communication with clients, record retention",
                    ],
                    ["VI Conflicts of interest", "Avoid or disclose, priority of transactions, referral fees"],
                    [
                        "VII Responsibilities as a member or candidate",
                        "Conduct in the programme, references to the designation and the programme",
                    ],
                ),
                WO(
                    "Clients come first, then the employer, then the member: the priority of transactions under "
                    "VI(B) follows the same order."
                ),
            ),
            topic(
                "The professional conduct programme",
                P(
                    "Professional conduct staff investigate possible breaches. Inquiries can start from a member's "
                    "annual **self-disclosure** statement, a written **complaint**, **media reports**, or analysis "
                    "of **exam proctor** reports."
                ),
                L(
                    "Staff may conclude no action is needed, issue a **cautionary letter**, or propose **sanctions**.",
                    "Sanctions range from public censure to **suspension or revocation** of membership and the "
                    "right to use the designation.",
                    "A member who rejects the proposed sanction can ask for a **hearing panel**.",
                ),
                WO(
                    "The disciplinary review committee oversees the process; the member is not convicted by "
                    "complaint alone. There is always a chance to respond."
                ),
            ),
        ],
        revision=sheet(
            "Priority: clients → employer → member",
            ("Code of Ethics", "Six principles: integrity, clients first, care, encourage, markets, competence"),
            ("Standard I", "Professionalism"),
            ("Standard II", "Integrity of capital markets"),
            ("Standard III", "Duties to clients"),
            ("Standard IV", "Duties to employers"),
            ("Standard V", "Investment analysis, recommendations and actions"),
            ("Standard VI", "Conflicts of interest"),
            ("Standard VII", "Responsibilities as member or candidate"),
            ("Conduct inquiry triggers", "Self-disclosure, complaints, media, proctor reports"),
        ),
        questions=[
            q(
                "E",
                "Under the Code of Ethics, members must place the integrity of the profession and the interests "
                "of clients:",
                [
                    "Above their own personal interests",
                    "Below their employer's interests",
                    "Equal to their own interests",
                ],
                0,
                "This is the second component of the Code of Ethics.",
                "2.b",
            ),
            q(
                "E",
                "Material non-public information is dealt with under which Standard?",
                ["I Professionalism", "II Integrity of capital markets", "IV Duties to employers"],
                1,
                "Standard II(A) covers MNPI and II(B) market manipulation.",
                "2.b",
            ),
            q(
                "M",
                "Suitability and fair dealing fall under:",
                [
                    "Standard III Duties to clients",
                    "Standard V Investment analysis",
                    "Standard VI Conflicts of interest",
                ],
                0,
                "III(B) Fair dealing and III(C) Suitability are duties to clients.",
                "2.b",
            ),
            q(
                "M",
                "Record retention is part of which Standard?",
                [
                    "III Duties to clients",
                    "IV Duties to employers",
                    "V Investment analysis, recommendations and actions",
                ],
                2,
                "V(C) Record retention sits with diligence and communication under Standard V.",
                "2.b",
            ),
            q(
                "E",
                "Which is not a way a professional conduct inquiry can begin?",
                ["A written complaint", "A member's annual self-disclosure", "A rise in the member's salary"],
                2,
                "Inquiries start from self-disclosure, complaints, media reports or proctor reports.",
                "2.a",
            ),
            q(
                "M",
                "A member who does not accept the sanction proposed by professional conduct staff may:",
                [
                    "Request a hearing before a panel",
                    "Ignore it with no consequence",
                    "Only appeal to a national court",
                ],
                0,
                "The member can reject the proposal, and the matter goes to a hearing panel.",
                "2.a",
            ),
            q(
                "H",
                "The most severe sanction available under the professional conduct programme is:",
                [
                    "A private warning",
                    "Revocation of membership and the right to use the designation",
                    "A fine paid to the client",
                ],
                1,
                "Revocation removes membership and the right to use the designation.",
                "2.a",
            ),
            q(
                "M",
                "'Use reasonable care and exercise independent professional judgement' is:",
                ["A component of the Code of Ethics", "A local securities law", "A GIPS requirement"],
                0,
                "It is the third principle of the Code of Ethics.",
                "2.b",
            ),
            q(
                "H",
                "Which ordering of priorities is consistent with the Code and Standards?",
                ["Member, employer, client", "Employer, client, member", "Client, employer, member"],
                2,
                "Clients come first, then the employer, then the member's own interests.",
                "2.c",
            ),
            q(
                "M",
                "Avoiding or disclosing conflicts and referral fees are covered under:",
                ["Standard VI", "Standard II", "Standard VII"],
                0,
                "VI(A) Avoid or disclose conflicts, VI(B) Priority of transactions, VI(C) Referral fees.",
                "2.b",
            ),
        ],
        flashcards=[
            fc(
                "Six components of the Code",
                "Integrity; clients first; reasonable care; encourage ethics; market integrity; competence.",
            ),
            fc(
                "Seven Standards (I–VII)",
                "Professionalism; Markets; Clients; Employers; Analysis; Conflicts; Member/Candidate.",
            ),
            fc("Order of priority", "Clients, then employer, then yourself."),
            fc("How a conduct inquiry starts", "Self-disclosure, complaint, media report, proctor report."),
            fc("Possible outcomes of an inquiry", "No action, cautionary letter, or sanctions up to revocation."),
            fc("Rejecting a proposed sanction", "The member can ask for a hearing panel."),
        ],
    )
)

# ---------------------------------------------------------------- LM3
LMS.append(
    dict(
        lm_no=3,
        title="Guidance for Standards I–VII",
        summary="What each Standard requires in practice, with the recommended procedures and common traps.",
        los=[
            (
                "3.a",
                "demonstrate",
                "Demonstrate the application of the Code and Standards to situations involving "
                "issues of professional integrity.",
            ),
            (
                "3.b",
                "distinguish",
                "Distinguish between conduct that conforms to the Code and Standards and conduct that violates them.",
            ),
            ("3.c", "recommend", "Recommend practices and procedures to prevent violations."),
        ],
        topics=[
            topic(
                "I Professionalism and II Integrity of capital markets",
                L(
                    "**I(A) Knowledge of the law**: follow the **stricter** of the law and the Code. If you know of a "
                    "violation, **dissociate** (stop working on it) and, if needed, report to compliance; you need not "
                    "report to regulators, though it may be appropriate.",
                    "**I(B) Independence and objectivity**: modest gifts are fine; client gifts must be disclosed to "
                    "the employer; gifts from issuers that could sway research are not.",
                    "**I(C) Misrepresentation**: no false claims, no plagiarism. Cite sources (recognised financial "
                    "and "
                    "statistical reporting services can be used without naming each).",
                    "**I(D) Misconduct**: no dishonesty, fraud or deceit that reflects badly on the profession.",
                    "**I(E) Competence**: act with and keep up competence.",
                    "**II(A) MNPI**: do not act or cause others to act on material non-public information. The "
                    "**mosaic theory** allows conclusions from public and non-material non-public pieces.",
                    "**II(B) Market manipulation**: no distorting prices or inflating volume to mislead.",
                ),
                EX(
                    "An analyst overhears in a lift that a client company will miss earnings badly. It is material "
                    "and not public. She must not trade, nor tip her family. She should encourage the company to "
                    "disclose it publicly."
                ),
                WO(
                    "Material = would likely move the price, or a reasonable investor would want it. Non-public = "
                    "not yet disseminated to the market. Both must hold."
                ),
            ),
            topic(
                "III Duties to clients and IV Duties to employers",
                L(
                    "**III(A) Loyalty, prudence and care**: the duty is owed to the **client** (for a pension plan, "
                    "the "
                    "beneficiaries). Proxy voting is part of it. Soft-dollar benefits must benefit the client.",
                    "**III(B) Fair dealing**: treat all clients **fairly**, not necessarily equally. Disseminate "
                    "recommendations at the same time; allocate block trades pro rata.",
                    "**III(C) Suitability**: know the client, write an IPS, review at least annually.",
                    "**III(D) Performance presentation**: fair, accurate, complete. GIPS compliance is one way to meet "
                    "it.",
                    "**III(E) Confidentiality**: keep client information private unless it reveals illegal activity "
                    "or the law requires disclosure.",
                    "**IV(A) Loyalty to employer**: you may prepare to leave, but not take client lists or files, or "
                    "solicit clients before you leave.",
                    "**IV(B) Additional compensation**: get **written consent** from the employer before accepting "
                    "outside pay that competes with it.",
                    "**IV(C) Supervisors**: make reasonable efforts to prevent and detect violations, with adequate "
                    "compliance procedures.",
                ),
                WO(
                    "Fair dealing allows different service levels (premium tiers) **if** they are disclosed and "
                    "available to all clients who pay for them."
                ),
            ),
            topic(
                "V Analysis, VI Conflicts and VII Membership",
                L(
                    "**V(A) Diligence and reasonable basis**: thorough research; you may rely on third-party research "
                    "after reasonable checks.",
                    "**V(B) Communication**: disclose the investment process, risks and limitations; separate **fact "
                    "from opinion**.",
                    "**V(C) Record retention**: keep records supporting recommendations. Absent rules, **seven years** "
                    "is recommended. Records belong to the employer.",
                    "**VI(A) Avoid or disclose conflicts**: prominent, plain-language disclosure.",
                    "**VI(B) Priority of transactions**: clients and employer before personal trades; family accounts "
                    "that are clients are treated like any client.",
                    "**VI(C) Referral fees**: disclose to clients and employer any compensation for referrals.",
                    "**VII(A) Conduct in the programme**: no cheating, no disclosing exam questions; general opinions "
                    "on the exam are fine.",
                    "**VII(B) References to the designation**: 'CFA' is an adjective, never a noun; no claims that "
                    "the designation guarantees superior returns. 'Passed Level I' is fine; 'CFA Level I' is not a "
                    "designation.",
                ),
                FUN(
                    "Saying 'I am a CFA' is like saying 'I am an MBBS'. Say 'I am a CFA charterholder' and the "
                    "grammar police (and the Standards) will leave you alone."
                ),
            ),
        ],
        revision=sheet(
            "Stricter of law and Code · Dissociate · Disclose · Seven years of records",
            ("I(A)", "Follow the stricter rule; dissociate from violations"),
            ("I(B)", "Disclose client gifts; refuse issuer pressure"),
            ("II(A)", "Material + non-public = do not trade; mosaic theory allowed"),
            ("III(B)", "Fair, not equal; same-time dissemination; pro-rata allocation"),
            ("III(C)", "Know the client; IPS; review annually"),
            ("IV(A)", "Prepare to leave, but no client lists or early solicitation"),
            ("IV(B)", "Written consent for competing outside pay"),
            ("V(C)", "Records: seven years if no regulation"),
            ("VI(B)", "Clients, then employer, then personal trades"),
            ("VII(B)", "'CFA' is an adjective, never a noun"),
        ),
        questions=[
            q(
                "M",
                "A member learns her firm's product is being sold in breach of local regulation. Her first "
                "obligation under Standard I(A) is to:",
                ["Dissociate from the activity", "Report directly to the media", "Resign immediately"],
                0,
                "Members must dissociate; reporting to compliance is advised; resignation may be needed if it "
                "continues.",
                "3.a",
            ),
            q(
                "E",
                "An analyst uses public data plus non-material non-public observations to conclude a stock is "
                "overvalued. Under II(A) this is:",
                [
                    "A violation because the conclusion is material",
                    "Permitted under the mosaic theory",
                    "Permitted only with client consent",
                ],
                1,
                "The mosaic theory allows material conclusions built from public and non-material information.",
                "3.b",
            ),
            q(
                "M",
                "Under Standard III(B) Fair dealing, a firm that offers a premium service tier:",
                [
                    "Violates the Standard",
                    "Must charge all clients the same fee",
                    "Complies if the tier is disclosed and available to all clients",
                ],
                2,
                "Fair dealing means fair, not equal; differing service levels are fine when disclosed and open to all.",
                "3.b",
            ),
            q(
                "H",
                "A portfolio manager for a company pension plan owes the duty of loyalty primarily to:",
                ["The plan's beneficiaries", "The company's management", "The plan's trustees personally"],
                0,
                "For a pension plan, the client is the beneficiaries.",
                "3.a",
            ),
            q(
                "M",
                "A member plans to start a competing firm. While still employed she may:",
                [
                    "Copy client contact lists for later use",
                    "Solicit current clients to move with her",
                    "Make preparations such as registering the new firm",
                ],
                2,
                "Preparing to leave is allowed; taking records or soliciting clients before leaving is not.",
                "3.b",
            ),
            q(
                "E",
                "If no regulation applies, the Standards recommend keeping records for at least:",
                ["Two years", "Seven years", "Twenty years"],
                1,
                "Seven years is the recommended minimum when no regulation sets a period.",
                "3.c",
            ),
            q(
                "M",
                "A member accepts paid board work for a company that competes with his employer without telling "
                "the employer. This violates:",
                [
                    "Standard IV(B) Additional compensation",
                    "Standard III(E) Confidentiality",
                    "Standard VII(A) Conduct in the programme",
                ],
                0,
                "Outside pay that could compete requires written consent from all parties.",
                "3.b",
            ),
            q(
                "H",
                "Which statement about references to the designation complies with Standard VII(B)?",
                ["'He is a CFA.'", "'She is a CFA charterholder.'", "'CFA charterholders always earn higher returns.'"],
                1,
                "'CFA' must be used as an adjective, and no superior performance can be implied.",
                "3.b",
            ),
            q(
                "M",
                "A client's confidential information may be disclosed when:",
                [
                    "Another client asks for it",
                    "It would help win new business",
                    "The law requires it or it concerns illegal activity",
                ],
                2,
                "III(E) allows disclosure only when required by law, it involves illegal activity, or the client "
                "permits.",
                "3.a",
            ),
            q(
                "H",
                "To meet Standard IV(C), a supervisor who discovers a likely violation by a subordinate should first:",
                [
                    "Wait for the employee to admit it",
                    "Respond promptly, investigate and limit the employee's activity",
                    "Report only at the annual review",
                ],
                1,
                "Supervisors must act promptly to investigate and prevent further violations.",
                "3.c",
            ),
        ],
        flashcards=[
            fc("Stricter of the two", "Follow whichever is stricter: the law or the Code and Standards."),
            fc("Mosaic theory", "Material conclusions from public plus non-material non-public data are allowed."),
            fc("Fair dealing", "Fair, not equal: same-time dissemination, pro-rata allocation, disclosed tiers."),
            fc("Leaving an employer", "Prepare, yes. Take client lists or solicit before leaving, no."),
            fc("Record retention default", "Seven years; records belong to the employer."),
            fc("Correct use of 'CFA'", "Adjective only: 'CFA charterholder', never 'a CFA'."),
        ],
    )
)

# ---------------------------------------------------------------- LM4
LMS.append(
    dict(
        lm_no=4,
        title="Introduction to the Global Investment Performance Standards (GIPS)",
        summary="Why GIPS exists, who can claim compliance, composites, and verification.",
        los=[
            (
                "4.a",
                "explain",
                "Explain why the GIPS standards were created, who can claim compliance and who "
                "benefits from compliance.",
            ),
            ("4.b", "describe", "Describe the key concepts of the GIPS standards for firms."),
            ("4.c", "explain", "Explain the purpose of composites."),
            ("4.d", "explain", "Explain the requirements and benefits of verification."),
        ],
        topics=[
            topic(
                "Why GIPS exists",
                P(
                    "Before GIPS, managers could show only their best accounts (**cherry-picking**), drop closed funds "
                    "(**survivorship bias**) or pick flattering periods. GIPS are voluntary, ethical standards for "
                    "calculating and presenting investment performance so clients can **compare managers fairly**."
                ),
                L(
                    "**Who claims compliance**: only **investment firms** (and asset owners), never individuals or "
                    "software. Compliance is **firm-wide**.",
                    "**Who benefits**: prospective clients get comparable, complete records; firms gain credibility "
                    "and an edge when bidding for mandates, plus stronger internal controls.",
                    "There is **no partial compliance**: a firm either meets all requirements or may not claim it.",
                ),
                WO("An individual portfolio manager cannot claim GIPS compliance. Only the firm can."),
            ),
            topic(
                "Composites and key concepts",
                P(
                    "A **composite** groups all actual, fee-paying, discretionary portfolios managed to a similar "
                    "strategy or objective, for example 'Indian large-cap equity'. Every such portfolio must be in "
                    "at least one composite, so the record cannot be cherry-picked."
                ),
                L(
                    "Firms define themselves and document **policies and procedures**.",
                    "Present at least **five years** of GIPS-compliant performance (or since inception if shorter), "
                    "adding a year each year until **ten years** are shown.",
                    "Portfolios are valued at fair value; returns are time-weighted (money-weighted is allowed in some "
                    "cases such as private equity).",
                    "Pooled funds and asset owners are also covered by the 2020 edition.",
                ),
                EX(
                    "Prakash Capital runs 40 discretionary large-cap accounts. It may not build its composite from the "
                    "10 best ones. All 40 must be in the composite; non-discretionary accounts are excluded."
                ),
            ),
            topic(
                "Verification",
                P(
                    "**Verification** is an independent third-party review of whether the firm has complied with "
                    "composite construction requirements and its policies are designed to calculate and present "
                    "performance in line with GIPS, **firm-wide**. It is **optional but recommended**."
                ),
                L(
                    "Benefits: credibility with prospects and consultants, and better internal processes.",
                    "It does not certify any single composite's numbers; that is a separate **performance "
                    "examination**.",
                    "A firm must not claim verification of an individual composite unless it was examined.",
                ),
                FUN(
                    "GIPS is the cricket scorecard rule: you must count every innings you played, not only the "
                    "centuries you show your friends."
                ),
            ),
        ],
        revision=sheet(
            "Composite = ALL actual, fee-paying, discretionary portfolios with similar strategy",
            ("Who complies", "Firms (and asset owners), never individuals"),
            ("Scope", "Firm-wide; no partial compliance"),
            ("Track record", "At least 5 years, building to 10"),
            ("Purpose", "Fair, comparable performance; stops cherry-picking"),
            ("Verification", "Optional, recommended, firm-wide, independent"),
            ("Performance examination", "Separate review of a specific composite"),
        ),
        questions=[
            q(
                "E",
                "GIPS compliance can be claimed by:",
                ["An individual portfolio manager", "An investment firm", "A performance software vendor"],
                1,
                "Only firms (and asset owners) can claim compliance.",
                "4.a",
            ),
            q(
                "M",
                "The main purpose of composites is to:",
                [
                    "Prevent firms from presenting only their best-performing portfolios",
                    "Reduce management fees",
                    "Replace the need for verification",
                ],
                0,
                "Including all similar portfolios stops cherry-picking.",
                "4.c",
            ),
            q(
                "M",
                "Which portfolio must be included in a composite?",
                [
                    "A non-fee-paying staff account",
                    "A non-discretionary account",
                    "An actual, fee-paying, discretionary portfolio",
                ],
                2,
                "Every actual, fee-paying, discretionary portfolio must be in at least one composite.",
                "4.c",
            ),
            q(
                "E",
                "Verification under GIPS is:",
                ["Mandatory", "Optional but recommended", "Prohibited for small firms"],
                1,
                "Verification is voluntary, though strongly encouraged.",
                "4.d",
            ),
            q(
                "H",
                "A firm meets every GIPS requirement except the record-keeping rule. It may claim:",
                ["Partial compliance", "Compliance except for record keeping", "No GIPS compliance"],
                2,
                "There is no partial compliance.",
                "4.b",
            ),
            q(
                "M",
                "At first, a GIPS-compliant firm must present at least:",
                ["Five years of performance, or since inception if shorter", "One year", "Twenty years"],
                0,
                "It starts with at least five years and builds to ten.",
                "4.b",
            ),
            q(
                "M",
                "Verification tests whether the firm:",
                [
                    "Beat its benchmark",
                    "Has complied with composite construction requirements firm-wide and has "
                    "policies to calculate and present performance per GIPS",
                    "Charges competitive fees",
                ],
                1,
                "Verification is firm-wide and covers composite construction and policies.",
                "4.d",
            ),
            q(
                "E",
                "Survivorship bias in performance presentation occurs when a firm:",
                [
                    "Drops closed or poor-performing portfolios from its record",
                    "Includes every portfolio",
                    "Uses time-weighted returns",
                ],
                0,
                "Excluding closed portfolios flatters the record; GIPS prevents it.",
                "4.a",
            ),
            q(
                "H",
                "A consultant comparing two GIPS-compliant managers benefits mainly because:",
                [
                    "Both managers are guaranteed to outperform",
                    "Performance is calculated and presented on a consistent, complete basis",
                    "Both use the same benchmark",
                ],
                1,
                "GIPS gives comparable and complete records, not guaranteed returns.",
                "4.a",
            ),
            q(
                "M",
                "Which statement about a performance examination is correct?",
                [
                    "It is the same as verification",
                    "It replaces the need for composites",
                    "It is a separate review of a specific composite or pooled fund",
                ],
                2,
                "Examination focuses on particular composites; verification is firm-wide.",
                "4.d",
            ),
        ],
        flashcards=[
            fc("Who can claim GIPS compliance?", "Firms and asset owners only."),
            fc("Composite", "All actual, fee-paying, discretionary portfolios with a similar strategy."),
            fc("Partial compliance?", "Not allowed. All requirements or no claim."),
            fc("Minimum record", "5 years (or since inception), building to 10."),
            fc("Verification", "Optional, independent, firm-wide review."),
            fc("Problem GIPS solves", "Cherry-picking and survivorship bias in track records."),
        ],
    )
)

# ---------------------------------------------------------------- LM5
LMS.append(
    dict(
        lm_no=5,
        title="Ethics Application",
        summary="Working through realistic cases: spot the Standard, judge the conduct, recommend the fix.",
        los=[
            ("5.a", "evaluate", "Evaluate practices, policies and conduct relative to the Code and Standards."),
            (
                "5.b",
                "explain",
                "Explain how the practices, policies and conduct support or violate the Code and Standards.",
            ),
        ],
        topics=[
            topic(
                "How to attack an ethics case",
                OL(
                    "Find **who the member owes duties to**: client, employer, market.",
                    "Spot the **trigger**: a gift, a tip, a new job, a trade, a performance claim, a conflict.",
                    "Map it to the **Standard** and ask: was it disclosed? Was there consent? Was the client harmed or "
                    "put second?",
                    "Recommend a **procedure** that would prevent it next time.",
                ),
                WO(
                    "Disclosure fixes many conflicts, but **not** MNPI, misrepresentation or market manipulation. "
                    "You cannot disclose your way out of trading on inside information."
                ),
            ),
            topic(
                "Case 1: the hot IPO",
                EX(
                    "Anil manages accounts at Moti Securities. An oversubscribed IPO is allocated to the firm. He "
                    "puts shares in his own account and his brother's (a fee-paying client) before filling other "
                    "clients' orders. Violations: VI(B) priority of transactions (his own account first) and III(B) "
                    "fair dealing. His brother may participate only on the same terms as other clients, pro rata. "
                    "Fix: a written allocation policy, pro-rata fills, and pre-clearance of personal trades."
                ),
                WO(
                    "Family accounts that are fee-paying clients must be treated like other clients: not better, "
                    "and not worse."
                ),
            ),
            topic(
                "Case 2: the research report and the trip",
                EX(
                    "Kavya writes research on Surya Hotels. Surya offers a free week at its new resort for her family. "
                    "Accepting would threaten I(B) independence and objectivity. Acceptable alternatives: decline, or "
                    "have her firm pay for any genuine site visit. Separately, her report copies two charts from "
                    "another broker without credit: I(C) misrepresentation (plagiarism)."
                ),
                FUN(
                    "A free family holiday from the company you are rating 'Buy' is the finance version of a "
                    "referee accepting dinner from one team before the final."
                ),
            ),
        ],
        revision=sheet(
            "Case method: duty owed → trigger → Standard → disclosed/consented? → procedure",
            ("Disclosure cures", "Conflicts, referral fees, outside work (with consent)"),
            ("Disclosure does not cure", "MNPI, plagiarism, manipulation, misrepresentation"),
            ("Hot issues", "Clients first; family-client accounts pro rata"),
            ("Issuer-paid travel", "Pay your own way to stay independent"),
            ("Recommended fix", "Written policies, pre-clearance, training, monitoring"),
        ),
        questions=[
            q(
                "M",
                "A portfolio manager fills her own order for an oversubscribed IPO before client orders. She has "
                "most likely violated:",
                ["VI(B) Priority of transactions", "V(C) Record retention", "VII(A) Conduct in the programme"],
                0,
                "Client transactions must take priority over personal ones.",
                "5.a",
            ),
            q(
                "M",
                "An analyst's brother is a fee-paying client of the firm. In a hot IPO, the brother's account should:",
                [
                    "Be excluded entirely",
                    "Receive shares pro rata like any other client",
                    "Receive priority allocation",
                ],
                1,
                "Family accounts that are clients are treated like other clients.",
                "5.b",
            ),
            q(
                "H",
                "Which conflict can not be resolved by disclosure alone?",
                [
                    "Owning shares in a company you cover",
                    "Receiving referral fees",
                    "Trading on material non-public information",
                ],
                2,
                "Trading on MNPI is prohibited regardless of disclosure.",
                "5.b",
            ),
            q(
                "E",
                "An analyst accepts an all-expenses-paid family holiday from a company she covers. The Standard most "
                "at risk is:",
                ["I(B) Independence and objectivity", "IV(A) Loyalty", "III(D) Performance presentation"],
                0,
                "Lavish issuer gifts threaten objectivity.",
                "5.a",
            ),
            q(
                "M",
                "An analyst copies charts from another firm's report into his own without citing them. This is:",
                ["Acceptable if the data are public", "A violation of I(C) Misrepresentation", "A violation of II(B)"],
                1,
                "Using others' work without attribution is plagiarism, a form of misrepresentation.",
                "5.a",
            ),
            q(
                "M",
                "A manager tells prospects 'our strategy has never had a losing year' but omits two closed "
                "portfolios that lost money. This violates:",
                ["VI(C) Referral fees", "III(D) Performance presentation", "IV(B) Additional compensation"],
                1,
                "Performance must be fair, accurate and complete.",
                "5.a",
            ),
            q(
                "H",
                "Which firm procedure best prevents personal trading conflicts?",
                [
                    "Pre-clearance and reporting of personal trades with blackout periods",
                    "Allowing staff to trade freely",
                    "Disclosing trades only once a year",
                ],
                0,
                "Pre-clearance, reporting and blackout periods are recommended procedures.",
                "5.b",
            ),
            q(
                "E",
                "Before analysing an ethics case, the first thing to establish is:",
                ["The member's salary", "To whom the member owes duties", "The stock's price target"],
                1,
                "Identifying duties owed frames which Standards apply.",
                "5.a",
            ),
            q(
                "M",
                "A member receives a referral fee from a broker for sending clients and discloses it to both the "
                "employer and clients in advance. This is:",
                ["Compliant with VI(C)", "A violation of II(A)", "A violation of III(E)"],
                0,
                "Referral fees are permitted when disclosed before the engagement.",
                "5.b",
            ),
            q(
                "H",
                "A supervisor's firm has no written compliance procedures, and a subordinate front-runs client "
                "trades. The supervisor most likely violated:",
                ["I(E) Competence", "VII(B)", "IV(C) Responsibilities of supervisors"],
                2,
                "Supervisors must ensure adequate procedures exist to prevent violations.",
                "5.a",
            ),
        ],
        flashcards=[
            fc("Ethics case: step 1", "Who is owed a duty: client, employer or market?"),
            fc("Not curable by disclosure", "MNPI, plagiarism, misrepresentation, manipulation."),
            fc("Hot IPO rule", "Clients first; family-client accounts pro rata."),
            fc("Issuer-paid trips", "Pay your own way where possible to keep independence."),
            fc("Front-running", "Trading ahead of client orders; breaches VI(B)."),
            fc("Prevent personal-trading conflicts", "Pre-clearance, reporting, blackout periods."),
        ],
    )
)


if __name__ == "__main__":
    # Prototype ethics questions: client priority is LM2; MNPI and duty of loyalty are Standards guidance (LM3).
    write_pack("eth", "Ethical and Professional Standards", LMS, {"34": 2, "35": 3, "36": 3}, balance_keys=True)
