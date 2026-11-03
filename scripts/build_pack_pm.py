"""Portfolio Management content pack.  python scripts/build_pack_pm.py, then re-seed."""

from packlib import EX, FUN, FX, OL, WO, L, P, T, fc, q, sheet, topic, write_pack

LMS = []

# ---------------------------------------------------------------- LM1
LMS.append(
    dict(
        lm_no=1,
        title="Portfolio Risk and Return: Part I",
        summary="Return and risk of assets and portfolios, correlation, risk aversion and the optimal portfolio.",
        los=[
            ("1.a", "describe", "Describe characteristics of the major asset classes that investors consider."),
            ("1.b", "calculate", "Calculate and interpret the mean, variance and covariance of a two-asset portfolio."),
            ("1.c", "explain", "Explain risk aversion and its implications for portfolio selection, and use utility."),
            ("1.d", "describe", "Describe the minimum-variance and efficient frontiers and the optimal portfolio."),
        ],
        topics=[
            topic(
                "Return and risk of a portfolio",
                P(
                    "Historically, riskier asset classes have earned higher average returns: small-cap shares > "
                    "large-cap "
                    "shares > corporate bonds > government bonds > T-bills, with volatility in the same order."
                ),
                FX("E(R_p) = w₁E(R₁) + w₂E(R₂) · σ²_p = w₁²σ₁² + w₂²σ₂² + 2w₁w₂ρ₁₂σ₁σ₂"),
                EX(
                    "60% in shares (E = 12%, σ = 20%) and 40% in bonds (E = 7%, σ = 10%), correlation 0.2. "
                    "E(R_p) = 0.6 × 12 + 0.4 × 7 = 10%. σ²_p = 0.36 × 0.04 + 0.16 × 0.01 + 2 × 0.6 × 0.4 × 0.2 × 0.2 × "
                    "0.1 = 0.01792, so σ_p = **13.4%**, less than the 16% weighted average."
                ),
                WO(
                    "Portfolio risk falls below the weighted-average risk whenever **ρ < 1**. With ρ = −1, a "
                    "zero-risk portfolio is possible."
                ),
            ),
            topic(
                "Risk aversion and utility",
                FX("U = E(r) − ½ A σ²   (A > 0 risk-averse, A = 0 risk-neutral, A < 0 risk-seeking)"),
                EX(
                    "A portfolio offers E(r) = 10% and σ = 20%. For an investor with A = 4, U = 0.10 − 0.5 × 4 × 0.04 "
                    "= "
                    "**0.02** (2%). A T-bill yielding 3% gives U = 0.03, so this investor prefers the T-bill."
                ),
                P(
                    "**Indifference curves** join portfolios with equal utility. More risk-averse investors have "
                    "steeper "
                    "curves."
                ),
            ),
            topic(
                "Efficient frontier and optimal portfolio",
                L(
                    "The **minimum-variance frontier** shows the lowest risk for each expected return.",
                    "The **global minimum-variance portfolio** is its leftmost point.",
                    "The **efficient frontier** is the part above it: no other portfolio gives more return for the "
                    "same "
                    "risk.",
                    "Adding a risk-free asset creates the **capital allocation line (CAL)**; the **optimal risky "
                    "portfolio** is where the CAL is tangent to the frontier.",
                    "Each investor's **optimal portfolio** is where their highest indifference curve touches the CAL.",
                ),
                FUN(
                    "The efficient frontier is the thali menu at a good restaurant: for every price, there is one "
                    "dish that is simply the most food. Everything below the line is a waste of money."
                ),
            ),
        ],
        revision=sheet(
            "σ²_p = w₁²σ₁² + w₂²σ₂² + 2w₁w₂ρσ₁σ₂ · U = E(r) − ½Aσ²",
            ("Diversification", "Risk falls when ρ < 1"),
            ("ρ = −1", "A riskless combination is possible"),
            ("Risk aversion A", "Higher A = steeper indifference curves"),
            ("Global min-variance", "Leftmost point on the frontier"),
            ("Efficient frontier", "Best return for each risk level"),
            ("Optimal portfolio", "Tangency of indifference curve and CAL"),
        ),
        questions=[
            q(
                "E",
                "A portfolio has 60% in an asset returning 10% and 40% in one returning 5%. Its expected return is:",
                ["7.5%", "8.0%", "9.0%"],
                1,
                "0.6 × 10 + 0.4 × 5 = 8%.",
                "1.b",
            ),
            q(
                "M",
                "Portfolio risk is lower than the weighted average of asset risks whenever the correlation is:",
                ["Less than +1", "Exactly +1", "Greater than +1"],
                0,
                "Any correlation below +1 gives diversification.",
                "1.b",
            ),
            q(
                "H",
                "60% shares (σ = 20%) and 40% bonds (σ = 10%), correlation 0.2. The portfolio standard deviation is "
                "closest to:",
                ["16.0%", "13.4%", "12.0%"],
                1,
                "Variance 0.01792 → σ = 13.4%.",
                "1.b",
            ),
            q(
                "M",
                "An investor with A = 4 evaluates a portfolio with E(r) = 10% and σ = 20%. Utility is:",
                ["2%", "6%", "10%"],
                0,
                "0.10 − 0.5 × 4 × 0.04 = 0.02.",
                "1.c",
            ),
            q(
                "E",
                "A risk-neutral investor has a risk-aversion coefficient of:",
                ["Greater than zero", "Zero", "Less than zero"],
                1,
                "A = 0 means risk does not affect utility.",
                "1.c",
            ),
            q(
                "M",
                "Compared with a less risk-averse investor, a more risk-averse investor's indifference curves are:",
                ["Flatter", "Steeper", "Identical"],
                1,
                "They need more return per unit of extra risk.",
                "1.c",
            ),
            q(
                "M",
                "The portion of the minimum-variance frontier above the global minimum-variance portfolio is the:",
                ["Capital market line", "Security market line", "Efficient frontier"],
                2,
                "Only these portfolios are efficient.",
                "1.d",
            ),
            q(
                "H",
                "An investor's optimal portfolio lies where:",
                [
                    "The investor's highest indifference curve is tangent to the capital allocation line",
                    "The efficient frontier meets the y-axis",
                    "Utility is zero",
                ],
                0,
                "That point maximises the investor's utility.",
                "1.d",
            ),
            q(
                "E",
                "Historically, which asset class has had the highest average return and volatility?",
                ["Small-cap equities", "Government bonds", "Treasury bills"],
                0,
                "Higher risk has been rewarded with higher average returns.",
                "1.a",
            ),
            q(
                "H",
                "With two assets perfectly negatively correlated (ρ = −1), it is possible to:",
                ["Create a portfolio with zero risk", "Eliminate all return", "Only increase risk"],
                0,
                "The right weights cancel all variance.",
                "1.b",
            ),
        ],
        flashcards=[
            fc("Two-asset portfolio variance", "w₁²σ₁² + w₂²σ₂² + 2w₁w₂ρσ₁σ₂."),
            fc("Utility formula", "U = E(r) − ½Aσ²."),
            fc("When does diversification help?", "Whenever correlation is below +1."),
            fc("Global minimum-variance portfolio", "Lowest-risk portfolio on the frontier."),
            fc("Efficient frontier", "Highest return for each level of risk."),
            fc("Investor's optimal portfolio", "Highest indifference curve tangent to the CAL."),
        ],
    )
)

