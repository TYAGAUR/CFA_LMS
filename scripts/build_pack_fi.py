"""Fixed Income content pack.  python scripts/build_pack_fi.py, then re-seed."""

from packlib import EX, FUN, FX, OL, WO, H, L, P, T, fc, q, sheet, topic, write_pack

LMS = []

# ---------------------------------------------------------------- LM1
LMS.append(
    dict(
        lm_no=1,
        title="Fixed-Income Instrument Features",
        summary="The basic terms of a bond, the indenture and covenants, and credit enhancements.",
        los=[
            ("1.a", "describe", "Describe the features of a fixed-income security."),
            (
                "1.b",
                "describe",
                "Describe the contents of a bond indenture and contrast affirmative and negative covenants.",
            ),
            ("1.c", "describe", "Describe collateral and credit enhancements."),
        ],
        topics=[
            topic(
                "Basic features",
                T(
                    ["Feature", "Meaning"],
                    ["Issuer", "Government, agency, supranational, company, SPE"],
                    ["Maturity / tenor", "Date principal is repaid; time remaining"],
                    ["Par (face) value", "Principal repaid at maturity"],
                    ["Coupon rate", "Annual interest as % of par; frequency (annual, semi-annual)"],
                    ["Currency", "Dual-currency bonds pay coupons in one currency and principal in another"],
                    ["Seniority", "Senior or subordinated; secured or unsecured"],
                ),
                EX(
                    "A ₹1,000 face bond with a 7% annual coupon pays **₹70 a year** and ₹1,000 at maturity. "
                    "Semi-annually "
                    "it would pay ₹35 every six months."
                ),
                WO(
                    "Bonds with maturities of one year or less trade in the **money market**; longer ones are "
                    "capital market securities."
                ),
            ),
            topic(
                "Indenture, covenants and enhancements",
                L(
                    "The **indenture** (trust deed) sets out the issuer's obligations and investors' rights; a "
                    "**trustee** acts for bondholders.",
                    "**Affirmative covenants**: what the issuer must do (pay on time, maintain insurance, file "
                    "reports, "
                    "pari passu).",
                    "**Negative covenants**: what it must not do (extra debt above a limit, sell key assets, negative "
                    "pledge, pay dividends beyond a limit).",
                    "**Collateral**: secured bonds are backed by specific assets; **debentures** in many markets are "
                    "unsecured.",
                    "**Internal enhancements**: subordination (tranching), overcollateralisation, excess spread, "
                    "reserve accounts.",
                    "**External enhancements**: guarantees, letters of credit, surety bonds.",
                ),
                FUN(
                    "Negative covenants are the 'no girlfriends till exams' rules of the bond world. The parents "
                    "(bondholders) want their money back before anything fun happens."
                ),
            ),
        ],
        revision=sheet(
            "Coupon payment = coupon rate × par ÷ payments per year",
            ("Indenture", "Legal contract; trustee represents holders"),
            ("Affirmative covenant", "Must do"),
            ("Negative covenant", "Must not do"),
            ("Secured bond", "Backed by collateral"),
            ("Internal enhancement", "Subordination, overcollateralisation, reserves"),
            ("External enhancement", "Guarantee, letter of credit"),
        ),
        questions=[
            q(
                "E",
                "A bond with ₹1,000 face value and a 7% annual coupon pays an annual coupon of:",
                ["₹70", "₹7", "₹700"],
                0,
                "7% × 1,000 = 70.",
                "1.a",
            ),
            q(
                "M",
                "A covenant requiring the issuer to maintain insurance on its assets is:",
                ["A negative covenant", "An affirmative covenant", "A credit enhancement"],
                1,
                "It requires an action.",
                "1.b",
            ),
            q(
                "M",
                "A covenant limiting additional borrowing is:",
                ["Affirmative", "Negative", "External"],
                1,
                "It restricts the issuer.",
                "1.b",
            ),
            q(
                "E",
                "The party that represents bondholders' interests under the indenture is the:",
                ["Underwriter", "Trustee", "Rating agency"],
                1,
                "The trustee monitors compliance.",
                "1.b",
            ),
            q(
                "M",
                "Which is an internal credit enhancement?",
                ["A bank letter of credit", "Overcollateralisation", "A parent company guarantee"],
                1,
                "Overcollateralisation is built into the structure.",
                "1.c",
            ),
            q(
                "H",
                "A bond pays coupons in US dollars and principal in yen. It is a:",
                ["Dual-currency bond", "Floating-rate note", "Covered bond"],
                0,
                "Two currencies are used.",
                "1.a",
            ),
            q(
                "E",
                "A bank guarantee backing a bond is a(n):",
                ["Internal credit enhancement", "External credit enhancement", "Negative covenant"],
                1,
                "It comes from a third party.",
                "1.c",
            ),
            q(
                "M",
                "A ₹1,000 bond with a 6% coupon paid semi-annually pays each period:",
                ["₹60", "₹30", "₹15"],
                1,
                "6% × 1,000 ÷ 2 = 30.",
                "1.a",
            ),
            q(
                "H",
                "A negative pledge clause prevents the issuer from:",
                [
                    "Paying coupons",
                    "Pledging assets to other lenders in a way that ranks them ahead",
                    "Filing financial statements",
                ],
                1,
                "It protects unsecured holders' position.",
                "1.b",
            ),
            q(
                "E",
                "A fixed-income security with an original maturity of six months is a:",
                ["Capital market security", "Money market security", "Perpetual bond"],
                1,
                "One year or less is money market.",
                "1.a",
            ),
        ],
        flashcards=[
            fc("Basic bond features", "Issuer, maturity, par, coupon, currency, seniority."),
            fc("Indenture and trustee", "Contract of terms; trustee acts for holders."),
            fc("Affirmative vs negative covenant", "Must do vs must not do."),
            fc("Internal enhancements", "Subordination, overcollateralisation, excess spread, reserves."),
            fc("External enhancements", "Guarantees, letters of credit, surety."),
            fc("Money vs capital market", "≤ 1 year vs > 1 year maturity."),
        ],
    )
)

# ---------------------------------------------------------------- LM2
LMS.append(
    dict(
        lm_no=2,
        title="Fixed-Income Cash Flows and Types",
        summary="Principal repayment structures, coupon structures, and bonds with embedded options.",
        los=[
            ("2.a", "describe", "Describe common cash flow structures of fixed-income instruments."),
            ("2.b", "describe", "Describe coupon structures such as floating-rate, step-up, PIK and inflation-linked."),
            ("2.c", "describe", "Describe contingency provisions: callable, putable and convertible bonds."),
        ],
        topics=[
            topic(
                "Principal and coupon structures",
                L(
                    "**Bullet**: all principal at maturity.",
                    "**Fully amortising**: equal payments repay principal over the life (like a home loan).",
                    "**Partially amortising**: some principal repaid, a **balloon** at the end.",
                    "**Sinking fund**: issuer retires part of the issue each year.",
                    "**Floating-rate note (FRN)**: coupon = market reference rate (MRR) + quoted margin, reset "
                    "periodically.",
                    "**Step-up**: coupon rises on a schedule.",
                    "**Payment-in-kind (PIK)**: pays interest with more bonds.",
                    "**Deferred coupon**: no coupons for an initial period.",
                    "**Inflation-linked**: principal or coupon indexed to inflation.",
                ),
                EX(
                    "An FRN pays MRR + 1.5%, reset semi-annually. If MRR is 6.8% at reset, the next annual coupon rate "
                    "is "
                    "8.3%, so a ₹100 face note pays **₹4.15** for the half-year."
                ),
            ),
            topic(
                "Embedded options",
                L(
                    "**Callable**: issuer can redeem early; benefits the **issuer**; investors demand a higher yield.",
                    "**Putable**: holder can sell back early; benefits the **investor**; lower yield.",
                    "**Convertible**: holder can convert into shares. Conversion value = conversion ratio × share "
                    "price.",
                ),
                EX(
                    "A ₹1,000 convertible has a conversion ratio of 20. With the share at ₹45, conversion value = "
                    "20 × 45 = **₹900**. If the bond trades at ₹960, the conversion premium = 60."
                ),
                WO("Who owns the option? Callable → issuer. Putable and convertible → investor."),
                FUN(
                    "A callable bond is like lending your cousin money with a clause letting him repay early, which "
                    "he will do the moment he finds a cheaper lender."
                ),
            ),
        ],
        revision=sheet(
            "FRN coupon = MRR + quoted margin · Conversion value = conversion ratio × share price",
            ("Bullet", "Principal at maturity"),
            ("Amortising", "Principal repaid over life"),
            ("Sinking fund", "Part of issue retired regularly"),
            ("PIK", "Interest paid in more bonds"),
            ("Callable", "Issuer's option; higher yield"),
            ("Putable", "Investor's option; lower yield"),
            ("Convertible", "Investor converts to shares"),
        ),
        questions=[
            q(
                "E",
                "A bond that repays all principal at maturity is a:",
                ["Bullet bond", "Fully amortising bond", "Sinking fund bond"],
                0,
                "Bullet = lump sum at the end.",
                "2.a",
            ),
            q(
                "M",
                "An FRN pays MRR + 1.5%. At reset MRR is 6.8%. The annualised coupon rate for the next period is:",
                ["6.8%", "8.3%", "5.3%"],
                1,
                "6.8 + 1.5 = 8.3%.",
                "2.b",
            ),
            q(
                "M",
                "Which bond gives the option to the investor?",
                ["Callable bond", "Putable bond", "Sinking fund bond"],
                1,
                "The holder can put the bond back.",
                "2.c",
            ),
            q(
                "M",
                "Compared with an otherwise identical straight bond, a callable bond has a:",
                ["Lower yield", "Higher yield", "Identical yield"],
                1,
                "Investors are compensated for the issuer's option.",
                "2.c",
            ),
            q(
                "H",
                "A convertible bond has a conversion ratio of 20 and the share trades at ₹45. The conversion value is:",
                ["₹900", "₹450", "₹2,000"],
                0,
                "20 × 45 = 900.",
                "2.c",
            ),
            q(
                "E",
                "A bond that pays interest in the form of additional bonds is a:",
                ["Step-up bond", "Payment-in-kind bond", "Zero-coupon bond"],
                1,
                "PIK bonds defer cash interest.",
                "2.b",
            ),
            q(
                "M",
                "A home-loan-style bond with equal payments that repay all principal by maturity is:",
                ["Bullet", "Partially amortising", "Fully amortising"],
                2,
                "Principal is repaid over the life.",
                "2.a",
            ),
            q(
                "M",
                "A partially amortising bond ends with:",
                ["No payment", "A balloon payment", "Conversion into shares"],
                1,
                "Remaining principal is paid at maturity.",
                "2.a",
            ),
            q(
                "H",
                "An inflation-linked bond protects investors mainly against:",
                ["Default risk", "Loss of purchasing power", "Call risk"],
                1,
                "Payments rise with inflation.",
                "2.b",
            ),
            q(
                "E",
                "A sinking fund provision requires the issuer to:",
                ["Retire part of the issue over time", "Pay no coupons", "Convert the bond to equity"],
                0,
                "It reduces credit risk at maturity.",
                "2.a",
            ),
        ],
        flashcards=[
            fc("Bullet vs amortising", "All principal at end vs repaid over life."),
            fc("FRN coupon", "MRR + quoted margin, reset periodically."),
            fc("PIK bond", "Interest paid with more bonds."),
            fc("Callable bond", "Issuer's option; higher yield for investors."),
            fc("Putable bond", "Investor's option; lower yield."),
            fc("Conversion value", "Conversion ratio × share price."),
        ],
    )
)

