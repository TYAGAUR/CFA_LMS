"""Alternative Investments content pack.  python scripts/build_pack_ai.py, then re-seed."""

from packlib import EX, FUN, FX, WO, H, L, P, T, fc, q, sheet, topic, write_pack

LMS = []

# ---------------------------------------------------------------- LM1
LMS.append(
    dict(
        lm_no=1,
        title="Alternative Investment Features, Methods and Structures",
        summary="What makes an investment 'alternative', how investors get access, and how fund fees work.",
        los=[
            ("1.a", "describe", "Describe the features and categories of alternative investments."),
            ("1.b", "compare", "Compare direct investment, co-investment and fund investment methods."),
            (
                "1.c",
                "describe",
                "Describe investment ownership and compensation structures commonly used in alternative investments.",
            ),
        ],
        topics=[
            topic(
                "What makes an investment alternative",
                L(
                    "**Illiquid** and often **long-horizon**: lock-ups, few buyers.",
                    "**Specialised** knowledge needed to value and manage.",
                    "**Low correlation** with stocks and bonds, which helps diversification.",
                    "**Less regulation and transparency**, and **high fees**.",
                    "Returns often based on **appraisals**, so reported volatility looks lower than reality.",
                ),
                T(
                    ["Category", "Examples"],
                    ["Private capital", "Private equity, private debt"],
                    ["Real assets", "Real estate, infrastructure, natural resources"],
                    ["Hedge funds", "Long/short, event-driven, macro, relative value"],
                    ["Digital assets", "Cryptocurrencies, tokens"],
                ),
            ),
            topic(
                "Ways to invest",
                T(
                    ["Method", "How", "Pros", "Cons"],
                    [
                        "Fund investing",
                        "Invest in a GP's fund as an LP",
                        "Diversified, needs little expertise",
                        "Highest fees, no say over deals",
                    ],
                    [
                        "Co-investing",
                        "Invest in a fund plus directly alongside it in chosen deals",
                        "Lower fees on co-invested deals, learn from the GP",
                        "Adverse selection: GP may offer weaker deals",
                    ],
                    [
                        "Direct investing",
                        "Buy assets yourself",
                        "No external fees, full control",
                        "Needs large teams and capital, concentrated",
                    ],
                ),
                WO(
                    "Co-investment fees are lower, but the investor still needs the skill to judge whether the deal "
                    "being offered is any good."
                ),
            ),
            topic(
                "Fund structures and fees",
                P(
                    "Most funds are **limited partnerships**: the **GP** manages and has unlimited liability; **LPs** "
                    "commit capital and have limited liability. Terms are set out in the **limited partnership "
                    "agreement**, often with **side letters** for large LPs."
                ),
                L(
                    "**Management fee**: 1–2% a year on committed or invested capital (or AUM).",
                    "**Incentive (performance) fee / carried interest**: typically 20% of profits.",
                    "**Hurdle rate**: minimum return before any incentive fee. A **soft** hurdle lets the GP earn on "
                    "all profit once it is beaten (via **catch-up**); a **hard** hurdle pays only on profit above it.",
                    "**High-water mark**: no incentive fee until previous losses are recovered.",
                    "**Clawback**: GP returns incentive fees paid earlier if later results fall short.",
                    "**Waterfall**: **European** (whole-of-fund: LPs get capital back first, LP-friendly) vs "
                    "**American** (deal-by-deal, GP-friendly).",
                ),
                EX(
                    "A fund starts at ₹100 crore and ends the year at ₹120 crore gross. Fees are 2 and 20, management "
                    "fee "
                    "on year-end value, incentive fee on profit net of the management fee. Management fee = 2% × 120 = "
                    "₹2.4 crore. Incentive = 20% × (120 − 100 − 2.4) = ₹3.52 crore. Net value = 120 − 2.4 − 3.52 = "
                    "₹114.08 crore, a **14.08%** net return versus 20% gross."
                ),
                FUN(
                    "'2 and 20' means the manager gets paid when you win and still gets paid when you lose, just a "
                    "bit less. Like a wedding caterer who bills per plate whether or not anyone enjoyed the food."
                ),
            ),
        ],
        revision=sheet(
            "Net value = Gross − Mgmt fee − Incentive fee (on gain above hurdle / HWM)",
            ("Alternative features", "Illiquid, specialised, low correlation, high fees, less transparent"),
            ("Fund investing", "Easy access, highest fees"),
            ("Co-investing", "Lower fees on some deals; adverse-selection risk"),
            ("Direct investing", "Cheapest, needs most skill and capital"),
            ("Hard hurdle", "Incentive fee only on profit above hurdle"),
            ("High-water mark", "Recover past losses before new incentive fee"),
            ("European waterfall", "Whole-of-fund, LP-friendly"),
            ("American waterfall", "Deal-by-deal, GP-friendly"),
        ),
        questions=[
            q(
                "E",
                "Which is a typical feature of alternative investments?",
                ["High liquidity", "Low fees", "Low correlation with traditional assets"],
                2,
                "Alternatives often diversify because their returns move differently from stocks and bonds.",
                "1.a",
            ),
            q(
                "M",
                "An investor who commits to a private equity fund and also invests directly in one of the fund's "
                "deals is using:",
                ["Co-investing", "Direct investing only", "Fund-of-funds investing"],
                0,
                "Co-investment means investing alongside the fund in selected deals.",
                "1.b",
            ),
            q(
                "M",
                "The main disadvantage of co-investing is:",
                ["Very high fees", "Adverse selection in the deals offered", "No access to the GP"],
                1,
                "The GP may offer co-investments in deals it is less keen to fund fully.",
                "1.b",
            ),
            q(
                "E",
                "In a limited partnership fund, the party that manages the fund is the:",
                ["Limited partner", "Custodian", "General partner"],
                2,
                "The GP manages the fund; LPs supply capital.",
                "1.c",
            ),
            q(
                "M",
                "A fund starts the year at ₹100 crore and ends at ₹120 crore before fees. It charges a 2% management "
                "fee on year-end value and a 20% incentive fee on profit net of the management fee. The investor's "
                "net return is closest to:",
                ["16.0%", "14.1%", "17.6%"],
                1,
                "Mgmt fee 2.4; incentive 0.2 × 17.6 = 3.52; net 114.08, a 14.08% return.",
                "1.c",
            ),
            q(
                "M",
                "A high-water mark provision means the manager:",
                [
                    "Earns incentive fees only on gains above the previous peak value",
                    "Always earns the incentive fee",
                    "Earns no management fee after a loss",
                ],
                0,
                "Losses must be recovered before a new incentive fee is earned.",
                "1.c",
            ),
            q(
                "H",
                "Compared with an American waterfall, a European waterfall:",
                [
                    "Pays carried interest deal by deal",
                    "Pays carried interest only after LPs recover all capital and the preferred return",
                    "Has no hurdle rate",
                ],
                1,
                "Whole-of-fund (European) distribution is more favourable to LPs.",
                "1.c",
            ),
            q(
                "H",
                "A clawback provision requires the:",
                [
                    "LPs to return excess distributions",
                    "GP to return previously paid incentive fees if later results do not justify them",
                    "Fund to pay a hurdle rate in cash",
                ],
                1,
                "Clawback protects LPs from overpaid carried interest.",
                "1.c",
            ),
            q(
                "E",
                "Direct investing is most suitable for investors who:",
                [
                    "Have little capital",
                    "Want the highest diversification",
                    "Have large capital and in-house expertise",
                ],
                2,
                "Direct investing avoids fees but needs scale and skill.",
                "1.b",
            ),
            q(
                "M",
                "Reported returns on appraisal-based alternatives tend to:",
                ["Understate true volatility", "Overstate true volatility", "Be identical to market prices"],
                0,
                "Appraisals smooth values, making reported volatility too low.",
                "1.a",
            ),
        ],
        flashcards=[
            fc("Features of alternatives", "Illiquid, specialised, low correlation, high fees, less transparent."),
            fc(
                "Fund vs co- vs direct investing",
                "Fund: easy, costly. Co: cheaper on some deals. Direct: cheapest, hardest.",
            ),
            fc("GP vs LP", "GP manages with unlimited liability; LPs supply capital with limited liability."),
            fc("Hard vs soft hurdle", "Hard: fee only above hurdle. Soft: fee on all profit once hurdle is beaten."),
            fc("High-water mark", "No incentive fee until the fund regains its previous peak."),
            fc("European vs American waterfall", "Whole-of-fund (LP-friendly) vs deal-by-deal (GP-friendly)."),
        ],
    )
)

