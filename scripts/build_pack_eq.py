"""Equity Investments content pack.  python scripts/build_pack_eq.py, then re-seed.

LM1–3 already have prototype notes and revision sheets (seed/notes.json) plus 14 prototype questions each, so
here they only get extra questions and flashcards. LM4–8 get the full set.
"""

from packlib import EX, FUN, FX, WO, L, P, T, fc, q, sheet, topic, write_pack

LMS = []

# ---------------------------------------------------------------- LM1
LMS.append(
    dict(
        lm_no=1,
        title="Overview of Equity Securities",
        summary="Types and features of equity, private versus public equity, foreign equity and the cost of equity.",
        los=[
            ("1.a", "describe", "Describe characteristics of types of equity securities."),
            ("1.b", "compare", "Compare the risk and return characteristics of equity securities."),
            ("1.c", "describe", "Describe methods for investing in non-domestic equity securities."),
            (
                "1.d",
                "compare",
                "Compare a company's book value and market value, and its cost of equity, return on "
                "equity and investors' required return.",
            ),
        ],
        topics=[],
        revision=None,
        questions=[
            q(
                "M",
                "With cumulative voting, a shareholder who owns 200 shares and four directors are being elected "
                "can cast:",
                ["200 votes for one director only", "Up to 800 votes for a single director", "50 votes per director"],
                1,
                "Cumulative voting gives shares × seats votes that can be concentrated, helping minority holders.",
                "1.a",
            ),
            q(
                "E",
                "A depository receipt is:",
                [
                    "A security traded locally that represents shares of a foreign company",
                    "A bank deposit certificate",
                    "A type of preference share",
                ],
                0,
                "DRs let investors hold foreign shares through a domestic depository bank.",
                "1.c",
            ),
            q(
                "M",
                "In a sponsored depository receipt, the foreign company:",
                [
                    "Has no involvement",
                    "Is involved, and DR holders usually get voting rights",
                    "Must be unlisted in its home market",
                ],
                1,
                "Sponsored DRs involve the issuer; unsponsored ones do not.",
                "1.c",
            ),
            q(
                "M",
                "A company's net income is ₹120 crore and average book equity is ₹800 crore. Its ROE is:",
                ["15%", "6.7%", "12%"],
                0,
                "ROE = 120 ÷ 800 = 15%.",
                "1.d",
            ),
            q(
                "H",
                "From the company's viewpoint, the investors' minimum required rate of return on its equity is its:",
                ["Return on equity", "Cost of equity", "Dividend yield"],
                1,
                "The investors' required return is the company's cost of equity.",
                "1.d",
            ),
            q(
                "E",
                "Market value of equity typically exceeds book value when investors expect the company to:",
                ["Earn returns above its cost of equity", "Make losses", "Be liquidated soon"],
                0,
                "Book value records past investment; market value prices future value creation.",
                "1.d",
            ),
        ],
        flashcards=[
            fc("Statutory vs cumulative voting", "One vote per share per seat vs votes pooled for one candidate."),
            fc("Depository receipt", "Local security representing foreign shares, held by a depository bank."),
            fc("Book vs market value of equity", "Accounting net assets vs price investors pay for future value."),
        ],
    )
)

# ---------------------------------------------------------------- LM2
LMS.append(
    dict(
        lm_no=2,
        title="Market Organization and Structure",
        summary="Functions of the financial system, market types, orders, positions, margin and market structures.",
        los=[
            ("2.a", "explain", "Explain the main functions of the financial system."),
            (
                "2.b",
                "calculate",
                "Calculate and interpret the leverage ratio, the rate of return on a margin "
                "transaction and the price at which a margin call occurs.",
            ),
            ("2.c", "compare", "Compare execution, validity and clearing instructions, and market structures."),
            ("2.d", "describe", "Describe primary and secondary security markets."),
        ],
        topics=[],
        revision=None,
        questions=[
            q(
                "M",
                "An investor buys on margin with 50% initial margin. The leverage ratio is:",
                ["0.5", "2.0", "1.5"],
                1,
                "Leverage ratio = 1 ÷ initial margin = 2.",
                "2.b",
            ),
            q(
                "H",
                "A share is bought at ₹200 with 50% initial margin and 25% maintenance margin. A margin call occurs "
                "when the price falls below about:",
                ["₹150.00", "₹100.00", "₹133.33"],
                2,
                "200 × (1 − 0.5)/(1 − 0.25) = 133.33.",
                "2.b",
            ),
            q(
                "M",
                "Ignoring interest and fees, a share bought at ₹200 with 50% margin rises to ₹240. The return on the "
                "investor's equity is:",
                ["20%", "40%", "80%"],
                1,
                "Gain 40 on own funds of 100 = 40%.",
                "2.b",
            ),
            q(
                "E",
                "A market in which dealers post bid and ask prices and trade from their own inventory is:",
                ["Quote-driven", "Order-driven", "Brokered"],
                0,
                "Dealer markets are quote-driven.",
                "2.c",
            ),
            q(
                "M",
                "A rights issue gives existing shareholders:",
                [
                    "Free shares with no payment",
                    "The right to buy new shares, usually at a discount, in proportion to their holdings",
                    "Preference over debt in liquidation",
                ],
                1,
                "Rights let holders avoid dilution by subscribing pro rata.",
                "2.d",
            ),
            q(
                "E",
                "A 'good-till-cancelled' instruction is a:",
                ["Validity instruction", "Execution instruction", "Clearing instruction"],
                0,
                "Validity instructions say when an order can be filled.",
                "2.c",
            ),
        ],
        flashcards=[
            fc("Leverage ratio", "1 ÷ initial margin."),
            fc("Margin call price", "P₀ × (1 − initial margin) ÷ (1 − maintenance margin)."),
            fc(
                "Quote- vs order- vs brokered market",
                "Dealers quote; orders match by rules; brokers find counterparties.",
            ),
            fc("Execution vs validity vs clearing", "How to fill (market/limit), when (day/GTC), how to settle."),
            fc("Seasoned offering", "New shares sold by an already-listed company."),
            fc("Primary vs secondary market", "New issues vs trading of existing securities."),
        ],
    )
)