# ---------------------------------------------------------------- LM3
LMS.append(
    dict(
        lm_no=3,
        title="Fixed-Income Issuance and Trading",
        summary="How bond markets are segmented, how bonds are issued, and how they trade.",
        los=[
            ("3.a", "describe", "Describe the classification of global fixed-income markets."),
            ("3.b", "describe", "Describe the mechanisms by which fixed-income securities are issued."),
            ("3.c", "describe", "Describe secondary markets for fixed-income securities and their liquidity."),
        ],
        topics=[
            topic(
                "Market classification",
                L(
                    "By **issuer**: sovereign, non-sovereign government, quasi-government, supranational, corporate "
                    "(financial and non-financial), securitised.",
                    "By **credit quality**: **investment grade** (BBB− / Baa3 or better) vs **high yield**.",
                    "By **maturity**: money market (≤ 1 year) vs capital market.",
                    "By **currency** and **geography**: domestic, foreign, **Eurobond** (issued outside the currency's "
                    "home country), global bonds; developed vs emerging markets.",
                    "**Green bonds** and other ESG-labelled bonds fund environmental projects.",
                ),
                WO(
                    "The investment-grade boundary matters: many funds may hold only IG bonds, so a downgrade to "
                    "BB+ forces selling."
                ),
            ),
            topic(
                "Primary and secondary markets",
                T(
                    ["Method", "How it works"],
                    ["Underwritten offering", "Bank buys the whole issue and resells it, bearing the risk"],
                    ["Best-efforts offering", "Bank sells as much as it can; no guarantee"],
                    ["Auction", "Typical for government bonds"],
                    ["Shelf registration", "Register once, issue in tranches over time"],
                    ["Private placement", "Sold directly to a few qualified investors; less liquid"],
                ),
                L(
                    "Most bonds trade **over the counter** through dealers, not on exchanges.",
                    "Liquidity is measured by the **bid–ask spread**; on-the-run government bonds are the most liquid.",
                    "Settlement: government bonds often T+1; corporates T+1 or T+2.",
                ),
                FUN(
                    "Buying a rarely traded corporate bond is like buying a vintage scooter: easy to buy from the "
                    "enthusiast, hard to sell when you need cash on a Monday."
                ),
            ),
        ],
        revision=sheet(
            "Investment grade = BBB− / Baa3 or higher",
            ("Eurobond", "Issued outside the home country of its currency"),
            ("Underwritten", "Bank bears placement risk"),
            ("Best efforts", "Bank acts as agent"),
            ("Shelf registration", "Issue in tranches"),
            ("Private placement", "Few investors, illiquid"),
            ("Secondary trading", "Mostly OTC dealers"),
        ),
        questions=[
            q(
                "E",
                "A bond rated BBB− by a rating agency is:",
                ["High yield", "Investment grade", "In default"],
                1,
                "BBB− is the lowest investment-grade rating.",
                "3.a",
            ),
            q(
                "M",
                "A rupee-denominated bond issued in London by an Indian company is best described as a:",
                ["Domestic bond", "Eurobond", "Municipal bond"],
                1,
                "It is issued outside the home market of its currency.",
                "3.a",
            ),
            q(
                "M",
                "In an underwritten offering, the investment bank:",
                [
                    "Acts only as an agent",
                    "Buys the entire issue and bears the risk of reselling it",
                    "Lends to the issuer",
                ],
                1,
                "The underwriter guarantees the proceeds.",
                "3.b",
            ),
            q(
                "E",
                "Most corporate bonds trade in:",
                ["Exchange order books", "Over-the-counter dealer markets", "Auctions"],
                1,
                "Dealers make the market.",
                "3.c",
            ),
            q(
                "M",
                "Shelf registration allows an issuer to:",
                ["Avoid all disclosure", "Register once and sell bonds in tranches over time", "Issue only to banks"],
                1,
                "It speeds up later issues.",
                "3.b",
            ),
            q(
                "H",
                "Compared with a public offering, a private placement is typically:",
                ["More liquid", "Less liquid and sold to fewer, qualified investors", "Always underwritten"],
                1,
                "There is little secondary market.",
                "3.b",
            ),
            q(
                "E",
                "Government bonds are most commonly issued through:",
                ["Best-efforts offerings", "Auctions", "Private placements"],
                1,
                "Treasuries and G-secs are auctioned.",
                "3.b",
            ),
            q(
                "M",
                "A narrower bid–ask spread indicates:",
                ["Lower liquidity", "Higher liquidity", "Higher credit risk"],
                1,
                "Trading costs are lower.",
                "3.c",
            ),
            q(
                "M",
                "Bonds whose proceeds fund environmental projects are:",
                ["Green bonds", "PIK bonds", "Covered bonds"],
                0,
                "They are ESG-labelled bonds.",
                "3.a",
            ),
            q(
                "H",
                "Why does a downgrade from BBB− to BB+ often hurt a bond's price sharply?",
                ["Coupons stop", "Many investors must sell non-investment-grade bonds", "It becomes callable"],
                1,
                "Mandates restrict holdings to investment grade.",
                "3.a",
            ),
        ],
        flashcards=[
            fc("Investment grade cut-off", "BBB− (S&P/Fitch), Baa3 (Moody's)."),
            fc("Eurobond", "Issued outside its currency's home country."),
            fc("Underwritten vs best efforts", "Bank bears risk vs bank acts as agent."),
            fc("Shelf registration", "Register once, issue tranches later."),
            fc("Private placement", "Direct sale to few investors; illiquid."),
            fc("Where bonds trade", "Mostly OTC dealer markets."),
        ],
    )
)

# ---------------------------------------------------------------- LM4
LMS.append(
    dict(
        lm_no=4,
        title="Fixed-Income Markets for Corporate Issuers",
        summary="Short-term funding through banks, commercial paper and repos, and long-term corporate debt.",
        los=[
            (
                "4.a",
                "compare",
                "Compare short-term funding alternatives available to corporations and financial institutions.",
            ),
            ("4.b", "describe", "Describe repurchase agreements and their risks."),
            ("4.c", "contrast", "Contrast long-term funding of investment-grade and high-yield corporate issuers."),
        ],
        topics=[
            topic(
                "Short-term funding",
                L(
                    "**Bank sources**: lines of credit (committed or uncommitted), revolving credit, secured loans, "
                    "factoring of receivables.",
                    "**Commercial paper (CP)**: unsecured, short-term (up to 1 year, often under 90 days), usually "
                    "issued at a discount by strong borrowers. **Rollover risk** is covered by **backup lines** of "
                    "credit.",
                    "**Financial institutions** also fund via deposits, interbank loans, certificates of deposit and "
                    "repos.",
                ),
                WO(
                    "CP is cheap but must be refinanced constantly. In a crisis, CP markets can freeze, which is why "
                    "backup lines matter."
                ),
            ),
            topic(
                "Repos and long-term debt",
                P(
                    "In a **repurchase agreement**, one party sells a security and agrees to buy it back later at a "
                    "higher price; economically a collateralised loan. The **haircut (repo margin)** is the gap "
                    "between "
                    "the collateral's value and the loan."
                ),
                FX("Repurchase price = loan × (1 + repo rate × days/360)"),
                EX(
                    "A dealer repos bonds worth ₹102 crore for ₹100 crore (haircut ≈ 2%) for 30 days at 6%. Repurchase "
                    "price "
                    "= 100 × (1 + 0.06 × 30/360) = **₹100.5 crore**."
                ),
                L(
                    "Repo rates are lower for high-quality, liquid collateral, short terms and strong counterparties.",
                    "**Investment-grade** issuers fund with long-term bullet bonds, often at fixed rates, and with "
                    "**medium-term notes**.",
                    "**High-yield** issuers rely more on bank loans and secured debt, with tighter covenants and "
                    "call features.",
                ),
                FUN(
                    "A repo is pawning your gold for a month. You get cash now, the jeweller keeps a margin, and "
                    "you buy it back with a little interest."
                ),
            ),
        ],
        revision=sheet(
            "Repurchase price = loan × (1 + repo rate × t/360) · Haircut = (collateral − loan)/collateral",
            ("Commercial paper", "Unsecured, short-term, discount, needs backup lines"),
            ("Rollover risk", "Cannot refinance maturing CP"),
            ("Repo", "Collateralised short-term loan"),
            ("Reverse repo", "The lender's side"),
            ("Lower repo rate", "Better collateral, shorter term"),
            ("IG long-term funding", "Fixed-rate bonds, MTNs"),
            ("HY funding", "Loans, secured debt, more covenants"),
        ),
        questions=[
            q(
                "E",
                "Commercial paper is best described as:",
                ["Long-term secured debt", "Short-term unsecured debt", "Equity"],
                1,
                "CP matures within a year.",
                "4.a",
            ),
            q(
                "M",
                "Issuers of commercial paper maintain backup lines of credit mainly to manage:",
                ["Interest rate risk", "Rollover risk", "Currency risk"],
                1,
                "Backup lines repay CP if it cannot be rolled.",
                "4.a",
            ),
            q(
                "M",
                "A ₹100 crore 30-day repo at 6% has a repurchase price closest to:",
                ["₹100.5 crore", "₹106.0 crore", "₹101.0 crore"],
                0,
                "100 × (1 + 0.06 × 30/360) = 100.5.",
                "4.b",
            ),
            q(
                "E",
                "Economically, a repurchase agreement is a:",
                ["Collateralised loan", "Equity sale", "Credit default swap"],
                0,
                "Securities are pledged against cash.",
                "4.b",
            ),
            q(
                "M",
                "The repo margin (haircut) is likely to be higher when the collateral is:",
                ["A short-term government bill", "A long-dated, illiquid corporate bond", "Cash"],
                1,
                "Riskier, less liquid collateral needs a bigger cushion.",
                "4.b",
            ),
            q(
                "H",
                "From the lender's perspective, the repo transaction is called a:",
                ["Repo", "Reverse repo", "Swap"],
                1,
                "The cash lender does a reverse repo.",
                "4.b",
            ),
            q(
                "M",
                "Compared with investment-grade issuers, high-yield issuers typically rely more on:",
                [
                    "Unsecured long-term bullet bonds",
                    "Bank loans and secured debt with stricter covenants",
                    "Commercial paper",
                ],
                1,
                "Lenders want more protection.",
                "4.c",
            ),
            q(
                "E",
                "Selling receivables to a third party at a discount for immediate cash is:",
                ["Factoring", "A repo", "A sinking fund"],
                0,
                "A bank or factor buys the receivables.",
                "4.a",
            ),
            q(
                "M",
                "Medium-term notes are mainly used by:",
                [
                    "Investment-grade corporate issuers for flexible long-term funding",
                    "Retail savers",
                    "Central banks only",
                ],
                0,
                "MTN programmes let issuers sell notes continuously.",
                "4.c",
            ),
            q(
                "H",
                "Which factor lowers the repo rate?",
                ["Longer repo term", "Weaker counterparty", "High-quality, liquid collateral"],
                2,
                "Safer collateral, cheaper loan.",
                "4.b",
            ),
        ],
        flashcards=[
            fc("Commercial paper", "Short-term, unsecured, discount; needs backup lines."),
            fc("Repo", "Sell and buy back later: a collateralised loan."),
            fc("Repurchase price", "Loan × (1 + repo rate × days/360)."),
            fc("Haircut", "Collateral value above the loan amount."),
            fc("Lower repo rates when", "Collateral is high quality, term short, counterparty strong."),
            fc("IG vs HY long-term funding", "Unsecured bonds/MTNs vs loans and secured debt."),
        ],
    )
)

# ---------------------------------------------------------------- LM5
LMS.append(
    dict(
        lm_no=5,
        title="Fixed-Income Markets for Government Issuers",
        summary="Sovereign, non-sovereign, agency and supranational bonds, and how governments issue debt.",
        los=[
            (
                "5.a",
                "describe",
                "Describe funding choices by sovereign and non-sovereign governments, agencies and supranationals.",
            ),
            (
                "5.b",
                "contrast",
                "Contrast the issuance, trading and characteristics of sovereign and non-sovereign government debt.",
            ),
        ],
        topics=[
            topic(
                "Sovereign debt",
                L(
                    "Issued by national governments to fund deficits; in **local currency** they are usually seen as "
                    "free of default risk, because the government can tax or print money.",
                    "**Foreign-currency** sovereign debt carries real default risk.",
                    "Issued by **auction**: competitive bids set the yield; non-competitive bids accept it.",
                    "**On-the-run** (newest) issues are most liquid and trade at slightly lower yields than "
                    "**off-the-run** issues.",
                    "Types: bills (≤ 1 year), notes and bonds, inflation-linked, floating-rate.",
                ),
                EX(
                    "India issues G-secs in rupees through RBI auctions. A dollar bond issued by a weaker emerging "
                    "market, "
                    "by contrast, depends on that country earning enough foreign exchange."
                ),
            ),
            topic(
                "Other government issuers",
                L(
                    "**Non-sovereign** (states, municipalities): **general obligation (GO)** bonds backed by taxing "
                    "power; "
                    "**revenue bonds** backed by a project's income (toll road, water utility), so riskier.",
                    "**Quasi-government / agencies**: government-sponsored entities, often with implicit support.",
                    "**Supranationals**: World Bank, Asian Development Bank; usually very highly rated.",
                ),
                WO(
                    "Revenue bonds depend only on the project's cash flows. Analysts check the **debt service coverage "
                    "ratio**."
                ),
                FUN("A revenue bond on a toll road is fine until everyone discovers the free flyover next door."),
            ),
        ],
        revision=sheet(
            "Local-currency sovereign ≈ default-free · Revenue bond risk > GO bond risk",
            ("Auction", "Competitive bids set the yield"),
            ("On-the-run", "Newest, most liquid, slightly lower yield"),
            ("Foreign-currency sovereign", "Real default risk"),
            ("GO bond", "Backed by taxing power"),
            ("Revenue bond", "Backed by project income"),
            ("Supranational", "Multilateral lenders, high ratings"),
        ),
        questions=[
            q(
                "E",
                "Sovereign bonds in a country's own currency are generally considered:",
                ["Highly risky", "Free of default risk", "Callable"],
                1,
                "The government can tax or create money.",
                "5.a",
            ),
            q(
                "M",
                "The most recently issued government bond of a given maturity is:",
                ["Off-the-run", "On-the-run", "A revenue bond"],
                1,
                "On-the-run bonds are the most liquid.",
                "5.b",
            ),
            q(
                "M",
                "A municipal bond backed by toll revenues from a bridge is a:",
                ["General obligation bond", "Revenue bond", "Supranational bond"],
                1,
                "It depends on the project's income.",
                "5.a",
            ),
            q(
                "H",
                "Compared with off-the-run issues, on-the-run government bonds typically have:",
                ["Higher yields", "Slightly lower yields due to greater liquidity", "No difference"],
                1,
                "Investors pay up for liquidity.",
                "5.b",
            ),
            q(
                "E",
                "The World Bank is an example of a:",
                ["Sovereign issuer", "Supranational issuer", "Municipal issuer"],
                1,
                "Owned by many governments.",
                "5.a",
            ),
            q(
                "M",
                "In a government bond auction, the yield is set by:",
                ["Non-competitive bids", "Competitive bids", "The rating agency"],
                1,
                "Competitive bids determine the clearing yield.",
                "5.b",
            ),
            q(
                "M",
                "Sovereign debt issued in a foreign currency:",
                [
                    "Has no default risk",
                    "Carries default risk because the government cannot print that currency",
                    "Is always AAA",
                ],
                1,
                "It must be repaid from foreign earnings.",
                "5.a",
            ),
            q(
                "H",
                "The key ratio analysts check for revenue bonds is the:",
                ["P/E ratio", "Debt service coverage ratio", "Current ratio"],
                1,
                "Project income ÷ debt service.",
                "5.b",
            ),
            q(
                "E",
                "Government securities maturing in one year or less are:",
                ["Bills", "Bonds", "Debentures"],
                0,
                "Bills are short-term.",
                "5.b",
            ),
            q(
                "M",
                "General obligation bonds are backed by:",
                ["A single project", "The issuer's taxing power", "A bank guarantee"],
                1,
                "Full faith and credit.",
                "5.a",
            ),
        ],
        flashcards=[
            fc("Local-currency sovereign debt", "Treated as default-free."),
            fc("On-the-run vs off-the-run", "Newest and most liquid vs older issues."),
            fc("GO vs revenue bond", "Taxing power vs project income."),
            fc("Supranational", "World Bank, ADB; high ratings."),
            fc("Government auction", "Competitive bids set the yield."),
            fc("Foreign-currency sovereign risk", "Default risk is real."),
        ],
    )
)

