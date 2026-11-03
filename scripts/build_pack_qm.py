"""Quantitative Methods content pack.  python scripts/build_pack_qm.py, then re-seed."""

from packlib import EX, FUN, FX, OL, WO, H, L, P, T, fc, q, sheet, topic, write_pack

LMS = []

# ---------------------------------------------------------------- LM1
LMS.append(dict(
    lm_no=1, title="Rates and Returns",
    summary="Interest rate components, return measures, money- vs time-weighted returns, annualising.",
    los=[("1.a", "interpret", "Interpret interest rates as required returns, discount rates or opportunity costs "
                              "and as a real risk-free rate plus risk premiums."),
         ("1.b", "calculate", "Calculate and interpret approaches to measuring returns over time and their uses."),
         ("1.c", "compare", "Compare money-weighted and time-weighted returns and evaluate portfolio "
                            "performance with them."),
         ("1.d", "calculate", "Calculate and interpret annualised and continuously compounded returns."),
         ("1.e", "calculate", "Calculate and interpret gross, net, real and leveraged returns.")],
    topics=[
        topic("Interest rates and return measures",
              P("An interest rate can be read as a **required rate of return**, a **discount rate** or an "
                "**opportunity cost**. It is built from a real risk-free rate plus premiums for risk."),
              FX("Required return ≈ real risk-free rate + inflation premium + default premium + liquidity "
                 "premium + maturity premium"),
              FX("Holding period return = (P1 − P0 + income) ÷ P0"),
              EX("Returns of +50% then −50%. Arithmetic mean = 0%, but ₹100 becomes 150 and then 75. Geometric "
                 "mean = √(1.5 × 0.5) − 1 = **−13.4%**, the true compound growth rate."),
              L("**Arithmetic mean**: best single-period estimate; overstates multi-period growth.",
                "**Geometric mean**: compound growth rate; always ≤ arithmetic mean.",
                "**Harmonic mean**: average cost under rupee-cost averaging. Buying ₹1,000 of stock at ₹10 and "
                "at ₹20 gives an average cost of 2 ÷ (1/10 + 1/20) = **₹13.33**.",
                "**Trimmed / winsorised means** reduce the effect of outliers.")),
        topic("Money-weighted vs time-weighted returns",
              L("**Money-weighted return (MWR)** is the IRR of the investor's cash flows. It is affected by the "
                "**timing and size of contributions**.",
                "**Time-weighted return (TWR)** links sub-period returns geometrically and ignores external "
                "flows. It is the standard for **judging managers**, who don't control client cash flows."),
              EX("₹100 grows to ₹120 in year 1 (+20%). The investor adds ₹100, so ₹220 is invested; it falls to "
                 "₹198 in year 2 (−10%). TWR = √(1.20 × 0.90) − 1 = **3.92%** a year. MWR solves −100 − 100/(1 + r) "
                 "+ 198/(1 + r)² = 0, giving **−0.67%**: more money was invested just before the bad year."),
              WO("Don't blame a manager for a low MWR caused by the client adding money at the wrong time. Use "
                 "TWR for manager evaluation.")),
        topic("Annualising, continuous compounding and real returns",
              FX("EAR = (1 + stated rate ÷ m)^m − 1 · Continuous: r_cc = ln(1 + HPR), EAR = e^r − 1 · "
                 "Annualised = (1 + period return)^(periods per year) − 1"),
              EX("12% compounded monthly: (1.01)¹² − 1 = **12.68%**. Compounded continuously: e^0.12 − 1 = "
                 "**12.75%**. A 10% holding period return equals ln(1.10) = **9.53%** continuously compounded."),
              FX("Real return = (1 + nominal) ÷ (1 + inflation) − 1"),
              EX("Nominal 9%, inflation 4%: 1.09 ÷ 1.04 − 1 = **4.81%**, a little less than the 5% shortcut."),
              P("**Gross return** is before fees; **net return** is after them. **Leveraged returns** "
                "magnify gains and losses on the investor's own equity."),
              FUN("Arithmetic mean is the friend who says 'up 50%, down 50%, so we're even'. Geometric mean "
                  "is the bank statement that says otherwise.")),
    ],
    revision=sheet("HPR = (P1 − P0 + D)/P0 · EAR = (1 + r/m)^m − 1 · r_cc = ln(1 + HPR) · Real = (1 + n)/(1 + i) − 1",
                   ("Geometric ≤ arithmetic", "Use geometric for compound growth"),
                   ("Harmonic mean", "Average cost in rupee-cost averaging"),
                   ("MWR", "IRR; sensitive to cash-flow timing"),
                   ("TWR", "Manager evaluation; ignores flows"),
                   ("Continuous", "Returns are additive over time"),
                   ("Rate components", "Real rf + inflation + default + liquidity + maturity")),
    questions=[
        q("E", "A nominal risk-free rate is approximately the real risk-free rate plus:",
          ["An inflation premium", "A default risk premium", "A liquidity premium"], 0,
          "Risk-free government debt carries no default premium; only expected inflation is added.", "1.a"),
        q("M", "A share bought at ₹200 pays a ₹10 dividend and is sold for ₹220. The holding period return is:",
          ["10%", "15%", "5%"], 1, "(220 − 200 + 10) ÷ 200 = 15%.", "1.b"),
        q("M", "Returns over two years are +50% and −50%. The geometric mean annual return is closest to:",
          ["0.0%", "−25.0%", "−13.4%"], 2, "√(1.5 × 0.5) − 1 = −13.4%.", "1.b"),
        q("M", "Which measure is most appropriate for evaluating a manager who does not control client cash "
               "flows?", ["Time-weighted return", "Money-weighted return", "Arithmetic mean of cash flows"], 0,
          "TWR removes the effect of the timing of client contributions and withdrawals.", "1.c"),
        q("H", "₹100 grows to ₹120 in year 1. The investor adds ₹100 and the portfolio ends year 2 at ₹198. The "
               "time-weighted annual return is closest to:", ["−0.67%", "3.92%", "10.00%"], 1,
          "Sub-period returns are +20% and −10%: √(1.2 × 0.9) − 1 = 3.92%. −0.67% is the MWR.", "1.c"),
        q("H", "In that example, the money-weighted return is below the time-weighted return because:",
          ["The manager charged higher fees", "Dividends were reinvested",
           "More money was invested just before the weaker period"], 2,
          "MWR weights periods by money invested, and the larger sum was exposed to the −10% year.", "1.c"),
        q("M", "A stated annual rate of 12% compounded monthly gives an effective annual rate closest to:",
          ["12.00%", "12.68%", "12.75%"], 1, "(1 + 0.12/12)¹² − 1 = 12.68%; 12.75% is continuous.", "1.d"),
        q("M", "A holding period return of 10% corresponds to a continuously compounded return closest to:",
          ["9.53%", "10.00%", "10.52%"], 0, "ln(1.10) = 0.0953.", "1.d"),
        q("H", "Nominal return is 9% and inflation is 4%. The real return is closest to:",
          ["5.00%", "4.81%", "13.36%"], 1, "1.09 ÷ 1.04 − 1 = 4.81%.", "1.e"),
        q("E", "An investor buys ₹1,000 of a stock each month at prices of ₹10 and then ₹20. The average cost per "
               "share is the:", ["Arithmetic mean, ₹15.00", "Geometric mean, ₹14.14", "Harmonic mean, ₹13.33"], 2,
          "More shares are bought at the lower price, so the harmonic mean gives the true average cost.", "1.b"),
    ],
    flashcards=[
        fc("Components of a required return", "Real risk-free + inflation + default + liquidity + maturity "
                                              "premiums."),
        fc("Geometric vs arithmetic mean", "Geometric = compound growth, always ≤ arithmetic."),
        fc("Money-weighted return", "IRR of the investor's cash flows; affected by timing of flows."),
        fc("Time-weighted return", "Geometric link of sub-period returns; used to evaluate managers."),
        fc("Continuously compounded return", "ln(1 + HPR); additive across periods."),
        fc("Real return", "(1 + nominal) ÷ (1 + inflation) − 1."),
    ],
))