# ---------------------------------------------------------------- LM2
LMS.append(
    dict(
        lm_no=2,
        title="Alternative Investment Performance and Returns",
        summary="The life cycle of a fund, IRR and multiples, fee effects, and biases in reported returns.",
        los=[
            ("2.a", "describe", "Describe the performance appraisal of alternative investments."),
            (
                "2.b",
                "calculate",
                "Calculate and interpret returns of alternative investments on both a before-fee and after-fee basis.",
            ),
            ("2.c", "describe", "Describe biases and other issues in measuring alternative investment performance."),
        ],
        topics=[
            topic(
                "Fund life cycle and the J-curve",
                P(
                    "Private funds draw capital in stages (**capital calls**) during an investment period, then "
                    "harvest and return cash. Early years show negative returns because fees and set-up costs come "
                    "before gains: the **J-curve**."
                ),
                L(
                    "**IRR**: the money-weighted return that sets the NPV of all calls and distributions to zero.",
                    "**MOIC** (multiple of invested capital) = (realised + unrealised value) ÷ invested capital.",
                    "Ratios like Sharpe can mislead when returns are smoothed or skewed; Sortino and drawdown help.",
                ),
                EX(
                    "An LP invests ₹10 crore and receives ₹6 crore in year 3 and ₹12 crore in year 5. MOIC = "
                    "(6 + 12) ÷ 10 = **1.8×**. The MOIC ignores timing; IRR does not."
                ),
                WO("A high MOIC earned over 12 years may be a worse IRR than a modest MOIC over 3 years."),
            ),
            topic(
                "Fees, hurdles and the high-water mark",
                EX(
                    "Fund value ₹200 crore at start, high-water mark ₹210 crore (after a loss last year). It ends "
                    "this year at ₹230 crore gross; management fee 1% of year-end value = ₹2.3 crore. With the HWM, "
                    "incentive = 20% × (230 − 2.3 − 210) = 20% × 17.7 = **₹3.54 crore**, not 20% of the full "
                    "27.7 crore gain since the start of the year."
                ),
                FX("Incentive fee = rate × max(0, value after mgmt fee − max(HWM, hurdle level))"),
                WO(
                    "Check the exact terms: fees may be charged on beginning or ending value, and the incentive "
                    "may be calculated before or after the management fee."
                ),
            ),
            topic(
                "Biases and measurement issues",
                L(
                    "**Survivorship bias**: failed funds drop out of databases, so averages look too good.",
                    "**Backfill bias**: funds add their history only after a good run.",
                    "**Appraisal smoothing**: valuations lag market moves, lowering reported volatility and "
                    "correlation.",
                    "**Illiquidity**: there may be no market price at all; the realised value can differ.",
                    "**Leverage and fat tails**: normal-distribution risk measures underestimate crash risk.",
                ),
                FUN(
                    "A hedge fund index with survivorship bias is like rating a cricket academy using only the "
                    "students who made the national team."
                ),
            ),
        ],
        revision=sheet(
            "MOIC = (realised + unrealised) ÷ invested · IRR sets NPV of all flows to 0",
            ("J-curve", "Negative early returns, gains later"),
            ("Capital call", "GP draws committed capital in stages"),
            ("IRR vs MOIC", "IRR uses timing; MOIC does not"),
            ("Survivorship bias", "Dead funds missing: returns overstated"),
            ("Backfill bias", "Good histories added later"),
            ("Smoothing", "Appraisals understate volatility and correlation"),
        ),
        questions=[
            q(
                "E",
                "The J-curve effect in private equity describes:",
                [
                    "Negative returns in early years followed by positive returns later",
                    "Constant returns",
                    "Returns that fall over the fund's life",
                ],
                0,
                "Fees and costs arrive before gains, so early returns are negative.",
                "2.a",
            ),
            q(
                "M",
                "An investor puts ₹10 crore into a fund and later receives a total of ₹18 crore. The MOIC is:",
                ["0.8×", "1.8×", "2.8×"],
                1,
                "MOIC = 18 ÷ 10 = 1.8.",
                "2.b",
            ),
            q(
                "M",
                "The main weakness of MOIC compared with IRR is that MOIC:",
                ["Ignores the timing of cash flows", "Cannot be computed for private equity", "Always exceeds IRR"],
                0,
                "MOIC is a simple multiple; it does not account for how long money was invested.",
                "2.a",
            ),
            q(
                "H",
                "A fund with a high-water mark of ₹210 crore ends the year at ₹230 crore gross, pays a ₹2.3 crore "
                "management fee and charges 20% incentive on gains above the HWM net of the management fee. "
                "The incentive fee is closest to:",
                ["₹5.54 crore", "₹4.00 crore", "₹3.54 crore"],
                2,
                "20% × (230 − 2.3 − 210) = 20% × 17.7 = ₹3.54 crore.",
                "2.b",
            ),
            q(
                "M",
                "Survivorship bias causes hedge fund index returns to be:",
                ["Understated", "Overstated", "Unaffected"],
                1,
                "Funds that failed are dropped, so the survivors' average looks better than reality.",
                "2.c",
            ),
            q(
                "M",
                "Backfill bias arises when:",
                [
                    "Funds are removed after closing",
                    "Funds add past returns to a database after a strong record",
                    "Funds report daily prices",
                ],
                1,
                "Managers choose to report only once they have good history to show.",
                "2.c",
            ),
            q(
                "H",
                "Appraisal-based valuations in real estate most likely cause:",
                [
                    "Reported correlation with equities to be too low",
                    "Reported volatility to be too high",
                    "No bias in risk measures",
                ],
                0,
                "Smoothed valuations lower measured volatility and correlation.",
                "2.c",
            ),
            q(
                "E",
                "When a private equity GP asks LPs to provide part of their committed capital, it is a:",
                ["Distribution", "Capital call", "Clawback"],
                1,
                "Capital calls (draw-downs) fund investments as they are made.",
                "2.a",
            ),
            q(
                "M",
                "For alternatives with skewed, fat-tailed returns, which risk measure is more informative than the "
                "standard deviation?",
                ["Maximum drawdown", "Beta to a bond index", "Dividend yield"],
                0,
                "Drawdown and downside measures capture tail losses better.",
                "2.a",
            ),
            q(
                "E",
                "The IRR of a private fund is best described as a:",
                ["Time-weighted return", "Money-weighted return", "Holding-period dividend yield"],
                1,
                "IRR weights by the cash actually invested over time.",
                "2.b",
            ),
        ],
        flashcards=[
            fc("J-curve", "Early negative returns from fees and costs, gains later."),
            fc("MOIC", "(Realised + unrealised value) ÷ invested capital; ignores timing."),
            fc("IRR in private funds", "Money-weighted return over calls and distributions."),
            fc("Survivorship bias", "Failed funds drop out; returns look too high."),
            fc("Backfill bias", "Funds report history only after a good run."),
            fc("Appraisal smoothing", "Understates volatility and correlation."),
        ],
    )
)