# ---------------------------------------------------------------- LM6
LMS.append(
    dict(
        lm_no=6,
        title="Fixed-Income Bond Valuation: Prices and Yields",
        summary="Pricing bonds with a single yield or spot rates, price–yield relationships, accrued interest "
        "and matrix pricing.",
        los=[
            ("6.a", "calculate", "Calculate a bond's price given a yield to maturity or spot rates."),
            ("6.b", "identify", "Identify the relationships among a bond's price, coupon rate, maturity and yield."),
            ("6.c", "describe", "Describe flat price, accrued interest and full price."),
            ("6.d", "describe", "Describe matrix pricing."),
        ],
        topics=[
            topic(
                "Pricing a bond",
                FX("Price = Σ CF_t ÷ (1 + r)^t  (single yield) · or each cash flow discounted at its own spot rate"),
                EX(
                    "3-year, 5% annual coupon, ₹100 face, yield 6%. Price = 5/1.06 + 5/1.06² + 105/1.06³ = 4.717 + "
                    "4.450 + "
                    "88.16 = **₹97.33** (a discount, since coupon < yield)."
                ),
                EX(
                    "With spot rates 4%, 5% and 6%: price = 5/1.04 + 5/1.05² + 105/1.06³ = 4.808 + 4.535 + 88.16 = "
                    "**₹97.50**."
                ),
                H("Price–yield relationships"),
                L(
                    "Price and yield move **inversely**.",
                    "Coupon < yield → **discount**; coupon > yield → **premium**; equal → par.",
                    "For the same yield change, **lower coupon** and **longer maturity** bonds move more.",
                    "The relationship is **convex**: prices rise more for a yield fall than they fall for an equal "
                    "rise.",
                    "**Pull to par**: a bond's price moves towards par as maturity approaches.",
                ),
            ),
            topic(
                "Accrued interest and matrix pricing",
                FX(
                    "Accrued interest = coupon per period × (days since last coupon ÷ days in period) · Full = flat + "
                    "AI"
                ),
                EX(
                    "Semi-annual coupon ₹3 per ₹100; 60 of 180 days since the last coupon. AI = 3 × 60/180 = "
                    "**₹1.00**. If "
                    "the flat (quoted) price is 98.50, the full price paid = **₹99.50**."
                ),
                P(
                    "**Matrix pricing** values bonds that rarely trade by interpolating yields of comparable, liquid "
                    "bonds "
                    "with similar credit quality, coupon and maturity."
                ),
                WO("Bonds are quoted at the **flat** price; the buyer pays the **full** (dirty) price."),
                FUN(
                    "Accrued interest is paying the previous tenant for the half month of electricity they already "
                    "paid for. Fair is fair."
                ),
            ),
        ],
        revision=sheet(
            "Price = Σ CF/(1 + r)^t · Full price = flat price + accrued interest",
            ("Inverse relationship", "Yield ↑, price ↓"),
            ("Discount bond", "Coupon < yield"),
            ("Premium bond", "Coupon > yield"),
            ("More sensitive", "Lower coupon, longer maturity"),
            ("Convexity", "Gains > losses for equal yield moves"),
            ("Matrix pricing", "Interpolate from comparable bonds"),
        ),
        questions=[
            q(
                "E",
                "When market yields rise, the price of an existing fixed-rate bond:",
                ["Rises", "Falls", "Stays the same"],
                1,
                "Price and yield move inversely.",
                "6.b",
            ),
            q(
                "M",
                "A 3-year, 5% annual coupon bond with ₹100 face value is priced at a 6% yield. Its price is closest "
                "to:",
                ["₹97.33", "₹100.00", "₹102.67"],
                0,
                "4.717 + 4.450 + 88.16 = 97.33.",
                "6.a",
            ),
            q(
                "E",
                "A bond whose coupon rate is above its yield to maturity trades at:",
                ["A discount", "Par", "A premium"],
                2,
                "Higher coupons than the market requires make it worth more.",
                "6.b",
            ),
            q(
                "H",
                "Using spot rates of 4%, 5% and 6%, a 3-year 5% annual coupon bond is priced closest to:",
                ["₹97.50", "₹97.33", "₹100.00"],
                0,
                "4.808 + 4.535 + 88.16 = 97.50.",
                "6.a",
            ),
            q(
                "M",
                "Semi-annual coupon ₹3, 60 of 180 days have passed and the flat price is 98.50. The full price is:",
                ["₹98.50", "₹99.50", "₹101.50"],
                1,
                "AI = 1.00; 98.50 + 1.00 = 99.50.",
                "6.c",
            ),
            q(
                "M",
                "For the same change in yield, which bond's price changes most?",
                ["Short maturity, high coupon", "Long maturity, low coupon", "Short maturity, low coupon"],
                1,
                "Long maturity and low coupon increase sensitivity.",
                "6.b",
            ),
            q(
                "E",
                "As a premium bond approaches maturity (yield unchanged), its price:",
                ["Rises", "Falls towards par", "Stays constant"],
                1,
                "Pull to par.",
                "6.b",
            ),
            q(
                "M",
                "Matrix pricing is used to:",
                ["Value bonds that trade rarely", "Calculate accrued interest", "Set coupon rates"],
                0,
                "It uses yields of comparable bonds.",
                "6.d",
            ),
            q(
                "H",
                "Because the price–yield curve is convex, a 1% fall in yield raises the price:",
                ["By less than a 1% rise lowers it", "By more than a 1% rise lowers it", "By exactly the same amount"],
                1,
                "Convexity favours price gains.",
                "6.b",
            ),
            q(
                "E",
                "The quoted price of a bond excluding accrued interest is the:",
                ["Full price", "Flat price", "Dirty price"],
                1,
                "Flat = clean price.",
                "6.c",
            ),
        ],
        flashcards=[
            fc("Bond price", "Sum of cash flows discounted at the yield or spot rates."),
            fc("Discount vs premium", "Coupon < yield vs coupon > yield."),
            fc("Most price-sensitive bonds", "Long maturity, low coupon."),
            fc("Full price", "Flat price + accrued interest."),
            fc("Pull to par", "Price converges to par at maturity."),
            fc("Matrix pricing", "Value illiquid bonds from comparable bonds' yields."),
        ],
    )
)

# ---------------------------------------------------------------- LM7
LMS.append(
    dict(
        lm_no=7,
        title="Yield and Yield Spread Measures for Fixed-Rate Bonds",
        summary="Periodicity, current yield, yield to call and worst, and spreads over benchmarks.",
        los=[
            ("7.a", "calculate", "Calculate annual yields on a bond for varying compounding periods."),
            ("7.b", "calculate", "Calculate and interpret yield measures for fixed-rate bonds."),
            ("7.c", "compare", "Compare, calculate and interpret yield spread measures."),
        ],
        topics=[
            topic(
                "Yield measures",
                FX("(1 + APR_m/m)^m = (1 + APR_n/n)^n · Current yield = annual coupon ÷ price"),
                EX("A 6% yield quoted semi-annually equals an effective annual yield of 1.03² − 1 = **6.09%**."),
                EX("A bond with a ₹60 coupon trades at ₹950. Current yield = 60/950 = **6.32%**."),
                L(
                    "**Yield to maturity**: IRR assuming held to maturity, coupons reinvested at the YTM, no default.",
                    "**Yield to call**: assumes redemption at the first (or each) call date and price.",
                    "**Yield to worst**: the lowest of YTM and all yields to call.",
                    "**Street convention** uses scheduled dates; the **true yield** uses actual payment dates "
                    "(weekends, holidays).",
                ),
            ),
            topic(
                "Spreads",
                T(
                    ["Spread", "Over"],
                    ["G-spread", "Government bond yield of the same maturity"],
                    ["I-spread", "Swap rate of the same maturity"],
                    ["Z-spread", "Constant spread over every point of the government spot curve"],
                    ["OAS", "Z-spread minus the value of embedded options"],
                ),
                EX("A 5-year corporate bond yields 8.1%; the 5-year G-sec yields 7.2%. **G-spread = 90 bp**."),
                WO(
                    "For a **callable** bond, OAS < Z-spread, because part of the spread pays for the issuer's call "
                    "option."
                ),
                FUN(
                    "The G-spread is the extra interest you demand to lend to your friend rather than to the "
                    "government. The worse his track record, the wider the spread."
                ),
            ),
        ],
        revision=sheet(
            "EAY = (1 + r/m)^m − 1 · Current yield = coupon/price · OAS = Z-spread − option value",
            ("YTM assumption", "Held to maturity; reinvest at YTM; no default"),
            ("Yield to worst", "Lowest of YTM and yields to call"),
            ("G-spread", "Over government yield"),
            ("I-spread", "Over swap rate"),
            ("Z-spread", "Over entire spot curve"),
            ("Callable bond", "OAS < Z-spread"),
        ),
        questions=[
            q(
                "M",
                "A 6% yield with semi-annual compounding is equivalent to an annual yield of:",
                ["6.00%", "6.09%", "5.91%"],
                1,
                "1.03² − 1 = 6.09%.",
                "7.a",
            ),
            q(
                "E",
                "A bond paying a ₹60 annual coupon trades at ₹950. Its current yield is closest to:",
                ["6.32%", "6.00%", "5.70%"],
                0,
                "60/950 = 6.32%.",
                "7.b",
            ),
            q(
                "M",
                "The yield to worst of a callable bond is:",
                ["The highest of its yields", "The lowest of YTM and yields to each call date", "Always the YTM"],
                1,
                "It is the most conservative yield.",
                "7.b",
            ),
            q(
                "M",
                "A corporate bond yields 8.1% and a government bond of the same maturity yields 7.2%. The G-spread is:",
                ["90 bp", "810 bp", "720 bp"],
                0,
                "8.1 − 7.2 = 0.9%.",
                "7.c",
            ),
            q(
                "H",
                "For a callable bond, the option-adjusted spread is:",
                ["Greater than the Z-spread", "Less than the Z-spread", "Equal to the Z-spread"],
                1,
                "OAS removes the value of the call, which the investor is short.",
                "7.c",
            ),
            q(
                "E",
                "The I-spread is measured relative to:",
                ["Government bond yields", "Swap rates", "Equity yields"],
                1,
                "I = interpolated swap rate.",
                "7.c",
            ),
            q(
                "M",
                "YTM assumes that coupons are reinvested at:",
                ["The current yield", "The yield to maturity", "Zero"],
                1,
                "A key, and often unrealistic, assumption.",
                "7.b",
            ),
            q(
                "H",
                "The Z-spread is a constant spread that, added to each:",
                [
                    "Government spot rate, makes the PV of cash flows equal the price",
                    "Coupon, gives the yield",
                    "Swap rate, gives the coupon",
                ],
                0,
                "It uses the whole spot curve.",
                "7.c",
            ),
            q(
                "M",
                "A yield that uses the actual payment dates, adjusting for weekends and holidays, is the:",
                ["Street convention yield", "True yield", "Current yield"],
                1,
                "True yield reflects actual timing.",
                "7.b",
            ),
            q(
                "E",
                "Which yield measure ignores capital gains and losses?",
                ["Yield to maturity", "Current yield", "Yield to call"],
                1,
                "It uses only coupon and price.",
                "7.b",
            ),
        ],
        flashcards=[
            fc("Converting periodicity", "(1 + r_m/m)^m = (1 + r_n/n)^n."),
            fc("Current yield", "Annual coupon ÷ price."),
            fc("Yield to worst", "Lowest of YTM and yields to call."),
            fc("G-spread vs I-spread", "Over government yield vs over swap rate."),
            fc("Z-spread", "Constant spread over the whole spot curve."),
            fc("OAS for callable bonds", "Z-spread minus the call option value; lower than Z."),
        ],
    )
)