# ---------------------------------------------------------------- LM2
LMS.append(dict(
    lm_no=2, title="Time Value of Money in Finance",
    summary="Valuing bonds and shares from cash flows, implied returns and growth, no-arbitrage pricing.",
    los=[("2.a", "calculate", "Calculate and interpret the present value of fixed-income and equity instruments "
                              "from expected cash flows."),
         ("2.b", "calculate", "Calculate and interpret implied returns of fixed-income instruments and the "
                              "required return and implied growth of equities."),
         ("2.c", "explain", "Explain cash flow additivity and its use in no-arbitrage pricing of forward rates, "
                            "forward exchange rates and options.")],
    topics=[
        topic("Valuing fixed income",
              FX("PV = FV ÷ (1 + r)^n · Bond price = Σ coupon ÷ (1 + r)^t + face ÷ (1 + r)^n · Perpetuity = C ÷ r"),
              EX("3-year bond, 8% annual coupon, ₹1,000 face, yield 10%: 80/1.10 + 80/1.10² + 1,080/1.10³ = "
                 "72.73 + 66.12 + 811.42 = **₹950.26**. The coupon is below the yield, so it trades at a "
                 "discount."),
              EX("A zero-coupon bond paying ₹1,000 in 5 years costs ₹713. Implied yield = (1,000 ÷ 713)^(1/5) − 1 "
                 "= **7.0%**."),
              WO("Coupon < yield → **discount**; coupon = yield → **par**; coupon > yield → **premium**.")),
        topic("Valuing equity",
              FX("Constant growth (Gordon): P0 = D1 ÷ (r − g) · Required return r = D1 ÷ P0 + g · "
                 "Implied growth g = r − D1 ÷ P0"),
              EX("Next dividend ₹20, growth 7%, required return 12%: P0 = 20 ÷ 0.05 = **₹400**. If the share "
                 "trades at ₹500 instead, implied growth = 12% − 20/500 = **8%**."),
              P("A **preferred share** with a fixed dividend and no maturity is a perpetuity: ₹9 a year at 10% "
                "is worth ₹90."),
              FUN("The Gordon model is like valuing a mango tree: next season's mangoes, divided by how "
                  "impatient you are minus how fast the tree grows.")),
        topic("Cash flow additivity and no-arbitrage",
              P("**Cash flow additivity**: the PV of a stream of cash flows equals the sum of the PVs of each "
                "flow. Two portfolios with identical future cash flows must have the same price, or there is a "
                "**riskless arbitrage**."),
              FX("Implied forward rate: (1 + z₂)² = (1 + z₁)(1 + f₁,₁)"),
              EX("One-year spot rate 5%, two-year spot rate 6%. f₁,₁ = 1.06² ÷ 1.05 − 1 = 1.1236 ÷ 1.05 − 1 = "
                 "**7.01%**."),
              P("The same idea prices **forward exchange rates** (covered interest parity) and **options** "
                "(a replicating portfolio of the underlying and borrowing must cost the same as the option).")),
    ],
    revision=sheet("PV = FV/(1 + r)^n · P0 = D1/(r − g) · (1 + z₂)² = (1 + z₁)(1 + f)",
                   ("Coupon < yield", "Discount"),
                   ("Perpetuity", "C ÷ r"),
                   ("Implied required return", "D1/P0 + g"),
                   ("Implied growth", "r − D1/P0"),
                   ("Additivity", "PV of total = sum of PVs"),
                   ("No-arbitrage", "Same cash flows, same price")),
    questions=[
        q("E", "The present value of ₹1,000 received in 3 years at a 10% annual discount rate is closest to:",
          ["₹751.31", "₹909.09", "₹729.00"], 0, "1,000 ÷ 1.10³ = 1,000 ÷ 1.331 = ₹751.31.", "2.a"),
        q("M", "A 3-year bond pays an 8% annual coupon on ₹1,000 face value. If the yield is 10%, its price is "
               "closest to:", ["₹1,000.00", "₹950.26", "₹1,050.25"], 1,
          "72.73 + 66.12 + 811.42 = ₹950.26.", "2.a"),
        q("M", "When a bond's coupon rate is below its yield, the bond trades:",
          ["At a premium", "At par", "At a discount"], 2,
          "Investors pay less than face value to earn the higher market yield.", "2.a"),
        q("M", "A share's next dividend is ₹20, growing at 7% forever. With a 12% required return its value is:",
          ["₹400", "₹285.71", "₹166.67"], 0, "20 ÷ (0.12 − 0.07) = ₹400.", "2.a"),
        q("H", "A share trades at ₹500, its next dividend is ₹20 and the required return is 12%. The implied "
               "constant growth rate is:", ["4%", "8%", "12%"], 1, "g = 12% − 20 ÷ 500 = 12% − 4% = 8%.", "2.b"),
        q("E", "A preferred share pays ₹9 a year forever. At a 10% required return its value is:",
          ["₹99", "₹9", "₹90"], 2, "Perpetuity: 9 ÷ 0.10 = ₹90.", "2.a"),
        q("H", "The one-year spot rate is 5% and the two-year spot rate is 6%. The implied one-year rate one year "
               "from now is closest to:", ["6.00%", "7.01%", "5.50%"], 1, "1.06² ÷ 1.05 − 1 = 7.01%.", "2.c"),
        q("M", "The cash flow additivity principle states that:",
          ["The PV of a series of cash flows equals the sum of their individual PVs",
           "Cash flows must be equal to be valued", "Future values cannot be added"], 0,
          "Each flow is discounted separately and the results are summed.", "2.c"),
        q("H", "If two portfolios with identical future cash flows trade at different prices:",
          ["Both prices are correct", "The cheaper one must carry more risk", "An arbitrage opportunity exists"],
          2, "Buy the cheaper, sell the dearer and lock in a riskless profit.", "2.c"),
        q("M", "A zero-coupon bond paying ₹1,000 in 5 years trades at ₹713. Its implied annual yield is closest "
               "to:", ["5.7%", "7.0%", "8.1%"], 1, "(1,000 ÷ 713)^(1/5) − 1 = 7.0%.", "2.b"),
    ],
    flashcards=[
        fc("Bond price vs yield", "Coupon < yield → discount; = → par; > → premium."),
        fc("Gordon growth model", "P0 = D1 ÷ (r − g)."),
        fc("Implied growth from price", "g = r − D1 ÷ P0."),
        fc("Perpetuity value", "Payment ÷ discount rate."),
        fc("Implied 1-year forward rate", "(1 + z₂)² ÷ (1 + z₁) − 1."),
        fc("Cash flow additivity", "PV of a stream = sum of PVs of each flow; basis for no-arbitrage."),
    ],
))

