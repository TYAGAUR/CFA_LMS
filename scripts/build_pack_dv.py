"""Derivatives content pack.  python scripts/build_pack_dv.py, then re-seed."""

from packlib import EX, FUN, FX, WO, H, L, P, T, fc, q, sheet, topic, write_pack

LMS = []

# ---------------------------------------------------------------- LM1
LMS.append(
    dict(
        lm_no=1,
        title="Derivative Instrument and Derivative Market Features",
        summary="What derivatives are, their underlyings, and how OTC and exchange-traded markets differ.",
        los=[
            ("1.a", "define", "Define a derivative and describe basic features of a derivative instrument."),
            (
                "1.b",
                "describe",
                "Describe the basic features of derivative markets, and contrast over-the-counter "
                "and exchange-traded derivative markets.",
            ),
        ],
        topics=[
            topic(
                "What a derivative is",
                P(
                    "A **derivative** is a contract whose value comes from an **underlying**: a share, index, bond, "
                    "interest rate, currency, commodity, credit event or even weather. It specifies the underlying, "
                    "size, price, maturity and settlement (physical delivery or cash)."
                ),
                L(
                    "**Long** = buyer; **short** = seller. One side's gain is the other's loss (a zero-sum contract, "
                    "before costs).",
                    "Derivatives let users take or shed exposure with little upfront cash, which creates **leverage**.",
                ),
                EX(
                    "A Nifty futures lot is 75 units. At an index level of 22,000, one contract controls ₹16.5 lakh of "
                    "exposure. If initial margin is 12%, the trader posts only about ₹2 lakh."
                ),
            ),
            topic(
                "OTC versus exchange-traded",
                T(
                    ["", "Exchange-traded", "Over-the-counter (OTC)"],
                    ["Terms", "Standardised", "Customised"],
                    [
                        "Counterparty risk",
                        "Low: clearing house guarantees",
                        "Higher, though central clearing and collateral reduce it",
                    ],
                    ["Transparency", "Prices public", "Private, though post-crisis reporting has increased"],
                    ["Liquidity", "High for main contracts", "Varies"],
                    ["Examples", "Futures, listed options", "Forwards, most swaps"],
                ),
                P(
                    "A **central counterparty (CCP)** stands between buyer and seller, collects margin and "
                    "guarantees performance. Regulators now require many standard OTC swaps to be centrally cleared."
                ),
                WO(
                    "Customisation is the OTC advantage; standardisation and the clearing guarantee are the exchange "
                    "advantage."
                ),
                FUN(
                    "An OTC forward is a tailor-made suit. An exchange future is off the rack: it fits most people "
                    "well enough and you can return it (close it out) easily."
                ),
            ),
        ],
        revision=sheet(
            "Derivative value = f(underlying) · Zero-sum before costs",
            ("Underlying", "Asset or rate the contract depends on"),
            ("Long / short", "Buyer / seller"),
            ("Exchange-traded", "Standardised, cleared, transparent"),
            ("OTC", "Customised, bilateral, more counterparty risk"),
            ("CCP", "Becomes buyer to every seller and seller to every buyer"),
            ("Settlement", "Physical delivery or cash"),
        ),
        questions=[
            q(
                "E",
                "The underlying of a derivative is:",
                [
                    "The asset or rate from which the derivative derives its value",
                    "The clearing house",
                    "The margin account",
                ],
                0,
                "The value of the contract depends on the underlying.",
                "1.a",
            ),
            q(
                "M",
                "Compared with OTC derivatives, exchange-traded derivatives are:",
                [
                    "Customised and private",
                    "Standardised with clearing-house guarantees",
                    "Higher in counterparty risk",
                ],
                1,
                "Exchanges standardise terms and clearing houses guarantee performance.",
                "1.b",
            ),
            q(
                "M",
                "A central counterparty reduces:",
                ["Counterparty credit risk", "Market risk", "Basis risk"],
                0,
                "The CCP guarantees performance and collects margin.",
                "1.b",
            ),
            q(
                "E",
                "Which is most likely an OTC derivative?",
                ["A listed index option", "An exchange-traded futures contract", "A customised currency forward"],
                2,
                "Forwards are privately negotiated.",
                "1.b",
            ),
            q(
                "M",
                "Derivatives provide leverage because:",
                [
                    "They must be fully paid upfront",
                    "A small upfront payment controls a large exposure",
                    "They have no counterparties",
                ],
                1,
                "Margin or premium is small relative to notional.",
                "1.a",
            ),
            q(
                "H",
                "A Nifty futures contract of 75 units at an index level of 22,000 with 12% initial margin needs margin "
                "closest to:",
                ["₹1.98 lakh", "₹16.5 lakh", "₹2.64 lakh"],
                0,
                "75 × 22,000 = ₹16.5 lakh; 12% = ₹1.98 lakh.",
                "1.a",
            ),
            q(
                "E",
                "Settlement of a derivative by paying the difference in value rather than delivering the asset is:",
                ["Physical settlement", "Cash settlement", "Netting"],
                1,
                "Cash settlement pays the gain or loss.",
                "1.a",
            ),
            q(
                "M",
                "Before transaction costs, derivatives are best described as:",
                ["Zero-sum between the long and the short", "Always profitable for the long", "Riskless"],
                0,
                "One party's gain equals the other's loss.",
                "1.a",
            ),
            q(
                "H",
                "Post-crisis regulation mainly affected OTC markets by:",
                [
                    "Banning swaps",
                    "Requiring central clearing and reporting for many standard contracts",
                    "Removing margin requirements",
                ],
                1,
                "Mandatory clearing and trade reporting increased transparency.",
                "1.b",
            ),
            q(
                "M",
                "Which is an advantage of OTC derivatives over exchange-traded ones?",
                ["Greater transparency", "Lower counterparty risk", "Terms can be tailored to the user"],
                2,
                "Customisation is the key OTC benefit.",
                "1.b",
            ),
        ],
        flashcards=[
            fc("Derivative", "Contract whose value comes from an underlying asset or rate."),
            fc("Long vs short", "Buyer vs seller of the contract."),
            fc("Exchange-traded features", "Standardised, cleared, transparent, liquid."),
            fc("OTC features", "Customised, bilateral, more counterparty risk."),
            fc("CCP", "Clearing counterparty guaranteeing both sides."),
            fc("Why derivatives are leveraged", "Small margin or premium controls large notional."),
        ],
    )
)