# ---------------------------------------------------------------- LM8
LMS.append(
    dict(
        lm_no=8,
        title="Yield and Yield Spread Measures for Floating-Rate Instruments",
        summary="Quoted and discount margins on FRNs, and money market yield conventions.",
        los=[
            ("8.a", "calculate", "Calculate and interpret yield spread measures for floating-rate instruments."),
            ("8.b", "calculate", "Calculate and interpret yield measures for money market instruments."),
        ],
        topics=[
            topic(
                "Floating-rate notes",
                L(
                    "**Quoted margin (QM)**: spread over MRR set in the contract.",
                    "**Discount (required) margin (DM)**: spread the market now requires.",
                    "DM = QM → FRN priced at **par** on reset dates. DM > QM → **discount**. DM < QM → **premium**.",
                ),
                EX(
                    "An FRN pays MRR + 1.0%. The issuer's credit worsens and investors now require MRR + 1.5%. The FRN "
                    "trades **below par**."
                ),
                WO(
                    "FRNs have little interest-rate risk (coupons reset), but they still carry **credit** risk through "
                    "changes in the required margin."
                ),
            ),
            topic(
                "Money market yields",
                FX("Discount basis: PV = FV × (1 − days/year × DR) · Add-on basis: PV = FV ÷ (1 + days/year × AOR)"),
                EX(
                    "A 180-day T-bill with face ₹100 quoted at a 4% discount rate (360-day year): PV = 100 × (1 − "
                    "180/360 × "
                    "0.04) = **₹98.00**. Its add-on yield = (100/98 − 1) × 360/180 = **4.08%**."
                ),
                P(
                    "A **bond equivalent yield** is a money market rate restated on a 365-day add-on basis so it can "
                    "be "
                    "compared with bond yields."
                ),
                FUN(
                    "A discount-rate quote is the shopkeeper's 'only 4% off!' sticker. The actual return you earn on "
                    "your ₹98 is a bit more."
                ),
            ),
        ],
        revision=sheet(
            "Discount: PV = FV(1 − t/360 × DR) · Add-on: PV = FV/(1 + t/360 × AOR)",
            ("Quoted margin", "Contract spread over MRR"),
            ("Discount margin", "Spread market requires"),
            ("DM > QM", "FRN below par"),
            ("DM < QM", "FRN above par"),
            ("Discount rate", "Understates true yield"),
            ("Bond equivalent yield", "365-day add-on basis"),
        ),
        questions=[
            q(
                "M",
                "An FRN pays MRR + 1.0%. Investors now require MRR + 1.5%. The FRN trades:",
                ["At par", "At a discount", "At a premium"],
                1,
                "Required margin exceeds the quoted margin.",
                "8.a",
            ),
            q(
                "E",
                "On a reset date, an FRN whose discount margin equals its quoted margin trades:",
                ["At par", "Below par", "Above par"],
                0,
                "Coupons equal the required return.",
                "8.a",
            ),
            q(
                "M",
                "A 180-day ₹100 T-bill is quoted at a 4% discount rate (360-day year). Its price is:",
                ["₹96.00", "₹98.00", "₹99.00"],
                1,
                "100 × (1 − 0.5 × 0.04) = 98.",
                "8.b",
            ),
            q(
                "H",
                "The add-on yield on that T-bill (360-day basis) is closest to:",
                ["4.00%", "4.08%", "3.92%"],
                1,
                "(100/98 − 1) × 2 = 4.08%.",
                "8.b",
            ),
            q(
                "M",
                "Compared with fixed-rate bonds, FRNs have:",
                ["More interest rate risk", "Less interest rate risk", "No credit risk"],
                1,
                "Coupons reset to market rates.",
                "8.a",
            ),
            q(
                "E",
                "A money market rate quoted on a discount basis:",
                ["Overstates the investor's return", "Understates the investor's return", "Equals the add-on yield"],
                1,
                "It is based on face value, not the price paid.",
                "8.b",
            ),
            q(
                "M",
                "The bond equivalent yield restates money market yields on a:",
                ["360-day discount basis", "365-day add-on basis", "Monthly basis"],
                1,
                "To compare with bond yields.",
                "8.b",
            ),
            q(
                "H",
                "If an issuer's credit improves so the required margin falls below the quoted margin, its FRN:",
                ["Falls below par", "Rises above par", "Stays at par"],
                1,
                "Coupons now exceed the required return.",
                "8.a",
            ),
            q(
                "E",
                "The quoted margin on an FRN is:",
                [
                    "The spread over MRR set in the contract",
                    "The market's current required spread",
                    "The coupon frequency",
                ],
                0,
                "Fixed at issue.",
                "8.a",
            ),
            q(
                "M",
                "A certificate of deposit paying interest on top of the principal at maturity is quoted on:",
                ["A discount basis", "An add-on basis", "A yield-to-call basis"],
                1,
                "Interest is added on.",
                "8.b",
            ),
        ],
        flashcards=[
            fc("Quoted vs discount margin", "Contract spread vs required spread."),
            fc("DM > QM", "FRN priced below par."),
            fc("Discount-basis price", "FV × (1 − days/360 × DR)."),
            fc("Add-on basis", "PV = FV ÷ (1 + days/year × rate)."),
            fc("Bond equivalent yield", "365-day add-on rate."),
            fc("FRN main risk", "Credit (margin) risk, not rate risk."),
        ],
    )
)

# ---------------------------------------------------------------- LM9
LMS.append(
    dict(
        lm_no=9,
        title="The Term Structure of Interest Rates: Spot, Par, and Forward Curves",
        summary="Spot, par and forward rates, the shapes of the yield curve and theories that explain them.",
        los=[
            ("9.a", "define", "Define spot rates, par rates and forward rates and the relationships among them."),
            ("9.b", "calculate", "Calculate forward rates from spot rates and par rates from spot rates."),
            ("9.c", "explain", "Explain theories of the term structure of interest rates."),
        ],
        topics=[
            topic(
                "Spot, par and forward rates",
                L(
                    "**Spot rate**: yield on a zero-coupon bond for a maturity.",
                    "**Par rate**: coupon that makes a bond priced at par using the spot rates.",
                    "**Forward rate**: rate for a loan starting in the future, implied by spot rates.",
                ),
                FX("(1 + z₂)² = (1 + z₁)(1 + f₁,₁) · Par rate p for 2 years: p/(1 + z₁) + (1 + p)/(1 + z₂)² = 1"),
                EX(
                    "z₁ = 3%, z₂ = 4%. f₁,₁ = 1.04² ÷ 1.03 − 1 = **5.01%**. Par rate: p × (0.9709 + 0.9246) + 0.9246 = "
                    "1, so "
                    "p = 0.0754 ÷ 1.8955 = **3.98%**."
                ),
                WO("Upward-sloping spot curve: forward > spot > par. Downward-sloping: the reverse."),
            ),
            topic(
                "Shapes and theories",
                L(
                    "Shapes: **upward** (normal), **flat**, **inverted** (often before recessions), humped.",
                    "**Unbiased expectations theory**: forward rates are unbiased forecasts of future spot rates.",
                    "**Local expectations**: all bonds earn the risk-free rate over short horizons.",
                    "**Liquidity preference**: investors demand a premium for longer maturities, so the curve slopes "
                    "up even with flat expectations.",
                    "**Segmented markets**: separate supply and demand at each maturity.",
                    "**Preferred habitat**: investors prefer certain maturities but will move for enough extra yield.",
                ),
                FUN(
                    "An inverted yield curve is the bond market's version of the dog refusing to go out before a "
                    "storm. Not always right, but people pay attention."
                ),
            ),
        ],
        revision=sheet(
            "(1 + z_B)^B = (1 + z_A)^A (1 + f_A,B−A)^(B−A)",
            ("Spot rate", "Zero-coupon yield"),
            ("Par rate", "Coupon that prices bond at par"),
            ("Forward rate", "Future-period rate implied today"),
            ("Upward curve", "Forward > spot > par"),
            ("Liquidity preference", "Term premium makes curve slope up"),
            ("Preferred habitat", "Will move maturity for extra yield"),
        ),
        questions=[
            q(
                "M",
                "One-year spot 3%, two-year spot 4%. The one-year forward rate one year from now is closest to:",
                ["5.01%", "4.00%", "3.50%"],
                0,
                "1.04²/1.03 − 1 = 5.01%.",
                "9.b",
            ),
            q(
                "E",
                "A spot rate is the yield on a:",
                ["Coupon bond at par", "Zero-coupon bond", "Floating-rate note"],
                1,
                "Spot rates are zero-coupon yields.",
                "9.a",
            ),
            q(
                "H",
                "With z₁ = 3% and z₂ = 4%, the two-year par rate is closest to:",
                ["3.98%", "4.00%", "5.01%"],
                0,
                "p = (1 − 0.9246)/(0.9709 + 0.9246) = 3.98%.",
                "9.b",
            ),
            q(
                "M",
                "When the spot curve slopes upward, forward rates are:",
                ["Below spot rates", "Above spot rates", "Equal to spot rates"],
                1,
                "Forward > spot > par.",
                "9.a",
            ),
            q(
                "M",
                "The theory that forward rates are unbiased predictors of future spot rates is the:",
                ["Liquidity preference theory", "Unbiased expectations theory", "Segmented markets theory"],
                1,
                "That is its definition.",
                "9.c",
            ),
            q(
                "H",
                "Under the liquidity preference theory, an upward-sloping yield curve:",
                [
                    "Must mean rates will rise",
                    "May reflect a term premium even if rates are expected to stay flat",
                    "Is impossible",
                ],
                1,
                "The premium alone can create upward slope.",
                "9.c",
            ),
            q(
                "E",
                "An inverted yield curve means:",
                ["Long rates are above short rates", "Short rates are above long rates", "All rates are zero"],
                1,
                "It slopes downward.",
                "9.a",
            ),
            q(
                "M",
                "The preferred habitat theory says investors:",
                [
                    "Never leave their preferred maturity",
                    "Will move to other maturities if paid enough extra yield",
                    "Only buy short-term bonds",
                ],
                1,
                "It blends segmentation with yield incentives.",
                "9.c",
            ),
            q(
                "M",
                "The coupon rate that prices a bond at par given the spot curve is the:",
                ["Par rate", "Forward rate", "Discount margin"],
                0,
                "Par rates are derived from spot rates.",
                "9.a",
            ),
            q(
                "E",
                "Under the segmented markets theory, each maturity's yield is set by:",
                ["Supply and demand within that maturity segment", "Forward rates only", "Central bank only"],
                0,
                "Segments are independent.",
                "9.c",
            ),
        ],
        flashcards=[
            fc("Spot rate", "Zero-coupon yield for a maturity."),
            fc("Par rate", "Coupon pricing a bond at par from spot rates."),
            fc("Forward from spots", "(1 + z₂)² = (1 + z₁)(1 + f₁,₁)."),
            fc("Upward curve ordering", "Forward > spot > par."),
            fc("Unbiased expectations", "Forwards forecast future spot rates."),
            fc("Liquidity preference", "Term premium for longer maturities."),
        ],
    )
)

# ---------------------------------------------------------------- LM10
LMS.append(
    dict(
        lm_no=10,
        title="Interest Rate Risk and Return",
        summary="Sources of bond return, reinvestment versus price risk, and the investment horizon.",
        los=[
            ("10.a", "calculate", "Calculate and interpret the sources of return from investing in a fixed-rate bond."),
            (
                "10.b",
                "describe",
                "Describe the relationships among a bond's holding period return, its Macaulay "
                "duration and the investment horizon.",
            ),
        ],
        topics=[
            topic(
                "Sources of return",
                OL(
                    "**Coupon** and principal payments.",
                    "**Reinvestment income** on coupons.",
                    "**Capital gain or loss** if sold before maturity.",
                ),
                EX(
                    "Buy a 3-year 6% annual coupon bond at par (₹100). Rates fall to 5% right after purchase and stay "
                    "there. Held to maturity, coupons are reinvested at 5%: total = 6 × 1.05² + 6 × 1.05 + 106 = 6.615 "
                    "+ "
                    "6.3 + 106 = ₹118.92, a horizon yield of (118.92/100)^(1/3) − 1 = **5.94%**, below the 6% YTM "
                    "because of "
                    "lower reinvestment income."
                ),
                WO(
                    "The YTM is realised only if the bond is held to maturity, there is no default, and coupons are "
                    "reinvested at the YTM."
                ),
            ),
            topic(
                "Two opposing risks and duration",
                L(
                    "When rates **rise**: reinvestment income **rises**, but the sale price **falls** (market price "
                    "risk).",
                    "When rates **fall**: the reverse.",
                    "**Short horizon** → price risk dominates. **Long horizon** → reinvestment risk dominates.",
                    "If the **investment horizon = Macaulay duration**, the two effects roughly **offset**.",
                    "**Duration gap** = Macaulay duration − investment horizon. Positive gap → exposed to rising "
                    "rates.",
                ),
                FUN(
                    "Rates rising is like rain for a farmer who also sells umbrellas: the crop suffers, the umbrella "
                    "shop booms. Macaulay duration tells you when the two cancel out."
                ),
            ),
        ],
        revision=sheet(
            "Duration gap = Macaulay duration − investment horizon",
            ("Return sources", "Coupons, reinvestment, capital gain/loss"),
            ("Rates up", "Reinvestment ↑, price ↓"),
            ("Short horizon", "Price risk dominates"),
            ("Long horizon", "Reinvestment risk dominates"),
            ("Horizon = MacDur", "Risks roughly offset"),
            ("Positive gap", "Hurt by rising rates"),
        ),
        questions=[
            q(
                "E",
                "Which is a source of return on a fixed-rate bond?",
                ["Dividends", "Reinvestment of coupons", "Stock splits"],
                1,
                "Coupons, reinvestment and capital gains.",
                "10.a",
            ),
            q(
                "M",
                "An investor with a short horizon is mainly exposed to:",
                ["Reinvestment risk", "Market price risk", "No risk"],
                1,
                "The bond must be sold soon.",
                "10.b",
            ),
            q(
                "M",
                "When the investment horizon equals the Macaulay duration, an immediate one-time change in rates:",
                [
                    "Has roughly offsetting effects on price and reinvestment income",
                    "Doubles the return",
                    "Only affects coupons",
                ],
                0,
                "That is the immunisation idea.",
                "10.b",
            ),
            q(
                "H",
                "A 3-year 6% bond is bought at par; rates fall to 5% at once and stay there. Held to maturity, the "
                "horizon yield is closest to:",
                ["6.00%", "5.94%", "5.00%"],
                1,
                "Future value 118.92 → 5.94% a year.",
                "10.a",
            ),
            q(
                "M",
                "A bond portfolio has a Macaulay duration of 7 years and the investor's horizon is 4 years. The "
                "duration "
                "gap is:",
                ["+3 years", "−3 years", "11 years"],
                0,
                "7 − 4 = 3.",
                "10.b",
            ),
            q(
                "H",
                "With a positive duration gap, the investor is mainly hurt by:",
                ["Falling rates", "Rising rates", "Lower coupons only"],
                1,
                "Price risk outweighs reinvestment gains.",
                "10.b",
            ),
            q(
                "E",
                "If rates rise after purchase, reinvestment income on coupons will:",
                ["Fall", "Rise", "Not change"],
                1,
                "Coupons are reinvested at higher rates.",
                "10.b",
            ),
            q(
                "M",
                "A bond held to maturity with no default earns exactly its YTM only if:",
                ["Coupons are reinvested at the YTM", "Rates rise", "It is callable"],
                0,
                "Reinvestment assumption.",
                "10.a",
            ),
            q(
                "M",
                "A long-horizon investor is mainly exposed to:",
                ["Reinvestment risk", "Price risk", "Liquidity risk only"],
                0,
                "Many coupons will be reinvested.",
                "10.b",
            ),
            q(
                "E",
                "Selling a bond for more than its carrying value at the time produces a:",
                ["Capital gain", "Capital loss", "Coupon"],
                0,
                "Price exceeded the amortised value.",
                "10.a",
            ),
        ],
        flashcards=[
            fc("Bond return sources", "Coupons, reinvestment income, capital gain/loss."),
            fc("Rates rise effect", "Reinvestment income up, price down."),
            fc("Short vs long horizon risk", "Price risk vs reinvestment risk."),
            fc("Horizon = Macaulay duration", "Price and reinvestment effects roughly offset."),
            fc("Duration gap", "Macaulay duration − horizon."),
            fc("Positive duration gap", "Vulnerable to rising rates."),
        ],
    )
)