# ---------------------------------------------------------------- LM2
LMS.append(
    dict(
        lm_no=2,
        title="Portfolio Risk and Return: Part II",
        summary="The capital market line, systematic risk, beta, CAPM and performance measures.",
        los=[
            (
                "2.a",
                "describe",
                "Describe the implications of combining a risk-free asset with the market portfolio "
                "(the capital market line).",
            ),
            ("2.b", "explain", "Explain systematic and nonsystematic risk and why only systematic risk is priced."),
            ("2.c", "calculate", "Calculate and interpret beta and the CAPM expected return."),
            ("2.d", "calculate", "Calculate and interpret the Sharpe ratio, Treynor ratio, M² and Jensen's alpha."),
        ],
        topics=[
            topic(
                "CML and systematic risk",
                P(
                    "If everyone holds the same expectations, the optimal risky portfolio is the **market portfolio**, "
                    "and the CAL becomes the **capital market line (CML)**: E(R_p) = R_f + [(E(R_m) − R_f)/σ_m] × σ_p."
                ),
                L(
                    "**Systematic (market) risk**: from economy-wide factors; cannot be diversified away.",
                    "**Nonsystematic (company-specific) risk**: can be diversified away, so it earns **no** extra "
                    "return.",
                    "Total risk = systematic + nonsystematic.",
                ),
                WO(
                    "Lending at R_f puts you left of the market portfolio on the CML; borrowing (leverage) puts you to "
                    "the "
                    "right."
                ),
            ),
            topic(
                "Beta and CAPM",
                FX("β_i = Cov(R_i, R_m) ÷ σ²_m = ρ_im σ_i ÷ σ_m · E(R_i) = R_f + β_i[E(R_m) − R_f]"),
                EX(
                    "R_f = 6%, E(R_m) = 12%, β = 1.2. E(R) = 6 + 1.2 × 6 = **13.2%**. If analysts forecast 14%, the "
                    "share plots **above** the SML: undervalued."
                ),
                P(
                    "The **security market line (SML)** plots expected return against beta. Every correctly priced "
                    "asset "
                    "lies on it."
                ),
            ),
            topic(
                "Performance measures",
                T(
                    ["Measure", "Formula", "Risk used"],
                    ["Sharpe ratio", "(R_p − R_f) ÷ σ_p", "Total"],
                    ["Treynor ratio", "(R_p − R_f) ÷ β_p", "Systematic"],
                    ["M²", "(R_p − R_f) × σ_m/σ_p − (R_m − R_f)", "Total, in % terms"],
                    ["Jensen's alpha", "R_p − [R_f + β_p(R_m − R_f)]", "Systematic"],
                ),
                EX(
                    "Fund return 14%, σ = 20%, β = 1.2; R_f = 6%, market 12%, σ_m = 18%. Sharpe = 8/20 = 0.40. Treynor "
                    "= 8/1.2 = 6.67. M² = 0.40 × 18 − 6 = **1.2%**. Alpha = 14 − 13.2 = **0.8%**."
                ),
                FUN(
                    "Beta is how loudly a stock screams when the market stubs its toe. β = 2 screams twice as loud; "
                    "β = 0.5 just says 'ouch'."
                ),
            ),
        ],
        revision=sheet(
            "CAPM: E(R) = R_f + β[E(R_m) − R_f] · β = ρσ_i/σ_m",
            ("CML", "Efficient portfolios, total risk (σ)"),
            ("SML", "All assets, systematic risk (β)"),
            ("Priced risk", "Only systematic"),
            ("Sharpe", "Excess return per σ"),
            ("Treynor", "Excess return per β"),
            ("M²", "Sharpe expressed as % vs market"),
            ("Jensen's alpha", "Actual − CAPM return"),
        ),
        questions=[
            q(
                "E",
                "Diversification mainly reduces:",
                ["Systematic risk", "Nonsystematic risk", "Interest rate risk only"],
                1,
                "Company-specific risk can be diversified away.",
                "2.b",
            ),
            q(
                "M",
                "R_f = 6%, E(R_m) = 12% and β = 1.2. The CAPM expected return is:",
                ["13.2%", "14.4%", "12.0%"],
                0,
                "6 + 1.2 × 6 = 13.2%.",
                "2.c",
            ),
            q(
                "M",
                "A stock's correlation with the market is 0.6, its σ is 30% and the market σ is 20%. Its beta is:",
                ["0.40", "0.90", "1.50"],
                1,
                "0.6 × 30/20 = 0.9.",
                "2.c",
            ),
            q(
                "H",
                "A share's forecast return is 14% and its CAPM required return is 13.2%. The share is:",
                ["Overvalued", "Fairly valued", "Undervalued"],
                2,
                "It plots above the SML.",
                "2.c",
            ),
            q(
                "M",
                "A fund earns 14% with σ = 20% when R_f = 6%. Its Sharpe ratio is:",
                ["0.40", "0.70", "0.30"],
                0,
                "(14 − 6)/20 = 0.40.",
                "2.d",
            ),
            q(
                "M",
                "Which measure uses beta as the risk measure?",
                ["Sharpe ratio", "M²", "Treynor ratio"],
                2,
                "Treynor divides excess return by beta.",
                "2.d",
            ),
            q(
                "H",
                "Fund return 14%, β = 1.2, R_f = 6%, market return 12%. Jensen's alpha is:",
                ["0.8%", "2.0%", "−0.8%"],
                0,
                "14 − (6 + 1.2 × 6) = 0.8%.",
                "2.d",
            ),
            q(
                "E",
                "The capital market line plots expected return against:",
                ["Beta", "Total risk (standard deviation)", "Correlation"],
                1,
                "The CML uses σ.",
                "2.a",
            ),
            q(
                "M",
                "A portfolio on the CML to the right of the market portfolio is created by:",
                [
                    "Lending at the risk-free rate",
                    "Borrowing at the risk-free rate to buy more of the market",
                    "Holding only T-bills",
                ],
                1,
                "Leverage moves the investor beyond the market portfolio.",
                "2.a",
            ),
            q(
                "H",
                "Why does CAPM reward only systematic risk?",
                [
                    "Investors can diversify away nonsystematic risk at no cost",
                    "Nonsystematic risk is always zero",
                    "Systematic risk is easy to diversify",
                ],
                0,
                "No reward is paid for risk that can be removed.",
                "2.b",
            ),
        ],
        flashcards=[
            fc("CAPM", "E(R) = R_f + β[E(R_m) − R_f]."),
            fc("Beta", "Cov(R_i, R_m)/σ²_m = ρσ_i/σ_m."),
            fc("CML vs SML", "CML: efficient portfolios vs σ. SML: all assets vs β."),
            fc("Sharpe vs Treynor", "Excess return per σ vs per β."),
            fc("Jensen's alpha", "Actual return − CAPM return."),
            fc("Which risk is priced?", "Only systematic (market) risk."),
        ],
    )
)