# ---------------------------------------------------------------- LM3
LMS.append(dict(
    lm_no=3, title="Statistical Measures of Asset Returns",
    summary="Central tendency, location, dispersion, skewness, kurtosis and correlation.",
    los=[("3.a", "calculate", "Calculate, interpret and evaluate measures of central tendency and location."),
         ("3.b", "calculate", "Calculate, interpret and evaluate measures of dispersion."),
         ("3.c", "interpret", "Interpret and evaluate measures of skewness and kurtosis."),
         ("3.d", "interpret", "Interpret correlation between two variables.")],
    topics=[
        topic("Central tendency and location",
              EX("Returns of 2%, 4%, 6%, 8% and 30%: mean = 50 ÷ 5 = **10%**, median = **6%**. One outlier pulls "
                 "the mean far above the typical value."),
              L("**Median** and **trimmed or winsorised means** resist outliers.",
                "**Mode**: most frequent value.",
                "**Quantiles** split sorted data: quartiles (4), quintiles (5), deciles (10), percentiles (100)."),
              FX("Position of the y-th percentile: L = (n + 1) × y ÷ 100"),
              EX("With 19 sorted observations, the 25th percentile is at position (19 + 1) × 25 ÷ 100 = **5**. "
                 "The interquartile range (Q3 − Q1) is the middle 50% shown by a box plot.")),
        topic("Dispersion",
              FX("Sample variance s² = Σ(x − x̄)² ÷ (n − 1) · Coefficient of variation = s ÷ x̄"),
              EX("Returns of 2%, 4% and 6%: mean 4%; squared deviations 4, 0, 4; s² = 8 ÷ 2 = 4; **s = 2%**. "
                 "A fund with mean 8% and s = 12% has CV = **1.5**: 1.5 units of risk per unit of return."),
              L("**Range** and **mean absolute deviation** are simpler but less used.",
                "**Target downside deviation** measures only returns **below a chosen target**, matching "
                "investors' focus on losses."),
              WO("Use **n − 1** for a sample variance. Dividing by n gives the population formula and "
                 "understates sample dispersion.")),
        topic("Skewness, kurtosis and correlation",
              T(["Shape", "Tail", "Order of measures"],
                ["Positive skew", "Long right tail", "Mean > median > mode"],
                ["Negative skew", "Long left tail", "Mean < median < mode"],
                ["Symmetric", "Balanced", "Mean = median = mode"]),
              L("**Kurtosis** measures tail weight. Normal kurtosis = 3. **Leptokurtic**: fat tails, excess "
                "kurtosis > 0. **Platykurtic**: thin tails, excess kurtosis < 0.",
                "**Correlation** runs from −1 to +1 and measures **linear** association only. Zero correlation "
                "does not rule out a non-linear relationship.",
                "Beware **spurious correlation** and outliers; correlation is not causation."),
              FUN("Positive skew is the lottery-ticket stock: mostly small losses, with the rare jackpot "
                  "stretching the right tail.")),
    ],
    revision=sheet("s² = Σ(x − x̄)²/(n − 1) · CV = s/x̄ · Percentile position = (n + 1)y/100",
                   ("Outliers", "Prefer median or trimmed mean"),
                   ("Positive skew", "Mean > median, long right tail"),
                   ("Leptokurtic", "Fat tails, excess kurtosis > 0"),
                   ("Downside deviation", "Only returns below target"),
                   ("Correlation", "−1 to +1, linear only"),
                   ("Zero correlation", "No linear link; not independence")),
    questions=[
        q("E", "Returns are 2%, 4%, 6%, 8% and 30%. The median is:", ["6%", "10%", "8%"], 0,
          "The middle of five sorted values is the third, 6%. 10% is the mean.", "3.a"),
        q("M", "When data contain an extreme outlier, the best measure of central tendency is usually the:",
          ["Arithmetic mean", "Median", "Range"], 1,
          "The median depends only on the middle value, so outliers barely affect it.", "3.a"),
        q("M", "Sample returns of 2%, 4% and 6% have a sample standard deviation of:",
          ["1.63%", "4.00%", "2.00%"], 2,
          "s² = (4 + 0 + 4) ÷ 2 = 4, s = 2%. 1.63% divides by n instead of n − 1.", "3.b"),
        q("M", "A fund has a mean return of 8% and a standard deviation of 12%. Its coefficient of variation is:",
          ["1.5", "0.67", "4.0"], 0, "12 ÷ 8 = 1.5.", "3.b"),
        q("E", "A positively skewed distribution has:",
          ["A long left tail with the mean below the median", "A long right tail with the mean above the median",
           "Equal mean and median"], 1, "Large positive values in the right tail pull the mean up.", "3.c"),
        q("H", "A return distribution with excess kurtosis greater than zero is:",
          ["Platykurtic, with thin tails", "Leptokurtic, with fat tails", "Mesokurtic, like the normal"], 1,
          "Fat tails mean extreme outcomes are more likely than under a normal distribution.", "3.c"),
        q("M", "A correlation coefficient of −1 means the two variables:",
          ["Have no relationship", "Always move in the same direction",
           "Move in exactly opposite directions in a perfect linear relationship"], 2,
          "−1 is perfect negative linear correlation.", "3.d"),
        q("H", "A correlation of zero between two variables means:",
          ["There is no linear relationship, although a non-linear one may exist",
           "The variables are independent in every way", "One variable causes the other"], 0,
          "Correlation captures only linear association.", "3.d"),
        q("H", "For 19 observations sorted from smallest to largest, the 25th percentile is at position:",
          ["4.75", "5", "5.25"], 1, "(19 + 1) × 25 ÷ 100 = 5.", "3.a"),
        q("M", "Target downside deviation measures:",
          ["Total variability around the mean", "The average absolute deviation of all returns",
           "Variability of returns below a chosen target"], 2,
          "It ignores returns above the target and focuses on shortfalls.", "3.b"),
    ],
    flashcards=[
        fc("Best centre measure with outliers", "Median (or trimmed / winsorised mean)."),
        fc("Sample variance", "Σ(x − x̄)² ÷ (n − 1)."),
        fc("Coefficient of variation", "Standard deviation ÷ mean: risk per unit of return."),
        fc("Positive skew", "Long right tail; mean > median > mode."),
        fc("Leptokurtic", "Fat tails; excess kurtosis > 0."),
        fc("Percentile position", "(n + 1) × y ÷ 100."),
    ],
))

# ---------------------------------------------------------------- LM4
LMS.append(dict(
    lm_no=4, title="Probability Trees and Conditional Expectations",
    summary="Expected value and variance, probability trees, total probability, Bayes' formula.",
    los=[("4.a", "calculate", "Calculate expected values, variances and standard deviations for investment "
                              "problems."),
         ("4.b", "explain", "Formulate an investment problem as a probability tree and explain conditional "
                            "expectations."),
         ("4.c", "calculate", "Calculate and interpret an updated probability using Bayes' formula.")],
    topics=[
        topic("Expected value and variance",
              FX("E(X) = Σ p × x · Var(X) = Σ p × (x − E(X))² · σ = √Var"),
              EX("EPS will be ₹10 (p = 0.3), ₹8 (p = 0.5) or ₹5 (p = 0.2). E(EPS) = 3.0 + 4.0 + 1.0 = **₹8.00**. "
                 "Var = 0.3 × 2² + 0.5 × 0² + 0.2 × (−3)² = 1.2 + 0 + 1.8 = **3.00**, so σ = **₹1.73**."),
              WO("Standard deviation is in the **same units** as the variable (rupees here); variance is in "
                 "squared units, which is harder to interpret.")),
        topic("Probability trees and conditional expectations",
              P("A **probability tree** lays out scenarios as branches. Probabilities on the branches leaving "
                "any node must **sum to 1**. A **conditional expectation** is the expected value given that a "
                "scenario occurs."),
              FX("Total probability rule: E(X) = Σ E(X | Sᵢ) × P(Sᵢ)"),
              EX("Good economy (p = 0.6): expected EPS ₹12. Bad economy (p = 0.4): ₹6. Unconditional E(EPS) = "
                 "0.6 × 12 + 0.4 × 6 = **₹9.60**."),
              FUN("A probability tree is your exam plan: if the paper is easy (60%), relax; if it's tough "
                  "(40%), at least the expected marks still add up.")),
        topic("Bayes' formula",
              FX("P(A | B) = P(B | A) × P(A) ÷ P(B), where P(B) = Σ P(B | Aᵢ) × P(Aᵢ)"),
              EX("Prior: a company beats estimates with p = 0.4. It gives positive guidance with p = 0.8 if it "
                 "beats and 0.3 if not. P(positive) = 0.4 × 0.8 + 0.6 × 0.3 = 0.32 + 0.18 = **0.50**. "
                 "P(beat | positive) = 0.32 ÷ 0.50 = **0.64**."),
              P("Bayes' formula **updates a prior probability** when new information arrives, the way analysts "
                "revise views after a news release.")),
    ],
    revision=sheet("E(X) = Σpx · Var = Σp(x − E)² · E(X) = ΣE(X|S)P(S) · P(A|B) = P(B|A)P(A)/P(B)",
                   ("Branches at a node", "Sum to 1"),
                   ("Conditional expectation", "Expected value given a scenario"),
                   ("Total probability", "Weight conditional values by scenario probabilities"),
                   ("Bayes", "Prior → posterior with new information"),
                   ("σ vs variance", "σ in original units")),
    questions=[
        q("E", "EPS will be ₹10 (probability 0.3), ₹8 (0.5) or ₹5 (0.2). Expected EPS is:",
          ["₹7.67", "₹8.00", "₹8.50"], 1, "0.3 × 10 + 0.5 × 8 + 0.2 × 5 = 3 + 4 + 1 = ₹8.00.", "4.a"),
        q("M", "For the same EPS distribution, the variance is closest to:", ["3.00", "1.73", "9.00"], 0,
          "0.3 × 4 + 0.5 × 0 + 0.2 × 9 = 3.00; 1.73 is the standard deviation.", "4.a"),
        q("M", "Good economy (probability 0.6): expected EPS ₹12. Bad economy (0.4): ₹6. Unconditional expected "
               "EPS is:", ["₹9.00", "₹9.60", "₹10.80"], 1, "0.6 × 12 + 0.4 × 6 = 9.60.", "4.b"),
        q("E", "A conditional expected value is:",
          ["The expected value given that a particular scenario occurs", "The most likely value",
           "The average of outcomes ignoring probabilities"], 0,
          "It is computed using probabilities conditional on that scenario.", "4.b"),
        q("M", "The total probability rule for expected value states that E(X) equals:",
          ["The product of the conditional expected values", "The largest conditional expected value",
           "The sum of conditional expected values weighted by scenario probabilities"], 2,
          "E(X) = Σ E(X | Sᵢ) × P(Sᵢ).", "4.b"),
        q("H", "Prior probability of beating estimates is 0.4. Positive guidance occurs with probability 0.8 if "
               "the firm beats and 0.3 if not. Given positive guidance, the updated probability of beating is:",
          ["0.64", "0.80", "0.50"], 0, "0.32 ÷ (0.32 + 0.18) = 0.64.", "4.c"),
        q("H", "Bayes' formula is used to:",
          ["Calculate a portfolio's standard deviation", "Update a probability in light of new information",
           "Discount future cash flows"], 1, "It turns a prior into a posterior probability.", "4.c"),
        q("M", "In the Bayes example above, the unconditional probability of positive guidance is:",
          ["0.32", "0.50", "0.18"], 1, "0.4 × 0.8 + 0.6 × 0.3 = 0.50.", "4.c"),
        q("H", "Standard deviation is often preferred to variance for interpretation because it:",
          ["Is always smaller than variance", "Ignores extreme outcomes", "Is in the same units as the variable"],
          2, "Variance is in squared units; σ is in rupees or percent.", "4.a"),
        q("M", "In a probability tree, the probabilities on the branches leaving any node must:",
          ["Be equal", "Each exceed 0.5", "Sum to 1"], 2, "The branches cover every possible outcome.", "4.b"),
    ],
    flashcards=[
        fc("Expected value", "Σ probability × outcome."),
        fc("Variance of a random variable", "Σ p × (x − E(X))²."),
        fc("Total probability rule", "E(X) = Σ E(X | Sᵢ) × P(Sᵢ)."),
        fc("Bayes' formula", "P(A | B) = P(B | A) × P(A) ÷ P(B)."),
        fc("Branches at a node in a probability tree", "Their probabilities sum to 1."),
        fc("Prior vs posterior", "Before vs after updating for new information."),
    ],
))