# ---------------------------------------------------------------- LM11
LMS.append(
    dict(
        lm_no=11,
        title="Yield-Based Bond Duration Measures and Properties",
        summary="Macaulay, modified and approximate duration, money duration, PVBP and the properties of duration.",
        los=[
            ("11.a", "define", "Define, calculate and interpret Macaulay, modified and effective durations."),
            (
                "11.b",
                "calculate",
                "Calculate the percentage price change for a given change in yield, money duration "
                "and the price value of a basis point.",
            ),
            ("11.c", "explain", "Explain how coupon, maturity and yield affect duration."),
        ],
        topics=[
            topic(
                "Duration measures",
                L(
                    "**Macaulay duration**: weighted average time to receive cash flows (weights = PV share).",
                    "**Modified duration** = Macaulay ÷ (1 + yield per period): % price change for a 1% yield change.",
                    "**Approximate modified duration** = (PV₋ − PV₊) ÷ (2 × Δy × PV₀).",
                    "**Money duration** = modified duration × full price.",
                    "**PVBP** (price value of a basis point) = price change for a 1 bp change in yield.",
                ),
                FX("%ΔP ≈ −ModDur × Δy · ModDur = MacDur ÷ (1 + r)"),
                EX(
                    "Macaulay duration 5.2 years, annual yield 4%. ModDur = 5.2/1.04 = **5.0**. If yields rise 50 bp, "
                    "price falls ≈ 5.0 × 0.5% = **2.5%**. On a ₹10 crore holding, money duration = ₹50 crore and PVBP "
                    "≈ "
                    "₹50,000."
                ),
            ),
            topic(
                "Properties",
                L(
                    "**Longer maturity** → higher duration (usually).",
                    "**Higher coupon** → lower duration (more cash early).",
                    "**Higher yield** → lower duration.",
                    "**Zero-coupon** bond: Macaulay duration = maturity.",
                    "**Perpetuity**: Macaulay duration = (1 + r)/r.",
                    "Portfolio duration ≈ weighted average of the holdings' durations.",
                ),
                EX("A perpetual bond at 5%: Macaulay duration = 1.05/0.05 = **21 years**."),
                WO(
                    "Duration is a linear approximation. For big yield changes it underestimates price rises and "
                    "overestimates price falls: add convexity."
                ),
                FUN(
                    "Macaulay duration is the bond's centre of gravity. A zero-coupon bond keeps all its weight at the "
                    "end, like someone saving every rupee for one big holiday."
                ),
            ),
        ],
        revision=sheet(
            "%ΔP ≈ −ModDur × Δy · ModDur = MacDur/(1 + r) · ApproxModDur = (PV₋ − PV₊)/(2ΔyPV₀)",
            ("Zero-coupon", "MacDur = maturity"),
            ("Perpetuity", "MacDur = (1 + r)/r"),
            ("Higher coupon", "Lower duration"),
            ("Higher yield", "Lower duration"),
            ("Money duration", "ModDur × full price"),
            ("PVBP", "Price change per 1 bp"),
        ),
        questions=[
            q(
                "E",
                "For a given yield change, which bond has the largest price change?",
                ["2-year 8% coupon", "10-year zero-coupon", "5-year 6% coupon"],
                1,
                "Long maturity and no coupons give the highest duration.",
                "11.c",
            ),
            q(
                "M",
                "Macaulay duration 5.2 and annual yield 4% give a modified duration of:",
                ["5.20", "5.00", "5.41"],
                1,
                "5.2/1.04 = 5.0.",
                "11.a",
            ),
            q(
                "M",
                "A bond with modified duration 5.0 sees yields rise 50 bp. Its price changes by about:",
                ["−2.5%", "−5.0%", "+2.5%"],
                0,
                "−5 × 0.5% = −2.5%.",
                "11.b",
            ),
            q(
                "E",
                "The Macaulay duration of a 7-year zero-coupon bond is:",
                ["Less than 7", "Exactly 7", "More than 7"],
                1,
                "All cash comes at maturity.",
                "11.c",
            ),
            q(
                "M",
                "Other things equal, a higher coupon rate gives:",
                ["Higher duration", "Lower duration", "No change"],
                1,
                "More cash is received earlier.",
                "11.c",
            ),
            q(
                "H",
                "A bond's price is 100; it would be 102.10 if yields fell 50 bp and 97.95 if they rose 50 bp. "
                "Approximate modified duration is:",
                ["4.15", "8.30", "2.08"],
                0,
                "(102.10 − 97.95)/(2 × 0.005 × 100) = 4.15.",
                "11.a",
            ),
            q(
                "M",
                "The Macaulay duration of a perpetual bond yielding 5% is:",
                ["20 years", "21 years", "Infinite"],
                1,
                "(1.05)/0.05 = 21.",
                "11.c",
            ),
            q(
                "H",
                "A ₹10 crore position has modified duration 5.0. Its PVBP is closest to:",
                ["₹5,000", "₹50,000", "₹5 lakh"],
                1,
                "ModDur × value × 0.0001 = 5 × ₹10 crore × 0.0001 = ₹50,000.",
                "11.b",
            ),
            q(
                "E",
                "Higher market yields, other things equal, make duration:",
                ["Higher", "Lower", "Unchanged"],
                1,
                "Distant cash flows are discounted more heavily.",
                "11.c",
            ),
            q(
                "M",
                "Money duration is:",
                ["Modified duration × full price", "Macaulay duration × coupon", "Price ÷ duration"],
                0,
                "It gives the currency change for a 1% yield change.",
                "11.b",
            ),
        ],
        flashcards=[
            fc("Macaulay duration", "PV-weighted average time to cash flows."),
            fc("Modified duration", "MacDur ÷ (1 + r); % price change per 1% yield."),
            fc("Approximate ModDur", "(PV₋ − PV₊)/(2 × Δy × PV₀)."),
            fc("Duration properties", "Up with maturity; down with coupon and yield."),
            fc("Perpetuity duration", "(1 + r)/r."),
            fc("PVBP", "Price change for a 1 bp yield move."),
        ],
    )
)

# ---------------------------------------------------------------- LM12
LMS.append(
    dict(
        lm_no=12,
        title="Yield-Based Bond Convexity and Portfolio Properties",
        summary="Convexity, combining duration and convexity, and duration and convexity of portfolios.",
        los=[
            (
                "12.a",
                "calculate",
                "Calculate and interpret approximate convexity and the price change using duration and convexity.",
            ),
            ("12.b", "describe", "Describe the duration and convexity of a bond portfolio and their limitations."),
        ],
        topics=[
            topic(
                "Convexity",
                FX("%ΔP ≈ −ModDur × Δy + ½ × Convexity × (Δy)² · ApproxCon = (PV₋ + PV₊ − 2PV₀) ÷ ((Δy)² × PV₀)"),
                EX(
                    "ModDur 5, convexity 40, yields rise 100 bp: %ΔP ≈ −5 × 0.01 + 0.5 × 40 × 0.0001 = −5% + 0.2% = "
                    "**−4.8%**. If yields fall 100 bp: +5% + 0.2% = **+5.2%**."
                ),
                L(
                    "Positive convexity helps the holder either way: gains are bigger and losses smaller than duration "
                    "alone predicts.",
                    "Convexity rises with maturity, lower coupons and lower yields; and with a more **dispersed** "
                    "cash flow pattern (a barbell has more convexity than a bullet of the same duration).",
                ),
            ),
            topic(
                "Portfolios",
                L(
                    "Portfolio duration and convexity ≈ **market-value-weighted** averages of the holdings'.",
                    "This assumes a **parallel** shift in the yield curve, which rarely happens exactly.",
                    "Alternatively, use the portfolio's cash flow yield, which is harder to compute and interpret.",
                ),
                EX(
                    "₹60 crore in a bond with ModDur 4 and ₹40 crore in one with ModDur 9. Portfolio ModDur = 0.6 × 4 "
                    "+ 0.4 × 9 "
                    "= **6.0**."
                ),
                WO("Weighted-average duration ignores non-parallel moves. Use key rate durations for twists."),
                FUN(
                    "Convexity is the airbag in a bond: you hardly notice it on a small bump, but on a big crash you "
                    "are very glad it's there."
                ),
            ),
        ],
        revision=sheet(
            "%ΔP ≈ −ModDur Δy + ½ Con (Δy)²",
            ("Positive convexity", "Bigger gains, smaller losses"),
            ("More convex", "Longer, lower coupon, lower yield, dispersed cash flows"),
            ("Barbell vs bullet", "Barbell more convex"),
            ("Portfolio duration", "Value-weighted average"),
            ("Limitation", "Assumes parallel shifts"),
        ),
        questions=[
            q(
                "M",
                "ModDur 5, convexity 40, and yields rise 100 bp. The estimated price change is:",
                ["−5.0%", "−4.8%", "−5.2%"],
                1,
                "−5% + 0.5 × 40 × 0.0001 = −4.8%.",
                "12.a",
            ),
            q(
                "M",
                "With the same bond, if yields fall 100 bp, the estimated price change is:",
                ["+5.2%", "+4.8%", "+5.0%"],
                0,
                "+5% + 0.2% = +5.2%.",
                "12.a",
            ),
            q(
                "E",
                "Positive convexity means that for equal yield moves:",
                ["Price gains exceed price losses", "Price losses exceed gains", "Prices do not change"],
                0,
                "The price–yield curve bends upward.",
                "12.a",
            ),
            q(
                "M",
                "A portfolio holds ₹60 crore of a bond with ModDur 4 and ₹40 crore with ModDur 9. Its duration is:",
                ["6.5", "6.0", "5.0"],
                1,
                "0.6 × 4 + 0.4 × 9 = 6.0.",
                "12.b",
            ),
            q(
                "H",
                "Compared with a bullet portfolio of the same duration, a barbell portfolio has:",
                ["Lower convexity", "Higher convexity", "Identical convexity"],
                1,
                "Cash flows are more dispersed.",
                "12.a",
            ),
            q(
                "M",
                "Using a weighted average of holdings' durations for a portfolio assumes:",
                ["A parallel shift in the yield curve", "No coupons", "Equal maturities"],
                0,
                "It ignores curve twists.",
                "12.b",
            ),
            q(
                "H",
                "Prices are 100 (current), 102.12 (yield −50 bp) and 97.92 (yield +50 bp). Approximate convexity is:",
                ["16", "160", "1.6"],
                0,
                "(102.12 + 97.92 − 200)/(0.005² × 100) = 0.04/0.0025 = 16.",
                "12.a",
            ),
            q(
                "E",
                "Duration alone tends to:",
                ["Overestimate price rises", "Underestimate price rises and overestimate price falls", "Be exact"],
                1,
                "For positively convex bonds.",
                "12.a",
            ),
            q(
                "M",
                "Which bond generally has the most convexity?",
                ["Short, high-coupon", "Long, low-coupon", "Floating-rate"],
                1,
                "Longer, lower-coupon bonds are more convex.",
                "12.a",
            ),
            q(
                "E",
                "Convexity measures:",
                ["The curvature of the price–yield relationship", "Credit risk", "Liquidity"],
                0,
                "A second-order effect.",
                "12.a",
            ),
        ],
        flashcards=[
            fc("Price change with convexity", "−ModDur Δy + ½ Con (Δy)²."),
            fc("Approximate convexity", "(PV₋ + PV₊ − 2PV₀)/((Δy)² PV₀)."),
            fc("Positive convexity benefit", "Gains larger, losses smaller."),
            fc("Barbell vs bullet", "Barbell is more convex."),
            fc("Portfolio duration", "Market-value-weighted average."),
            fc("Weighted duration limitation", "Assumes parallel shifts."),
        ],
    )
)