# ---------------------------------------------------------------- LM2
LMS.append(
    dict(
        lm_no=2,
        title="Forward Commitment and Contingent Claim Features and Instruments",
        summary="Forwards, futures and swaps (obligations) versus options and credit derivatives (rights).",
        los=[
            (
                "2.a",
                "define",
                "Define forward contracts, futures contracts, swaps, options and credit derivatives, "
                "and compare their basic characteristics.",
            ),
            ("2.b", "determine", "Determine the value at expiration and profit of derivatives."),
            ("2.c", "contrast", "Contrast forward commitments with contingent claims."),
        ],
        topics=[
            topic(
                "Forward commitments",
                L(
                    "**Forward**: OTC agreement to buy or sell at a fixed price on a future date. Long payoff at "
                    "expiry = S_T − F₀.",
                    "**Futures**: exchange-traded forward with daily **mark-to-market** and margin.",
                    "**Swap**: exchange of a series of cash flows, e.g. fixed for floating interest. Equivalent to a "
                    "series of forwards.",
                ),
                EX(
                    "Meera agrees to buy 1 kg of silver in three months at ₹90,000 (forward). At expiry silver is "
                    "₹95,000. Long payoff = 95,000 − 90,000 = **+₹5,000**; the short loses ₹5,000."
                ),
                WO("Forward commitments are **symmetric**: both gains and losses can be large for either side."),
            ),
            topic(
                "Contingent claims: options and credit derivatives",
                T(
                    ["", "Call", "Put"],
                    ["Buyer's right", "Buy at strike X", "Sell at strike X"],
                    ["Payoff at expiry (long)", "max(0, S_T − X)", "max(0, X − S_T)"],
                    ["Long profit", "max(0, S_T − X) − c₀", "max(0, X − S_T) − p₀"],
                    ["Breakeven", "X + c₀", "X − p₀"],
                ),
                L(
                    "The buyer pays a **premium** and has a right, not an obligation. The writer has the obligation.",
                    "**European** options exercise only at expiry; **American** any time before.",
                    "**Credit default swap (CDS)**: protection buyer pays a periodic premium; seller pays if a credit "
                    "event occurs on the reference entity.",
                ),
                EX(
                    "A call on Infosys with strike ₹1,500 costs ₹40. At expiry the share is ₹1,580. Payoff = 80; "
                    "profit = 80 − 40 = **₹40**. Breakeven = 1,540. A put with the same strike at ₹30 expires "
                    "worthless: the buyer loses ₹30."
                ),
                WO("The maximum loss for an option buyer is the premium; for a call writer it is unlimited."),
            ),
        ],
        revision=sheet(
            "Long forward = S_T − F₀ · Long call = max(0, S_T − X) − c₀ · Long put = max(0, X − S_T) − p₀",
            ("Forward commitment", "Obligation; symmetric payoff"),
            ("Contingent claim", "Right; asymmetric payoff"),
            ("Futures", "Standardised forward with daily MTM"),
            ("Swap", "Series of forwards"),
            ("Call breakeven", "X + premium"),
            ("Put breakeven", "X − premium"),
            ("CDS", "Premium for protection against a credit event"),
        ),
        questions=[
            q(
                "E",
                "A forward contract differs from a futures contract because it is typically:",
                ["Traded on an exchange", "Customised and traded over the counter", "Marked to market daily"],
                1,
                "Forwards are private OTC contracts; futures are standardised and exchange-traded.",
                "2.a",
            ),
            q(
                "E",
                "The buyer of a call option has:",
                ["The obligation to buy", "The right to sell", "The right, but not the obligation, to buy"],
                2,
                "A call gives the holder the right to buy at the strike.",
                "2.a",
            ),
            q(
                "M",
                "A long forward at ₹90,000 expires with the spot price at ₹95,000. The long's payoff is:",
                ["+₹5,000", "−₹5,000", "₹0"],
                0,
                "S_T − F₀ = 95,000 − 90,000.",
                "2.b",
            ),
            q(
                "M",
                "A call with strike ₹1,500 costs ₹40. At expiry the stock is at ₹1,580. The buyer's profit is:",
                ["₹80", "₹40", "₹120"],
                1,
                "Payoff 80 − premium 40 = 40.",
                "2.b",
            ),
            q(
                "M",
                "The breakeven price at expiry for a long put with strike ₹500 and premium ₹25 is:",
                ["₹525", "₹500", "₹475"],
                2,
                "Put breakeven = X − premium.",
                "2.b",
            ),
            q(
                "H",
                "The maximum loss for the writer of an uncovered call is:",
                ["The premium received", "Unlimited", "The strike price"],
                1,
                "The share price can rise without limit.",
                "2.b",
            ),
            q(
                "E",
                "Which is a contingent claim?",
                ["A forward", "An interest rate swap", "An option"],
                2,
                "Options pay off only if certain conditions are met.",
                "2.c",
            ),
            q(
                "M",
                "In a credit default swap, the protection seller:",
                ["Pays periodic premiums", "Pays compensation if a credit event occurs", "Owns the reference bond"],
                1,
                "The buyer pays premiums; the seller pays on default.",
                "2.a",
            ),
            q(
                "H",
                "An interest rate swap can be viewed as:",
                ["A series of forward contracts", "A single call option", "A futures contract on equities"],
                0,
                "Each exchange date is like a forward on the reference rate.",
                "2.c",
            ),
            q(
                "E",
                "An option that can be exercised only on the expiry date is:",
                ["American", "European", "Bermudan"],
                1,
                "European options exercise at expiry only.",
                "2.a",
            ),
        ],
        flashcards=[
            fc("Forward commitment vs contingent claim", "Obligation (symmetric) vs right (asymmetric)."),
            fc("Long call payoff", "max(0, S_T − X)."),
            fc("Long put payoff", "max(0, X − S_T)."),
            fc("Call and put breakevens", "Call: X + premium. Put: X − premium."),
            fc("European vs American", "Exercise at expiry only vs any time to expiry."),
            fc("Credit default swap", "Protection buyer pays premiums; seller pays on a credit event."),
        ],
    )
)