# ---------------------------------------------------------------- LM3
LMS.append(
    dict(
        lm_no=3,
        title="Portfolio Management: An Overview",
        summary="The portfolio approach, the management process, types of investors and pooled products.",
        los=[
            ("3.a", "describe", "Describe the portfolio approach to investing."),
            ("3.b", "describe", "Describe the steps in the portfolio management process."),
            ("3.c", "describe", "Describe types of investors and distinctive characteristics and needs of each."),
            ("3.d", "describe", "Describe mutual funds and compare them with other pooled investment products."),
        ],
        topics=[
            topic(
                "The portfolio approach and process",
                P(
                    "Judge each investment by its effect on the **whole portfolio**, not in isolation. Diversification "
                    "lowers risk without necessarily lowering expected return; the **diversification ratio** = "
                    "portfolio risk ÷ average risk of the holdings."
                ),
                OL(
                    "**Planning**: understand the client, write the **investment policy statement (IPS)**, form "
                    "capital "
                    "market expectations.",
                    "**Execution**: asset allocation, security selection, portfolio construction and trading.",
                    "**Feedback**: monitor and rebalance; measure and report performance.",
                ),
                WO("The IPS comes first, before any security is chosen."),
            ),
            topic(
                "Types of investors",
                T(
                    ["Investor", "Horizon", "Risk tolerance", "Liquidity needs"],
                    ["Individual", "Varies", "Varies", "Varies"],
                    ["Defined benefit pension", "Long", "High", "Low"],
                    ["Endowment / foundation", "Very long", "High", "Low"],
                    ["Bank", "Short", "Low", "High"],
                    ["Insurer", "Short (P&C) to long (life)", "Low", "High"],
                    ["Sovereign wealth fund", "Long", "High", "Low"],
                ),
                P(
                    "In a **defined benefit** plan the employer promises a pension and bears investment risk. In a "
                    "**defined contribution** plan the employer contributes; the employee bears the risk."
                ),
            ),
            topic(
                "Pooled products",
                L(
                    "**Open-end mutual fund**: units issued and redeemed at NAV daily.",
                    "**Closed-end fund**: fixed number of units that trade on an exchange, often at a discount or "
                    "premium to NAV.",
                    "**ETF**: trades on an exchange like a share, usually tracks an index, low cost; creation and "
                    "redemption by authorised participants keeps price near NAV.",
                    "**Separately managed account**: investor owns the securities directly; tailored, higher minimum.",
                    "**Hedge funds and private equity**: less regulated, high fees, limited liquidity.",
                ),
                FUN(
                    "A mutual fund is a shared auto-rickshaw: everyone pays a fraction of the fare and goes the same "
                    "way. "
                    "A separately managed account is your own car with a driver."
                ),
            ),
        ],
        revision=sheet(
            "Process: Planning (IPS) → Execution → Feedback",
            ("Portfolio approach", "Judge each asset by its effect on the whole"),
            ("DB plan", "Employer bears risk"),
            ("DC plan", "Employee bears risk"),
            ("Bank", "Short horizon, low risk, high liquidity"),
            ("Endowment", "Very long horizon, high risk tolerance"),
            ("Open-end vs closed-end", "Redeem at NAV vs trade on exchange"),
            ("ETF", "Exchange-traded, low cost, near NAV"),
        ),
        questions=[
            q(
                "E",
                "The first step in the portfolio management process is:",
                ["Security selection", "Planning, including writing the IPS", "Performance measurement"],
                1,
                "Planning starts with understanding the client and the IPS.",
                "3.b",
            ),
            q(
                "M",
                "In a defined benefit pension plan, investment risk is borne by:",
                ["The employee", "The employer (plan sponsor)", "The government"],
                1,
                "The sponsor must meet promised benefits.",
                "3.c",
            ),
            q(
                "M",
                "Which investor typically has the shortest horizon and the highest liquidity needs?",
                ["University endowment", "Bank", "Sovereign wealth fund"],
                1,
                "Banks must meet deposit withdrawals.",
                "3.c",
            ),
            q(
                "E",
                "An open-end mutual fund:",
                ["Has a fixed number of units", "Issues and redeems units at NAV", "Trades only at a discount"],
                1,
                "Investors buy from and sell to the fund at NAV.",
                "3.d",
            ),
            q(
                "M",
                "A closed-end fund's units:",
                ["Trade on an exchange and may differ from NAV", "Are redeemed by the fund daily", "Must trade at NAV"],
                0,
                "Supply and demand set the price.",
                "3.d",
            ),
            q(
                "H",
                "Which feature keeps an ETF's price close to its NAV?",
                [
                    "Daily redemption by retail investors",
                    "Creation and redemption by authorised participants",
                    "A fixed price set by the regulator",
                ],
                1,
                "APs arbitrage away price gaps.",
                "3.d",
            ),
            q(
                "M",
                "The portfolio approach to investing means:",
                [
                    "Judging each security in isolation",
                    "Evaluating investments by their effect on the overall portfolio",
                    "Holding only one asset",
                ],
                1,
                "Correlation matters as much as individual risk.",
                "3.a",
            ),
            q(
                "E",
                "Rebalancing and performance reporting belong to which step of the process?",
                ["Planning", "Execution", "Feedback"],
                2,
                "Feedback monitors and reports.",
                "3.b",
            ),
            q(
                "M",
                "University endowments typically have:",
                [
                    "Very long horizons and high risk tolerance",
                    "Short horizons and low risk tolerance",
                    "High liquidity needs",
                ],
                0,
                "They aim to support the institution in perpetuity.",
                "3.c",
            ),
            q(
                "H",
                "Compared with a mutual fund, a separately managed account offers:",
                [
                    "Lower minimum investment",
                    "Direct ownership of securities and tailoring",
                    "Exchange trading of units",
                ],
                1,
                "The investor owns the holdings in their own account.",
                "3.d",
            ),
        ],
        flashcards=[
            fc("Portfolio process", "Planning (IPS) → Execution → Feedback."),
            fc("DB vs DC plan risk", "DB: employer bears. DC: employee bears."),
            fc("Bank profile", "Short horizon, low risk tolerance, high liquidity."),
            fc("Endowment profile", "Very long horizon, high risk tolerance."),
            fc("Open-end vs closed-end fund", "Redeem at NAV vs trade on exchange (premium/discount)."),
            fc("ETF price stays near NAV because", "Authorised participants create and redeem units."),
        ],
    )
)