# ---------------------------------------------------------------- LM13
LMS.append(
    dict(
        lm_no=13,
        title="Curve-Based and Empirical Fixed-Income Risk Measures",
        summary="Effective duration and convexity for bonds with options, key rate durations and empirical duration.",
        los=[
            (
                "13.a",
                "explain",
                "Explain why effective duration and effective convexity are the right measures for "
                "bonds with embedded options.",
            ),
            ("13.b", "calculate", "Calculate and interpret effective duration and effective convexity."),
            ("13.c", "define", "Define key rate duration and describe its use."),
            ("13.d", "explain", "Explain how empirical duration differs from analytical duration."),
        ],
        topics=[
            topic(
                "Effective duration and convexity",
                P(
                    "For bonds whose cash flows change with rates (callable, putable, MBS), yield-based duration is "
                    "wrong. **Effective duration** shifts the **benchmark curve** and reprices with a model."
                ),
                FX("EffDur = (PV₋ − PV₊) ÷ (2 × ΔCurve × PV₀) · EffCon = (PV₋ + PV₊ − 2PV₀) ÷ ((ΔCurve)² × PV₀)"),
                EX(
                    "A callable bond priced at 101.0 would be 102.0 if the curve fell 25 bp and 99.8 if it rose 25 bp. "
                    "EffDur = (102.0 − 99.8)/(2 × 0.0025 × 101) = **4.36**. EffCon = (102.0 + 99.8 − 202)/(0.0025² × "
                    "101) "
                    "= **−317**: negative convexity."
                ),
                WO(
                    "Callable bonds show **negative convexity** at low yields: as rates fall, the price is capped near "
                    "the call price. Putable bonds have more positive convexity."
                ),
            ),
            topic(
                "Key rate and empirical duration",
                L(
                    "**Key rate (partial) duration**: sensitivity to a change in one maturity point of the curve. The "
                    "sum of key rate durations ≈ effective duration. Captures **shaping risk** (twists).",
                    "**Empirical duration**: estimated from historical price changes against rate changes.",
                    "For **high-yield** bonds, credit spreads often narrow when government rates rise (better "
                    "economy), "
                    "so empirical duration is **lower** than analytical duration.",
                ),
                FUN(
                    "Key rate duration is checking each tyre's pressure separately rather than just asking whether the "
                    "car feels bumpy."
                ),
            ),
        ],
        revision=sheet(
            "EffDur = (PV₋ − PV₊)/(2 ΔCurve PV₀) · EffCon = (PV₋ + PV₊ − 2PV₀)/((ΔCurve)² PV₀)",
            ("When to use effective", "Bonds with embedded options, MBS"),
            ("Callable bond", "Negative convexity at low yields"),
            ("Putable bond", "Extra positive convexity"),
            ("Key rate duration", "Sensitivity to one curve point"),
            ("Sum of key rates", "≈ effective duration"),
            ("Empirical duration (HY)", "Lower than analytical"),
        ),
        questions=[
            q(
                "E",
                "The appropriate duration measure for a callable bond is:",
                ["Macaulay duration", "Modified duration", "Effective duration"],
                2,
                "Its cash flows change with rates.",
                "13.a",
            ),
            q(
                "H",
                "A callable bond is priced at 101.0; it would be 102.0 if the curve fell 25 bp and 99.8 if it rose "
                "25 bp. Effective duration is closest to:",
                ["4.36", "8.71", "2.18"],
                0,
                "(102.0 − 99.8)/(2 × 0.0025 × 101) = 4.36.",
                "13.b",
            ),
            q(
                "M",
                "At low yields, a callable bond typically exhibits:",
                ["Positive convexity", "Negative convexity", "Zero duration"],
                1,
                "Price upside is capped near the call price.",
                "13.a",
            ),
            q(
                "M",
                "Key rate duration measures sensitivity to:",
                ["A parallel shift in the curve", "A change in one specific maturity point", "Credit spreads only"],
                1,
                "It isolates shaping risk.",
                "13.c",
            ),
            q(
                "M",
                "The sum of a bond's key rate durations is approximately equal to its:",
                ["Effective duration", "Convexity", "Yield to maturity"],
                0,
                "Partial durations add up.",
                "13.c",
            ),
            q(
                "H",
                "For high-yield bonds, empirical duration is often lower than analytical duration because:",
                ["Coupons are low", "Credit spreads tend to narrow when benchmark rates rise", "They have no maturity"],
                1,
                "Spread changes partly offset rate changes.",
                "13.d",
            ),
            q(
                "E",
                "Empirical duration is estimated using:",
                ["Historical price and rate data", "Only the coupon rate", "The bond's par value"],
                0,
                "Statistical regression.",
                "13.d",
            ),
            q(
                "M",
                "Effective duration is computed by shifting:",
                ["The bond's own yield", "The benchmark yield curve", "The coupon rate"],
                1,
                "Curve-based, not yield-based.",
                "13.b",
            ),
            q(
                "M",
                "Compared with an otherwise identical straight bond, a putable bond has:",
                ["Less positive convexity", "More positive convexity", "Negative convexity"],
                1,
                "The put sets a price floor.",
                "13.a",
            ),
            q(
                "E",
                "Shaping risk refers to the risk from:",
                ["Non-parallel changes in the yield curve", "Default", "Currency moves"],
                0,
                "Twists and humps.",
                "13.c",
            ),
        ],
        flashcards=[
            fc("Effective duration", "Curve-based, model-priced duration for bonds with options."),
            fc("Callable bond convexity", "Negative at low yields."),
            fc("Putable bond convexity", "More positive than a straight bond."),
            fc("Key rate duration", "Sensitivity to one curve point; sum ≈ effective duration."),
            fc("Empirical duration", "Estimated from historical data."),
            fc("High-yield empirical duration", "Lower than analytical; spreads offset rate moves."),
        ],
    )
)

# ---------------------------------------------------------------- LM14
LMS.append(
    dict(
        lm_no=14,
        title="Credit Risk",
        summary="Default probability, loss given default, expected loss, the four Cs, ratings and credit spreads.",
        los=[
            (
                "14.a",
                "describe",
                "Describe credit risk and its components: probability of default and loss given default.",
            ),
            ("14.b", "describe", "Describe the uses of ratings and the risks of relying on them."),
            ("14.c", "describe", "Describe qualitative and quantitative factors used in credit analysis."),
            ("14.d", "calculate", "Calculate and interpret the effect of credit spread changes on bond prices."),
        ],
        topics=[
            topic(
                "Components of credit risk",
                FX("Expected loss = Probability of default × Loss given default · LGD = 1 − recovery rate"),
                EX("PD 2% a year, recovery 40% → LGD 60%. Expected loss = 0.02 × 0.60 = **1.2%** a year."),
                L(
                    "Seniority ranking (highest recovery first): first lien / senior secured → second lien → senior "
                    "unsecured → subordinated.",
                    "**Pari passu**: claims of the same rank share equally.",
                    "Other credit-related risks: **spread risk** (downgrade or wider spreads), **liquidity risk**.",
                ),
                WO(
                    "The **absolute priority** rule is not always followed in bankruptcy; junior creditors sometimes "
                    "get "
                    "something in negotiated settlements."
                ),
            ),
            topic(
                "Ratings and analysis",
                L(
                    "**Ratings**: AAA to D; investment grade is BBB− (Baa3) and above. **Notching**: lower ratings for "
                    "subordinated issues of the same issuer.",
                    "Risks of ratings: they change, lag market prices, and can be wrong.",
                    "**Four Cs**: **capacity** (cash flow), **collateral**, **covenants**, **character** (management).",
                    "Credit spread = yield on risky bond − benchmark yield ≈ expected loss + compensation for "
                    "uncertainty and illiquidity.",
                ),
                FX("%ΔP ≈ −ModDur × Δspread + ½ × Convexity × (Δspread)²"),
                EX(
                    "A bond with ModDur 6 and convexity 50 sees its spread widen 50 bp. %ΔP ≈ −6 × 0.005 + 0.5 × 50 × "
                    "0.000025 = −3.0% + 0.06% = **−2.94%**."
                ),
                FUN(
                    "A credit rating is like a cricket selector's opinion: very useful, sometimes late, and the "
                    "market often knows the player is out of form before the selectors do."
                ),
            ),
        ],
        revision=sheet(
            "EL = PD × LGD · %ΔP ≈ −ModDur × Δspread + ½ Con (Δspread)²",
            ("LGD", "1 − recovery rate"),
            ("Seniority", "Secured > senior unsecured > subordinated"),
            ("Notching", "Lower ratings for junior issues"),
            ("Four Cs", "Capacity, collateral, covenants, character"),
            ("Investment grade", "BBB− and above"),
            ("Rating risks", "Lag, change, can be wrong"),
        ),
        questions=[
            q(
                "M",
                "A bond has a 2% default probability and an expected 40% recovery. Its expected loss is:",
                ["0.8%", "1.2%", "2.0%"],
                1,
                "0.02 × 0.60 = 1.2%.",
                "14.a",
            ),
            q(
                "E",
                "Loss given default equals:",
                ["1 − recovery rate", "Probability of default", "The coupon rate"],
                0,
                "It is the share not recovered.",
                "14.a",
            ),
            q(
                "M",
                "Which ranks highest in priority of claims?",
                ["Subordinated debt", "Senior unsecured debt", "First-lien senior secured debt"],
                2,
                "Secured by specific assets.",
                "14.a",
            ),
            q(
                "M",
                "Notching refers to:",
                [
                    "Rating junior issues of an issuer lower than its senior debt",
                    "Rounding yields",
                    "A coupon schedule",
                ],
                0,
                "Lower recovery means a lower issue rating.",
                "14.b",
            ),
            q(
                "H",
                "A bond with ModDur 6 and convexity 50 sees its spread widen 50 bp. Its price changes by about:",
                ["−3.00%", "−2.94%", "−3.06%"],
                1,
                "−3% + 0.06% = −2.94%.",
                "14.d",
            ),
            q(
                "E",
                "Which is one of the four Cs of credit analysis?",
                ["Capacity", "Currency", "Convexity"],
                0,
                "Capacity, collateral, covenants, character.",
                "14.c",
            ),
            q(
                "M",
                "A risk of relying on credit ratings is that they:",
                ["Never change", "Can lag market prices", "Are always conservative"],
                1,
                "Markets often move first.",
                "14.b",
            ),
            q(
                "M",
                "Claims of equal rank that share equally in recoveries are:",
                ["Subordinated", "Pari passu", "Secured"],
                1,
                "Pari passu = on equal footing.",
                "14.a",
            ),
            q(
                "H",
                "The credit spread on a corporate bond compensates investors for:",
                ["Only expected loss", "Expected loss plus uncertainty and illiquidity", "Inflation only"],
                1,
                "Spreads also include risk and liquidity premiums.",
                "14.d",
            ),
            q(
                "E",
                "The lowest investment-grade rating on the S&P scale is:",
                ["BB+", "BBB−", "A−"],
                1,
                "BBB− is the cut-off.",
                "14.b",
            ),
        ],
        flashcards=[
            fc("Expected loss", "PD × LGD."),
            fc("LGD", "1 − recovery rate."),
            fc("Priority of claims", "Secured → senior unsecured → subordinated."),
            fc("Four Cs", "Capacity, collateral, covenants, character."),
            fc("Notching", "Junior issues rated below senior debt."),
            fc("Spread price effect", "−ModDur × Δspread + ½ Con (Δspread)²."),
        ],
    )
)