# ---------------------------------------------------------------- LM3
LMS.append(
    dict(
        lm_no=3,
        title="Derivative Benefits, Risks, and Issuer and Investor Uses",
        summary="Why markets need derivatives, the risks they bring, and how companies and investors use them.",
        los=[
            ("3.a", "describe", "Describe benefits and risks of derivative instruments."),
            ("3.b", "compare", "Compare the use of derivatives among issuers and investors."),
        ],
        topics=[
            topic(
                "Benefits and risks",
                L(
                    "**Benefits**: risk transfer and hedging; **price discovery** (futures prices reveal expected "
                    "spot prices); lower transaction costs; operational ease such as shorting; more efficient "
                    "markets.",
                    "**Risks**: high **leverage** magnifies losses; complexity; **counterparty credit risk**; "
                    "**liquidity** risk from margin calls; **basis risk** when hedge and exposure differ; "
                    "**systemic risk** when large positions fail together.",
                ),
                FUN(
                    "A derivative is like a kitchen knife: brilliant for cooking, dangerous in the wrong hands, "
                    "and the hospital bill is not the knife's fault."
                ),
            ),
            topic(
                "How issuers and investors use them",
                T(
                    ["User", "Typical use"],
                    ["Issuer (company)", "Hedge interest rates on debt, FX on exports and imports, commodity inputs"],
                    ["Investor", "Modify portfolio exposure cheaply, hedge, replicate a market, express views"],
                ),
                H("Hedge accounting for issuers"),
                L(
                    "**Cash flow hedge**: hedges variable future cash flows, e.g. pay-fixed swap on floating debt.",
                    "**Fair value hedge**: hedges the value of an asset or liability, e.g. receive-fixed swap on "
                    "fixed-rate debt.",
                    "**Net investment hedge**: hedges FX on a foreign subsidiary.",
                ),
                EX(
                    "Bharat Motors exports to the US and expects $10 million in six months. It sells dollars forward "
                    "at ₹83.5. Whether the rupee strengthens to 81 or weakens to 86, it receives ₹83.5 crore. The "
                    "hedge removes FX risk but also gives up any windfall."
                ),
                WO(
                    "Basis risk: hedging jet fuel with crude oil futures leaves the airline exposed to the gap "
                    "between the two prices."
                ),
            ),
        ],
        revision=sheet(
            "Hedge accounting: cash flow · fair value · net investment",
            ("Price discovery", "Futures signal expected prices"),
            ("Leverage risk", "Small moves, big losses"),
            ("Basis risk", "Hedge and exposure move differently"),
            ("Counterparty risk", "Other side may default"),
            ("Cash flow hedge", "Fix variable cash flows"),
            ("Fair value hedge", "Protect asset or liability value"),
            ("Net investment hedge", "FX on a foreign subsidiary"),
        ),
        questions=[
            q(
                "E",
                "Futures prices helping markets estimate future spot prices is an example of:",
                ["Price discovery", "Counterparty risk", "Basis risk"],
                0,
                "Derivative markets reveal information about expected prices.",
                "3.a",
            ),
            q(
                "M",
                "An airline hedges jet fuel costs with crude oil futures. The main remaining risk is:",
                ["Systemic risk", "Basis risk", "Settlement risk"],
                1,
                "Jet fuel and crude prices do not move exactly together.",
                "3.a",
            ),
            q(
                "M",
                "A company with floating-rate debt enters a pay-fixed swap. Under hedge accounting this is most "
                "likely a:",
                ["Fair value hedge", "Net investment hedge", "Cash flow hedge"],
                2,
                "It fixes uncertain interest cash flows.",
                "3.b",
            ),
            q(
                "H",
                "A company with fixed-rate debt enters a receive-fixed, pay-floating swap to offset changes in the "
                "debt's value. This is a:",
                ["Fair value hedge", "Cash flow hedge", "Speculative position"],
                0,
                "It protects against changes in the liability's fair value.",
                "3.b",
            ),
            q(
                "E",
                "Which is a risk of derivatives?",
                ["Lower transaction costs", "Leverage that magnifies losses", "Risk transfer"],
                1,
                "Leverage cuts both ways.",
                "3.a",
            ),
            q(
                "M",
                "An exporter expecting $10 million sells dollars forward at ₹83.5. If the spot rate at receipt is ₹86, "
                "the exporter:",
                ["Receives ₹86 crore", "Receives ₹83.5 crore", "Loses ₹2.5 crore in cash"],
                1,
                "The forward locks the rate; it gives up the upside.",
                "3.b",
            ),
            q(
                "M",
                "Investors commonly use equity index futures to:",
                ["Change market exposure quickly and cheaply", "Avoid all market risk forever", "Earn dividends"],
                0,
                "Futures adjust beta without trading every stock.",
                "3.b",
            ),
            q(
                "H",
                "Systemic risk from derivatives refers to:",
                [
                    "Risk of one small option expiring worthless",
                    "Risk that failures spread across the financial system",
                    "The risk of high transaction costs",
                ],
                1,
                "Large, interconnected positions can transmit losses across institutions.",
                "3.a",
            ),
            q(
                "E",
                "Hedging a foreign subsidiary's value against currency moves is a:",
                ["Net investment hedge", "Cash flow hedge", "Fair value hedge"],
                0,
                "It hedges a net investment abroad.",
                "3.b",
            ),
            q(
                "M",
                "Liquidity risk for a futures hedger mainly arises from:",
                ["Margin calls requiring cash", "The premium paid upfront", "Exercise rights"],
                0,
                "Daily losses must be met in cash even if the hedged item gains later.",
                "3.a",
            ),
        ],
        flashcards=[
            fc("Benefits of derivatives", "Risk transfer, price discovery, low costs, efficiency."),
            fc("Risks of derivatives", "Leverage, counterparty, liquidity, basis, systemic."),
            fc("Basis risk", "Hedge and hedged item do not move together exactly."),
            fc("Cash flow hedge", "Fixes variable cash flows, e.g. pay-fixed swap on floating debt."),
            fc("Fair value hedge", "Protects value, e.g. receive-fixed swap on fixed debt."),
            fc("Net investment hedge", "Hedges FX on a foreign subsidiary."),
        ],
    )
)

# ---------------------------------------------------------------- LM4
LMS.append(
    dict(
        lm_no=4,
        title="Arbitrage, Replication, and the Cost of Carry in Pricing Derivatives",
        summary="No-arbitrage pricing, replication, and how carry costs and benefits set forward prices.",
        los=[
            (
                "4.a",
                "explain",
                "Explain how the concepts of arbitrage and replication are used in pricing derivatives.",
            ),
            (
                "4.b",
                "explain",
                "Explain the difference between the spot and expected future price of an underlying "
                "and the cost of carry associated with holding the underlying asset.",
            ),
        ],
        topics=[
            topic(
                "Arbitrage and replication",
                P(
                    "**Arbitrage** is a riskless profit with no net investment. If two portfolios have identical "
                    "future "
                    "payoffs, they must cost the same today (**law of one price**). Derivatives are priced so that no "
                    "arbitrage exists."
                ),
                P(
                    "**Replication**: a long forward can be replicated by borrowing money to buy the underlying and "
                    "holding it until expiry. So the forward price must equal the cost of that strategy."
                ),
                FX("F₀(T) = S₀ × (1 + r)^T   (no carry costs or benefits)"),
                EX(
                    "A share trades at ₹1,000, pays no dividend, and the one-year rate is 6%. F₀ = 1,000 × 1.06 = "
                    "**₹1,060**. If the forward traded at ₹1,080, sell the forward, borrow ₹1,000, buy the share; at "
                    "expiry deliver the share for ₹1,080 and repay ₹1,060: riskless profit ₹20."
                ),
            ),
            topic(
                "Cost of carry",
                P(
                    "Holding the underlying can generate **benefits** (dividends, coupons, convenience yield) and "
                    "**costs** (storage, insurance). Benefits lower the forward price; costs raise it."
                ),
                FX("F₀(T) = [S₀ − PV(benefits) + PV(costs)] × (1 + r)^T  ·  continuous: F₀ = S₀ e^{(r + c − i)T}"),
                EX(
                    "Gold spot ₹70,000 per 10 g, storage costs with a PV of ₹500, rate 5%, one year. F₀ = (70,000 + "
                    "500) × "
                    "1.05 = **₹74,025**."
                ),
                WO(
                    "Risk-neutral pricing: the forward price does not depend on the expected future spot price or on "
                    "investors' risk preferences, only on spot, rates and carry."
                ),
                FUN(
                    "Arbitrageurs are the people who notice the same mango is ₹40 at one stall and ₹50 at the next. "
                    "After a few minutes, both stalls charge ₹45."
                ),
            ),
        ],
        revision=sheet(
            "F₀ = (S₀ − PV benefits + PV costs) × (1 + r)^T",
            ("Arbitrage", "Riskless profit, no investment"),
            ("Law of one price", "Same payoff, same price"),
            ("Replication", "Borrow and buy underlying = long forward"),
            ("Carry benefits", "Dividends, coupons, convenience yield: lower F₀"),
            ("Carry costs", "Storage, insurance: raise F₀"),
            ("Risk-neutral pricing", "No need for expected spot or risk aversion"),
        ),
        questions=[
            q(
                "E",
                "Arbitrage is best described as:",
                [
                    "A riskless profit with no net investment",
                    "A high-risk speculative trade",
                    "A hedge with basis risk",
                ],
                0,
                "Arbitrage earns a certain gain without committing capital.",
                "4.a",
            ),
            q(
                "M",
                "A non-dividend share trades at ₹1,000 and the one-year rate is 6%. The no-arbitrage one-year forward "
                "price is:",
                ["₹1,000", "₹1,060", "₹940"],
                1,
                "1,000 × 1.06 = 1,060.",
                "4.a",
            ),
            q(
                "H",
                "With spot ₹1,000, rate 6% and a one-year forward trading at ₹1,080, an arbitrageur should:",
                [
                    "Buy the forward and short the share",
                    "Do nothing",
                    "Sell the forward, borrow ₹1,000 and buy the share",
                ],
                2,
                "The forward is too expensive; this cash-and-carry trade earns ₹20.",
                "4.a",
            ),
            q(
                "M",
                "A long forward can be replicated by:",
                ["Borrowing to buy the underlying", "Lending cash and shorting the underlying", "Buying a put"],
                0,
                "Buying the asset with borrowed money gives the same payoff at expiry.",
                "4.a",
            ),
            q(
                "M",
                "Dividends paid by the underlying share will make its forward price:",
                ["Higher", "Lower", "Unchanged"],
                1,
                "Benefits of holding the asset reduce the forward price.",
                "4.b",
            ),
            q(
                "M",
                "Gold spot is ₹70,000, PV of storage costs ₹500, and the one-year rate 5%. The forward price is "
                "closest to:",
                ["₹74,025", "₹73,500", "₹73,475"],
                0,
                "(70,000 + 500) × 1.05 = 74,025.",
                "4.b",
            ),
            q(
                "H",
                "Under no-arbitrage pricing, the forward price depends on:",
                [
                    "Investors' expectations of the future spot price",
                    "Spot price, interest rate and carry",
                    "The risk aversion of the buyer",
                ],
                1,
                "Risk-neutral pricing removes the need for expectations.",
                "4.b",
            ),
            q(
                "E",
                "Storage and insurance costs on a commodity are examples of:",
                ["Carry benefits", "Carry costs", "Convenience yield"],
                1,
                "They raise the cost of holding.",
                "4.b",
            ),
            q(
                "M",
                "Convenience yield is:",
                ["A benefit of holding the physical commodity", "A storage cost", "A transaction fee"],
                0,
                "It reflects the value of having the physical asset on hand.",
                "4.b",
            ),
            q(
                "H",
                "The law of one price states that:",
                [
                    "All assets have the same price",
                    "Assets with identical future cash flows must have the same price today",
                    "Prices never change",
                ],
                1,
                "Otherwise an arbitrage would exist.",
                "4.a",
            ),
        ],
        flashcards=[
            fc("Arbitrage", "Riskless profit with no net investment."),
            fc("No-arbitrage forward (no carry)", "F₀ = S₀ (1 + r)^T."),
            fc("Forward with carry", "F₀ = (S₀ − PV benefits + PV costs)(1 + r)^T."),
            fc("Replicating a long forward", "Borrow and buy the underlying."),
            fc("Carry benefit examples", "Dividends, coupons, convenience yield."),
            fc("Risk-neutral pricing", "Price uses only spot, rate, carry; not expected spot."),
        ],
    )
)