# ---------------------------------------------------------------- LM4
LMS.append(
    dict(
        lm_no=4,
        title="Basics of Portfolio Planning and Construction",
        summary="The IPS, risk and return objectives, constraints, asset allocation and ESG integration.",
        los=[
            ("4.a", "describe", "Describe the reasons for a written IPS and its major components."),
            (
                "4.b",
                "describe",
                "Describe risk and return objectives and constraints, and distinguish willingness "
                "from ability to take risk.",
            ),
            ("4.c", "explain", "Explain the specification of asset classes and strategic asset allocation."),
            ("4.d", "describe", "Describe how ESG considerations may be integrated into portfolio planning."),
        ],
        topics=[
            topic(
                "The investment policy statement",
                P(
                    "An IPS records the client's goals, risk and constraints, the manager's duties, the benchmark and "
                    "the review process. It keeps decisions consistent and protects both client and manager."
                ),
                L(
                    "**Return objective**: absolute or relative, stated as a required return.",
                    "**Risk objective**: **ability** (horizon, wealth, liabilities) and **willingness** "
                    "(psychology). If they conflict, usually adopt the **lower**.",
                    "**Constraints**: **liquidity, time horizon, tax, legal and regulatory, unique circumstances**.",
                ),
                EX(
                    "Sunita, 35, earns well and has a 30-year horizon: high ability. She panicked and sold everything "
                    "in the last crash: low willingness. The adviser should set a **moderate** risk tolerance, and "
                    "educate her over time."
                ),
                WO(
                    "Unique circumstances include religious or ethical restrictions, such as avoiding alcohol or "
                    "tobacco companies."
                ),
            ),
            topic(
                "Strategic asset allocation",
                L(
                    "Asset classes should be **internally similar** and **not highly correlated** with each other, "
                    "and together should cover most investable assets.",
                    "**Strategic asset allocation** sets long-term target weights from the IPS and capital market "
                    "expectations.",
                    "**Tactical** allocation makes short-term deviations to exploit views.",
                    "Rebalancing policies keep weights within corridors such as ±5%.",
                ),
                FUN(
                    "Strategic allocation is your diet plan. Tactical allocation is deciding that today is a "
                    "samosa day."
                ),
            ),
            topic(
                "ESG integration",
                T(
                    ["Approach", "What it means"],
                    ["Negative screening", "Exclude sectors or companies (tobacco, weapons)"],
                    ["Positive / best-in-class", "Choose the best ESG performers in each sector"],
                    ["ESG integration", "Include ESG factors in financial analysis"],
                    ["Thematic investing", "Target themes such as clean energy or water"],
                    ["Impact investing", "Seek measurable social or environmental impact plus a return"],
                    ["Engagement / stewardship", "Use shareholder rights to influence companies"],
                ),
            ),
        ],
        revision=sheet(
            "Constraints: Liquidity · Time horizon · Tax · Legal/regulatory · Unique (LTTLU)",
            ("IPS purpose", "Consistent decisions; guidance for manager and client"),
            ("Ability vs willingness", "If they conflict, use the lower"),
            ("Strategic allocation", "Long-term targets"),
            ("Tactical allocation", "Short-term deviations"),
            ("Good asset class", "Similar inside, low correlation outside"),
            ("Negative screening", "Exclude"),
            ("Impact investing", "Measurable impact + return"),
        ),
        questions=[
            q(
                "E",
                "An investment policy statement should include the client's:",
                ["Favourite stocks", "Return objectives, risk tolerance and constraints", "Credit card limits"],
                1,
                "The IPS documents objectives and constraints.",
                "4.a",
            ),
            q(
                "M",
                "A young investor with a long horizon is very nervous about losses. Her risk tolerance should "
                "generally be set:",
                [
                    "At the higher, ability level",
                    "At the lower, willingness level, with education over time",
                    "At zero",
                ],
                1,
                "When ability and willingness conflict, the more conservative usually prevails.",
                "4.b",
            ),
            q(
                "E",
                "Which is a constraint in an IPS?",
                ["Liquidity needs", "Required return", "Risk aversion"],
                0,
                "Constraints are liquidity, horizon, tax, legal and unique circumstances.",
                "4.b",
            ),
            q(
                "M",
                "Which factor relates to an investor's ability (not willingness) to take risk?",
                ["Anxiety about losses", "A long time horizon and large wealth", "Past regret"],
                1,
                "Ability is objective; willingness is psychological.",
                "4.b",
            ),
            q(
                "M",
                "Strategic asset allocation is:",
                [
                    "Short-term bets on market moves",
                    "Long-term target weights set from the IPS",
                    "Picking individual stocks",
                ],
                1,
                "It is the long-run policy mix.",
                "4.c",
            ),
            q(
                "H",
                "Asset classes used for allocation should ideally be:",
                [
                    "Highly correlated with each other",
                    "Internally similar with low correlation between classes",
                    "Limited to one market",
                ],
                1,
                "This gives distinct risk-return behaviour for diversification.",
                "4.c",
            ),
            q(
                "E",
                "Excluding tobacco and weapons makers from a portfolio is:",
                ["Negative screening", "Thematic investing", "Engagement"],
                0,
                "It screens out sectors.",
                "4.d",
            ),
            q(
                "M",
                "Investing to achieve a measurable social outcome as well as a financial return is:",
                ["Best-in-class", "Impact investing", "Tactical allocation"],
                1,
                "Impact investing targets measurable outcomes.",
                "4.d",
            ),
            q(
                "H",
                "A client's religious ban on interest-bearing investments is an example of:",
                ["A tax constraint", "A unique circumstance", "A liquidity constraint"],
                1,
                "Ethical or religious preferences are unique circumstances.",
                "4.b",
            ),
            q(
                "M",
                "Using shareholder votes and dialogue to change a company's practices is:",
                ["Engagement or stewardship", "Negative screening", "Thematic investing"],
                0,
                "Active ownership aims to improve company behaviour.",
                "4.d",
            ),
        ],
        flashcards=[
            fc("IPS components", "Objectives (return, risk) and constraints."),
            fc("IPS constraints", "Liquidity, time horizon, tax, legal/regulatory, unique."),
            fc("Ability vs willingness conflict", "Usually adopt the lower; educate the client."),
            fc("Strategic vs tactical allocation", "Long-term targets vs short-term deviations."),
            fc("Negative screening", "Excluding sectors or firms."),
            fc("Impact investing", "Measurable social or environmental impact plus return."),
        ],
    )
)