# ---------------------------------------------------------------- LM5
LMS.append(dict(
    lm_no=5, title="Portfolio Mathematics",
    summary="Portfolio expected return and risk, covariance from joint probabilities, safety-first.",
    los=[("5.a", "calculate", "Calculate and interpret the expected value, variance, standard deviation, "
                              "covariance and correlation of portfolio returns."),
         ("5.b", "calculate", "Calculate and interpret covariance and correlation using a joint probability "
                              "function."),
         ("5.c", "calculate", "Define shortfall risk, calculate the safety-first ratio and choose a portfolio "
                              "using Roy's safety-first criterion.")],
    topics=[
        topic("Portfolio return and risk",
              FX("E(Rp) = Σ wᵢ E(Rᵢ) · σp² = w₁²σ₁² + w₂²σ₂² + 2w₁w₂ρσ₁σ₂ · Cov = ρσ₁σ₂"),
              EX("60% in a stock (E = 10%, σ = 20%) and 40% in a bond (E = 6%, σ = 10%), ρ = 0.2. E(Rp) = **8.4%**. "
                 "σp² = 0.36 × 0.04 + 0.16 × 0.01 + 2 × 0.6 × 0.4 × 0.2 × 0.20 × 0.10 = 0.0144 + 0.0016 + 0.00192 "
                 "= 0.01792, so **σp = 13.4%**, below the 16% weighted average of the two σs."),
              WO("Diversification benefit comes from **correlation below +1**. The lower the correlation, the "
                 "lower portfolio risk for the same weights.")),
        topic("Covariance from a joint probability function",
              FX("Cov(A, B) = Σ p × (R_A − E_A)(R_B − E_B) · ρ = Cov ÷ (σ_A σ_B)"),
              EX("Two equally likely scenarios. A returns 20% or 0% (mean 10%); B returns 10% or 4% (mean 7%). "
                 "Cov = 0.5 × (10)(3) + 0.5 × (−10)(−3) = **30** (in %²), i.e. 0.0030."),
              FUN("Covariance is the cricket and samosa sales at a stadium: when one goes up, so does the "
                  "other.")),
        topic("Shortfall risk and safety-first",
              P("**Shortfall risk** is the probability that the portfolio return falls below a minimum "
                "acceptable level, R_L. **Roy's safety-first** rule picks the portfolio that minimises it, "
                "which (for normal returns) is the one with the **highest SFRatio**."),
              FX("SFRatio = [E(Rp) − R_L] ÷ σp"),
              EX("R_L = 3%. Portfolio Y: E = 7%, σ = 6%: SFRatio = 4 ÷ 6 = **0.67**. Portfolio Z: E = 9%, σ = 12%: "
                 "6 ÷ 12 = **0.50**. Choose **Y**, despite its lower expected return."),
              WO("When R_L equals the risk-free rate, the SFRatio **is the Sharpe ratio**.")),
    ],
    revision=sheet("σp² = w₁²σ₁² + w₂²σ₂² + 2w₁w₂ρσ₁σ₂ · SFRatio = (E(Rp) − R_L)/σp",
                   ("Portfolio return", "Weighted average of returns"),
                   ("ρ < 1", "Portfolio σ below weighted average σ"),
                   ("Covariance", "ρσ₁σ₂ or Σp(R_A − E_A)(R_B − E_B)"),
                   ("Shortfall risk", "P(return < R_L)"),
                   ("Safety-first", "Choose highest SFRatio"),
                   ("R_L = risk-free", "SFRatio = Sharpe ratio")),
    questions=[
        q("E", "A portfolio is 60% in a stock with expected return 10% and 40% in a bond with expected return "
               "6%. Its expected return is:", ["8.0%", "8.4%", "7.6%"], 1, "0.6 × 10 + 0.4 × 6 = 8.4%.", "5.a"),
        q("M", "Same weights; σ stock 20%, σ bond 10%, correlation 0.2. The portfolio standard deviation is "
               "closest to:", ["13.4%", "16.0%", "17.9%"], 0,
          "√0.01792 = 13.4%. 16% would apply only with correlation of +1.", "5.a"),
        q("M", "Holding everything else constant, a lower correlation between two assets:",
          ["Raises portfolio standard deviation", "Lowers portfolio standard deviation", "Has no effect"], 1,
          "The covariance term shrinks, reducing portfolio variance.", "5.a"),
        q("M", "Two assets have standard deviations of 20% and 10% and a correlation of 0.5. Their covariance is:",
          ["0.0200", "0.0050", "0.0100"], 2, "0.5 × 0.20 × 0.10 = 0.0100.", "5.a"),
        q("H", "Two equally likely scenarios: Asset A returns 20% or 0%; Asset B returns 10% or 4% in the same "
               "scenarios. The covariance of returns (in %²) is:", ["30", "15", "−30"], 0,
          "Means 10% and 7%: 0.5 × (10 × 3) + 0.5 × (−10 × −3) = 30.", "5.b"),
        q("E", "Shortfall risk is the:",
          ["Probability that portfolio return falls below a minimum acceptable level",
           "Standard deviation of returns", "Expected return minus the risk-free rate"], 0,
          "It focuses on the chance of missing a required threshold.", "5.c"),
        q("M", "The threshold return is 3%. Portfolio X has an expected return of 9% and σ of 12%. Its "
               "safety-first ratio is:", ["0.75", "0.50", "0.25"], 1, "(9 − 3) ÷ 12 = 0.50.", "5.c"),
        q("H", "Under Roy's safety-first criterion, an investor prefers the portfolio with the:",
          ["Lowest standard deviation", "Highest expected return", "Highest safety-first ratio"], 2,
          "The highest SFRatio minimises the probability of falling below the threshold.", "5.c"),
        q("H", "Threshold 3%. Portfolio Y: expected 7%, σ 6%. Portfolio Z: expected 9%, σ 12%. Which is "
               "preferred under safety-first?", ["Y, ratio 0.67", "Z, ratio 0.50", "Z, because its return is higher"],
          0, "Y: 4 ÷ 6 = 0.67; Z: 6 ÷ 12 = 0.50.", "5.c"),
        q("M", "When the threshold return equals the risk-free rate, the safety-first ratio equals the:",
          ["Coefficient of variation", "Sharpe ratio", "Treynor ratio"], 1,
          "(E(Rp) − Rf) ÷ σp is the Sharpe ratio.", "5.c"),
    ],
    flashcards=[
        fc("Two-asset portfolio variance", "w₁²σ₁² + w₂²σ₂² + 2w₁w₂ρσ₁σ₂."),
        fc("Covariance from correlation", "Cov = ρ × σ₁ × σ₂."),
        fc("Covariance from a joint probability table", "Σ p × (R_A − E_A)(R_B − E_B)."),
        fc("Shortfall risk", "Probability the return falls below a minimum acceptable level."),
        fc("Safety-first ratio", "(E(Rp) − R_L) ÷ σp; choose the highest."),
        fc("SFRatio with R_L = risk-free rate", "Equals the Sharpe ratio."),
    ],
))