# ---------------------------------------------------------------- LM5
LMS.append(
    dict(
        lm_no=5,
        title="Pricing and Valuation of Forward Contracts and for an Underlying with Varying Maturities",
        summary="Forward price versus forward value, valuing a forward during its life, and forward rates.",
        los=[
            (
                "5.a",
                "explain",
                "Explain how the value and price of a forward contract are determined at "
                "initiation, during the life of the contract and at expiration.",
            ),
            (
                "5.b",
                "explain",
                "Explain how forward rates are determined for an underlying with a term structure "
                "and describe their uses.",
            ),
        ],
        topics=[
            topic(
                "Price versus value",
                P(
                    "The **forward price** F₀ is fixed at the start and set so the contract's **value is zero** at "
                    "initiation. As the spot price moves, the contract gains or loses **value**."
                ),
                FX("Value of long forward at t: V_t = S_t − PV(benefits) + PV(costs) − F₀ ÷ (1 + r)^(T − t)"),
                EX(
                    "A one-year forward on a non-dividend share was agreed at ₹1,060. Six months later the share is "
                    "₹1,100 and the rate is 6%. V = 1,100 − 1,060 ÷ 1.06^0.5 = 1,100 − 1,029.6 = **₹70.4** to the long."
                ),
                WO(
                    "At expiry V_T = S_T − F₀. At initiation V₀ = 0. Do not confuse the forward **price** (a "
                    "number in the contract) with its **value** (what it is worth now)."
                ),
            ),
            topic(
                "Forward rates and FRAs",
                P(
                    "From spot (zero) rates we can derive **implied forward rates**: the rate for a future period that "
                    "makes investing for the long period equal to rolling short-period investments."
                ),
                FX("(1 + z₂)² = (1 + z₁)(1 + f(1,1))"),
                EX(
                    "One-year spot rate 5%, two-year spot rate 6%. f(1,1) = 1.06² ÷ 1.05 − 1 = 1.1236 ÷ 1.05 − 1 = "
                    "**7.01%**."
                ),
                P(
                    "A **forward rate agreement (FRA)** locks in an interest rate for a future period. The long (pay "
                    "fixed) gains if the market rate ends above the FRA rate."
                ),
                FUN(
                    "An implied forward rate is the market whispering what it thinks rates will be next year, "
                    "while charging you for listening."
                ),
            ),
        ],
        revision=sheet(
            "V_t (long) = S_t − PV(benefits) + PV(costs) − F₀/(1 + r)^(T−t) · V₀ = 0 · V_T = S_T − F₀",
            ("Forward price", "Fixed in the contract; set so V₀ = 0"),
            ("Forward value", "Changes with spot and rates"),
            ("Implied forward", "(1 + z₂)² = (1 + z₁)(1 + f)"),
            ("FRA long", "Pays fixed; gains if rates rise"),
            ("At expiry", "Value = spot − forward price"),
        ),
        questions=[
            q(
                "E",
                "At initiation, the value of a forward contract is:",
                ["Zero", "Equal to the forward price", "Equal to the spot price"],
                0,
                "The forward price is set so neither side pays anything upfront.",
                "5.a",
            ),
            q(
                "M",
                "A long forward has a forward price of ₹1,060. At expiry the spot price is ₹1,020. The value to the "
                "long is:",
                ["+₹40", "−₹40", "₹0"],
                1,
                "S_T − F₀ = 1,020 − 1,060.",
                "5.a",
            ),
            q(
                "H",
                "A one-year forward on a non-dividend share was agreed at ₹1,060. After six months the share is at "
                "₹1,100 and the annual rate is 6%. The value of the long position is closest to:",
                ["₹40.0", "₹70.4", "₹100.0"],
                1,
                "1,100 − 1,060/1.06^0.5 = 1,100 − 1,029.6 = 70.4.",
                "5.a",
            ),
            q(
                "M",
                "The one-year spot rate is 5% and the two-year spot rate is 6%. The one-year rate one year from now "
                "is closest to:",
                ["7.0%", "5.5%", "6.0%"],
                0,
                "1.06²/1.05 − 1 = 7.01%.",
                "5.b",
            ),
            q(
                "M",
                "The long side of a forward rate agreement benefits when:",
                ["Rates fall below the FRA rate", "Rates rise above the FRA rate", "Rates stay unchanged"],
                1,
                "The long pays fixed and receives the market rate.",
                "5.b",
            ),
            q(
                "E",
                "The forward price of a contract:",
                ["Changes every day", "Is fixed when the contract is agreed", "Is always zero"],
                1,
                "Price is fixed; value changes.",
                "5.a",
            ),
            q(
                "H",
                "If the underlying pays a dividend during the contract, the value of a long forward during its life:",
                [
                    "Ignores the dividend",
                    "Is reduced by the present value of the remaining dividend",
                    "Is increased by the dividend",
                ],
                1,
                "Benefits reduce the long's value.",
                "5.a",
            ),
            q(
                "M",
                "An implied forward rate makes an investor indifferent between:",
                [
                    "Investing for the long period and rolling over shorter investments",
                    "Buying stocks and bonds",
                    "Fixed and floating swaps",
                ],
                0,
                "That is the no-arbitrage definition.",
                "5.b",
            ),
            q(
                "E",
                "Implied forward rates are derived from:",
                ["Equity prices", "The term structure of spot rates", "Exchange rates only"],
                1,
                "Spot rates for different maturities imply forward rates.",
                "5.b",
            ),
            q(
                "M",
                "During its life, a long forward position gains value when:",
                ["The underlying's spot price rises", "Storage costs fall", "The forward price is renegotiated"],
                0,
                "Higher spot means the right to buy at F₀ is worth more.",
                "5.a",
            ),
        ],
        flashcards=[
            fc("Forward value at initiation", "Zero."),
            fc("Forward value during life (long)", "S_t − PV(benefits) + PV(costs) − F₀/(1 + r)^(T−t)."),
            fc("Forward value at expiry", "S_T − F₀."),
            fc("Price vs value", "Price is fixed in the contract; value moves with the market."),
            fc("Implied forward rate", "(1 + z₂)² = (1 + z₁)(1 + f(1,1))."),
            fc("FRA long", "Pays fixed; gains if the reference rate rises."),
        ],
    )
)