# ---------------------------------------------------------------- LM3
LMS.append(
    dict(
        lm_no=3,
        title="Investments in Private Capital: Equity and Debt",
        summary="Private equity strategies and exits, private debt types, and their risk and return.",
        los=[
            ("3.a", "explain", "Explain features of private equity and its investment characteristics."),
            ("3.b", "explain", "Explain features of private debt and its investment characteristics."),
            ("3.c", "describe", "Describe the diversification benefits that private capital can provide."),
        ],
        topics=[
            topic(
                "Private equity",
                T(
                    ["Strategy", "Target", "Notes"],
                    [
                        "Leveraged buyout (LBO)",
                        "Mature, cash-generative companies",
                        "Funded mostly with debt; MBO when existing managers buy, MBI when outsiders come in",
                    ],
                    ["Venture capital", "Start-ups", "Stages: pre-seed/seed → early (Series A) → later stage"],
                    ["Growth equity", "Established, growing firms", "Usually minority stakes, little debt"],
                ),
                H("Exit routes"),
                L(
                    "**Trade sale** to a strategic buyer, often the highest price.",
                    "**IPO**: highest value in strong markets, but costly and slow.",
                    "**Secondary sale** to another PE fund.",
                    "**Recapitalisation**: re-lever the company and pay a dividend to the fund.",
                    "**Write-off** if it fails.",
                ),
                EX(
                    "An LBO fund buys Kaveri Foods for ₹500 crore using ₹150 crore equity and ₹350 crore debt. Five "
                    "years later it sells for ₹700 crore and debt has been paid down to ₹250 crore. Equity value = "
                    "700 − 250 = ₹450 crore, a **3× multiple** on ₹150 crore. Leverage turned a 40% rise in enterprise "
                    "value into a 200% equity gain."
                ),
            ),
            topic(
                "Private debt",
                L(
                    "**Direct lending**: senior loans from non-banks to mid-sized firms, often floating rate.",
                    "**Mezzanine debt**: subordinated, higher coupon, often with **warrants** or conversion rights.",
                    "**Venture debt**: loans to start-ups backed by VCs, often with warrants.",
                    "**Distressed debt**: buy debt of troubled firms cheaply, sometimes to gain control in "
                    "restructuring.",
                    "**Unitranche**: one loan blending senior and subordinated tranches at a single rate.",
                ),
                WO(
                    "Mezzanine sits **between** senior debt and equity in the capital structure; higher return comes "
                    "from that lower priority."
                ),
            ),
            topic(
                "Risk, return and diversification",
                P(
                    "Private equity aims to beat public equity with higher risk (leverage, illiquidity, "
                    "concentration). "
                    "Private debt offers higher yields than public bonds as compensation for illiquidity and credit "
                    "risk. Both have only partial correlation with listed markets, though smoothing exaggerates the "
                    "diversification benefit."
                ),
                FUN(
                    "Venture capital is a cricket team where nine batters get out for a duck, one scores 50 and one "
                    "hits a triple century. The triple century pays for the whole season."
                ),
            ),
        ],
        revision=sheet(
            "LBO equity multiple = (Exit EV − remaining debt) ÷ equity invested",
            ("LBO", "Debt-funded buyout of a mature firm"),
            ("MBO / MBI", "Insiders / outsiders buy the firm"),
            ("VC stages", "Pre-seed, seed, early, later"),
            ("Exits", "Trade sale, IPO, secondary, recap, write-off"),
            ("Mezzanine", "Subordinated debt with warrants"),
            ("Unitranche", "Senior + junior in one loan"),
            ("Distressed", "Buy troubled debt cheaply, maybe gain control"),
        ),
        questions=[
            q(
                "E",
                "A buyout in which a company's existing managers acquire the business is a:",
                ["Management buy-in", "Management buyout", "Venture round"],
                1,
                "MBO = insiders buy; MBI = outside managers come in.",
                "3.a",
            ),
            q(
                "M",
                "An LBO fund invests ₹150 crore of equity and ₹350 crore of debt to buy a firm. It exits at ₹700 "
                "crore with ₹250 crore of debt outstanding. The equity multiple is:",
                ["3.0×", "1.4×", "4.7×"],
                0,
                "Equity = 700 − 250 = 450; 450 ÷ 150 = 3.0×.",
                "3.a",
            ),
            q(
                "E",
                "Venture capital mainly invests in:",
                ["Mature cash-cow companies", "Government bonds", "Start-ups and early-stage firms"],
                2,
                "VC funds back young companies with high growth potential.",
                "3.a",
            ),
            q(
                "M",
                "Which exit route is usually the slowest and most costly but can achieve high valuations in strong "
                "markets?",
                ["Trade sale", "Initial public offering", "Write-off"],
                1,
                "IPOs take time and fees but can deliver high prices when markets are buoyant.",
                "3.a",
            ),
            q(
                "M",
                "Mezzanine debt is best described as:",
                ["Senior secured bank debt", "Subordinated debt, often with warrants", "Common equity"],
                1,
                "Mezzanine ranks below senior debt and usually carries equity kickers.",
                "3.b",
            ),
            q(
                "H",
                "A loan that combines senior and subordinated debt into a single facility at one blended rate is:",
                ["A unitranche loan", "Venture debt", "A recapitalisation"],
                0,
                "Unitranche blends tranches into one loan.",
                "3.b",
            ),
            q(
                "M",
                "Distressed debt investors typically aim to:",
                [
                    "Hold AAA bonds to maturity",
                    "Buy debt of troubled firms at a discount and profit from recovery or restructuring",
                    "Lend only to start-ups",
                ],
                1,
                "They buy cheaply and may influence or take control in restructuring.",
                "3.b",
            ),
            q(
                "H",
                "The diversification benefit of private capital measured from reported returns is likely:",
                [
                    "Overstated because of appraisal smoothing",
                    "Understated because of daily pricing",
                    "Exactly correct",
                ],
                0,
                "Smoothed valuations lower measured correlation with public markets.",
                "3.c",
            ),
            q(
                "E",
                "Compared with listed equity, private equity is mainly characterised by:",
                ["Daily liquidity", "Illiquidity and long holding periods", "Lower fees"],
                1,
                "PE investments are locked up for years.",
                "3.a",
            ),
            q(
                "M",
                "A recapitalisation as an exit strategy involves:",
                [
                    "Selling the company to a competitor",
                    "Adding debt to the company to pay a dividend to the fund",
                    "Listing the shares on an exchange",
                ],
                1,
                "Recaps return cash to the fund while it keeps ownership.",
                "3.a",
            ),
        ],
        flashcards=[
            fc("LBO", "Buyout of a mature company funded mostly with debt."),
            fc("VC stages", "Pre-seed, seed, early (Series A), later stage."),
            fc("PE exit routes", "Trade sale, IPO, secondary sale, recapitalisation, write-off."),
            fc("Mezzanine debt", "Subordinated debt with warrants or conversion rights."),
            fc("Direct lending", "Non-bank senior loans to mid-sized firms, often floating."),
            fc("Unitranche", "Single loan blending senior and junior debt."),
        ],
    )
)