# ---------------------------------------------------------------- LM3
LMS.append(
    dict(
        lm_no=3,
        title="Market Efficiency",
        summary="Forms of efficiency, what makes markets efficient, anomalies, and behavioural explanations.",
        los=[
            ("3.a", "describe", "Describe market efficiency and distinguish market value from intrinsic value."),
            ("3.b", "explain", "Explain factors that affect a market's efficiency."),
            (
                "3.c",
                "contrast",
                "Contrast weak-form, semi-strong-form and strong-form efficiency and their "
                "implications for active and passive management.",
            ),
            ("3.d", "describe", "Describe market anomalies and behavioural finance explanations."),
        ],
        topics=[],
        revision=None,
        questions=[
            q(
                "E",
                "Intrinsic value is best described as:",
                [
                    "The current market price",
                    "The value an investor with full understanding of the asset would place on it",
                    "The book value per share",
                ],
                1,
                "Market value is the price; intrinsic value is the fundamental worth.",
                "3.a",
            ),
            q(
                "M",
                "Which factor tends to make a market more efficient?",
                ["High transaction costs", "Restrictions on short selling", "Many active analysts and investors"],
                2,
                "More participants and analysis speed up price adjustment.",
                "3.b",
            ),
            q(
                "M",
                "If markets are semi-strong efficient, the best strategy for most investors is:",
                ["Frequent trading on public news", "Low-cost passive investing", "Technical analysis"],
                1,
                "Public information is already priced, so costs dominate.",
                "3.c",
            ),
            q(
                "M",
                "Small-cap stocks earning higher risk-adjusted returns than large caps in some studies is the:",
                ["Size effect", "January effect", "Momentum effect"],
                0,
                "It is a cross-sectional anomaly.",
                "3.d",
            ),
            q(
                "H",
                "An apparent anomaly that disappears once transaction costs and risk are properly measured is "
                "evidence that the market is:",
                ["Inefficient", "Probably efficient", "Strong-form inefficient"],
                1,
                "Many anomalies vanish after costs or risk adjustment.",
                "3.d",
            ),
            q(
                "E",
                "Short-term persistence in returns (winners keep winning) is called:",
                ["Momentum", "Overreaction", "Mean reversion"],
                0,
                "Momentum is a time-series anomaly.",
                "3.d",
            ),
        ],
        flashcards=[
            fc("Market vs intrinsic value", "Price paid vs fundamental worth."),
            fc("What makes markets efficient", "Many participants, free information, low costs, few trading limits."),
            fc("Weak / semi-strong / strong", "Past prices / all public info / all info including private."),
            fc("Size and value effects", "Small caps and cheap stocks beating risk-adjusted expectations."),
        ],
    )
)