# ---------------------------------------------------------------- LM6
LMS.append(
    dict(
        lm_no=6,
        title="Pricing and Valuation of Futures Contracts",
        summary="Mark-to-market, margin mechanics, and why futures and forward prices can differ.",
        los=[
            ("6.a", "compare", "Compare the value and price of forward and futures contracts."),
            ("6.b", "calculate", "Calculate and interpret variation margin and the effect of mark-to-market."),
            ("6.c", "explain", "Explain why forward and futures prices differ."),
        ],
        topics=[
            topic(
                "Mark-to-market and margin",
                L(
                    "**Initial margin**: deposit to open a position.",
                    "**Maintenance margin**: minimum balance. Below it, a **margin call** requires topping up back to "
                    "the **initial** margin (**variation margin**).",
                    "Gains and losses are settled **daily**, so a futures contract's value resets to zero each day.",
                ),
                EX(
                    "Long 1 gold futures (100 g) at ₹7,000/g; initial margin ₹50,000, maintenance ₹40,000. Day 1 price "
                    "falls to ₹6,880: loss 120 × 100 = ₹12,000, balance ₹38,000 < 40,000. Margin call: deposit "
                    "**₹12,000** to restore ₹50,000."
                ),
                WO("Variation margin restores the account to the **initial** margin, not to the maintenance level."),
            ),
            topic(
                "Futures versus forward prices",
                P(
                    "With constant interest rates, futures and forward prices are equal. When rates are random, daily "
                    "settlement matters:"
                ),
                L(
                    "**Positive correlation** between underlying prices and interest rates: gains arrive when rates "
                    "are "
                    "high (reinvest at high rates), so long futures are more attractive and **futures price > "
                    "forward**.",
                    "**Negative correlation** (e.g. bond futures): **futures price < forward**.",
                    "Interest rate futures are quoted as 100 − rate; a 1 bp change has a fixed value (basis point "
                    "value).",
                ),
                FUN("Mark-to-market is a strict landlord: rent is due every evening, not at the end of the lease."),
            ),
        ],
        revision=sheet(
            "Variation margin = initial margin − current balance (when balance < maintenance)",
            ("Initial margin", "Deposit to open"),
            ("Maintenance margin", "Trigger level for a call"),
            ("Variation margin", "Restores to initial"),
            ("Daily settlement", "Futures value resets to zero"),
            ("Positive corr. with rates", "Futures price > forward price"),
            ("Negative corr. with rates", "Futures price < forward price"),
        ),
        questions=[
            q(
                "E",
                "Futures contracts differ from forwards mainly because futures are:",
                ["Marked to market daily", "Customised", "Free of margin"],
                0,
                "Daily settlement is the key difference.",
                "6.a",
            ),
            q(
                "M",
                "A trader's futures margin account falls below the maintenance margin. He must deposit enough to "
                "bring the balance back to the:",
                ["Maintenance margin", "Initial margin", "Zero level"],
                1,
                "Variation margin restores the initial margin.",
                "6.b",
            ),
            q(
                "M",
                "Initial margin is ₹50,000 and maintenance ₹40,000. After a ₹12,000 loss, the variation margin "
                "required is:",
                ["₹2,000", "₹12,000", "₹10,000"],
                1,
                "Balance 38,000 < 40,000; top up to 50,000 = 12,000.",
                "6.b",
            ),
            q(
                "H",
                "If underlying prices are positively correlated with interest rates, futures prices will tend to be:",
                ["Lower than forward prices", "Equal to forward prices", "Higher than forward prices"],
                2,
                "Long futures gains can be reinvested at higher rates.",
                "6.c",
            ),
            q(
                "M",
                "With constant interest rates, futures and forward prices are:",
                ["Equal", "Always different", "Unrelated"],
                0,
                "The timing of settlement no longer matters.",
                "6.c",
            ),
            q(
                "E",
                "At the end of each trading day after settlement, a futures contract's value is:",
                ["The futures price", "Zero", "The initial margin"],
                1,
                "Gains and losses are paid daily.",
                "6.a",
            ),
            q(
                "M",
                "A long gold futures of 100 g at ₹7,000/g settles the next day at ₹6,880. The long's daily loss is:",
                ["₹120", "₹1,200", "₹12,000"],
                2,
                "120 × 100 = 12,000.",
                "6.b",
            ),
            q(
                "H",
                "Bond futures, whose underlying falls when rates rise, are most likely priced:",
                ["Below equivalent forwards", "Above equivalent forwards", "At zero"],
                0,
                "Negative correlation with rates makes futures less attractive than forwards.",
                "6.c",
            ),
            q(
                "M",
                "An interest rate futures contract is typically quoted as:",
                ["The rate itself", "100 minus the annualised rate", "A percentage of par value"],
                1,
                "So prices rise when rates fall, like bonds.",
                "6.a",
            ),
            q(
                "E",
                "The deposit required to open a futures position is the:",
                ["Variation margin", "Initial margin", "Premium"],
                1,
                "Initial margin opens the position.",
                "6.b",
            ),
        ],
        flashcards=[
            fc("Mark-to-market", "Gains and losses settled daily; value resets to zero."),
            fc("Initial vs maintenance margin", "Deposit to open vs level that triggers a call."),
            fc("Variation margin", "Restores account to initial margin."),
            fc("Futures vs forward price: positive correlation with rates", "Futures price higher."),
            fc("Futures vs forward price: negative correlation", "Futures price lower."),
            fc("Rate futures quote", "100 − annualised rate."),
        ],
    )
)