# ---------------------------------------------------------------- LM5
LMS.append(
    dict(
        lm_no=5,
        title="The Behavioral Biases of Individuals",
        summary="Cognitive errors and emotional biases, how they affect decisions, and market anomalies.",
        los=[
            ("5.a", "compare", "Compare cognitive errors and emotional biases."),
            (
                "5.b",
                "discuss",
                "Discuss commonly recognised behavioural biases and their implications for financial decision-making.",
            ),
            (
                "5.c",
                "describe",
                "Describe how behavioural biases of investors can lead to market characteristics "
                "that may not be explained by traditional finance.",
            ),
        ],
        topics=[
            topic(
                "Cognitive errors",
                P(
                    "Cognitive errors come from faulty reasoning or memory. They are easier to **correct** with "
                    "information and education."
                ),
                T(
                    ["Group", "Bias", "Example"],
                    ["Belief perseverance", "Conservatism", "Slow to update a view after new data"],
                    ["", "Confirmation", "Reading only news that supports your stock"],
                    ["", "Representativeness", "A good company must be a good stock"],
                    ["", "Illusion of control", "Believing you can influence random outcomes"],
                    ["", "Hindsight", "'I knew the crash was coming'"],
                    ["Processing errors", "Anchoring", "Sticking to the purchase price as a reference"],
                    ["", "Mental accounting", "Treating bonus money differently from salary"],
                    ["", "Framing", "Choosing based on how options are presented"],
                    ["", "Availability", "Judging likelihood by what comes to mind easily"],
                ),
            ),
            topic(
                "Emotional biases",
                P(
                    "Emotional biases come from feelings and impulses. They are hard to correct, so advisers often "
                    "**adapt** to them."
                ),
                L(
                    "**Loss aversion**: losses hurt about twice as much as equal gains please; leads to holding losers "
                    "and selling winners too early (disposition effect).",
                    "**Overconfidence**: overestimating skill or knowledge; trading too much, under-diversifying.",
                    "**Self-control**: favouring today's spending over long-term goals.",
                    "**Status quo**: doing nothing when change would help.",
                    "**Endowment**: valuing what you own more than an identical asset you don't.",
                    "**Regret aversion**: avoiding decisions that might cause regret; herding.",
                ),
                EX(
                    "Amit bought Lotus Pharma at ₹800; it now trades at ₹560. He refuses to sell 'until it gets back "
                    "to 800'. That is **anchoring** on the purchase price plus **loss aversion**."
                ),
                FUN("Loss aversion is why finding ₹500 on the road feels nice, but losing ₹500 ruins the whole week."),
            ),
            topic(
                "Behavioural finance and markets",
                L(
                    "**Momentum** and bubbles: herding and overconfidence push prices too far.",
                    "**Value vs growth** anomalies: representativeness makes investors overpay for glamour stocks.",
                    "**Home bias**: familiarity leads to under-diversification.",
                    "These patterns may persist because limits to arbitrage stop rational traders correcting them.",
                ),
                WO(
                    "In the curriculum, **overconfidence** is classed as an **emotional** bias, even though it has "
                    "cognitive features."
                ),
            ),
        ],
        revision=sheet(
            "Cognitive → correct (educate) · Emotional → adapt",
            ("Conservatism", "Slow to update"),
            ("Confirmation", "Seek supporting evidence"),
            ("Representativeness", "Stereotype-based judgement"),
            ("Anchoring", "Stuck on a reference number"),
            ("Mental accounting", "Money in separate buckets"),
            ("Loss aversion", "Losses hurt more than gains please"),
            ("Overconfidence", "Emotional bias; overtrading"),
            ("Status quo / endowment", "Inertia; overvaluing what you own"),
        ),
        questions=[
            q(
                "E",
                "Loss aversion means investors:",
                ["Feel losses more strongly than equal gains", "Prefer losses to gains", "Ignore losses"],
                0,
                "Losses hurt about twice as much as gains please.",
                "5.b",
            ),
            q(
                "M",
                "Cognitive errors differ from emotional biases in that cognitive errors:",
                [
                    "Are impossible to correct",
                    "Can often be corrected with better information and education",
                    "Arise only in markets",
                ],
                1,
                "They stem from reasoning mistakes.",
                "5.a",
            ),
            q(
                "M",
                "An investor refuses to sell a share until it returns to his purchase price. This is mainly:",
                ["Anchoring", "Availability", "Status quo bias"],
                0,
                "He is fixed on an arbitrary reference point.",
                "5.b",
            ),
            q(
                "M",
                "Treating a tax refund as 'fun money' to gamble while being cautious with salary is:",
                ["Framing", "Mental accounting", "Hindsight bias"],
                1,
                "Money is put in separate mental buckets.",
                "5.b",
            ),
            q(
                "E",
                "Overconfidence bias leads investors to:",
                ["Trade too much and under-diversify", "Hold too much cash", "Avoid all equities"],
                0,
                "They overrate their information and skill.",
                "5.b",
            ),
            q(
                "H",
                "In the curriculum, overconfidence is classified as:",
                ["A cognitive processing error", "An emotional bias", "A belief perseverance error"],
                1,
                "It is treated as emotional.",
                "5.a",
            ),
            q(
                "M",
                "Searching only for news that supports an existing investment is:",
                ["Confirmation bias", "Endowment bias", "Self-control bias"],
                0,
                "A belief perseverance error.",
                "5.b",
            ),
            q(
                "H",
                "An adviser dealing with a client's strong emotional bias should usually:",
                ["Ignore it", "Adapt the portfolio to accommodate the bias", "Insist it is corrected immediately"],
                1,
                "Emotional biases are hard to change, so advisers adapt.",
                "5.a",
            ),
            q(
                "M",
                "Assuming a well-known, well-run company must be a good investment is:",
                ["Representativeness", "Conservatism", "Regret aversion"],
                0,
                "Judging by stereotype rather than price and value.",
                "5.b",
            ),
            q(
                "H",
                "Behavioural explanations for momentum in share prices most often cite:",
                ["Herding and overconfidence", "Mental accounting only", "Perfectly rational arbitrage"],
                0,
                "Crowd behaviour can push prices beyond fair value.",
                "5.c",
            ),
        ],
        flashcards=[
            fc("Cognitive vs emotional", "Reasoning errors (correct) vs feelings (adapt)."),
            fc("Anchoring", "Sticking to a reference point like the purchase price."),
            fc("Mental accounting", "Treating money differently by its source or bucket."),
            fc("Loss aversion", "Losses feel ~2× as bad as equal gains feel good."),
            fc("Overconfidence", "Emotional bias: overtrading, under-diversifying."),
            fc("Confirmation bias", "Seeking evidence that supports your view."),
        ],
    )
)