# ---------------------------------------------------------------- LM4
LMS.append(
    dict(
        lm_no=4,
        title="Security Market Indexes",
        summary="How indexes are built and weighted, price versus total return, rebalancing, and index types.",
        los=[
            ("4.a", "describe", "Describe a security market index and distinguish price return and total return."),
            ("4.b", "calculate", "Calculate and interpret the value, price return and total return of an index."),
            ("4.c", "compare", "Compare the different weighting methods used in index construction."),
            ("4.d", "describe", "Describe rebalancing and reconstitution, uses of indexes, and types of indexes."),
        ],
        topics=[
            topic(
                "Index construction and returns",
                P(
                    "An **index** measures the value of a group of securities. Building one means choosing the target "
                    "market, the constituents, the weighting, and how often to rebalance and reconstitute."
                ),
                L(
                    "**Price return** index: price changes only.",
                    "**Total return** index: price changes plus reinvested income (dividends). Over time the total "
                    "return index pulls ahead.",
                ),
                FX("Price return = (P₁ − P₀) ÷ P₀ · Total return = (P₁ − P₀ + Income) ÷ P₀"),
            ),
            topic(
                "Weighting methods",
                T(
                    ["Method", "Weight by", "Feature"],
                    ["Price-weighted", "Share price", "High-priced shares dominate; splits change weights"],
                    ["Equal-weighted", "1/N each", "Small caps overweighted; frequent rebalancing"],
                    [
                        "Market-cap weighted",
                        "Price × shares outstanding",
                        "Big firms dominate; overweights overvalued shares",
                    ],
                    ["Float-adjusted", "Price × freely tradable shares", "Most common for major indexes"],
                    ["Fundamental", "Sales, earnings, book value, dividends", "Value tilt"],
                ),
                EX(
                    "Three shares: A ₹100 (1 crore shares), B ₹50 (4 crore), C ₹30 (10 crore). Price-weighted average "
                    "= "
                    "(100 + 50 + 30) ÷ 3 = 60. If A rises 10% to ₹110, the price-weighted index rises to 63.33 "
                    "(**+5.6%**). In a market-cap index, A is ₹100 crore of ₹600 crore total, so the index rises only "
                    "10% × 100/600 = **1.7%**."
                ),
                WO(
                    "In a price-weighted index, a stock split **reduces** that stock's weight; the divisor is adjusted "
                    "so the index level does not jump."
                ),
            ),
            topic(
                "Maintenance, uses and types",
                L(
                    "**Rebalancing**: restoring weights (mostly equal-weighted indexes).",
                    "**Reconstitution**: changing constituents as companies grow, shrink, merge or delist.",
                    "Uses: gauging sentiment, benchmarking managers, proxy for the market in CAPM and beta, basis for "
                    "index funds, ETFs and derivatives.",
                    "Types: broad market, sector, style (value/growth, size), fixed income, commodity, real estate, "
                    "hedge fund indexes.",
                ),
                WO(
                    "Bond indexes are hard to build: huge numbers of issues, many trade rarely, and constituents "
                    "change as bonds mature."
                ),
                FUN(
                    "A price-weighted index is like ranking cricketers by the price of their bat. The batter with "
                    "the ₹2 lakh bat gets the most say, however he plays."
                ),
            ),
        ],
        revision=sheet(
            "Price-weighted index = Σ prices ÷ divisor · Total return = price return + income return",
            ("Price-weighted", "High-priced shares dominate"),
            ("Equal-weighted", "Small-cap tilt; needs rebalancing"),
            ("Market-cap", "Big firms dominate; momentum tilt"),
            ("Float-adjusted", "Uses freely tradable shares"),
            ("Fundamental", "Value tilt"),
            ("Rebalancing", "Reset weights"),
            ("Reconstitution", "Change constituents"),
        ),
        questions=[
            q(
                "E",
                "A total return index includes:",
                ["Only price changes", "Price changes and reinvested income", "Only dividends"],
                1,
                "Total return adds income to price changes.",
                "4.a",
            ),
            q(
                "M",
                "In a price-weighted index, the stock with the greatest weight is the one with the highest:",
                ["Market capitalisation", "Share price", "Dividend yield"],
                1,
                "Weights depend on price alone.",
                "4.c",
            ),
            q(
                "M",
                "An index holds shares priced ₹100, ₹50 and ₹30, divisor 3. If the ₹100 share rises to ₹110, the "
                "price-weighted index changes by about:",
                ["+10.0%", "+3.3%", "+5.6%"],
                2,
                "Index goes from 60 to 63.33, +5.6%.",
                "4.b",
            ),
            q(
                "M",
                "Equal-weighted indexes tend to:",
                [
                    "Overweight small companies relative to market-cap indexes",
                    "Never need rebalancing",
                    "Overweight the largest companies",
                ],
                0,
                "Every stock gets 1/N, regardless of size.",
                "4.c",
            ),
            q(
                "H",
                "A criticism of market-cap weighting is that it:",
                ["Ignores large firms", "Overweights shares that have become overvalued", "Is impossible to replicate"],
                1,
                "Rising prices raise weights, regardless of fundamentals.",
                "4.c",
            ),
            q(
                "E",
                "Adding and removing constituents of an index is:",
                ["Rebalancing", "Reconstitution", "Float adjustment"],
                1,
                "Reconstitution changes the membership.",
                "4.d",
            ),
            q(
                "M",
                "A portfolio's value rises from ₹100 to ₹104 and it receives ₹2 of dividends. Its total return is:",
                ["4%", "6%", "2%"],
                1,
                "(104 − 100 + 2)/100 = 6%.",
                "4.b",
            ),
            q(
                "M",
                "A float-adjusted market-cap index weights each company by:",
                ["Total shares outstanding × price", "Shares available to the public × price", "Price only"],
                1,
                "Promoter and locked-in holdings are excluded.",
                "4.c",
            ),
            q(
                "H",
                "Fundamental weighting typically leads to a tilt towards:",
                ["Growth stocks", "Value stocks", "High-momentum stocks"],
                1,
                "Weighting by sales or earnings favours cheaply priced firms.",
                "4.c",
            ),
            q(
                "E",
                "Which is a common use of security market indexes?",
                ["Benchmarking portfolio managers", "Setting tax rates", "Fixing bond coupons"],
                0,
                "Indexes are standard performance benchmarks.",
                "4.d",
            ),
        ],
        flashcards=[
            fc("Price vs total return index", "Price only vs price plus reinvested income."),
            fc("Price-weighted", "Weight by share price; splits reduce weight."),
            fc("Equal-weighted", "1/N each; small-cap tilt; frequent rebalancing."),
            fc("Market-cap / float-adjusted", "Weight by (free-float) market value."),
            fc("Fundamental weighting", "By sales, earnings, book or dividends; value tilt."),
            fc("Rebalancing vs reconstitution", "Reset weights vs change members."),
        ],
    )
)