# ---------------------------------------------------------------- LM4
LMS.append(
    dict(
        lm_no=4,
        title="Real Estate and Infrastructure",
        summary="Forms of real estate investment, REITs, valuation approaches, and infrastructure assets.",
        los=[
            ("4.a", "explain", "Explain features and characteristics of real estate."),
            ("4.b", "explain", "Explain the investment characteristics of real estate investments."),
            ("4.c", "explain", "Explain features and characteristics of infrastructure."),
            ("4.d", "explain", "Explain the investment characteristics of infrastructure investments."),
        ],
        topics=[
            topic(
                "Real estate: forms and features",
                T(
                    ["", "Private", "Public"],
                    ["Equity", "Direct ownership, private funds", "REITs, real estate company shares"],
                    ["Debt", "Mortgages, private loans", "Mortgage-backed securities"],
                ),
                L(
                    "Each property is **unique** (location), **indivisible** and expensive, with high transaction "
                    "costs and low liquidity.",
                    "Returns come from **rental income** and **capital appreciation**; leases give fairly stable "
                    "income and some inflation protection.",
                    "**REITs** pay out most of their income, trade on exchanges and give liquidity, but behave more "
                    "like equities in the short run.",
                ),
                WO(
                    "Listed REITs are liquid and priced daily; direct property is appraised, so its returns look "
                    "smoother."
                ),
            ),
            topic(
                "Valuing property",
                L(
                    "**Income approach**: value = NOI ÷ cap rate (direct capitalisation) or DCF of future cash flows.",
                    "**Cost approach**: replacement cost of the building plus land, minus depreciation.",
                    "**Sales comparison approach**: prices of similar recent transactions, adjusted for differences.",
                ),
                FX("Value = NOI ÷ Cap rate · NOI = rental income − operating expenses (before interest and tax)"),
                EX(
                    "A Pune office block earns ₹12 crore a year in rent with ₹2 crore of operating expenses. NOI = "
                    "₹10 crore. At an 8% cap rate, value = 10 ÷ 0.08 = **₹125 crore**."
                ),
                WO(
                    "NOI excludes financing costs (interest) and income tax. Subtracting interest would mix capital "
                    "structure into property value."
                ),
            ),
            topic(
                "Infrastructure",
                L(
                    "**Economic** infrastructure (roads, ports, power, telecom) vs **social** infrastructure "
                    "(schools, hospitals).",
                    "**Greenfield**: build new; higher risk and return. **Brownfield**: buy existing assets with "
                    "operating history; lower risk.",
                    "Long lives, high entry barriers, often regulated or contracted cash flows, monopoly-like "
                    "features.",
                    "Access via direct stakes, unlisted funds, or listed infrastructure companies and funds (InvITs "
                    "in India).",
                ),
                FUN("A toll road is the only business where customers queue up and pay you to make them wait."),
            ),
        ],
        revision=sheet(
            "Value = NOI ÷ Cap rate · NOI excludes interest and tax",
            ("Four quadrants", "Private/public × equity/debt"),
            ("REIT", "Listed, high payout, equity-like volatility"),
            ("Income approach", "Direct cap or DCF"),
            ("Cost approach", "Replacement cost less depreciation"),
            ("Sales comparison", "Recent similar deals"),
            ("Greenfield", "New build: higher risk"),
            ("Brownfield", "Existing asset: lower risk"),
        ),
        questions=[
            q(
                "E",
                "Compared with listed shares, direct real estate is generally:",
                ["More liquid", "Less liquid with higher transaction costs", "Free of valuation issues"],
                1,
                "Property is indivisible, unique and costly to trade.",
                "4.a",
            ),
            q(
                "M",
                "A property has rental income of ₹12 crore and operating expenses of ₹2 crore. At an 8% cap rate its "
                "value is closest to:",
                ["₹125 crore", "₹150 crore", "₹100 crore"],
                0,
                "NOI = 10; 10 ÷ 0.08 = 125.",
                "4.b",
            ),
            q(
                "M",
                "Net operating income for a property excludes:",
                ["Rental income", "Maintenance costs", "Interest expense"],
                2,
                "NOI is before financing costs and income taxes.",
                "4.b",
            ),
            q(
                "E",
                "An investment in commercial mortgage-backed securities is a form of:",
                ["Public real estate debt", "Private real estate equity", "Public real estate equity"],
                0,
                "CMBS are traded securities backed by property loans.",
                "4.a",
            ),
            q(
                "M",
                "The cost approach to property valuation estimates value as:",
                [
                    "NOI divided by cap rate",
                    "Replacement cost of the building plus land, less depreciation",
                    "The average of recent comparable sales",
                ],
                1,
                "It asks what it would cost to rebuild the property today.",
                "4.b",
            ),
            q(
                "M",
                "Compared with direct property, REITs typically offer:",
                ["Lower liquidity", "Smoother reported returns", "Higher liquidity and daily pricing"],
                2,
                "REITs trade on exchanges.",
                "4.b",
            ),
            q(
                "E",
                "Building a new airport from scratch is an example of:",
                ["Brownfield investment", "Greenfield investment", "Social infrastructure only"],
                1,
                "Greenfield means new construction.",
                "4.c",
            ),
            q(
                "H",
                "Compared with greenfield projects, brownfield infrastructure investments typically have:",
                ["Lower risk because of operating history", "Higher construction risk", "No regulatory risk"],
                0,
                "Existing assets have known cash flows and no construction risk.",
                "4.d",
            ),
            q(
                "M",
                "Hospitals and schools are examples of:",
                ["Economic infrastructure", "Social infrastructure", "Timberland"],
                1,
                "Social infrastructure serves community needs.",
                "4.c",
            ),
            q(
                "H",
                "Infrastructure assets are often attractive to pension funds because they offer:",
                [
                    "Short lives and volatile cash flows",
                    "Long-lived, stable and often inflation-linked cash flows",
                    "High liquidity",
                ],
                1,
                "Long, predictable cash flows suit long-term liabilities.",
                "4.d",
            ),
        ],
        flashcards=[
            fc("Real estate quadrants", "Private/public × equity/debt."),
            fc("NOI", "Rent minus operating expenses; before interest and tax."),
            fc("Direct capitalisation", "Value = NOI ÷ cap rate."),
            fc("Three valuation approaches", "Income, cost, sales comparison."),
            fc("Greenfield vs brownfield", "New build (riskier) vs existing asset (safer)."),
            fc("Economic vs social infrastructure", "Roads, ports, power vs schools, hospitals."),
        ],
    )
)