# ---------------------------------------------------------------- LM6
LMS.append(dict(
    lm_no=6, title="Simulation Methods",
    summary="Normal and lognormal returns, Monte Carlo simulation, bootstrap resampling.",
    los=[("6.a", "explain", "Explain the relationship between normally distributed returns and lognormally "
                            "distributed prices."),
         ("6.b", "describe", "Describe Monte Carlo simulation and its investment applications."),
         ("6.c", "describe", "Describe bootstrap resampling for simulations based on observed data.")],
    topics=[
        topic("Normal returns, lognormal prices",
              P("If **continuously compounded returns are normal**, prices are **lognormal**: bounded below by "
                "zero and **skewed to the right**. That suits asset prices, which can't go negative."),
              EX("Continuously compounded returns of +5% and −2% add to +3%. A ₹100 price becomes 100 × e^0.03 = "
                 "**₹103.05**. Multiplying 1.05 × 0.98 would wrongly treat them as simple returns."),
              WO("**Continuously compounded returns are additive** over time; simple returns must be "
                 "compounded (multiplied).")),
        topic("Monte Carlo simulation",
              OL("Specify the model and the probability distributions of its risk factors.",
                 "Draw random values for each factor and compute the outcome.",
                 "Repeat thousands of times.",
                 "Analyse the distribution of outcomes: mean, percentiles, probability of loss."),
              P("Uses: valuing complex securities, estimating **value at risk**, retirement planning (the "
                "probability a corpus lasts 30 years), stress testing."),
              WO("Monte Carlo is only as good as its **assumed distributions and inputs**: garbage in, garbage "
                 "out. It gives statistical estimates, not exact answers."),
              FUN("Monte Carlo is like asking 10,000 parallel versions of yourself how retirement went, "
                  "then averaging their complaints.")),
        topic("Bootstrap resampling",
              P("**Bootstrapping** draws repeated samples **with replacement** from the observed data. It needs "
                "**no assumed parametric distribution**, so it preserves the real features of history such as "
                "fat tails."),
              T(["", "Monte Carlo", "Bootstrap"],
                ["Source of draws", "Assumed distributions", "Observed historical data"],
                ["Distribution assumption", "Required", "Not required"],
                ["Main weakness", "Wrong assumptions", "Limited to what history contains"])),
    ],
    revision=sheet("Normal ln-returns ⇒ lognormal prices · Price_T = Price_0 × e^(Σ r_cc)",
                   ("Lognormal", "Bounded at 0, right-skewed"),
                   ("Continuous returns", "Additive"),
                   ("Monte Carlo", "Random draws from assumed distributions"),
                   ("MC weakness", "Garbage in, garbage out"),
                   ("Bootstrap", "Resample observed data with replacement"),
                   ("Bootstrap weakness", "Can't go beyond history")),
    questions=[
        q("E", "If continuously compounded returns are normally distributed, asset prices are:",
          ["Lognormally distributed", "Normally distributed", "Uniformly distributed"], 0,
          "The exponential of a normal variable is lognormal.", "6.a"),
        q("M", "A lognormal distribution is:",
          ["Symmetric and unbounded", "Bounded below by zero and skewed to the right", "Bounded above by zero"],
          1, "That is why it fits prices, which cannot be negative.", "6.a"),
        q("M", "Continuously compounded returns are +5% in year 1 and −2% in year 2. A ₹100 price becomes "
               "closest to:", ["₹102.90", "₹103.00", "₹103.05"], 2,
          "100 × e^(0.05 − 0.02) = 100 × e^0.03 = ₹103.05.", "6.a"),
        q("M", "Continuously compounded returns over several periods are:",
          ["Additive", "Only multiplicative", "Always equal to holding period returns"], 0,
          "ln(P_T/P_0) is the sum of the period log returns.", "6.a"),
        q("E", "Monte Carlo simulation generates outcomes by:",
          ["Using only actual historical returns in order",
           "Repeatedly drawing random values from assumed distributions of the risk factors",
           "Solving a single closed-form equation"], 1, "Thousands of random trials build a distribution.", "6.b"),
        q("H", "A key limitation of Monte Carlo simulation is that:",
          ["Results are only as good as the assumed distributions and inputs",
           "It cannot handle more than one variable", "It always overstates risk"], 0,
          "Wrong distributional assumptions give wrong answers.", "6.b"),
        q("M", "Bootstrap resampling draws samples:",
          ["From an assumed normal distribution", "Without replacement from a theoretical model",
           "With replacement from the observed data"], 2,
          "Each draw comes from the actual sample, and values can repeat.", "6.c"),
        q("H", "Compared with Monte Carlo simulation, bootstrapping:",
          ["Requires more distributional assumptions", "Does not require assuming a parametric distribution",
           "Cannot be used for investment problems"], 1,
          "It uses the empirical distribution of the data.", "6.c"),
        q("H", "A limitation of bootstrapping is that it:",
          ["Requires a normal distribution", "Uses no data",
           "Cannot produce outcomes beyond what the historical sample contains"], 2,
          "If history lacks a type of event, the resamples will too.", "6.c"),
        q("M", "Which is a common investment use of Monte Carlo simulation?",
          ["Estimating the probability a retirement portfolio lasts 30 years", "Calculating book value",
           "Recording dividends"], 0, "Simulating many return paths gives a probability of success.", "6.b"),
    ],
    flashcards=[
        fc("Normal returns imply…", "Lognormal prices: bounded at zero, right-skewed."),
        fc("Adding continuously compounded returns", "Total r_cc = sum of period r_cc; price = P0 × e^(sum)."),
        fc("Monte Carlo steps", "Specify distributions, draw randomly, compute, repeat, analyse."),
        fc("Main weakness of Monte Carlo", "Results depend on assumed distributions and inputs."),
        fc("Bootstrap", "Resampling observed data with replacement; no distribution assumed."),
        fc("Main weakness of bootstrapping", "Cannot generate events history doesn't contain."),
    ],
))

# ---------------------------------------------------------------- LM7
LMS.append(dict(
    lm_no=7, title="Estimation and Inference",
    summary="Sampling methods and error, the central limit theorem, standard error, bootstrap and jackknife.",
    los=[("7.a", "compare", "Compare simple random, stratified random, cluster, convenience and judgmental "
                            "sampling and their effect on sampling error."),
         ("7.b", "explain", "Explain the central limit theorem and its importance for the distribution and "
                            "standard error of the sample mean."),
         ("7.c", "describe", "Describe resampling (bootstrap, jackknife) to estimate a statistic's sampling "
                             "distribution.")],
    topics=[
        topic("Sampling methods",
              T(["Method", "How", "Note"],
                ["Simple random", "Every member has an equal chance", "Baseline method"],
                ["Stratified random", "Split into strata, sample each in proportion", "Used to replicate bond "
                                                                                       "indices; more precise"],
                ["Cluster", "Split into clusters, sample whole clusters", "Cheaper but less precise"],
                ["Convenience", "Whatever is easy to access", "Non-probability; may be biased"],
                ["Judgmental", "Analyst picks the sample", "Non-probability; selection bias"]),
              P("**Sampling error** = sample statistic − population parameter. It exists even with a perfect "
                "random sample.")),
        topic("Central limit theorem and standard error",
              P("The **central limit theorem**: for a large sample (n ≥ 30), the sample mean is approximately "
                "**normally distributed**, whatever the population's distribution, with mean μ and variance "
                "σ² ÷ n."),
              FX("Standard error of the sample mean = σ ÷ √n (or s ÷ √n when σ is unknown)"),
              EX("100 monthly returns with s = 20%: standard error = 20% ÷ √100 = **2%**. To halve the standard "
                 "error to 1%, you need **four times** the data: 400 observations."),
              FUN("The CLT is the hostel mess: individual dishes vary wildly, but the average taste over "
                  "30 meals is reassuringly predictable.")),
        topic("Resampling",
              L("**Bootstrap**: draw many samples of size n **with replacement** from the data, compute the "
                "statistic each time, and use the spread as its standard error.",
                "**Jackknife**: recompute the statistic **leaving out one observation at a time** (n samples). "
                "Useful for estimating bias and standard error."),
              WO("Resampling is most useful when **no analytical formula** exists for a statistic's standard "
                 "error, e.g. for a median or a ratio.")),
    ],
    revision=sheet("SE(x̄) = s/√n · CLT: x̄ ~ approx. normal (μ, σ²/n) for n ≥ 30",
                   ("Stratified", "Proportional sampling within groups"),
                   ("Cluster", "Cheaper, less precise"),
                   ("Sampling error", "Statistic − parameter"),
                   ("Halve the SE", "Quadruple n"),
                   ("Bootstrap", "With replacement, many resamples"),
                   ("Jackknife", "Leave one out")),
    questions=[
        q("E", "In simple random sampling, each member of the population:",
          ["Has an equal chance of being selected", "Is chosen by the analyst's judgement",
           "Is grouped into clusters first"], 0, "Equal probability of selection defines simple random sampling.",
          "7.a"),
        q("M", "A bond index manager who divides the index by maturity and credit rating and samples each group "
               "in proportion is using:", ["Cluster sampling", "Stratified random sampling", "Convenience sampling"],
          1, "Sampling within each stratum in proportion is stratified random sampling.", "7.a"),
        q("M", "Compared with stratified random sampling, cluster sampling is generally:",
          ["More precise but costlier", "Identical in precision", "Cheaper but less precise"], 2,
          "Sampling whole clusters saves time and cost but captures less variation.", "7.a"),
        q("M", "Sampling error is:",
          ["The difference between a sample statistic and the population parameter",
           "A mistake in recording data", "Bias from using the wrong formula"], 0,
          "It arises because a sample is only part of the population.", "7.a"),
        q("E", "The central limit theorem states that, for large samples, the distribution of the sample mean is "
               "approximately:", ["Uniform", "Normal, whatever the population's distribution",
                                  "Identical to the population distribution"], 1,
          "This lets analysts use z- and t-based inference on means.", "7.b"),
        q("M", "A sample of 100 monthly returns has a standard deviation of 20%. The standard error of the sample "
               "mean is:", ["0.2%", "2.0%", "20.0%"], 1, "20% ÷ √100 = 2%.", "7.b"),
        q("H", "To halve the standard error of the sample mean, the sample size must be:",
          ["Doubled", "Halved", "Quadrupled"], 2, "SE falls with √n, so n must rise fourfold.", "7.b"),
        q("H", "The jackknife method estimates a statistic's variability by:",
          ["Repeatedly leaving out one observation and recalculating", "Sampling with replacement many times",
           "Assuming a normal distribution"], 0, "It creates n samples, each missing one observation.", "7.c"),
        q("H", "Judgmental sampling is most likely to suffer from:",
          ["No sampling error", "Bias from the researcher's selection", "Excessive randomness"], 1,
          "The analyst's choices can make the sample unrepresentative.", "7.a"),
        q("M", "Bootstrap resampling is especially useful when:",
          ["The population is fully known", "The sample size is zero",
           "No analytical formula exists for a statistic's standard error"], 2,
          "The spread across resamples approximates the sampling distribution.", "7.c"),
    ],
    flashcards=[
        fc("Stratified random sampling", "Split into strata and sample each in proportion."),
        fc("Cluster vs stratified", "Cluster: cheaper, less precise. Stratified: more precise."),
        fc("Central limit theorem", "For n ≥ 30, the sample mean is approx. normal with variance σ²/n."),
        fc("Standard error of the mean", "s ÷ √n."),
        fc("Bootstrap vs jackknife", "Resample with replacement vs leave one out."),
        fc("Sampling error", "Sample statistic − population parameter."),
    ],
))