# ---------------------------------------------------------------- LM5
LMS.append(
    dict(
        lm_no=5,
        title="Company Analysis: Past and Present",
        summary="Business models, revenue and cost drivers, profitability, capital investment and return on capital.",
        los=[
            ("5.a", "describe", "Describe the elements that should be covered in a thorough company research report."),
            ("5.b", "determine", "Determine a company's business model."),
            ("5.c", "evaluate", "Evaluate a company's revenue and revenue drivers, including pricing power."),
            (
                "5.d",
                "evaluate",
                "Evaluate a company's operating profitability, working capital and capital investment.",
            ),
        ],
        topics=[
            topic(
                "Research report and business model",
                L(
                    "A good report covers: the **business model**, revenue and cost drivers, profitability, capital "
                    "structure and investment, competitive position, **risks**, valuation and a recommendation.",
                    "The **business model** explains who the customers are, what they buy, how the company delivers "
                    "it, and how it gets paid.",
                ),
                EX(
                    "A food-delivery app earns commission from restaurants, delivery fees from customers and "
                    "advertising. Its main drivers are orders per user, average order value and take rate."
                ),
            ),
            topic(
                "Revenue and costs",
                FX("Revenue = Volume × Price · Volume = market size × market share"),
                L(
                    "**Pricing power**: ability to raise prices without losing much volume. Signs: rising gross "
                    "margin, "
                    "brand loyalty, few substitutes.",
                    "Revenue can be split by segment, geography or product.",
                    "**Operating leverage**: high fixed costs mean profits swing more than revenue.",
                ),
                EX(
                    "Narmada Cement has fixed costs of ₹300 crore and variable costs of 40% of sales. At sales of "
                    "₹1,000 "
                    "crore, EBIT = 1,000 − 400 − 300 = ₹300 crore. If sales rise 10% to ₹1,100 crore, EBIT = 1,100 − "
                    "440 "
                    "− 300 = ₹360 crore, up **20%**: a degree of operating leverage of 2."
                ),
                WO(
                    "Strong revenue growth from price increases is more valuable than growth bought with heavy "
                    "discounts."
                ),
            ),
            topic(
                "Profitability, working capital and capital investment",
                L(
                    "**Gross margin**, **operating (EBIT) margin**, **EBITDA margin** show how much of each rupee of "
                    "sales becomes profit.",
                    "**Working capital** needs: days of receivables, inventory and payables; the **cash conversion "
                    "cycle**.",
                    "**Capital investment**: maintenance vs growth capex; capex relative to depreciation.",
                ),
                FX("ROIC = NOPAT ÷ Invested capital · NOPAT = EBIT × (1 − tax rate)"),
                EX(
                    "EBIT ₹200 crore, tax 25%, invested capital ₹1,000 crore. NOPAT = 150; ROIC = **15%**. If the cost "
                    "of capital is 11%, the company is creating value."
                ),
                FUN(
                    "A business with negative working capital, like a restaurant that collects cash today and pays "
                    "suppliers next month, is basically being funded by its own vegetable vendor."
                ),
            ),
        ],
        revision=sheet(
            "ROIC = EBIT(1 − t) ÷ invested capital · Revenue = volume × price",
            ("Business model", "Customer, product, channel, pricing"),
            ("Pricing power", "Raise prices without losing volume"),
            ("Operating leverage", "Fixed costs magnify profit swings"),
            ("Cash conversion cycle", "DSO + DIO − DPO"),
            ("Maintenance vs growth capex", "Sustain vs expand capacity"),
            ("Value creation", "ROIC > cost of capital"),
        ),
        questions=[
            q(
                "E",
                "A company's revenue can be analysed as:",
                ["Volume × price", "Assets − liabilities", "Net income ÷ equity"],
                0,
                "Revenue = volume × price.",
                "5.c",
            ),
            q(
                "M",
                "A sign of strong pricing power is:",
                ["Falling gross margins", "Ability to raise prices with little loss of volume", "Heavy discounting"],
                1,
                "Pricing power shows in stable volumes after price rises.",
                "5.c",
            ),
            q(
                "M",
                "Fixed costs ₹300 crore, variable costs 40% of sales, sales ₹1,000 crore. If sales rise 10%, EBIT "
                "rises "
                "by:",
                ["10%", "20%", "30%"],
                1,
                "EBIT from 300 to 360 = 20%.",
                "5.d",
            ),
            q(
                "M",
                "EBIT ₹200 crore, tax rate 25% and invested capital ₹1,000 crore give an ROIC of:",
                ["15%", "20%", "25%"],
                0,
                "NOPAT 150 ÷ 1,000 = 15%.",
                "5.d",
            ),
            q(
                "H",
                "A company creates value for shareholders when:",
                ["Revenue grows", "ROIC exceeds its cost of capital", "It pays a dividend"],
                1,
                "Returns above the cost of capital add value.",
                "5.d",
            ),
            q(
                "E",
                "A thorough company research report should include:",
                [
                    "Only the share price chart",
                    "Business model, drivers, risks, valuation and recommendation",
                    "Only the management's guidance",
                ],
                1,
                "All these elements support the conclusion.",
                "5.a",
            ),
            q(
                "M",
                "Capex needed just to keep existing capacity running is:",
                ["Growth capex", "Maintenance capex", "Working capital"],
                1,
                "Growth capex expands capacity.",
                "5.d",
            ),
            q(
                "M",
                "A company with high fixed costs relative to variable costs has:",
                ["Low operating leverage", "High operating leverage", "No business risk"],
                1,
                "Profits are very sensitive to sales.",
                "5.d",
            ),
            q(
                "H",
                "A shorter cash conversion cycle generally means a company:",
                ["Needs less working capital financing", "Has higher inventory", "Collects receivables more slowly"],
                0,
                "Cash is tied up for fewer days.",
                "5.d",
            ),
            q(
                "E",
                "A company's business model describes:",
                [
                    "How it makes money: customers, products, channels and pricing",
                    "Its tax filings",
                    "Its share register",
                ],
                0,
                "That is the definition.",
                "5.b",
            ),
        ],
        flashcards=[
            fc("Revenue drivers", "Volume × price; volume = market size × share."),
            fc("Pricing power signs", "Stable volume after price rises, rising gross margin."),
            fc("Operating leverage", "High fixed costs magnify EBIT changes."),
            fc("ROIC", "NOPAT ÷ invested capital; NOPAT = EBIT(1 − t)."),
            fc("Value creation test", "ROIC above cost of capital."),
            fc("Maintenance vs growth capex", "Keep capacity running vs add capacity."),
        ],
    )
)