# ---------------------------------------------------------------- LM5
LMS.append(
    dict(
        lm_no=5,
        title="Natural Resources",
        summary="Commodities, farmland and timberland, and the three sources of commodity futures returns.",
        los=[
            ("5.a", "explain", "Explain features of raw land, timberland, farmland and commodities."),
            ("5.b", "explain", "Explain the investment characteristics of natural resources."),
            ("5.c", "describe", "Describe the components of commodity futures returns."),
        ],
        topics=[
            topic(
                "Land, timber and farms",
                L(
                    "**Timberland**: returns from biological growth, timber price changes and land value. Harvests "
                    "can be delayed when prices are low, a built-in option.",
                    "**Farmland**: crops each season plus land value; exposed to weather and crop prices; harvest "
                    "cannot be delayed.",
                    "**Raw land**: no income, a bet on future development or rezoning.",
                ),
                WO(
                    "Timber can be left growing when prices are low; crops cannot. That flexibility makes timberland "
                    "returns less tied to the current commodity price."
                ),
            ),
            topic(
                "Commodities and futures",
                P(
                    "Most investors get commodity exposure through **futures**, ETFs or commodity-producer shares "
                    "rather "
                    "than storing barrels of oil. Categories: energy, metals (industrial, precious), agriculture, "
                    "livestock."
                ),
                L(
                    "**Contango**: futures price > spot. Rolling into a pricier contract gives a **negative roll "
                    "return**.",
                    "**Backwardation**: futures price < spot. Rolling gives a **positive roll return**.",
                ),
                FX("Total futures return = Spot price return + Roll return + Collateral (interest) return"),
                EX(
                    "Gold futures: spot rises 3%, the roll costs 1% because the curve is in contango, and the cash "
                    "collateral earns 5%. Total ≈ 3 − 1 + 5 = **7%**."
                ),
            ),
            topic(
                "Why investors hold natural resources",
                L(
                    "**Inflation hedge**: commodity prices often rise with inflation.",
                    "**Diversification**: low or negative correlation with stocks and bonds at times.",
                    "Risks: price volatility, weather, geopolitics, storage costs, ESG concerns (land use, water).",
                ),
                FUN(
                    "Timberland is the only investment that keeps growing while you sleep, literally. Your mutual "
                    "fund cannot photosynthesise."
                ),
            ),
        ],
        revision=sheet(
            "Futures return = spot return + roll return + collateral return",
            ("Contango", "Futures > spot; negative roll"),
            ("Backwardation", "Futures < spot; positive roll"),
            ("Timberland", "Can delay harvest; growth adds value"),
            ("Farmland", "Harvest fixed; weather risk"),
            ("Raw land", "No income; development option"),
            ("Why hold", "Inflation hedge, diversification"),
        ),
        questions=[
            q(
                "E",
                "A commodity futures market where futures prices are above the spot price is in:",
                ["Backwardation", "Contango", "Equilibrium"],
                1,
                "Contango means futures exceed spot.",
                "5.c",
            ),
            q(
                "M",
                "In backwardation, the roll return for a long futures investor is:",
                ["Positive", "Negative", "Always zero"],
                0,
                "The investor rolls into a cheaper contract that converges up to spot.",
                "5.c",
            ),
            q(
                "M",
                "A commodity futures position has a 3% spot return, a −1% roll return and a 5% collateral return. "
                "The total return is closest to:",
                ["9%", "2%", "7%"],
                2,
                "3 − 1 + 5 = 7%.",
                "5.c",
            ),
            q(
                "E",
                "Which is not a component of commodity futures returns?",
                ["Dividend return", "Roll return", "Collateral return"],
                0,
                "Futures return = spot + roll + collateral; there are no dividends.",
                "5.c",
            ),
            q(
                "M",
                "An advantage of timberland over farmland is that:",
                [
                    "Timber cannot be harvested",
                    "Harvests can be delayed when prices are low",
                    "It produces income every month",
                ],
                1,
                "Trees keep growing, so the owner can wait for better prices.",
                "5.a",
            ),
            q(
                "M",
                "Raw land as an investment mainly offers:",
                ["Regular rental income", "Potential gains from development or rezoning", "Fixed coupons"],
                1,
                "Raw land earns nothing until it is developed or sold.",
                "5.a",
            ),
            q(
                "H",
                "Commodities are often included in portfolios mainly for:",
                ["Steady dividend income", "Their low cost of storage", "Inflation hedging and diversification"],
                2,
                "Commodity prices tend to rise with inflation and move differently from financial assets.",
                "5.b",
            ),
            q(
                "E",
                "Most institutional investors gain commodity exposure through:",
                ["Storing physical goods", "Futures contracts and related funds", "Real estate"],
                1,
                "Futures avoid storage and handling costs.",
                "5.b",
            ),
            q(
                "H",
                "The collateral return on a fully collateralised commodity futures position comes from:",
                ["Interest earned on cash held as margin", "Changes in the spot price", "Rolling contracts"],
                0,
                "Cash backing the position earns the short-term rate.",
                "5.c",
            ),
            q(
                "M",
                "A key risk of farmland that timberland largely avoids is:",
                [
                    "Having to harvest at a fixed time regardless of price",
                    "Exposure to land values",
                    "Long holding periods",
                ],
                0,
                "Crops must be harvested when ripe, so price timing risk is higher.",
                "5.a",
            ),
        ],
        flashcards=[
            fc("Futures return components", "Spot + roll + collateral."),
            fc("Contango", "Futures above spot; roll return negative."),
            fc("Backwardation", "Futures below spot; roll return positive."),
            fc("Timberland advantage", "Harvest can be delayed; trees keep growing."),
            fc("Raw land return source", "Development or rezoning gains; no income."),
            fc("Why add commodities", "Inflation hedge and diversification."),
        ],
    )
)