# ---------------------------------------------------------------- LM8
LMS.append(dict(
    lm_no=8, title="Hypothesis Testing",
    summary="Steps of a test, Type I and II errors, power, p-values, tests of means and variances.",
    los=[("8.a", "explain", "Explain hypothesis testing and its components, including significance, Type I and "
                            "Type II errors and power."),
         ("8.b", "construct", "Construct hypothesis tests and determine their significance, errors and power at "
                              "a given significance level."),
         ("8.c", "compare", "Compare parametric and nonparametric tests and when each is appropriate.")],
    topics=[
        topic("The logic of a test",
              OL("State H₀ (always includes =, ≤ or ≥) and Hₐ.",
                 "Choose the test statistic and its distribution.",
                 "Set the significance level α.",
                 "State the decision rule (critical values).",
                 "Compute the statistic from the sample.",
                 "Decide: reject or fail to reject H₀."),
              T(["", "H₀ true", "H₀ false"],
                ["Reject H₀", "**Type I error** (probability α)", "Correct (power = 1 − β)"],
                ["Fail to reject H₀", "Correct", "**Type II error** (probability β)"]),
              L("The **p-value** is the smallest significance level at which H₀ can be rejected. Reject if "
                "p-value < α.",
                "Lowering α reduces Type I errors but **raises Type II errors**, for a given sample size.",
                "H₀: μ ≤ 0 vs Hₐ: μ > 0 is a **one-tailed** (right-tail) test; H₀: μ = 0 is two-tailed."),
              WO("We 'fail to reject' H₀; we never 'accept' it. The data may simply lack the power to detect a "
                 "difference.")),
        topic("Common tests",
              FX("t = (x̄ − μ₀) ÷ (s ÷ √n), df = n − 1"),
              EX("Mean monthly alpha 1.2%, s = 4%, n = 36, H₀: μ = 0. SE = 4 ÷ 6 = 0.667%, t = **1.80**. Two-tailed "
                 "5% critical value ≈ 2.03: **fail to reject**. One-tailed (Hₐ: μ > 0) critical ≈ 1.69: **reject**."),
              T(["Hypothesis about", "Test"],
                ["One mean (σ unknown)", "t-test"],
                ["Difference in means (independent samples)", "t-test of difference in means"],
                ["Mean difference (paired samples)", "Paired comparisons t-test"],
                ["One variance", "Chi-square test"],
                ["Equality of two variances", "F-test (larger variance on top)"])),
        topic("Parametric vs nonparametric tests",
              P("**Parametric** tests concern population parameters and rely on distribution assumptions. "
                "**Nonparametric** tests are used when those assumptions fail, data are **ranks**, there are "
                "**outliers**, or the hypothesis isn't about a parameter (e.g. randomness)."),
              L("Wilcoxon signed-rank test (single mean or paired data), Mann–Whitney U (two independent "
                "samples), Spearman rank correlation, runs test."),
              FUN("Type I error: the fire alarm rings for burnt toast. Type II error: it stays quiet while "
                  "the kitchen is actually on fire.")),
    ],
    revision=sheet("t = (x̄ − μ₀)/(s/√n) · Reject if |stat| > critical, or p-value < α · Power = 1 − β",
                   ("Type I", "Reject true H₀ (α)"),
                   ("Type II", "Fail to reject false H₀ (β)"),
                   ("Lower α", "More Type II errors"),
                   ("p-value", "Smallest α to reject"),
                   ("Variance tests", "Chi-square (one), F (two)"),
                   ("Nonparametric", "Ranks, outliers, non-normal data")),
    questions=[
        q("E", "A Type I error occurs when:",
          ["A true null hypothesis is rejected", "A false null hypothesis is not rejected",
           "The sample is too small"], 0, "Its probability equals the significance level α.", "8.a"),
        q("M", "The power of a test is:",
          ["The probability of a Type I error", "1 minus the probability of a Type II error",
           "The significance level"], 1, "Power is the probability of correctly rejecting a false H₀.", "8.a"),
        q("M", "The p-value is:",
          ["The probability that the null is true", "Always 5%",
           "The smallest significance level at which the null can be rejected"], 2,
          "Reject H₀ when the p-value is below α.", "8.a"),
        q("M", "Sample mean return 1.2%, s 4%, n 36, H₀: μ = 0. The t-statistic is:", ["1.80", "0.30", "10.80"],
          0, "1.2 ÷ (4 ÷ √36) = 1.2 ÷ 0.667 = 1.80.", "8.b"),
        q("H", "With t = 1.80 and a 5% two-tailed critical value of about 2.03, the analyst should:",
          ["Reject H₀", "Fail to reject H₀", "Accept the alternative with certainty"], 1,
          "|1.80| < 2.03, so the evidence is not strong enough at 5% two-tailed.", "8.b"),
        q("H", "Reducing the significance level from 5% to 1%, all else equal:",
          ["Raises the probability of a Type II error", "Raises the probability of a Type I error",
           "Increases the power of the test"], 0,
          "A stricter rejection rule means false nulls are rejected less often.", "8.a"),
        q("M", "Which test compares the variances of two normally distributed populations?",
          ["t-test", "F-test", "Chi-square test of independence"], 1,
          "The F-statistic is the ratio of the two sample variances.", "8.b"),
        q("H", "A nonparametric test is most appropriate when:",
          ["The population is normal with known variance", "The sample is large and normally distributed",
           "Data are ranks or the assumptions of a parametric test are not met"], 2,
          "Nonparametric tests need fewer distributional assumptions.", "8.c"),
        q("E", "For H₀: μ ≤ 0 versus Hₐ: μ > 0, the test is:",
          ["One-tailed (right tail)", "Two-tailed", "One-tailed (left tail)"], 0,
          "Only large positive values of the statistic lead to rejection.", "8.b"),
        q("M", "A chi-square test is used for hypotheses about:",
          ["The means of two populations", "The slope of a regression",
           "The variance of a single normal population"], 2,
          "χ² = (n − 1)s² ÷ σ₀² with n − 1 degrees of freedom.", "8.b"),
    ],
    flashcards=[
        fc("Type I vs Type II error", "Reject a true H₀ (α) vs fail to reject a false H₀ (β)."),
        fc("Power of a test", "1 − β: probability of rejecting a false H₀."),
        fc("p-value", "Smallest significance level at which H₀ is rejected."),
        fc("t-statistic for a mean", "(x̄ − μ₀) ÷ (s ÷ √n), df n − 1."),
        fc("Tests of variance", "Chi-square for one variance; F-test for two."),
        fc("When to go nonparametric", "Ranks, outliers, failed assumptions, non-parameter hypotheses."),
    ],
))