# ---------------------------------------------------------------- LM6
LMS.append(
    dict(
        lm_no=6,
        title="Industry and Competitive Analysis",
        summary="Defining industries, the five forces, the industry life cycle and competitive strategies.",
        los=[
            ("6.a", "describe", "Describe the purposes of, and steps involved in, industry and competitive analysis."),
            ("6.b", "describe", "Describe industry classification methods and how to define an industry."),
            ("6.c", "analyze", "Analyse an industry's size, growth, profitability and market share trends."),
            ("6.d", "analyze", "Analyse competitive forces and a company's competitive strategy."),
        ],
        topics=[
            topic(
                "Defining and classifying industries",
                L(
                    "Industries group companies with similar products, customers or production.",
                    "Commercial systems classify by **principal business activity** in levels: sector → industry "
                    "group → industry → sub-industry.",
                    "Classification can also be **cyclical vs non-cyclical** (defensive) or by statistical clustering.",
                ),
                P(
                    "Measure industry **size** (sales), **growth**, **profitability** and **concentration** (how "
                    "much the top firms control)."
                ),
            ),
            topic(
                "Five forces",
                T(
                    ["Force", "Industry is more attractive when…"],
                    ["Threat of new entrants", "Barriers are high (scale, licences, brands)"],
                    ["Threat of substitutes", "Few close substitutes"],
                    ["Supplier power", "Many suppliers, easy switching"],
                    ["Buyer power", "Many small buyers"],
                    ["Rivalry", "Few competitors, fast growth, differentiated products"],
                ),
                EX(
                    "Indian airlines: low switching costs for flyers, powerful aircraft lessors and fuel suppliers, "
                    "intense price rivalry. Even with strong demand, margins stay thin."
                ),
                WO(
                    "High concentration usually reduces rivalry, but not always: two giants fighting for share can "
                    "still "
                    "wage a price war."
                ),
            ),
            topic(
                "Life cycle and competitive strategy",
                T(
                    ["Stage", "Growth", "Profitability"],
                    ["Embryonic", "Slow, high prices", "Low or negative"],
                    ["Growth", "Rapid", "Improving"],
                    ["Shakeout", "Slowing", "Falling as weak firms exit"],
                    ["Mature", "Little", "Stable, high cash flow"],
                    ["Decline", "Negative", "Falling, consolidation"],
                ),
                L(
                    "**Cost leadership**: lowest cost producer.",
                    "**Differentiation**: unique product, premium price.",
                    "**Focus**: serve a niche with either cost or differentiation.",
                ),
                FUN(
                    "The shakeout stage is musical chairs for companies. When growth stops, someone ends up without a "
                    "seat and gets bought by the one who did."
                ),
            ),
        ],
        revision=sheet(
            "Five forces: entrants · substitutes · suppliers · buyers · rivalry",
            ("Classification", "By principal business activity"),
            ("Cyclical vs defensive", "Sensitive vs insensitive to the economy"),
            ("Concentration", "Share held by top firms"),
            ("Life cycle", "Embryonic → growth → shakeout → mature → decline"),
            ("Strategies", "Cost leadership, differentiation, focus"),
        ),
        questions=[
            q(
                "E",
                "Which industry life cycle stage features rapid growth and improving profitability?",
                ["Embryonic", "Growth", "Decline"],
                1,
                "The growth stage.",
                "6.c",
            ),
            q(
                "M",
                "An industry becomes less attractive when:",
                ["Barriers to entry are high", "Buyers have strong bargaining power", "There are few substitutes"],
                1,
                "Powerful buyers push prices down.",
                "6.d",
            ),
            q(
                "M",
                "Commercial industry classification systems mainly group companies by:",
                ["Share price", "Principal business activity", "Country of listing"],
                1,
                "They use the main source of revenue.",
                "6.b",
            ),
            q(
                "E",
                "A firm that competes by being the lowest-cost producer follows a:",
                ["Differentiation strategy", "Cost leadership strategy", "Focus strategy"],
                1,
                "Cost leadership.",
                "6.d",
            ),
            q(
                "H",
                "In the shakeout stage of the life cycle, typically:",
                [
                    "Demand grows fastest",
                    "Growth slows, competition intensifies and weaker firms exit",
                    "Prices are highest",
                ],
                1,
                "Overcapacity leads to consolidation.",
                "6.c",
            ),
            q(
                "M",
                "Defensive (non-cyclical) industries are those whose demand is:",
                [
                    "Very sensitive to the business cycle",
                    "Relatively insensitive to the business cycle",
                    "Always declining",
                ],
                1,
                "Examples: utilities, consumer staples, healthcare.",
                "6.b",
            ),
            q(
                "M",
                "High switching costs for customers mainly reduce:",
                ["Buyer power", "Supplier power", "The threat of substitutes only"],
                0,
                "Customers locked in cannot easily bargain or leave.",
                "6.d",
            ),
            q(
                "H",
                "Which statement about industry concentration is most accurate?",
                [
                    "High concentration always eliminates rivalry",
                    "High concentration usually reduces rivalry, but not in every case",
                    "Concentration does not affect pricing",
                ],
                1,
                "Large rivals can still fight over share.",
                "6.c",
            ),
            q(
                "E",
                "A company selling a unique product at a premium price follows a:",
                ["Differentiation strategy", "Cost leadership strategy", "Shakeout strategy"],
                0,
                "Differentiation.",
                "6.d",
            ),
            q(
                "M",
                "The first step in industry analysis is to:",
                ["Value the shares", "Define the industry and its competitors", "Forecast dividends"],
                1,
                "You must know the boundaries before analysing.",
                "6.a",
            ),
        ],
        flashcards=[
            fc("Five forces", "Entrants, substitutes, suppliers, buyers, rivalry."),
            fc("Life cycle stages", "Embryonic, growth, shakeout, mature, decline."),
            fc("Competitive strategies", "Cost leadership, differentiation, focus."),
            fc("Cyclical vs defensive", "Sensitive vs insensitive to the economy."),
            fc("High barriers to entry", "Protect incumbents' profits."),
            fc("Classification basis", "Principal business activity."),
        ],
    )
)