# ---------------------------------------------------------------- LM6
LMS.append(
    dict(
        lm_no=6,
        title="Hedge Funds",
        summary="Hedge fund strategies, fund terms that limit liquidity, and the risks of investing.",
        los=[
            ("6.a", "explain", "Explain investment characteristics of hedge funds."),
            ("6.b", "explain", "Explain investment forms and vehicles for hedge fund investments."),
            ("6.c", "describe", "Describe hedge fund strategy categories and their risk and return."),
        ],
        topics=[
            topic(
                "What hedge funds are",
                L(
                    "Private, lightly regulated funds that can use **leverage, short selling and derivatives**.",
                    "Aim for **absolute returns** rather than beating an index.",
                    "High fees (management + incentive), high minimum investment, limited transparency.",
                    "**Lock-up** periods, **notice periods** for redemption, **gates** that cap withdrawals, and "
                    "**side pockets** for illiquid holdings.",
                ),
                WO(
                    "A gate limits how much investors can withdraw at once, protecting the remaining investors from "
                    "forced fire sales."
                ),
            ),
            topic(
                "Strategy families",
                T(
                    ["Category", "Examples", "Typical risk"],
                    ["Equity hedge", "Long/short, market neutral, short bias", "Stock-picking, some market beta"],
                    ["Event-driven", "Merger arbitrage, distressed securities, activism", "Deal failure, credit"],
                    ["Relative value", "Fixed-income arbitrage, convertible arbitrage", "Leverage, liquidity, spreads"],
                    ["Opportunistic", "Global macro, managed futures (CTAs)", "Directional macro bets"],
                    ["Multi-manager", "Multi-strategy, fund of funds", "Extra fee layer (FoF)"],
                ),
                EX(
                    "Merger arbitrage: Tara Pharma bids ₹500 a share for Lotus Labs, which trades at ₹470. The "
                    "manager buys Lotus at ₹470. If the deal closes, the gain is 30 ÷ 470 ≈ **6.4%**. If it fails, "
                    "Lotus may fall back to ₹400. Small, steady gains with occasional large losses."
                ),
            ),
            topic(
                "Ways to invest",
                L(
                    "**Master–feeder** structure: onshore and offshore feeders invest in one master fund.",
                    "**Fund of funds**: diversified and gives access to closed managers, but adds a second layer of "
                    "fees.",
                    "**Separately managed accounts**: transparency and control, but higher minimums.",
                    "**Liquid alternatives**: regulated mutual-fund versions with daily liquidity and limits on "
                    "leverage.",
                ),
                FUN(
                    "A 'market-neutral' fund in a crash is like a 'waterproof' phone in the sea. The label is true "
                    "right up until it isn't."
                ),
            ),
        ],
        revision=sheet(
            "Merger arb gain = (offer price − current price) ÷ current price, if the deal closes",
            ("Equity hedge", "Long/short stock picking"),
            ("Event-driven", "Mergers, distress, activism"),
            ("Relative value", "Mispricings between related securities"),
            ("Opportunistic", "Global macro, managed futures"),
            ("Fund of funds", "Diversified, double fees"),
            ("Lock-up / gate", "Limits on when and how much you can redeem"),
            ("Side pocket", "Illiquid assets ring-fenced"),
        ),
        questions=[
            q(
                "E",
                "A hedge fund charging '2 and 20' takes:",
                ["2% of profits and 20% of assets", "2% of assets and 20% of profits", "20% of assets only"],
                1,
                "2% management fee on assets and a 20% incentive fee on profits.",
                "6.a",
            ),
            q(
                "M",
                "A redemption gate in a hedge fund:",
                [
                    "Limits the amount investors can withdraw in a period",
                    "Guarantees daily liquidity",
                    "Charges a fee on new subscriptions",
                ],
                0,
                "Gates protect the fund from forced selling.",
                "6.a",
            ),
            q(
                "M",
                "Merger arbitrage is part of which strategy category?",
                ["Relative value", "Event-driven", "Opportunistic"],
                1,
                "It profits from corporate events.",
                "6.c",
            ),
            q(
                "M",
                "An acquirer offers ₹500 a share for a target trading at ₹470. A merger arbitrageur's gain if the deal "
                "closes is closest to:",
                ["6.4%", "3.0%", "6.0%"],
                0,
                "30 ÷ 470 = 6.4%.",
                "6.c",
            ),
            q(
                "E",
                "A fund that takes directional bets on interest rates, currencies and indices based on economic views "
                "follows:",
                ["Global macro", "Convertible arbitrage", "Equity market neutral"],
                0,
                "Global macro is an opportunistic strategy.",
                "6.c",
            ),
            q(
                "M",
                "The main drawback of a fund of hedge funds is:",
                ["No diversification", "An extra layer of fees", "Too much transparency"],
                1,
                "FoFs charge their own fees on top of the underlying funds' fees.",
                "6.b",
            ),
            q(
                "H",
                "Convertible arbitrage typically involves:",
                [
                    "Buying a convertible bond and shorting the issuer's stock",
                    "Buying both the bond and the stock",
                    "Shorting government bonds only",
                ],
                0,
                "The manager hedges the equity exposure of an underpriced convertible.",
                "6.c",
            ),
            q(
                "M",
                "Separately managed accounts offer investors:",
                ["Lower minimums than funds", "Greater transparency and control", "Exemption from fees"],
                1,
                "Assets sit in the investor's own account.",
                "6.b",
            ),
            q(
                "H",
                "Which statement about liquid alternative funds is most accurate?",
                [
                    "They have unlimited leverage",
                    "They offer daily liquidity but face limits on leverage and illiquid holdings",
                    "They are only for institutions",
                ],
                1,
                "Regulated vehicles trade off flexibility for liquidity.",
                "6.b",
            ),
            q(
                "E",
                "A side pocket is used to:",
                ["Hold the manager's fees", "Separate illiquid investments from the main fund", "Pay the hurdle rate"],
                1,
                "Illiquid assets are ring-fenced until they can be realised.",
                "6.a",
            ),
        ],
        flashcards=[
            fc("Hedge fund aim", "Absolute returns using leverage, shorts and derivatives."),
            fc("Five strategy families", "Equity hedge, event-driven, relative value, opportunistic, multi-manager."),
            fc("Merger arbitrage", "Buy target below the offer; risk is deal failure."),
            fc("Gate", "Cap on withdrawals in a period."),
            fc("Fund of funds", "Diversified access, but double fees."),
            fc("Master–feeder", "Onshore and offshore feeders invest in one master fund."),
        ],
    )
)