# ---------------------------------------------------------------- LM9
LMS.append(dict(
    lm_no=9, title="Tests of Independence",
    summary="Parametric and rank-correlation tests of zero correlation; chi-square contingency tables.",
    los=[("9.a", "explain", "Explain parametric and nonparametric tests of whether a population correlation is "
                            "zero, and decide whether to reject at a given significance level."),
         ("9.b", "explain", "Explain tests of independence based on contingency table data.")],
    topics=[
        topic("Testing correlation",
              FX("t = r√(n − 2) ÷ √(1 − r²), df = n − 2"),
              EX("r = 0.4 with n = 27: t = 0.4 × √25 ÷ √0.84 = 2.0 ÷ 0.9165 = **2.18**. The 5% two-tailed critical "
                 "value with 25 df is about 2.06, so **reject H₀: ρ = 0**."),
              L("For a given r, a **larger sample** gives a larger t, making it easier to reject ρ = 0.",
                "**Spearman rank correlation** is the nonparametric alternative, used with outliers or "
                "non-normal data."),
              FX("Spearman r_s = 1 − 6Σd² ÷ [n(n² − 1)]"),
              EX("Five pairs of ranks with Σd² = 4: r_s = 1 − 24 ÷ (5 × 24) = 1 − 0.2 = **0.80**.")),
        topic("Contingency tables and chi-square",
              P("A **contingency table** counts observations by two categorical variables, e.g. fund style "
                "versus size. The test asks whether the two are **independent**."),
              FX("Expected frequency = row total × column total ÷ grand total · χ² = Σ (O − E)² ÷ E · "
                 "df = (rows − 1)(columns − 1)"),
              EX("A cell with row total 60, column total 50 and grand total 200 has expected frequency "
                 "60 × 50 ÷ 200 = **15**. A 3 × 4 table has (3 − 1)(4 − 1) = **6** degrees of freedom."),
              WO("A **large** χ² means observed counts are far from what independence predicts, so **reject "
                 "independence**."),
              FUN("A contingency table is a wedding seating chart: if all of the bride's side sits on one "
                  "side, the seating was not independent.")),
    ],
    revision=sheet("t = r√(n − 2)/√(1 − r²) · r_s = 1 − 6Σd²/[n(n² − 1)] · E = row × col ÷ total · "
                   "df = (r − 1)(c − 1)",
                   ("Correlation test df", "n − 2"),
                   ("Larger n", "Bigger t for the same r"),
                   ("Spearman", "Nonparametric, rank-based"),
                   ("Large χ²", "Reject independence"),
                   ("Expected count", "Row total × column total ÷ grand total")),
    questions=[
        q("E", "The t-test of H₀: ρ = 0 uses degrees of freedom of:", ["n − 2", "n − 1", "n"], 0,
          "The test statistic has n − 2 degrees of freedom.", "9.a"),
        q("M", "A sample correlation of 0.4 is based on n = 27. The t-statistic is closest to:",
          ["2.00", "2.18", "1.53"], 1, "0.4 × √25 ÷ √(1 − 0.16) = 2.0 ÷ 0.9165 = 2.18.", "9.a"),
        q("M", "Holding r constant, a larger sample size:",
          ["Increases the t-statistic, making it easier to reject ρ = 0", "Decreases the t-statistic",
           "Has no effect"], 0, "t grows with √(n − 2).", "9.a"),
        q("M", "Five pairs of ranks have Σd² = 4. The Spearman rank correlation is:", ["0.20", "0.96", "0.80"], 2,
          "1 − 6 × 4 ÷ (5 × 24) = 0.80.", "9.a"),
        q("E", "The Spearman rank correlation test is preferred to the parametric test when:",
          ["The data are perfectly normal", "The data contain outliers or are not normally distributed",
           "There are no ranks available"], 1, "Ranks reduce the influence of extreme values.", "9.a"),
        q("M", "In a contingency table, a cell's row total is 60, its column total is 50 and the grand total is "
               "200. Its expected frequency is:", ["15", "30", "3,000"], 0, "60 × 50 ÷ 200 = 15.", "9.b"),
        q("H", "A contingency table has 3 rows and 4 columns. The chi-square test of independence has degrees of "
               "freedom of:", ["12", "6", "7"], 1, "(3 − 1) × (4 − 1) = 6.", "9.b"),
        q("H", "In a chi-square test of independence, a large test statistic suggests:",
          ["The variables are independent", "The sample is too small", "The variables are not independent"], 2,
          "Observed counts differ greatly from what independence would predict.", "9.b"),
        q("M", "The chi-square test of independence compares:",
          ["Observed frequencies with those expected if the variables were independent", "Two sample means",
           "Two population variances"], 0, "χ² sums (O − E)² ÷ E across cells.", "9.b"),
        q("H", "r = 0.4, n = 27, t = 2.18 and the 5% two-tailed critical value is 2.06. The conclusion is:",
          ["Fail to reject H₀", "Reject H₀: the correlation is significantly different from zero",
           "The test is invalid"], 1, "2.18 > 2.06, so reject ρ = 0 at the 5% level.", "9.a"),
    ],
    flashcards=[
        fc("t-test for correlation", "t = r√(n − 2) ÷ √(1 − r²), df n − 2."),
        fc("Spearman rank correlation", "1 − 6Σd² ÷ [n(n² − 1)]; nonparametric."),
        fc("Contingency table expected count", "Row total × column total ÷ grand total."),
        fc("Chi-square statistic", "Σ (O − E)² ÷ E."),
        fc("df for a contingency table", "(rows − 1) × (columns − 1)."),
        fc("Large chi-square means…", "Reject independence."),
    ],
))

# ---------------------------------------------------------------- LM10
LMS.append(dict(
    lm_no=10, title="Simple Linear Regression",
    summary="Least squares, assumptions, ANOVA, R², F-test, standard error of estimate, prediction, "
            "functional forms.",
    los=[("10.a", "describe", "Describe simple linear regression, how least squares estimates the coefficients, "
                              "and how to interpret them."),
         ("10.b", "explain", "Explain the assumptions of the model and how residual plots reveal violations."),
         ("10.c", "calculate", "Calculate and interpret measures of fit and test the fit and the coefficients."),
         ("10.d", "describe", "Describe ANOVA in regression and calculate the standard error of estimate."),
         ("10.e", "calculate", "Calculate a predicted value of the dependent variable and its prediction "
                               "interval."),
         ("10.f", "describe", "Describe different functional forms of simple linear regression.")],
    topics=[
        topic("Estimating the line",
              FX("Y = b₀ + b₁X + ε · b₁ = Cov(X, Y) ÷ Var(X) · b₀ = Ȳ − b₁X̄"),
              EX("Cov(X, Y) = 0.0018 and Var(X) = 0.0012, so b₁ = **1.5**. With X̄ = 2% and Ȳ = 3.5%, b₀ = 3.5 − 1.5 "
                 "× 2 = **0.5%**. For X = 4%, predicted Ŷ = 0.5 + 1.5 × 4 = **6.5%**."),
              P("**Ordinary least squares** picks b₀ and b₁ to **minimise the sum of squared residuals**. The "
                "slope is the change in Y for a one-unit change in X."),
              H("Assumptions"),
              L("**Linearity** between X and Y.",
                "**Homoskedasticity**: residual variance is constant for all X.",
                "**Independence** of residuals (no serial correlation).",
                "**Normality** of residuals."),
              WO("A residual plot that **fans out** as X rises shows **heteroskedasticity**. A pattern over time "
                 "suggests the errors aren't independent.")),
        topic("ANOVA and measures of fit",
              FX("SST = SSR + SSE · R² = SSR ÷ SST · MSR = SSR ÷ 1 · MSE = SSE ÷ (n − 2) · F = MSR ÷ MSE · "
                 "SEE = √MSE"),
              EX("n = 32, SSR = 60, SSE = 40. SST = 100, so **R² = 0.60**. MSE = 40 ÷ 30 = 1.333, **F = 60 ÷ 1.333 "
                 "= 45**, and **SEE = √1.333 = 1.15**."),
              L("Test the slope with t = (b₁ − B₁) ÷ s_b₁, df = n − 2. In simple regression, F = t² for H₀: b₁ = 0.",
                "A **prediction interval** is Ŷ ± t_c × s_f. It widens the further X is from its mean.")),
        topic("Functional forms",
              T(["Form", "Model", "Slope means"],
                ["Log-lin", "ln Y = b₀ + b₁X", "% change in Y for a one-unit change in X"],
                ["Lin-log", "Y = b₀ + b₁ ln X", "Change in Y for a % change in X"],
                ["Log-log", "ln Y = b₀ + b₁ ln X", "Elasticity: % change in Y for a 1% change in X"]),
              FUN("Regression is drawing the one straight line through a scatter of dots that annoys all "
                  "the dots the least, squared.")),
    ],
    revision=sheet("b₁ = Cov/Var(X) · b₀ = Ȳ − b₁X̄ · R² = SSR/SST · F = MSR/MSE · SEE = √(SSE/(n − 2))",
                   ("OLS", "Minimise sum of squared residuals"),
                   ("Homoskedasticity", "Constant residual variance"),
                   ("Fanning residuals", "Heteroskedasticity"),
                   ("Slope test df", "n − 2"),
                   ("Simple regression", "F = t²"),
                   ("Log-log slope", "Elasticity")),
    questions=[
        q("E", "In Y = b₀ + b₁X, the slope b₁ is estimated as:",
          ["Cov(X, Y) ÷ Var(X)", "Var(X) ÷ Cov(X, Y)", "Mean of Y ÷ mean of X"], 0,
          "OLS slope = covariance over the variance of X.", "10.a"),
        q("M", "Cov(X, Y) = 0.0018 and Var(X) = 0.0012. The mean of X is 2% and the mean of Y is 3.5%. The "
               "intercept is:", ["1.5%", "0.5%", "3.5%"], 1, "b₁ = 1.5; b₀ = 3.5 − 1.5 × 2 = 0.5%.", "10.a"),
        q("M", "With b₀ = 0.5% and b₁ = 1.5, the predicted Y when X = 4% is:", ["6.0%", "6.5%", "2.5%"], 1,
          "0.5 + 1.5 × 4 = 6.5%.", "10.e"),
        q("M", "Homoskedasticity means the residuals:",
          ["Have constant variance across all values of X", "Are correlated with each other",
           "Have a mean of one"], 0, "Their spread does not change with X.", "10.b"),
        q("M", "SSR = 60 and SSE = 40. R² is:", ["0.40", "1.50", "0.60"], 2, "60 ÷ (60 + 40) = 0.60.", "10.c"),
        q("H", "n = 32, SSR = 60 and SSE = 40 in a simple regression. The F-statistic is:", ["45.0", "1.5", "30.0"],
          0, "MSE = 40 ÷ 30 = 1.333; F = 60 ÷ 1.333 = 45.", "10.d"),
        q("H", "For the same regression, the standard error of estimate is closest to:", ["1.33", "1.15", "0.67"],
          1, "√(40 ÷ 30) = √1.333 = 1.15.", "10.d"),
        q("E", "Ordinary least squares chooses coefficients that minimise:",
          ["The sum of residuals", "The largest residual", "The sum of squared residuals"], 2,
          "Squaring stops positive and negative residuals cancelling.", "10.a"),
        q("H", "In a log-log regression, the slope coefficient is interpreted as:",
          ["An elasticity: the % change in Y for a 1% change in X", "The change in Y for a one-unit change in X",
           "The % change in Y for a one-unit change in X"], 0,
          "Both variables are in logs, so the slope is a ratio of percentage changes.", "10.f"),
        q("M", "A residual plot that fans out as X increases suggests:",
          ["A perfect fit", "Independent errors", "Heteroskedasticity"], 2,
          "Residual variance growing with X breaks the constant-variance assumption.", "10.b"),
    ],
    flashcards=[
        fc("OLS slope and intercept", "b₁ = Cov(X, Y) ÷ Var(X); b₀ = Ȳ − b₁X̄."),
        fc("Regression assumptions", "Linearity, homoskedasticity, independence, normal residuals."),
        fc("R²", "SSR ÷ SST: share of variation in Y explained by X."),
        fc("F-statistic in simple regression", "MSR ÷ MSE, with MSE = SSE ÷ (n − 2); equals t²."),
        fc("Standard error of estimate", "√MSE."),
        fc("Log-log slope", "Elasticity of Y with respect to X."),
    ],
))