# ---------------------------------------------------------------- LM15
LMS.append(
    dict(
        lm_no=15,
        title="Credit Analysis for Government Issuers",
        summary="Assessing sovereign and non-sovereign credit: institutional, economic, fiscal, monetary and "
        "external factors.",
        los=[
            (
                "15.a",
                "explain",
                "Explain special considerations when evaluating the credit of sovereign and "
                "non-sovereign government issuers.",
            ),
            (
                "15.b",
                "describe",
                "Describe the qualitative and quantitative factors used in sovereign credit analysis.",
            ),
        ],
        topics=[
            topic(
                "Sovereign credit factors",
                T(
                    ["Factor", "What analysts look at"],
                    ["Institutional", "Rule of law, political stability, corruption, willingness to pay"],
                    ["Economic", "GDP per capita, growth, diversification"],
                    ["Fiscal", "Debt-to-GDP, deficits, interest burden"],
                    ["Monetary", "Central bank independence, inflation track record, exchange rate regime"],
                    ["External", "Reserve currency status, current account, FX reserves, external debt"],
                ),
                WO(
                    "Sovereigns can be **able but unwilling** to pay. Willingness matters as much as ability, and "
                    "bondholders have limited legal recourse."
                ),
                EX(
                    "Country A: debt/GDP 55%, deficit 3%, FX reserves cover 12 months of imports, independent central "
                    "bank. "
                    "Country B: debt/GDP 90%, deficit 8%, reserves cover 2 months, history of default. Country A "
                    "deserves the higher rating."
                ),
            ),
            topic(
                "Non-sovereign government credit",
                L(
                    "**GO bonds**: rely on the taxing power and economy of the region: population, income, "
                    "unemployment, debt per capita, pension liabilities.",
                    "**Revenue bonds**: analysed like a business: demand for the service, pricing, **debt service "
                    "coverage ratio** (DSCR = net revenue ÷ debt service).",
                    "Non-sovereigns usually **cannot print money**, so they are riskier than their national "
                    "government.",
                ),
                EX("A water utility bond: net revenues ₹120 crore, annual debt service ₹80 crore. DSCR = **1.5×**."),
                FUN(
                    "A sovereign can print its own currency, which is like a family that owns the ATM. A state "
                    "government just has a very large credit card."
                ),
            ),
        ],
        revision=sheet(
            "DSCR = net revenue ÷ debt service · Sovereign = ability + willingness to pay",
            ("Institutional", "Rule of law, stability, willingness"),
            ("Fiscal", "Debt/GDP, deficits"),
            ("Monetary", "Independence, inflation"),
            ("External", "Reserves, current account, reserve currency"),
            ("GO bonds", "Tax base and economy"),
            ("Revenue bonds", "Project cash flow, DSCR"),
        ),
        questions=[
            q(
                "E",
                "Debt-to-GDP is mainly a measure of a sovereign's:",
                ["Fiscal position", "Monetary policy", "Institutional strength"],
                0,
                "It reflects fiscal burden.",
                "15.b",
            ),
            q(
                "M",
                "A country whose currency is a global reserve currency usually has:",
                [
                    "Weaker external flexibility",
                    "Greater flexibility to borrow in its own currency",
                    "Higher inflation",
                ],
                1,
                "Demand for its currency supports borrowing.",
                "15.b",
            ),
            q(
                "M",
                "A revenue bond with net revenues of ₹120 crore and debt service of ₹80 crore has a DSCR of:",
                ["0.67×", "1.5×", "2.0×"],
                1,
                "120 ÷ 80 = 1.5.",
                "15.a",
            ),
            q(
                "H",
                "A key difference between sovereign and corporate credit is that sovereigns:",
                ["Always repay", "May be able but unwilling to pay, and enforcement is limited", "Have no tax base"],
                1,
                "Willingness to pay is crucial.",
                "15.a",
            ),
            q(
                "E",
                "Central bank independence and inflation history are part of which factor?",
                ["Monetary", "External", "Economic"],
                0,
                "They shape monetary credibility.",
                "15.b",
            ),
            q(
                "M",
                "General obligation bonds are analysed mainly on the:",
                ["Revenue of one project", "Issuer's tax base and regional economy", "Price of oil"],
                1,
                "Backed by taxing power.",
                "15.a",
            ),
            q(
                "M",
                "Large foreign exchange reserves relative to imports strengthen a sovereign's:",
                ["External position", "Fiscal position", "Institutional score"],
                0,
                "Reserves meet external obligations.",
                "15.b",
            ),
            q(
                "H",
                "Non-sovereign governments are typically riskier than their national government because they:",
                ["Have higher GDP", "Cannot print money", "Always have revenue bonds"],
                1,
                "They lack monetary control.",
                "15.a",
            ),
            q(
                "E",
                "Political stability and rule of law are examples of:",
                ["Institutional factors", "Fiscal factors", "External factors"],
                0,
                "They affect willingness and ability.",
                "15.b",
            ),
            q(
                "M",
                "A persistent large current account deficit financed by short-term foreign debt is a weakness in a "
                "sovereign's:",
                ["External position", "Monetary policy", "GDP growth"],
                0,
                "It creates refinancing vulnerability.",
                "15.b",
            ),
        ],
        flashcards=[
            fc("Five sovereign factors", "Institutional, economic, fiscal, monetary, external."),
            fc("Sovereign-specific risk", "Willingness to pay; limited enforcement."),
            fc("Reserve currency benefit", "Easier borrowing in own currency."),
            fc("GO bond analysis", "Tax base, economy, debt per capita."),
            fc("Revenue bond analysis", "DSCR = net revenue ÷ debt service."),
            fc("Why non-sovereigns are riskier", "They cannot print money."),
        ],
    )
)

# ---------------------------------------------------------------- LM16
LMS.append(
    dict(
        lm_no=16,
        title="Credit Analysis for Corporate Issuers",
        summary="Qualitative and quantitative corporate credit analysis, leverage and coverage ratios, and seniority.",
        los=[
            ("16.a", "describe", "Describe qualitative factors in assessing a corporate issuer's credit."),
            ("16.b", "calculate", "Calculate and interpret financial ratios used in corporate credit analysis."),
            ("16.c", "explain", "Explain how seniority, structural subordination and covenants affect credit."),
        ],
        topics=[
            topic(
                "Qualitative and quantitative factors",
                L(
                    "**Business model** and industry: cyclicality, competition, pricing power, scale.",
                    "**Management** and governance; **ESG** risks such as pollution liabilities.",
                    "**Profitability**: EBITDA margin, stability of cash flow.",
                ),
                T(
                    ["Ratio", "Formula", "Better when"],
                    ["Debt / EBITDA", "Total debt ÷ EBITDA", "Lower"],
                    ["EBITDA / interest", "EBITDA ÷ interest expense", "Higher"],
                    ["FFO / debt", "Funds from operations ÷ total debt", "Higher"],
                    ["Debt / capital", "Debt ÷ (debt + equity)", "Lower"],
                ),
                EX(
                    "Rajhans Chemicals: debt ₹600 crore, EBITDA ₹200 crore, interest ₹40 crore. Debt/EBITDA = "
                    "**3.0×**; "
                    "EBITDA/interest = **5.0×**. A peer at 5.5× leverage and 2× coverage would be rated lower."
                ),
            ),
            topic(
                "Seniority, structure and covenants",
                L(
                    "Higher seniority and security → higher expected recovery → higher issue rating.",
                    "**Structural subordination**: holding-company debt is paid only from dividends of operating "
                    "subsidiaries, after the subsidiaries' own creditors. So holdco debt ranks effectively below opco "
                    "debt.",
                    "**Covenants** (limits on leverage, asset sales, dividends) protect bondholders; high-yield bonds "
                    "carry more of them.",
                ),
                WO("A holdco's 'senior' bond can still be riskier than an opco's senior bond of the same group."),
                FUN(
                    "Structural subordination is being the cousin who gets wedding sweets only after the immediate "
                    "family has eaten. Technically invited, practically last in line."
                ),
            ),
        ],
        revision=sheet(
            "Leverage: Debt/EBITDA (lower better) · Coverage: EBITDA/interest (higher better)",
            ("Qualitative", "Business model, industry, management, ESG"),
            ("FFO / debt", "Cash flow capacity"),
            ("Seniority", "Higher → better recovery"),
            ("Structural subordination", "Holdco ranks behind opco creditors"),
            ("Covenants", "Protect lenders; stricter for HY"),
        ),
        questions=[
            q(
                "M",
                "Debt ₹600 crore and EBITDA ₹200 crore give debt/EBITDA of:",
                ["3.0×", "0.33×", "4.0×"],
                0,
                "600 ÷ 200 = 3.0.",
                "16.b",
            ),
            q(
                "M",
                "EBITDA ₹200 crore and interest expense ₹40 crore give interest coverage of:",
                ["5.0×", "0.2×", "8.0×"],
                0,
                "200 ÷ 40 = 5.",
                "16.b",
            ),
            q(
                "E",
                "Which indicates stronger credit quality?",
                ["Higher debt/EBITDA", "Higher EBITDA/interest", "Lower FFO/debt"],
                1,
                "More coverage is better.",
                "16.b",
            ),
            q(
                "H",
                "Debt of a holding company that depends on dividends from subsidiaries is:",
                [
                    "Structurally senior to subsidiary debt",
                    "Structurally subordinated to subsidiary debt",
                    "Always secured",
                ],
                1,
                "Subsidiary creditors are paid first.",
                "16.c",
            ),
            q(
                "M",
                "Which is a qualitative factor in corporate credit analysis?",
                ["Debt/EBITDA", "Competitive position and industry structure", "Coupon rate"],
                1,
                "Business risk matters.",
                "16.a",
            ),
            q(
                "E",
                "Funds from operations ÷ total debt measures:",
                ["Leverage relative to cash flow", "Liquidity only", "Profit margin"],
                0,
                "Higher is better.",
                "16.b",
            ),
            q(
                "M",
                "Compared with investment-grade bonds, high-yield bonds usually have:",
                ["Fewer covenants", "More and stricter covenants", "No indenture"],
                1,
                "Lenders need more protection.",
                "16.c",
            ),
            q(
                "M",
                "Higher seniority of a bond within a company's capital structure generally means:",
                ["Lower expected recovery", "Higher expected recovery", "No difference"],
                1,
                "Senior claims are paid first.",
                "16.c",
            ),
            q(
                "H",
                "A highly cyclical company with volatile cash flows should be assessed with:",
                ["Only one year of peak data", "Ratios across the cycle, including downturns", "Equity valuation only"],
                1,
                "Credit depends on the worst years.",
                "16.a",
            ),
            q(
                "E",
                "Debt ÷ (debt + equity) is the:",
                ["Debt-to-capital ratio", "Coverage ratio", "Current ratio"],
                0,
                "A leverage measure.",
                "16.b",
            ),
        ],
        flashcards=[
            fc("Debt / EBITDA", "Leverage; lower is better."),
            fc("EBITDA / interest", "Coverage; higher is better."),
            fc("FFO / debt", "Cash flow capacity to repay."),
            fc("Structural subordination", "Holdco debt ranks behind opco creditors."),
            fc("Qualitative credit factors", "Business model, industry, management, ESG."),
            fc("HY covenants", "More and stricter."),
        ],
    )
)

# ---------------------------------------------------------------- LM17
LMS.append(
    dict(
        lm_no=17,
        title="Fixed-Income Securitization",
        summary="Why assets are securitised, the parties and structure, credit tranching and covered bonds.",
        los=[
            ("17.a", "explain", "Explain benefits of securitisation for issuers, investors, economies and markets."),
            ("17.b", "describe", "Describe securitisation, including the parties and their roles."),
            ("17.c", "describe", "Describe typical structures of securitisations, including credit tranching."),
            ("17.d", "describe", "Describe covered bonds and contrast them with ABS."),
        ],
        topics=[
            topic(
                "Why and how",
                L(
                    "**Benefits**: lowers funding cost, frees bank capital to lend more, gives investors access to "
                    "diversified loan pools, improves liquidity.",
                    "**Originator / seller**: makes the loans and sells them.",
                    "**Special purpose entity (SPE)**: buys the loans and issues securities; it is **bankruptcy "
                    "remote** "
                    "from the originator.",
                    "**Servicer**: collects payments; **trustee** protects investors.",
                ),
                EX(
                    "Shakti Finance has ₹500 crore of auto loans. It sells them to an SPE, which issues ₹500 crore of "
                    "ABS. "
                    "Shakti gets cash to make new loans; if Shakti later fails, the loan cash flows still go to the "
                    "ABS "
                    "holders."
                ),
                WO("Bankruptcy remoteness is the key: the ABS rating depends on the loan pool, not on the originator."),
            ),
            topic(
                "Structures and covered bonds",
                L(
                    "**Credit tranching**: senior, mezzanine and junior (equity) tranches. Losses hit the most junior "
                    "first (**subordination**) — a waterfall.",
                    "**Time tranching**: tranches receive principal in sequence, spreading prepayment risk.",
                    "**Covered bonds**: issued by a bank, backed by a **cover pool** that stays **on the bank's "
                    "balance "
                    "sheet**. Investors have **dual recourse** (the bank and the pool). The pool is **dynamic**: bad "
                    "loans must be replaced.",
                ),
                EX(
                    "A ₹100 crore pool funds: senior ₹80 crore, mezzanine ₹15 crore, junior ₹5 crore. Losses of ₹8 "
                    "crore wipe "
                    "out the junior tranche and take ₹3 crore from the mezzanine; the senior tranche is untouched."
                ),
                FUN(
                    "Credit tranching is the family seating at a crowded wedding: the junior cousins stand at the back "
                    "and leave first when the hall gets too full; the grandparents keep their chairs."
                ),
            ),
        ],
        revision=sheet(
            "Losses hit junior → mezzanine → senior",
            ("Originator", "Makes and sells loans"),
            ("SPE", "Buys pool, issues ABS; bankruptcy remote"),
            ("Servicer", "Collects loan payments"),
            ("Credit tranching", "Redistributes credit risk"),
            ("Time tranching", "Redistributes prepayment risk"),
            ("Covered bond", "On balance sheet, dual recourse, dynamic pool"),
        ),
        questions=[
            q(
                "E",
                "The entity that buys the loans and issues the securities in a securitisation is the:",
                ["Servicer", "Special purpose entity", "Trustee"],
                1,
                "The SPE holds the pool.",
                "17.b",
            ),
            q(
                "M",
                "Bankruptcy remoteness means that if the originator fails:",
                [
                    "ABS investors lose everything",
                    "The SPE's assets are protected for ABS investors",
                    "The servicer must repay investors",
                ],
                1,
                "The pool is legally separate.",
                "17.b",
            ),
            q(
                "M",
                "A ₹100 crore pool has senior ₹80 crore, mezzanine ₹15 crore and junior ₹5 crore. Losses of ₹8 crore "
                "reduce the mezzanine tranche by:",
                ["₹8 crore", "₹3 crore", "₹0"],
                1,
                "Junior absorbs 5, mezzanine 3.",
                "17.c",
            ),
            q(
                "E",
                "Which is a benefit of securitisation for banks?",
                ["It frees capital to make new loans", "It eliminates all risk", "It increases deposits"],
                0,
                "Selling loans recycles capital.",
                "17.a",
            ),
            q(
                "M",
                "Covered bonds differ from ABS because the assets:",
                ["Are sold to an SPE", "Stay on the issuing bank's balance sheet", "Must be equity"],
                1,
                "Investors have recourse to the bank and the pool.",
                "17.d",
            ),
            q(
                "H",
                "In a covered bond, non-performing loans in the cover pool are:",
                ["Left in place", "Replaced with performing loans", "Converted into equity"],
                1,
                "The pool is dynamic.",
                "17.d",
            ),
            q(
                "M",
                "Time tranching mainly redistributes:",
                ["Credit risk", "Prepayment (timing) risk", "Currency risk"],
                1,
                "Sequential principal payments.",
                "17.c",
            ),
            q(
                "E",
                "The party that collects payments from borrowers is the:",
                ["Servicer", "Underwriter", "Rating agency"],
                0,
                "It services the loans.",
                "17.b",
            ),
            q(
                "H",
                "Dual recourse in a covered bond means investors can claim on:",
                ["Two SPEs", "Both the issuing bank and the cover pool", "The government and the bank"],
                1,
                "This makes covered bonds very safe.",
                "17.d",
            ),
            q(
                "M",
                "Credit tranching works by:",
                [
                    "Allocating losses first to junior tranches",
                    "Paying all tranches equally",
                    "Giving juniors priority",
                ],
                0,
                "Subordination protects senior tranches.",
                "17.c",
            ),
        ],
        flashcards=[
            fc("Securitisation parties", "Originator, SPE, servicer, trustee."),
            fc("Bankruptcy remote", "SPE assets safe if the originator fails."),
            fc("Credit tranching", "Losses hit junior first."),
            fc("Time tranching", "Sequential principal; spreads prepayment risk."),
            fc("Covered bond", "On balance sheet; dual recourse; dynamic pool."),
            fc("Securitisation benefit", "Cheaper funding; frees bank capital."),
        ],
    )
)