# ---------------------------------------------------------------- LM7
LMS.append(
    dict(
        lm_no=7,
        title="Pricing and Valuation of Interest Rate and Other Swaps",
        summary="Swaps as portfolios of forwards, the par swap rate, and valuing a swap after initiation.",
        los=[
            (
                "7.a",
                "describe",
                "Describe how swap contracts are similar to but different from a series of forward contracts.",
            ),
            ("7.b", "contrast", "Contrast the value and price of swaps."),
        ],
        topics=[
            topic(
                "Swaps as a series of forwards",
                P(
                    "In a plain-vanilla **interest rate swap**, one side pays a fixed rate and the other a floating "
                    "reference rate on a notional amount; only the net amount changes hands. Each settlement is like a "
                    "forward, but a swap uses **one fixed rate** for all periods, so individual 'forwards' are "
                    "off-market even though the whole swap has zero value at the start."
                ),
                FX("Par swap rate s = (1 − DF_N) ÷ (DF₁ + DF₂ + … + DF_N)"),
                EX(
                    "Two-year annual swap with discount factors 0.97 (year 1) and 0.94 (year 2). s = (1 − 0.94) ÷ "
                    "(0.97 + 0.94) = 0.06 ÷ 1.91 = **3.14%**."
                ),
            ),
            topic(
                "Value after initiation",
                P(
                    "The swap **price** is the fixed rate agreed. Its **value** starts at zero and changes as rates "
                    "move. "
                    "A **pay-fixed** party gains when rates rise, because it pays the old lower rate while receiving a "
                    "higher floating rate."
                ),
                FX("Value to fixed payer ≈ (new swap rate − old fixed rate) × notional × Σ remaining discount factors"),
                EX(
                    "Rohit's firm pays 3% fixed on ₹100 crore with two years left. The current two-year swap rate is "
                    "4% "
                    "and discount factors are 0.96 and 0.92. Value = (0.04 − 0.03) × 100 × (0.96 + 0.92) = "
                    "**₹1.88 crore** gain to the fixed payer."
                ),
                WO("Pay-fixed = like being short a fixed-rate bond: it gains when rates rise."),
                FUN(
                    "A pay-fixed swap is like booking a festival-season flight in July. When fares jump in October, "
                    "you look like a genius."
                ),
            ),
        ],
        revision=sheet(
            "s = (1 − DF_N) ÷ ΣDF · Value (pay-fixed) = (s_new − s_old) × N × ΣDF_remaining",
            ("Swap", "Series of forwards with one fixed rate"),
            ("Value at start", "Zero"),
            ("Price", "The fixed swap rate"),
            ("Pay-fixed gains", "When rates rise"),
            ("Receive-fixed gains", "When rates fall"),
            ("Net settlement", "Only the difference is paid"),
        ),
        questions=[
            q(
                "E",
                "At initiation, a plain-vanilla interest rate swap has a value of:",
                ["Zero", "The notional amount", "The fixed rate"],
                0,
                "The fixed rate is set so that the swap is worth zero at the start.",
                "7.b",
            ),
            q(
                "M",
                "A swap is similar to a series of forwards except that:",
                [
                    "A swap uses a single fixed rate for all periods",
                    "Swaps are always exchange-traded",
                    "Forwards have no counterparty",
                ],
                0,
                "Each period's forward rate differs, but the swap uses one rate.",
                "7.a",
            ),
            q(
                "M",
                "Discount factors for years 1 and 2 are 0.97 and 0.94. The two-year par swap rate is closest to:",
                ["3.14%", "6.00%", "3.00%"],
                0,
                "(1 − 0.94)/(0.97 + 0.94) = 3.14%.",
                "7.b",
            ),
            q(
                "M",
                "The party paying fixed in an interest rate swap gains when:",
                ["Rates fall", "Rates rise", "The notional falls"],
                1,
                "It pays a below-market rate and receives more floating.",
                "7.b",
            ),
            q(
                "H",
                "A firm pays 3% fixed on ₹100 crore with two years left. The current swap rate is 4% and remaining "
                "discount factors are 0.96 and 0.92. The swap value to the firm is closest to:",
                ["−₹1.88 crore", "+₹1.00 crore", "+₹1.88 crore"],
                2,
                "0.01 × 100 × 1.88 = 1.88 gain.",
                "7.b",
            ),
            q(
                "E",
                "In a plain-vanilla interest rate swap, which cash flow is exchanged?",
                ["The notional principal", "Only the net interest difference", "Equity dividends"],
                1,
                "Payments are netted; notional is not exchanged.",
                "7.a",
            ),
            q(
                "M",
                "A receive-fixed swap position is economically similar to:",
                [
                    "Being long a fixed-rate bond and short a floating-rate note",
                    "Being short a fixed-rate bond",
                    "Owning a call option",
                ],
                0,
                "It gains when rates fall, like a fixed bond.",
                "7.a",
            ),
            q(
                "H",
                "The 'price' of a swap is best described as:",
                ["Its market value", "The fixed rate agreed at initiation", "The notional"],
                1,
                "Swap price = fixed rate; value changes over time.",
                "7.b",
            ),
            q(
                "M",
                "Which statement about the individual 'forwards' embedded in a swap is correct?",
                [
                    "Each has zero value at initiation",
                    "They can have non-zero values though the swap's total is zero",
                    "They are all identical",
                ],
                1,
                "Using one fixed rate makes some periods positive and others negative.",
                "7.a",
            ),
            q(
                "E",
                "A company with floating-rate debt that wants fixed payments should:",
                ["Receive fixed in a swap", "Pay fixed in a swap", "Buy a call option"],
                1,
                "Paying fixed and receiving floating converts floating debt to fixed.",
                "7.a",
            ),
        ],
        flashcards=[
            fc("Swap = ?", "Series of forwards with one fixed rate."),
            fc("Par swap rate", "(1 − DF_N) ÷ sum of DFs."),
            fc("Swap value at initiation", "Zero."),
            fc("Pay-fixed gains when", "Rates rise."),
            fc("Swap price vs value", "Price = fixed rate; value moves with rates."),
            fc("Converting floating debt to fixed", "Enter a pay-fixed swap."),
        ],
    )
)