# ---------------------------------------------------------------- LM11
LMS.append(dict(
    lm_no=11, title="Introduction to Big Data Techniques",
    summary="Fintech, Big Data, artificial intelligence and machine learning, and their investment uses.",
    los=[("11.a", "describe", "Describe aspects of fintech relevant to gathering and analysing financial data."),
         ("11.b", "describe", "Describe Big Data, artificial intelligence and machine learning."),
         ("11.c", "describe", "Describe applications of Big Data and data science in investment management.")],
    topics=[
        topic("Big Data and alternative data",
              P("**Big Data** is defined by **volume** (huge size), **velocity** (arrives fast, often in real "
                "time) and **variety** (many formats). **Veracity**, the reliability of the data, is often "
                "added as a fourth V."),
              T(["Source", "Examples"],
                ["Traditional", "Financial statements, prices, economic statistics"],
                ["Individuals", "Social media posts, product reviews, web searches"],
                ["Business processes", "Credit card transactions, corporate exhaust, supply chain data"],
                ["Sensors", "Satellite images, IoT devices, mobile location data"]),
              L("**Structured data** fits rows and columns. **Unstructured data**, such as text, images and "
                "audio, has no predefined format and needs extra processing.")),
        topic("Artificial intelligence and machine learning",
              L("**Supervised learning** learns from **labelled** data to predict an output, e.g. which loans "
                "will default.",
                "**Unsupervised learning** finds structure in **unlabelled** data, e.g. clustering similar "
                "companies.",
                "**Deep learning** uses **neural networks with many layers**, e.g. for image or speech "
                "recognition."),
              WO("**Overfitting**: a model that memorises noise looks brilliant on training data and fails on "
                 "new data. **Underfitting**: too simple to capture the pattern. Hold out validation and test "
                 "sets to check."),
              FUN("An overfitted model is the student who memorised last year's paper word for word, then "
                  "met a new question.")),
        topic("Uses in investment management",
              L("**Text analytics and NLP**: sentiment in earnings calls, news and filings.",
                "**Alternative data** forecasts: card spending to predict a retailer's sales, satellite photos of "
                "car parks, shipping traffic.",
                "**Robo-advisers**: automated portfolio advice and rebalancing with little human involvement.",
                "**Algorithmic trading**, risk management and fraud detection."),
              P("Data processing steps: **capture**, **curation** (cleaning), **storage**, **search** and "
                "**transfer**. Visualisation tools such as word clouds help present unstructured data.")),
    ],
    revision=sheet("Big Data = volume + velocity + variety (+ veracity)",
                   ("Alternative data", "Individuals, business processes, sensors"),
                   ("Unstructured", "Text, images, audio"),
                   ("Supervised", "Labelled data → prediction"),
                   ("Unsupervised", "No labels → clustering"),
                   ("Deep learning", "Multi-layer neural networks"),
                   ("Overfitting", "Great in-sample, poor out-of-sample")),
    questions=[
        q("E", "The three original characteristics of Big Data are:",
          ["Volume, velocity and variety", "Value, vision and variance", "Validity, volatility and voice"], 0,
          "Veracity is often added as a fourth.", "11.b"),
        q("M", "Satellite images of retailers' car parks are an example of:",
          ["Traditional financial statement data", "Alternative data from sensors", "Data from corporate filings"],
          1, "Sensor-based data is a major type of alternative data.", "11.a"),
        q("M", "Supervised machine learning:",
          ["Learns from labelled data to predict an output", "Finds structure in data without labels",
           "Requires no data"], 0, "The model is trained on inputs paired with known outputs.", "11.b"),
        q("M", "Grouping companies with similar characteristics, without predefined labels, is an example of:",
          ["Supervised learning", "Unsupervised learning (clustering)", "Linear regression"], 1,
          "No target variable is given; the algorithm finds the groups.", "11.b"),
        q("H", "A model that performs very well on training data but poorly on new data is:",
          ["Underfitted", "Well generalised", "Overfitted"], 2,
          "It has learned noise in the training data rather than the true pattern.", "11.b"),
        q("E", "Natural language processing would most likely be used to:",
          ["Analyse the sentiment of earnings call transcripts", "Calculate a bond's duration",
           "Count shares outstanding"], 0, "NLP turns text into measurable signals.", "11.c"),
        q("H", "Unstructured data is best described as data that:",
          ["Is organised in rows and columns", "Comes only from stock exchanges",
           "Does not follow a predefined format, such as text, images or audio"], 2,
          "It needs processing before it can be analysed like a table.", "11.a"),
        q("M", "Deep learning algorithms are based on:",
          ["Neural networks with many layers", "Simple averages", "Manual rule books"], 0,
          "Stacked layers learn increasingly complex features.", "11.b"),
        q("H", "Which is a typical use of Big Data in investment management?",
          ["Replacing financial statements with guesswork",
           "Using credit card transaction data to forecast a retailer's sales",
           "Removing the need for risk management"], 1, "Transaction data can lead official sales figures.",
          "11.c"),
        q("M", "A robo-adviser is best described as:",
          ["A trading floor robot", "A type of bond",
           "An automated platform that gives portfolio advice and management with little human involvement"], 2,
          "Robo-advisers use algorithms to build and rebalance portfolios.", "11.c"),
    ],
    flashcards=[
        fc("Three Vs of Big Data", "Volume, velocity, variety (plus veracity)."),
        fc("Sources of alternative data", "Individuals, business processes, sensors."),
        fc("Supervised vs unsupervised learning", "Labelled data to predict vs unlabelled data to find structure."),
        fc("Deep learning", "Neural networks with many layers."),
        fc("Overfitting", "Fits noise: strong in-sample, weak out-of-sample."),
        fc("NLP in investing", "Sentiment analysis of calls, news and filings."),
    ],
))


if __name__ == "__main__":
    # Prototype questions 37 (compounding) and 39 (perpetuity) belong to Time Value of Money.
    write_pack("qm", "Quantitative Methods", LMS, {"37": 2, "39": 2})