# ---------------------------------------------------------------- LM7
LMS.append(
    dict(
        lm_no=7,
        title="Introduction to Digital Assets",
        summary="Blockchain basics, types of digital assets, and how investors gain exposure.",
        los=[
            ("7.a", "describe", "Describe financial applications of distributed ledger technology."),
            ("7.b", "explain", "Explain how digital assets differ from traditional assets."),
            ("7.c", "describe", "Describe different types of digital assets."),
            ("7.d", "describe", "Describe investment forms and vehicles for digital assets."),
        ],
        topics=[
            topic(
                "Distributed ledgers and blockchain",
                P(
                    "A **distributed ledger** is a database shared across many computers (nodes). A **blockchain** "
                    "groups transactions into blocks linked by cryptographic hashes, so changing history is extremely "
                    "hard."
                ),
                L(
                    "**Permissionless** (public, anyone can join, e.g. Bitcoin) vs **permissioned** (only approved "
                    "nodes, used by banks).",
                    "**Consensus**: **proof of work** (miners spend energy solving puzzles) vs **proof of stake** "
                    "(validators lock up coins; far less energy).",
                    "Uses: payments, settlement, tokenisation of real assets, smart contracts.",
                ),
                WO("Proof of stake is the energy-efficient method; proof of work is the energy-hungry one."),
            ),
            topic(
                "Types of digital assets",
                T(
                    ["Type", "What it is"],
                    ["Cryptocurrency", "Native coin of a blockchain, e.g. Bitcoin, Ether"],
                    ["Stablecoin", "Token pegged to a fiat currency or asset, backed by reserves or algorithms"],
                    ["Utility token", "Gives access to a platform's service"],
                    ["Security token", "Represents ownership or a claim; regulated like securities"],
                    ["NFT", "Unique, non-interchangeable token for one item"],
                    ["CBDC", "Digital currency issued by a central bank, e.g. the e-rupee"],
                ),
                P(
                    "**DeFi** (decentralised finance) runs lending, trading and exchange through smart contracts "
                    "without traditional intermediaries."
                ),
            ),
            topic(
                "Investing in digital assets",
                L(
                    "**Direct**: buy and hold in a wallet, via an exchange. Custody and key loss are real risks.",
                    "**Indirect**: exchange-traded products, futures, trusts, and shares of crypto-related companies.",
                    "Characteristics: no cash flows for most coins (value rests on adoption and scarcity), extreme "
                    "volatility, evolving regulation, fraud and hacking risk, 24/7 trading.",
                ),
                FUN(
                    "Losing your private key is like losing the only key to a bank locker that also has no bank, no "
                    "manager, and no complaints desk."
                ),
            ),
        ],
        revision=sheet(
            "No cash flows → value depends on adoption, scarcity and trust in the network",
            ("Blockchain", "Hash-linked blocks on a distributed ledger"),
            ("Permissionless vs permissioned", "Open to all vs approved nodes"),
            ("PoW vs PoS", "Energy-heavy mining vs staked validators"),
            ("Stablecoin", "Pegged to fiat or assets"),
            ("Security token", "Ownership claim; regulated"),
            ("NFT", "Unique, non-fungible token"),
            ("Indirect access", "ETPs, futures, crypto-company shares"),
        ),
        questions=[
            q(
                "E",
                "A blockchain that anyone can join and validate transactions on is:",
                ["Permissioned", "Permissionless", "Centralised"],
                1,
                "Public blockchains are open to all.",
                "7.a",
            ),
            q(
                "M",
                "Compared with proof of work, proof of stake:",
                ["Uses much less energy", "Requires more mining hardware", "Has no validators"],
                0,
                "Validators stake coins instead of solving energy-intensive puzzles.",
                "7.a",
            ),
            q(
                "E",
                "A token pegged to the value of the US dollar is a:",
                ["Utility token", "Non-fungible token", "Stablecoin"],
                2,
                "Stablecoins aim to hold a fixed value.",
                "7.c",
            ),
            q(
                "M",
                "A token that represents a share of ownership in a real estate project is best classified as a:",
                ["Security token", "Utility token", "Cryptocurrency"],
                0,
                "Ownership claims are securities and regulated as such.",
                "7.c",
            ),
            q(
                "M",
                "A key way most cryptocurrencies differ from shares and bonds is that they:",
                [
                    "Pay regular coupons",
                    "Generate no cash flows, so value depends on adoption and demand",
                    "Are issued by companies",
                ],
                1,
                "Without cash flows, fundamental valuation is difficult.",
                "7.b",
            ),
            q(
                "E",
                "An NFT is:",
                [
                    "A unique token that cannot be exchanged one-for-one with another",
                    "A government bond",
                    "A coin backed by gold",
                ],
                0,
                "Non-fungible means each token is distinct.",
                "7.c",
            ),
            q(
                "M",
                "Decentralised finance (DeFi) refers to:",
                [
                    "Central bank digital currencies",
                    "Financial services run through smart contracts without traditional intermediaries",
                    "Bank-issued credit cards",
                ],
                1,
                "DeFi replaces intermediaries with code.",
                "7.a",
            ),
            q(
                "H",
                "An investor who wants bitcoin exposure without managing private keys would most likely use:",
                [
                    "A hardware wallet",
                    "Direct purchase on a peer-to-peer network",
                    "An exchange-traded product or futures",
                ],
                2,
                "Indirect vehicles avoid self-custody.",
                "7.d",
            ),
            q(
                "H",
                "Which is a risk particular to holding digital assets directly?",
                ["Loss of private keys or exchange hacks", "Coupon reinvestment risk", "Prepayment risk"],
                0,
                "Lost keys mean lost assets, with no recourse.",
                "7.d",
            ),
            q(
                "M",
                "A digital currency issued by a country's central bank is a:",
                ["Stablecoin", "CBDC", "Utility token"],
                1,
                "Central bank digital currency, such as the e-rupee.",
                "7.c",
            ),
        ],
        flashcards=[
            fc("Blockchain", "Distributed ledger of hash-linked blocks."),
            fc("PoW vs PoS", "Mining with energy vs validators staking coins."),
            fc("Stablecoin", "Token pegged to fiat or another asset."),
            fc("Security vs utility token", "Ownership claim vs access to a service."),
            fc("NFT", "Unique, non-interchangeable token."),
            fc("Digital asset risks", "Volatility, key loss, hacks, fraud, regulation."),
        ],
    )
)


if __name__ == "__main__":
    # Prototype questions: real estate liquidity is LM4; '2 and 20' is fees (LM1); PE features LM3.
    write_pack("ai", "Alternative Investments", LMS, {"55": 4, "56": 1, "57": 3}, balance_keys=True)