# ---------------------------------------------------------------- LM6
LMS.append(
    dict(
        lm_no=6,
        title="Introduction to Risk Management",
        summary="Risk governance, risk tolerance and budgeting, types of risk, measuring and modifying risk.",
        los=[
            ("6.a", "define", "Define risk management and describe the features of a risk management framework."),
            ("6.b", "describe", "Describe risk governance, risk tolerance and risk budgeting."),
            ("6.c", "identify", "Identify financial and non-financial sources of risk."),
            ("6.d", "describe", "Describe methods for measuring and modifying risk exposures."),
        ],
        topics=[
            topic(
                "The risk management framework",
                P(
                    "**Risk management** is the process of setting the level of risk an organisation wants, "
                    "measuring the risk it actually has, and adjusting one towards the other. The aim is **not** to "
                    "minimise risk but to take the **right** risks."
                ),
                L(
                    "**Risk governance**: top-down oversight by the board; sets risk tolerance.",
                    "**Risk tolerance**: how much loss the organisation can and will accept.",
                    "**Risk budgeting**: allocating total risk across activities, e.g. by tracking error or VaR.",
                    "Identification, measurement, monitoring, reporting and a strong risk culture.",
                ),
            ),
            topic(
                "Sources of risk",
                T(
                    ["Financial", "Non-financial"],
                    ["Market risk (prices, rates, FX)", "Operational risk (people, systems, fraud)"],
                    ["Credit risk (default)", "Legal and compliance risk"],
                    ["Liquidity risk (cannot sell without big price cut)", "Model risk, settlement risk, tax risk"],
                    ["", "Solvency risk (running out of cash)"],
                ),
                WO("Risks interact: a market crash raises credit risk and can create liquidity problems, as in 2008."),
            ),
            topic(
                "Measuring and modifying risk",
                L(
                    "**Standard deviation**, **beta**, **duration**, option **Greeks** (delta, gamma, vega).",
                    "**Value at risk (VaR)**: minimum loss at a given probability over a period. '5% one-day VaR of "
                    "₹2 crore' = a 5% chance of losing **at least** ₹2 crore in a day.",
                    "**Conditional VaR**: average loss beyond VaR.",
                    "**Scenario analysis** and **stress testing** for extreme but plausible events.",
                ),
                T(
                    ["Method", "Example"],
                    ["Prevention / avoidance", "Not entering a risky market"],
                    ["Acceptance (self-insurance, diversification)", "Holding reserves"],
                    ["Risk transfer", "Buying insurance"],
                    ["Risk shifting", "Using derivatives to change exposure"],
                ),
                FUN(
                    "VaR tells you how bad a normal bad day is. It says nothing about the day the monsoon floods the "
                    "trading floor. That is what stress tests are for."
                ),
            ),
        ],
        revision=sheet(
            "VaR = minimum loss at a given probability over a period · CVaR = average loss beyond VaR",
            ("Goal", "Right risks, not zero risk"),
            ("Risk governance", "Board-level oversight"),
            ("Risk budgeting", "Allocate total risk across activities"),
            ("Financial risks", "Market, credit, liquidity"),
            ("Non-financial", "Operational, legal, model, solvency"),
            ("Modify risk", "Avoid, accept, transfer, shift"),
        ),
        questions=[
            q(
                "E",
                "The main aim of risk management is to:",
                [
                    "Eliminate all risk",
                    "Take the risks the organisation wants and manage them to the chosen level",
                    "Maximise volatility",
                ],
                1,
                "Risk management aligns actual risk with risk tolerance.",
                "6.a",
            ),
            q(
                "M",
                "Allocating an organisation's total risk across asset classes or traders is:",
                ["Risk governance", "Risk budgeting", "Risk transfer"],
                1,
                "A risk budget spreads total risk.",
                "6.b",
            ),
            q(
                "E",
                "Which is a non-financial risk?",
                ["Credit risk", "Operational risk", "Market risk"],
                1,
                "Operational risk arises from people and systems.",
                "6.c",
            ),
            q(
                "M",
                "A 5% one-day VaR of ₹2 crore means there is a 5% chance of losing:",
                ["Exactly ₹2 crore", "At least ₹2 crore in a day", "At most ₹2 crore in a day"],
                1,
                "VaR is a minimum loss at the stated probability.",
                "6.d",
            ),
            q(
                "H",
                "Conditional VaR measures:",
                ["The average loss when losses exceed VaR", "The maximum possible loss", "The median daily return"],
                0,
                "It looks into the tail beyond VaR.",
                "6.d",
            ),
            q(
                "M",
                "Buying an insurance policy to cover fire damage is an example of:",
                ["Risk avoidance", "Risk transfer", "Self-insurance"],
                1,
                "The insurer takes the risk for a premium.",
                "6.d",
            ),
            q(
                "M",
                "Using futures to reduce a portfolio's equity exposure is:",
                ["Risk shifting", "Risk prevention", "Risk acceptance"],
                0,
                "Derivatives shift the distribution of outcomes.",
                "6.d",
            ),
            q(
                "H",
                "Board-level oversight that sets the organisation's risk tolerance is called:",
                ["Risk budgeting", "Risk governance", "Stress testing"],
                1,
                "Governance is top-down.",
                "6.b",
            ),
            q(
                "E",
                "The risk of being unable to sell an asset quickly without a large price cut is:",
                ["Liquidity risk", "Model risk", "Legal risk"],
                0,
                "A financial risk.",
                "6.c",
            ),
            q(
                "M",
                "Which tool examines the effect of extreme but plausible events on a portfolio?",
                ["Stress testing", "Beta", "Mean return"],
                0,
                "Stress tests explore tail scenarios.",
                "6.d",
            ),
        ],
        flashcards=[
            fc("Risk management aim", "Right risks at the chosen level, not zero risk."),
            fc("Risk governance", "Board oversight; sets risk tolerance."),
            fc("Risk budgeting", "Allocating total risk across activities."),
            fc("Financial vs non-financial risk", "Market, credit, liquidity vs operational, legal, model, solvency."),
            fc("VaR", "Minimum loss at a given probability over a period."),
            fc("Ways to modify risk", "Avoid, accept, transfer (insurance), shift (derivatives)."),
        ],
    )
)


if __name__ == "__main__":
    # Prototype questions: 58 diversification (systematic vs specific, LM2), 59 expected return (LM1), 60 IPS (LM4).
    write_pack("pm", "Portfolio Management", LMS, {"58": 2, "59": 1, "60": 4}, balance_keys=True)