# ---------------------------------------------------------------- LM8
LMS.append(
    dict(
        lm_no=8,
        title="Pricing and Valuation of Options",
        summary="Exercise value, time value, moneyness, lower bounds, and the factors that drive option prices.",
        los=[
            ("8.a", "explain", "Explain the exercise value, moneyness and time value of an option."),
            (
                "8.b",
                "contrast",
                "Contrast the use of arbitrage and replication concepts in pricing forward "
                "commitments and contingent claims.",
            ),
            (
                "8.c",
                "identify",
                "Identify the factors that determine the value of an option and describe how each "
                "factor affects the value of an option.",
            ),
        ],
        topics=[
            topic(
                "Exercise value and time value",
                L(
                    "**Exercise (intrinsic) value**: call = max(0, S − X); put = max(0, X − S).",
                    "**Moneyness**: a call is **in the money** if S > X, at the money if S = X, out of the money if "
                    "S < X (reverse for puts).",
                    "**Time value** = option premium − exercise value; it shrinks to zero at expiry (time decay).",
                ),
                EX("Share ₹520, call strike ₹500, premium ₹35. Exercise value = 20; time value = 35 − 20 = **₹15**."),
                FX("European call lower bound: c ≥ max(0, S₀ − X/(1 + r)^T) · put: p ≥ max(0, X/(1 + r)^T − S₀)"),
            ),
            topic(
                "What drives option values",
                T(
                    ["Increase in…", "Call value", "Put value"],
                    ["Underlying price", "↑", "↓"],
                    ["Exercise price", "↓", "↑"],
                    ["Time to expiry", "↑", "↑ (usually)"],
                    ["Volatility", "↑", "↑"],
                    ["Risk-free rate", "↑", "↓"],
                    ["Carry benefits (dividends)", "↓", "↑"],
                ),
                WO(
                    "Volatility raises **both** calls and puts. Higher volatility increases the upside the buyer "
                    "keeps, while the downside is capped at the premium."
                ),
                WO(
                    "Forwards are priced by replication without probabilities; options need a model of possible "
                    "prices, because the payoff is non-linear."
                ),
                FUN(
                    "Volatility is to an option what bad weather is to an umbrella seller. The worse it gets, the "
                    "more everyone wants one."
                ),
            ),
        ],
        revision=sheet(
            "Premium = exercise value + time value · c ≥ max(0, S₀ − X/(1 + r)^T)",
            ("Call ITM", "S > X"),
            ("Put ITM", "S < X"),
            ("Time value", "Premium − exercise value; zero at expiry"),
            ("Volatility ↑", "Calls ↑ and puts ↑"),
            ("Rates ↑", "Calls ↑, puts ↓"),
            ("Dividends ↑", "Calls ↓, puts ↑"),
        ),
        questions=[
            q(
                "E",
                "A call option is in the money when:",
                [
                    "The underlying price is above the strike",
                    "The underlying price is below the strike",
                    "The premium exceeds the strike",
                ],
                0,
                "Exercising would be profitable before the premium.",
                "8.a",
            ),
            q(
                "M",
                "A share trades at ₹520. A call with strike ₹500 costs ₹35. Its time value is:",
                ["₹20", "₹15", "₹35"],
                1,
                "Exercise value 20; time value 35 − 20 = 15.",
                "8.a",
            ),
            q(
                "M",
                "An increase in volatility of the underlying will:",
                ["Increase call values and decrease put values", "Increase both call and put values", "Decrease both"],
                1,
                "Option holders benefit from wider outcomes.",
                "8.c",
            ),
            q(
                "M",
                "An increase in the risk-free rate will, other things equal:",
                ["Increase call values and decrease put values", "Decrease call values", "Increase put values"],
                0,
                "A higher rate lowers the PV of the strike, helping calls and hurting puts.",
                "8.c",
            ),
            q(
                "H",
                "The lower bound of a European call on a non-dividend share with S₀ = ₹100, X = ₹100, r = 5% and "
                "T = 1 is closest to:",
                ["₹0.00", "₹5.00", "₹4.76"],
                2,
                "100 − 100/1.05 = 4.76.",
                "8.a",
            ),
            q(
                "E",
                "At expiry, an option's time value is:",
                ["Zero", "Equal to the premium", "Equal to the strike"],
                0,
                "Only exercise value remains.",
                "8.a",
            ),
            q(
                "M",
                "A higher expected dividend on the underlying will:",
                ["Raise call values", "Lower call values and raise put values", "Not affect options"],
                1,
                "Dividends lower the expected share price.",
                "8.c",
            ),
            q(
                "H",
                "Options cannot be priced by replication with a single static position in the underlying, as "
                "forwards can, mainly because:",
                [
                    "Options have linear payoffs",
                    "Option payoffs are non-linear and depend on the range of possible prices",
                    "Options are always exchange-traded",
                ],
                1,
                "Contingent payoffs need a model of future price paths.",
                "8.b",
            ),
            q(
                "E",
                "A put option is out of the money when:",
                ["S < X", "S > X", "S = 0"],
                1,
                "A put pays only if the price falls below the strike.",
                "8.a",
            ),
            q(
                "M",
                "An increase in the exercise price will:",
                ["Raise call values", "Lower put values", "Lower call values and raise put values"],
                2,
                "Buying gets dearer for calls; selling higher helps puts.",
                "8.c",
            ),
        ],
        flashcards=[
            fc("Exercise value", "Call max(0, S − X); put max(0, X − S)."),
            fc("Time value", "Premium − exercise value; decays to zero."),
            fc("Volatility up", "Calls and puts both rise."),
            fc("Rates up", "Calls rise, puts fall."),
            fc("European call lower bound", "max(0, S₀ − X/(1 + r)^T)."),
            fc("Dividends up", "Calls fall, puts rise."),
        ],
    )
)

# ---------------------------------------------------------------- LM9
LMS.append(
    dict(
        lm_no=9,
        title="Option Replication Using Put–Call Parity",
        summary="Put–call parity, synthetic positions, and put–call–forward parity.",
        los=[
            ("9.a", "explain", "Explain put–call parity for European options."),
            ("9.b", "explain", "Explain put–call forward parity for European options."),
        ],
        topics=[
            topic(
                "Put–call parity",
                FX("S₀ + p₀ = c₀ + X/(1 + r)^T   (protective put = fiduciary call)"),
                P(
                    "A **protective put** (share + put) and a **fiduciary call** (call + risk-free bond paying X) have "
                    "identical payoffs at expiry: the greater of S_T and X. So they must cost the same."
                ),
                EX(
                    "S₀ = ₹100, X = ₹100, r = 5%, one year, call ₹10. PV(X) = 95.24. p₀ = c₀ + PV(X) − S₀ = 10 + "
                    "95.24 − 100 = **₹5.24**."
                ),
                H("Synthetic positions"),
                L(
                    "Synthetic call = S₀ + p₀ − PV(X).",
                    "Synthetic put = c₀ + PV(X) − S₀.",
                    "Synthetic share = c₀ − p₀ + PV(X).",
                ),
                WO("Parity holds for **European** options with the same strike and expiry on the same underlying."),
            ),
            topic(
                "Put–call–forward parity",
                FX("F₀/(1 + r)^T + p₀ = c₀ + X/(1 + r)^T"),
                P(
                    "Replace the share with a forward and a bond paying F₀. Then long call − long put = long forward "
                    "at the strike: c₀ − p₀ = (F₀ − X)/(1 + r)^T."
                ),
                EX("F₀ = ₹105, X = ₹100, r = 5%, one year. c₀ − p₀ = 5 ÷ 1.05 = **₹4.76**."),
                FUN(
                    "Put–call parity is the finance version of 'two ₹50 notes equal one ₹100 note'. If a shop says "
                    "otherwise, buy from one counter and sell to the other."
                ),
            ),
        ],
        revision=sheet(
            "S₀ + p₀ = c₀ + PV(X) · F₀/(1 + r)^T + p₀ = c₀ + PV(X)",
            ("Protective put", "Share + put"),
            ("Fiduciary call", "Call + bond paying X"),
            ("Synthetic put", "c₀ + PV(X) − S₀"),
            ("Synthetic call", "S₀ + p₀ − PV(X)"),
            ("c₀ − p₀", "= S₀ − PV(X) = (F₀ − X)/(1 + r)^T"),
        ),
        questions=[
            q(
                "E",
                "Put–call parity states that:",
                ["S₀ + p₀ = c₀ + PV(X)", "S₀ + c₀ = p₀ + PV(X)", "c₀ = p₀"],
                0,
                "Protective put equals fiduciary call.",
                "9.a",
            ),
            q(
                "M",
                "S₀ = ₹100, X = ₹100, r = 5%, T = 1 and the call costs ₹10. The put value is closest to:",
                ["₹5.24", "₹10.00", "₹14.76"],
                0,
                "10 + 95.24 − 100 = 5.24.",
                "9.a",
            ),
            q(
                "M",
                "A fiduciary call consists of:",
                [
                    "A long call and a risk-free bond that pays the strike at expiry",
                    "A long share and a long put",
                    "A short call and a long put",
                ],
                0,
                "That is the definition.",
                "9.a",
            ),
            q(
                "M",
                "A synthetic put can be created by:",
                [
                    "Buying a call, lending PV(X) and shorting the share",
                    "Buying the share and a call",
                    "Shorting a call and buying the share",
                ],
                0,
                "p₀ = c₀ + PV(X) − S₀.",
                "9.a",
            ),
            q(
                "H",
                "F₀ = ₹105, X = ₹100, r = 5% and T = 1. c₀ − p₀ is closest to:",
                ["₹5.00", "₹4.76", "₹0.00"],
                1,
                "(105 − 100)/1.05 = 4.76.",
                "9.b",
            ),
            q(
                "E",
                "A protective put is:",
                ["Long share plus long put", "Long call plus long bond", "Short share plus short put"],
                0,
                "It sets a floor under a share position.",
                "9.a",
            ),
            q(
                "M",
                "Put–call parity applies to:",
                [
                    "American options with different strikes",
                    "European options with the same strike and expiry",
                    "Any two options",
                ],
                1,
                "The payoffs only match exactly in that case.",
                "9.a",
            ),
            q(
                "H",
                "If the call is priced above its put–call parity value, an arbitrageur would:",
                [
                    "Buy the call and sell the synthetic call",
                    "Sell the call and buy a synthetic call (share + put − bond)",
                    "Do nothing",
                ],
                1,
                "Sell the expensive side, buy the cheap replica.",
                "9.a",
            ),
            q(
                "M",
                "Long call plus short put with the same strike and expiry is equivalent to:",
                ["A long forward at the strike", "A short share", "A risk-free bond"],
                0,
                "c − p replicates a long forward.",
                "9.b",
            ),
            q(
                "E",
                "In put–call–forward parity, the share in standard parity is replaced by:",
                ["A futures margin account", "A forward contract plus a bond paying F₀", "A call option"],
                1,
                "Holding a forward and a bond replicates the share at expiry.",
                "9.b",
            ),
        ],
        flashcards=[
            fc("Put–call parity", "S₀ + p₀ = c₀ + PV(X)."),
            fc("Protective put", "Share + put."),
            fc("Fiduciary call", "Call + bond paying X."),
            fc("Synthetic put", "c₀ + PV(X) − S₀."),
            fc("Put–call–forward parity", "F₀/(1 + r)^T + p₀ = c₀ + PV(X)."),
            fc("Long call − long put", "Long forward at the strike."),
        ],
    )
)