# ---------------------------------------------------------------- LM7
LMS.append(
    dict(
        lm_no=7,
        title="Company Analysis: Forecasting",
        summary="Forecasting approaches, revenue and cost forecasts, the forecast horizon and scenario analysis.",
        los=[
            ("7.a", "explain", "Explain principles and approaches to forecasting a company's financial results."),
            (
                "7.b",
                "explain",
                "Explain approaches to forecasting revenues, costs, balance sheet items and capital investments.",
            ),
            ("7.c", "describe", "Describe how to choose the forecast horizon and use scenario analysis."),
        ],
        topics=[
            topic(
                "Approaches",
                T(
                    ["Approach", "Starts from", "Example"],
                    ["Top-down", "Economy → industry → company", "GDP growth → cement demand → company share"],
                    ["Bottom-up", "Company data", "Stores × sales per store"],
                    ["Hybrid", "Both, then reconciled", "Most analysts in practice"],
                ),
                P(
                    "Good forecasts are driven by a few **key drivers** and checked for consistency across the income "
                    "statement, balance sheet and cash flow statement."
                ),
            ),
            topic(
                "Forecasting the statements",
                L(
                    "**Revenue**: growth relative to GDP, market size × share, or volume × price.",
                    "**Costs**: split fixed and variable; gross margin often stable unless prices or input costs "
                    "change; "
                    "use **economies of scale**.",
                    "**Working capital**: use days or % of sales.",
                    "**Capex**: maintenance ≈ depreciation; growth capex for new capacity.",
                    "Long-run assumptions should allow **mean reversion**: very high margins and growth tend to fade.",
                ),
                EX(
                    "Sales this year ₹2,000 crore; forecast growth 12%; gross margin 35%; SG&A fixed at ₹300 crore. "
                    "Next "
                    "year: sales ₹2,240 crore, gross profit ₹784 crore, operating profit **₹484 crore** (up from ₹400 "
                    "crore)."
                ),
                WO(
                    "Extrapolating a recent boom for ten years is the classic forecasting error. Competition usually "
                    "erodes excess returns."
                ),
            ),
            topic(
                "Horizon and scenarios",
                L(
                    "Horizon depends on the investment strategy, the industry's cycle and any expected change "
                    "(merger, new plant). Long enough to reach a steady state.",
                    "**Scenario analysis**: base, bull and bear cases with different drivers, and their effect on "
                    "value.",
                    "**Sensitivity analysis**: change one driver at a time.",
                ),
                FUN(
                    "A forecast is like a wedding guest count: whatever number you pick, make sure your caterer has a "
                    "plan for 20% more and 20% fewer."
                ),
            ),
        ],
        revision=sheet(
            "Top-down · bottom-up · hybrid · mean reversion in the long run",
            ("Top-down", "Economy → industry → firm"),
            ("Bottom-up", "Firm-level drivers"),
            ("Costs", "Split fixed and variable"),
            ("Working capital", "Days or % of sales"),
            ("Maintenance capex", "≈ depreciation"),
            ("Scenario analysis", "Base, bull, bear"),
            ("Sensitivity", "One driver at a time"),
        ),
        questions=[
            q(
                "E",
                "Forecasting a company's sales from GDP growth and its market share is a:",
                ["Bottom-up approach", "Top-down approach", "Hybrid of tax analysis"],
                1,
                "It starts from the economy.",
                "7.a",
            ),
            q(
                "M",
                "Sales of ₹2,000 crore grow 12%. Gross margin is 35% and SG&A is fixed at ₹300 crore. Forecast "
                "operating profit is:",
                ["₹484 crore", "₹400 crore", "₹784 crore"],
                0,
                "2,240 × 0.35 = 784; 784 − 300 = 484.",
                "7.b",
            ),
            q(
                "M",
                "Long-term forecasts of very high margins should usually assume:",
                ["Margins rise forever", "Some mean reversion as competition increases", "Margins become zero"],
                1,
                "Excess returns tend to be competed away.",
                "7.b",
            ),
            q(
                "E",
                "Maintenance capital expenditure is often approximated by:",
                ["Depreciation", "Net income", "Dividends"],
                0,
                "It replaces worn-out assets.",
                "7.b",
            ),
            q(
                "M",
                "Forecasting a retailer's sales as number of stores × sales per store is:",
                ["Top-down", "Bottom-up", "Scenario analysis"],
                1,
                "It builds from company data.",
                "7.a",
            ),
            q(
                "H",
                "Changing one forecast driver at a time to see the effect on value is:",
                ["Sensitivity analysis", "Scenario analysis", "Top-down analysis"],
                0,
                "Scenarios change several drivers together.",
                "7.c",
            ),
            q(
                "M",
                "The forecast horizon should generally be:",
                [
                    "Exactly one year",
                    "Long enough for the company to reach a steady state",
                    "Equal to the analyst's tenure",
                ],
                1,
                "Then a terminal value can be applied.",
                "7.c",
            ),
            q(
                "H",
                "Forecasting working capital items as days of sales or cost of sales mainly ensures:",
                ["They grow consistently with the business", "They stay fixed", "Taxes are lower"],
                0,
                "Receivables, inventory and payables scale with activity.",
                "7.b",
            ),
            q(
                "E",
                "Base, bull and bear cases are used in:",
                ["Scenario analysis", "Index rebalancing", "GIPS verification"],
                0,
                "Each case uses different assumptions.",
                "7.c",
            ),
            q(
                "M",
                "When forecasting costs, splitting them into fixed and variable helps capture:",
                ["Operating leverage", "Dividend policy", "Tax rates"],
                0,
                "Fixed costs create operating leverage.",
                "7.b",
            ),
        ],
        flashcards=[
            fc("Top-down vs bottom-up", "Economy → firm vs firm-level drivers."),
            fc("Hybrid forecasting", "Combine both and reconcile."),
            fc("Mean reversion", "Very high growth and margins fade over time."),
            fc("Maintenance capex proxy", "Depreciation."),
            fc("Scenario vs sensitivity", "Several drivers together vs one at a time."),
            fc("Forecast horizon", "Long enough to reach steady state."),
        ],
    )
)