# ---------------------------------------------------------------- LM18
LMS.append(
    dict(
        lm_no=18,
        title="Asset-Backed Security (ABS) Instrument and Market Features",
        summary="Auto loan ABS, credit card ABS, and collateralised debt obligations.",
        los=[
            (
                "18.a",
                "describe",
                "Describe characteristics and risks of covered bonds and ABS backed by auto loans "
                "and credit card receivables.",
            ),
            ("18.b", "describe", "Describe collateralised debt obligations, including their structure and risks."),
        ],
        topics=[
            topic(
                "Auto loan and credit card ABS",
                L(
                    "**Auto loan ABS**: **amortising** pools; cash flows include interest, scheduled principal and "
                    "**prepayments**. Credit enhancement via subordination, overcollateralisation, reserve accounts "
                    "and **excess spread**.",
                    "**Credit card ABS**: **non-amortising** revolving pools. During the **lockout (revolving) "
                    "period**, "
                    "principal collected buys new receivables; investors get only interest. Then principal is paid "
                    "out. **Early amortisation** triggers (e.g. high losses) start repayment early.",
                ),
                EX(
                    "A card ABS has a 3-year lockout. In those years investors receive only finance charges; principal "
                    "repayments from cardholders are reinvested in new card balances."
                ),
                WO("Credit card ABS have little prepayment risk during the lockout, because the pool keeps revolving."),
            ),
            topic(
                "Collateralised debt obligations",
                L(
                    "A **CDO** is backed by a pool of debt: corporate bonds, loans (**CLO**), or other structured "
                    "securities.",
                    "A **collateral manager** actively buys and sells the collateral.",
                    "Tranches: senior, mezzanine, subordinated (equity). The equity tranche earns what is left after "
                    "paying the others: high return, high risk.",
                    "Key risk: **correlation** of defaults. If defaults cluster, even mezzanine tranches can lose.",
                ),
                EX(
                    "A CLO holds ₹1,000 crore of loans yielding 9%; it pays 6% on ₹900 crore of debt tranches. Excess: "
                    "90 − 54 = "
                    "₹36 crore minus fees goes to the ₹100 crore equity tranche: a potential **~36% gross** return, "
                    "wiped out "
                    "quickly if loans default."
                ),
                FUN(
                    "A CDO equity tranche is the friend who offers to pay for everyone's dinner if he can keep "
                    "the change from a very big tip. Great evening, until someone orders the lobster."
                ),
            ),
        ],
        revision=sheet(
            "Card ABS: lockout → only interest; then principal · Auto ABS: amortising, prepayments",
            ("Auto loan ABS", "Amortising; prepayment risk"),
            ("Credit card ABS", "Non-amortising, revolving"),
            ("Lockout period", "Principal reinvested"),
            ("Early amortisation", "Triggered by poor performance"),
            ("CLO", "CDO backed by leveraged loans"),
            ("CDO key risk", "Default correlation"),
        ),
        questions=[
            q(
                "E",
                "Credit card receivable ABS are typically:",
                ["Amortising", "Non-amortising", "Zero-coupon"],
                1,
                "Receivables revolve.",
                "18.a",
            ),
            q(
                "M",
                "During the lockout period of a credit card ABS, principal collected is:",
                ["Paid to investors", "Used to buy new receivables", "Paid to the servicer as a fee"],
                1,
                "Investors receive only interest.",
                "18.a",
            ),
            q(
                "M",
                "Auto loan ABS cash flows include:",
                ["Only interest", "Interest, scheduled principal and prepayments", "Dividends"],
                1,
                "They amortise.",
                "18.a",
            ),
            q(
                "H",
                "An early amortisation provision in a credit card ABS is triggered by:",
                [
                    "Strong collateral performance",
                    "Events such as rising losses that threaten investors",
                    "A fall in interest rates",
                ],
                1,
                "It returns principal early to protect investors.",
                "18.a",
            ),
            q(
                "E",
                "A CDO backed by leveraged bank loans is a:",
                ["CMO", "CLO", "Covered bond"],
                1,
                "Collateralised loan obligation.",
                "18.b",
            ),
            q(
                "M",
                "The tranche of a CDO that absorbs losses first is the:",
                ["Senior tranche", "Mezzanine tranche", "Equity (subordinated) tranche"],
                2,
                "It is paid last.",
                "18.b",
            ),
            q(
                "H",
                "The key risk that can cause losses even on mezzanine CDO tranches is:",
                ["Low default correlation", "High default correlation", "Low coupons"],
                1,
                "Clustered defaults overwhelm subordination.",
                "18.b",
            ),
            q(
                "M",
                "Excess spread in an auto ABS refers to:",
                [
                    "Interest collected on loans above what is paid on the ABS and fees",
                    "The price of the ABS",
                    "Prepayments",
                ],
                0,
                "It absorbs losses as a credit enhancement.",
                "18.a",
            ),
            q(
                "E",
                "A CDO's collateral manager:",
                ["Collects card payments", "Actively buys and sells the collateral", "Issues the original loans"],
                1,
                "CDOs are often actively managed.",
                "18.b",
            ),
            q(
                "M",
                "Compared with auto loan ABS, credit card ABS during the lockout have:",
                ["More prepayment risk", "Less prepayment risk", "Identical prepayment risk"],
                1,
                "Principal is reinvested, not passed through.",
                "18.a",
            ),
        ],
        flashcards=[
            fc("Auto loan ABS", "Amortising; interest, principal, prepayments."),
            fc("Credit card ABS", "Non-amortising; revolving receivables."),
            fc("Lockout period", "Principal reinvested; only interest paid."),
            fc("Early amortisation", "Trigger returns principal early."),
            fc("CLO", "CDO backed by leveraged loans."),
            fc("CDO key risk", "Default correlation."),
        ],
    )
)

# ---------------------------------------------------------------- LM19
LMS.append(
    dict(
        lm_no=19,
        title="Mortgage-Backed Security (MBS) Instrument and Market Features",
        summary="Mortgage loan features, pass-throughs, prepayment risk, CMOs and commercial MBS.",
        los=[
            (
                "19.a",
                "define",
                "Define prepayment risk and describe the prepayment risk of mortgage-backed securities.",
            ),
            (
                "19.b",
                "describe",
                "Describe characteristics and risks of residential mortgage-backed securities, "
                "including pass-throughs and CMOs.",
            ),
            ("19.c", "describe", "Describe characteristics and risks of commercial mortgage-backed securities."),
        ],
        topics=[
            topic(
                "Mortgages and prepayment",
                L(
                    "Features: fixed or adjustable rate; amortising; **prepayment** option (sometimes with penalties); "
                    "**recourse** (lender can claim beyond the property) or non-recourse; **loan-to-value (LTV)**.",
                    "**Contraction risk**: rates fall → borrowers refinance → principal comes back early, to reinvest "
                    "at lower rates.",
                    "**Extension risk**: rates rise → prepayments slow → the investor is stuck with a below-market "
                    "security for longer.",
                    "Prepayment speed: **CPR** (annual) and **SMM** (monthly): SMM = 1 − (1 − CPR)^(1/12).",
                ),
                EX(
                    "CPR of 6% → SMM = 1 − 0.94^(1/12) = **0.514%** a month. With ₹100 crore of principal outstanding "
                    "after "
                    "scheduled repayment of ₹0.5 crore, prepayment = 0.00514 × 99.5 ≈ **₹0.51 crore** this month."
                ),
                WO("MBS have **negative convexity**: falling rates bring faster prepayments, capping price gains."),
            ),
            topic(
                "Pass-throughs, CMOs and CMBS",
                L(
                    "**Agency RMBS** carry a government-backed guarantee; **non-agency** need credit enhancement.",
                    "**Pass-through**: investors get a share of all cash flows, less servicing and guarantee fees.",
                    "**CMOs** redistribute prepayment risk: **sequential-pay** tranches receive principal in order; "
                    "**PAC** tranches get a stable schedule while **support** tranches absorb prepayment variation; "
                    "Z-tranches accrue interest.",
                    "**CMBS**: backed by commercial property loans; key ratios **DSCR** and **LTV**; strong **call "
                    "protection** (prepayment lockouts, **defeasance**, prepayment penalties, **yield maintenance**); "
                    "**balloon risk** at maturity.",
                ),
                FUN(
                    "Prepayment risk is the guest who leaves your party the moment a better party starts nearby, and "
                    "stays forever when it's raining outside."
                ),
            ),
        ],
        revision=sheet(
            "SMM = 1 − (1 − CPR)^(1/12) · rates ↓ → contraction · rates ↑ → extension",
            ("Recourse loan", "Lender can claim beyond the property"),
            ("Pass-through", "Pro-rata share of pool cash flows"),
            ("Sequential CMO", "Principal tranche by tranche"),
            ("PAC / support", "Stable schedule / absorbs variation"),
            ("CMBS call protection", "Lockout, defeasance, penalties, yield maintenance"),
            ("CMBS ratios", "DSCR, LTV; balloon risk"),
        ),
        questions=[
            q(
                "E",
                "When interest rates fall sharply, MBS investors face mainly:",
                ["Extension risk", "Contraction risk", "No prepayment risk"],
                1,
                "Borrowers refinance and prepay.",
                "19.a",
            ),
            q(
                "M",
                "A CPR of 6% corresponds to a single monthly mortality rate closest to:",
                ["0.50%", "0.51%", "6.00%"],
                1,
                "1 − 0.94^(1/12) = 0.514%.",
                "19.a",
            ),
            q(
                "M",
                "Rising interest rates slow prepayments and expose investors to:",
                ["Contraction risk", "Extension risk", "Call risk"],
                1,
                "The MBS lasts longer at a below-market rate.",
                "19.a",
            ),
            q(
                "E",
                "In a mortgage pass-through security, investors receive:",
                ["A fixed coupon only", "A pro-rata share of the pool's cash flows, less fees", "Equity dividends"],
                1,
                "Cash flows are passed through.",
                "19.b",
            ),
            q(
                "M",
                "In a CMO with PAC and support tranches, prepayment variation is absorbed mainly by:",
                ["The PAC tranche", "The support tranche", "The servicer"],
                1,
                "Support tranches protect the PAC schedule.",
                "19.b",
            ),
            q(
                "H",
                "Which provides call protection in CMBS?",
                ["Defeasance and yield maintenance charges", "Adjustable rates", "Recourse"],
                0,
                "They discourage or neutralise prepayment.",
                "19.c",
            ),
            q(
                "M",
                "Two key ratios for analysing commercial mortgage loans are:",
                ["P/E and P/B", "DSCR and LTV", "Current and quick ratios"],
                1,
                "Income coverage and leverage.",
                "19.c",
            ),
            q(
                "H",
                "MBS exhibit negative convexity because:",
                [
                    "Coupons are floating",
                    "Falling rates increase prepayments, limiting price gains",
                    "They have no maturity",
                ],
                1,
                "The prepayment option caps upside.",
                "19.a",
            ),
            q(
                "E",
                "A mortgage where the lender can claim the borrower's other assets after foreclosure is:",
                ["Non-recourse", "Recourse", "Interest-only"],
                1,
                "Recourse loans reduce strategic default.",
                "19.b",
            ),
            q(
                "M",
                "Balloon risk in CMBS is the risk that:",
                ["Borrowers cannot refinance the large final payment at maturity", "Rates fall", "Tenants pay early"],
                0,
                "Many commercial loans have balloon maturities.",
                "19.c",
            ),
        ],
        flashcards=[
            fc("Contraction risk", "Rates fall → faster prepayments."),
            fc("Extension risk", "Rates rise → slower prepayments."),
            fc("SMM from CPR", "1 − (1 − CPR)^(1/12)."),
            fc("Sequential-pay CMO", "Principal to tranches in order."),
            fc("PAC vs support tranche", "Stable schedule vs absorbs prepayment variation."),
            fc("CMBS call protection", "Lockouts, defeasance, penalties, yield maintenance."),
        ],
    )
)


if __name__ == "__main__":
    # Prototype questions: 49 price–yield (LM6), 50 coupon payment (LM1), 51 price sensitivity (LM11).
    write_pack("fi", "Fixed Income", LMS, {"49": 6, "50": 1, "51": 11}, balance_keys=True)