# ---------------------------------------------------------------- LM10
LMS.append(
    dict(
        lm_no=10,
        title="Valuing a Derivative Using a One-Period Binomial Model",
        summary="Up and down moves, the hedge ratio, risk-neutral probabilities and option values.",
        los=[
            ("10.a", "explain", "Explain how to value a derivative using a one-period binomial model."),
            ("10.b", "describe", "Describe the concept of risk neutrality in derivatives pricing."),
        ],
        topics=[
            topic(
                "The one-period binomial model",
                P(
                    "The underlying moves to S⁺ = S₀u or S⁻ = S₀d in one period. Work out the option payoff in each "
                    "state, then discount the **risk-neutral** expected payoff at the risk-free rate."
                ),
                FX("π = (1 + r − d) ÷ (u − d) · c₀ = [πc⁺ + (1 − π)c⁻] ÷ (1 + r)"),
                EX(
                    "S₀ = ₹100, u = 1.2, d = 0.8, r = 5%, call strike ₹100. S⁺ = 120 → c⁺ = 20; S⁻ = 80 → c⁻ = 0. "
                    "π = (1.05 − 0.8) ÷ 0.4 = 0.625. c₀ = 0.625 × 20 ÷ 1.05 = **₹11.90**."
                ),
                H("Replication and the hedge ratio"),
                FX("h = (c⁺ − c⁻) ÷ (S⁺ − S⁻)"),
                P(
                    "Buying h shares and selling one call gives a riskless portfolio. In the example h = 20 ÷ 40 = "
                    "0.5: "
                    "hold half a share per call written."
                ),
            ),
            topic(
                "Risk neutrality",
                P(
                    "π is **not** the real-world probability of an up move. It is the probability that makes the "
                    "underlying earn the risk-free rate. Because the option can be replicated, its price does not "
                    "depend "
                    "on investors' risk preferences or real-world probabilities."
                ),
                WO(
                    "A put uses the same π: p₀ = [πp⁺ + (1 − π)p⁻] ÷ (1 + r). In the example p⁺ = 0, p⁻ = 20, so "
                    "p₀ = 0.375 × 20 ÷ 1.05 = ₹7.14. Check with parity: 11.90 + 95.24 − 100 = 7.14."
                ),
                FUN(
                    "Risk-neutral probability is a polite fiction, like a GPS saying '5 minutes away' in Mumbai "
                    "traffic. It gets you the right price even if it isn't how the world really works."
                ),
            ),
        ],
        revision=sheet(
            "π = (1 + r − d)/(u − d) · Value = [π V⁺ + (1 − π) V⁻]/(1 + r) · h = ΔV/ΔS",
            ("S⁺, S⁻", "S₀u and S₀d"),
            ("Risk-neutral π", "Makes the underlying earn r"),
            ("Hedge ratio", "Shares per option for a riskless hedge"),
            ("Real-world probability", "Not needed"),
            ("Check", "Call and put values satisfy put–call parity"),
        ),
        questions=[
            q(
                "M",
                "With u = 1.2, d = 0.8 and r = 5%, the risk-neutral probability of an up move is:",
                ["0.500", "0.625", "0.750"],
                1,
                "(1.05 − 0.8)/(1.2 − 0.8) = 0.625.",
                "10.a",
            ),
            q(
                "H",
                "S₀ = ₹100, u = 1.2, d = 0.8, r = 5%. A one-period call with strike ₹100 is worth closest to:",
                ["₹11.90", "₹12.50", "₹20.00"],
                0,
                "0.625 × 20/1.05 = 11.90.",
                "10.a",
            ),
            q(
                "M",
                "In the same model, the hedge ratio for the call is:",
                ["0.25", "1.00", "0.50"],
                2,
                "(20 − 0)/(120 − 80) = 0.5.",
                "10.a",
            ),
            q(
                "H",
                "Using the same inputs, a one-period put with strike ₹100 is worth closest to:",
                ["₹7.14", "₹5.24", "₹11.90"],
                0,
                "0.375 × 20/1.05 = 7.14.",
                "10.a",
            ),
            q(
                "M",
                "Risk-neutral probabilities are:",
                [
                    "The real-world chances of each move",
                    "Probabilities that make the underlying's expected return equal the risk-free rate",
                    "Always 50%",
                ],
                1,
                "They come from no-arbitrage, not from forecasts.",
                "10.b",
            ),
            q(
                "E",
                "In a binomial model, the option's expected payoff is discounted at:",
                ["The expected return on the share", "The risk-free rate", "The option's premium"],
                1,
                "Under risk neutrality, the risk-free rate applies.",
                "10.a",
            ),
            q(
                "M",
                "The option price in the binomial model does not depend on:",
                ["The up and down factors", "The risk-free rate", "Investors' risk preferences"],
                2,
                "Replication removes the need for risk preferences.",
                "10.b",
            ),
            q(
                "H",
                "A riskless portfolio in the binomial model is formed by:",
                [
                    "Buying h shares for each call written",
                    "Buying one call and one put",
                    "Lending at the risk-free rate only",
                ],
                0,
                "h shares offset the call's exposure in both states.",
                "10.a",
            ),
            q(
                "E",
                "If the share can only rise to ₹120 or fall to ₹80, the payoff of a ₹100-strike call in the down state "
                "is:",
                ["₹20", "₹0", "₹80"],
                1,
                "The call expires out of the money.",
                "10.a",
            ),
            q(
                "M",
                "If the risk-free rate rises in the binomial model, the risk-neutral probability of an up move:",
                ["Falls", "Rises", "Is unchanged"],
                1,
                "π = (1 + r − d)/(u − d) increases with r.",
                "10.b",
            ),
        ],
        flashcards=[
            fc("Risk-neutral probability", "π = (1 + r − d)/(u − d)."),
            fc("Binomial option value", "[πV⁺ + (1 − π)V⁻]/(1 + r)."),
            fc("Hedge ratio", "(V⁺ − V⁻)/(S⁺ − S⁻)."),
            fc("Is π the real-world probability?", "No. It makes the asset earn the risk-free rate."),
            fc("Discount rate in binomial pricing", "The risk-free rate."),
            fc("Why risk preferences don't matter", "The option can be replicated."),
        ],
    )
)


if __name__ == "__main__":
    # Prototype questions: 52 underlying (LM1); 53 forward vs futures and 54 call buyer (LM2).
    write_pack("dv", "Derivatives", LMS, {"52": 1, "53": 2, "54": 2}, balance_keys=True)