# ---------------------------------------------------------------- LM8
LMS.append(
    dict(
        lm_no=8,
        title="Equity Valuation: Concepts and Basic Tools",
        summary="Intrinsic value, dividend discount models, free cash flow, multiples and asset-based valuation.",
        los=[
            ("8.a", "evaluate", "Evaluate whether a security is overvalued, fairly valued or undervalued."),
            ("8.b", "describe", "Describe major categories of equity valuation models."),
            (
                "8.c",
                "calculate",
                "Calculate and interpret the intrinsic value of an equity security using the "
                "Gordon growth model and the value of preferred stock.",
            ),
            ("8.d", "calculate", "Calculate and interpret justified multiples and enterprise value multiples."),
        ],
        topics=[
            topic(
                "Valuation categories",
                L(
                    "**Present value models**: dividends (DDM) or free cash flow to equity (FCFE).",
                    "**Multiplier models**: P/E, P/B, P/S, P/CF, or **EV/EBITDA**.",
                    "**Asset-based models**: value of assets minus liabilities, adjusted to market.",
                ),
                P(
                    "If estimated **intrinsic value > price**, the share is **undervalued**; < price, overvalued. "
                    "Allow a margin for uncertainty in the estimate."
                ),
            ),
            topic(
                "Dividend discount models",
                FX("Gordon growth: V₀ = D₁ ÷ (r − g) · Preferred: V₀ = D ÷ r · FCFE = CFO − FCInv + net borrowing"),
                EX(
                    "Sona Paints paid D₀ = ₹10; dividends grow 5% for ever; required return 11%. D₁ = 10.5. V₀ = 10.5 "
                    "÷ "
                    "0.06 = **₹175**. At a market price of ₹160 it looks undervalued."
                ),
                EX("A perpetual preference share pays ₹8 a year; required return 10%. V₀ = 8 ÷ 0.10 = **₹80**."),
                WO(
                    "Gordon growth needs r > g, and suits mature companies with stable payout. Use multistage models "
                    "for high-growth firms."
                ),
            ),
            topic(
                "Multiples and asset-based value",
                FX("Justified forward P/E = (D₁/E₁) ÷ (r − g) · EV = market cap + debt + preferred − cash"),
                EX(
                    "Payout 40%, r = 11%, g = 5%: justified forward P/E = 0.40 ÷ 0.06 = **6.67×**. If EBITDA is ₹500 "
                    "crore "
                    "and EV is ₹4,000 crore, EV/EBITDA = 8×."
                ),
                L(
                    "Method of comparables: compare multiples with peers, adjusting for growth and risk.",
                    "EV/EBITDA is useful across firms with different leverage.",
                    "Asset-based valuation suits firms with mostly tangible or financial assets (holding companies, "
                    "resource firms); hard for firms with large intangibles.",
                ),
                FUN(
                    "Valuing a company only by its P/E is like choosing a groom only by salary. A useful number, but "
                    "ask about growth and risk before the wedding."
                ),
            ),
        ],
        revision=sheet(
            "V₀ = D₁/(r − g) · Preferred V₀ = D/r · Justified P/E = payout/(r − g)",
            ("Undervalued", "Intrinsic value > price"),
            ("PV models", "DDM, FCFE"),
            ("Multiplier models", "P/E, P/B, P/S, EV/EBITDA"),
            ("Asset-based", "Assets − liabilities at market values"),
            ("Gordon condition", "r > g, stable growth"),
            ("EV", "Market cap + debt + preferred − cash"),
        ),
        questions=[
            q(
                "M",
                "D₀ = ₹10, growth 5% for ever and required return 11%. The Gordon growth value is:",
                ["₹175.00", "₹166.67", "₹90.91"],
                0,
                "D₁ = 10.5; 10.5/0.06 = 175.",
                "8.c",
            ),
            q(
                "E",
                "A share with intrinsic value ₹175 trading at ₹160 is:",
                ["Overvalued", "Undervalued", "Fairly valued"],
                1,
                "Value exceeds price.",
                "8.a",
            ),
            q(
                "M",
                "A perpetual preference share pays ₹8 a year and investors require 10%. Its value is:",
                ["₹80", "₹8", "₹88"],
                0,
                "8 ÷ 0.10 = 80.",
                "8.c",
            ),
            q(
                "M",
                "With a payout ratio of 40%, r = 11% and g = 5%, the justified forward P/E is closest to:",
                ["6.67×", "4.00×", "8.00×"],
                0,
                "0.40 ÷ 0.06 = 6.67.",
                "8.d",
            ),
            q(
                "E",
                "Which is a multiplier model?",
                ["Gordon growth model", "EV/EBITDA", "FCFE model"],
                1,
                "EV/EBITDA is an enterprise multiple.",
                "8.b",
            ),
            q(
                "M",
                "Enterprise value is calculated as:",
                ["Market cap + debt + preferred − cash", "Market cap − debt", "Book equity + cash"],
                0,
                "EV is the value of the whole operating business.",
                "8.d",
            ),
            q(
                "H",
                "The Gordon growth model is least appropriate for:",
                [
                    "A mature utility with stable dividends",
                    "A fast-growing tech firm that pays no dividend",
                    "A firm with steady 4% growth",
                ],
                1,
                "It needs stable growth below the required return.",
                "8.c",
            ),
            q(
                "M",
                "EV/EBITDA is especially useful when comparing companies with:",
                ["Different capital structures", "Identical leverage", "No debt only"],
                0,
                "EBITDA is before interest, so leverage matters less.",
                "8.d",
            ),
            q(
                "H",
                "Asset-based valuation is most suitable for a:",
                [
                    "Software firm with large intangibles",
                    "Holding company with mostly marketable investments",
                    "High-growth start-up",
                ],
                1,
                "Asset values can be measured reliably.",
                "8.b",
            ),
            q(
                "E",
                "If g rises closer to r in the Gordon growth model, the estimated value:",
                ["Falls", "Rises sharply", "Is unchanged"],
                1,
                "The denominator (r − g) shrinks.",
                "8.c",
            ),
        ],
        flashcards=[
            fc("Gordon growth model", "V₀ = D₁/(r − g)."),
            fc("Preferred share value", "D/r."),
            fc("Justified forward P/E", "Payout ratio ÷ (r − g)."),
            fc("Enterprise value", "Market cap + debt + preferred − cash."),
            fc("Three valuation families", "Present value, multiplier, asset-based."),
            fc("Undervalued means", "Intrinsic value above market price."),
        ],
    )
)


if __name__ == "__main__":
    write_pack("eq", "Equity Investments", LMS, balance_keys=True)
