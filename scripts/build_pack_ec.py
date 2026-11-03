"""Economics content pack.  python scripts/build_pack_ec.py, then re-seed."""

from packlib import EX, FUN, FX, WO, L, P, T, fc, q, sheet, topic, write_pack

LMS = []

# ---------------------------------------------------------------- LM1
LMS.append(dict(
    lm_no=1, title="Firms and Market Structures",
    summary="Breakeven and shutdown, economies of scale, the four market structures, concentration measures.",
    los=[("1.a", "determine", "Determine and interpret breakeven and shutdown points of production."),
         ("1.b", "describe", "Describe how economies and diseconomies of scale affect costs."),
         ("1.c", "describe", "Describe the characteristics of perfect competition, monopolistic competition, "
                             "oligopoly and pure monopoly."),
         ("1.d", "explain", "Explain pricing and output decisions of firms under different market structures."),
         ("1.e", "describe", "Describe the use and limitations of concentration measures.")],
    topics=[
        topic("Breakeven, shutdown and scale",
              P("Every firm maximises profit where **marginal revenue = marginal cost (MR = MC)**. Whether it "
                "should keep producing depends on how price compares with its average costs."),
              T(["Condition", "Short run", "Long run"],
                ["P ≥ ATC", "Operate (profit or breakeven)", "Stay in the market"],
                ["AVC ≤ P < ATC", "Operate: covers variable cost and part of fixed cost", "Exit"],
                ["P < AVC", "Shut down", "Exit"]),
              EX("Narmada Mills sells cloth at ₹50 a metre. ATC is ₹55 and AVC is ₹45. It loses ₹5 a metre, but "
                 "each metre still adds ₹5 towards fixed costs, so it **keeps operating in the short run**. If "
                 "the price stays below ₹55, it exits in the long run."),
              P("**Economies of scale**: long-run average cost falls as output rises (specialisation, bulk "
                "buying). **Diseconomies of scale**: LRAC rises because the firm is too large to manage well. "
                "The lowest point of the LRAC curve is the **minimum efficient scale**."),
              WO("**Breakeven** is where price equals **average total cost**. **Shutdown** is where price falls "
                 "below **average variable cost**. Don't swap them.")),
        topic("The four market structures",
              T(["", "Perfect competition", "Monopolistic competition", "Oligopoly", "Monopoly"],
                ["Sellers", "Many", "Many", "Few", "One"],
                ["Product", "Identical", "Differentiated", "Identical or differentiated", "Unique"],
                ["Entry barriers", "Very low", "Low", "High", "Very high"],
                ["Pricing power", "None (price taker)", "Some", "Some to considerable", "Considerable"],
                ["Non-price competition", "None", "Advertising, branding", "Advertising, branding",
                 "Advertising"]),
              L("**Perfect competition**: the firm faces a horizontal demand curve, so P = MR. Long-run economic "
                "profit is zero.",
                "**Monopolistic competition**: downward-sloping demand; new entrants push long-run economic "
                "profit to zero.",
                "**Oligopoly**: firms are interdependent. Models include **kinked demand**, **Cournot** "
                "(firms choose output at the same time), **Stackelberg** (one firm moves first) and the "
                "**dominant firm** model. A **Nash equilibrium** is where no firm can gain by changing alone.",
                "**Monopoly**: sets output where MR = MC, then charges the highest price demand allows. It may "
                "price-discriminate. Natural monopolies are often regulated."),
              FUN("Perfect competition is the sabzi mandi: a hundred tomato sellers and nobody can charge "
                  "a rupee more. A monopoly is the only chai stall at the railway station at 3 a.m.")),
        topic("Concentration measures",
              FX("N-firm concentration ratio = sum of the top N firms' market shares · "
                 "HHI = sum of the squared market shares"),
              EX("Four firms hold 30%, 25%, 20% and 15%. Four-firm ratio = **90%**. Four-firm HHI = 0.30² + "
                 "0.25² + 0.20² + 0.15² = 0.09 + 0.0625 + 0.04 + 0.0225 = **0.215**."),
              L("The concentration ratio **ignores mergers among the top N firms**: if the top two merge, the "
                "ratio doesn't change, though market power does. HHI does change.",
                "Neither measure captures **barriers to entry** or potential competition, so a concentrated "
                "market can still behave competitively.")),
    ],
    revision=sheet("Profit max: MR = MC · Breakeven: P = ATC · Short-run shutdown: P < AVC · HHI = Σ share²",
                   ("AVC ≤ P < ATC", "Operate short run, exit long run"),
                   ("Economies of scale", "LRAC falls as output rises"),
                   ("Perfect competition", "Price taker, P = MR, zero long-run profit"),
                   ("Monopolistic competition", "Differentiated, zero long-run profit"),
                   ("Stackelberg", "Leader moves first; Cournot: simultaneous"),
                   ("Monopoly", "MR = MC; price from demand curve"),
                   ("Concentration ratio", "Blind to mergers among top N")),
    questions=[
        q("E", "In the short run, a firm should keep operating as long as price is at least equal to:",
          ["Average variable cost", "Average total cost", "Zero marginal revenue"], 0,
          "Above AVC the firm covers its variable costs and some fixed costs, so producing loses less than "
          "shutting down.", "1.a"),
        q("M", "A firm sells at ₹50 per unit. ATC is ₹55 and AVC is ₹45. In the short run it should:",
          ["Shut down immediately", "Keep operating, because price covers variable cost",
           "Raise output until ATC equals ₹50"], 1,
          "Each unit contributes 50 − 45 = ₹5 to fixed costs, so the loss is smaller than if it shut down.",
          "1.a"),
        q("M", "A firm's breakeven point is where:",
          ["Total revenue equals total variable cost", "Marginal cost equals zero",
           "Total revenue equals total cost"], 2,
          "At breakeven, price equals average total cost and economic profit is zero.", "1.a"),
        q("E", "A firm maximises profit at the output where:",
          ["Marginal revenue equals marginal cost", "Price equals average variable cost",
           "Total revenue is at its maximum"], 0,
          "Producing more than this adds more cost than revenue; producing less forgoes profit.", "1.d"),
        q("M", "Economies of scale exist when:",
          ["Short-run marginal cost rises", "Long-run average cost falls as output increases",
           "Fixed costs rise with output"], 1,
          "Larger scale allows specialisation and bulk buying, lowering cost per unit.", "1.b"),
        q("M", "Which market structure has many sellers offering differentiated products with low entry "
               "barriers?", ["Perfect competition", "Monopolistic competition", "Oligopoly"], 1,
          "Differentiation gives some pricing power; low barriers keep entry easy.", "1.c"),
        q("H", "In long-run equilibrium, a firm in monopolistic competition earns:",
          ["Positive economic profit protected by barriers", "Negative economic profit",
           "Zero economic profit"], 2,
          "Low barriers mean entrants keep arriving until economic profit is competed away.", "1.d"),
        q("H", "In the Stackelberg model of oligopoly:",
          ["Firms choose output simultaneously", "One firm moves first and the others react",
           "All firms price at marginal cost"], 1,
          "The leader chooses output knowing how followers will respond; Cournot firms move together.", "1.d"),
        q("H", "Four firms have market shares of 30%, 25%, 20% and 15%. Their four-firm HHI is closest to:",
          ["0.215", "0.900", "0.250"], 0,
          "0.09 + 0.0625 + 0.04 + 0.0225 = 0.215. 0.90 is the four-firm concentration ratio.", "1.e"),
        q("M", "A limitation of the N-firm concentration ratio is that it:",
          ["Needs data on every firm in the industry", "Squares each market share",
           "Does not change when firms within the top N merge"], 2,
          "Combined share stays the same after such a merger, so the ratio misses the rise in market power.",
          "1.e"),
    ],
    flashcards=[
        fc("Profit-maximising output", "Where MR = MC."),
        fc("Breakeven vs shutdown", "Breakeven: P = ATC. Short-run shutdown: P < AVC."),
        fc("Minimum efficient scale", "Output at the lowest point of the long-run average cost curve."),
        fc("Cournot vs Stackelberg", "Cournot: firms choose output simultaneously. Stackelberg: a leader moves "
                                     "first."),
        fc("Which structures earn zero long-run economic profit?", "Perfect and monopolistic competition."),
        fc("HHI", "Sum of squared market shares; unlike the concentration ratio, it rises after mergers."),
    ],
))

# ---------------------------------------------------------------- LM2
LMS.append(dict(
    lm_no=2, title="Understanding Business Cycles",
    summary="Phases of the business cycle, credit cycles, how activity varies, and economic indicators.",
    los=[("2.a", "describe", "Describe the business cycle and its phases."),
         ("2.b", "describe", "Describe credit cycles."),
         ("2.c", "describe", "Describe how resource use, consumer and business activity, housing and external "
                             "trade vary over the cycle, and how economic indicators measure them.")],
    topics=[
        topic("Phases and credit cycles",
              T(["Phase", "Output vs potential", "What typically happens"],
                ["Recovery", "Below potential but rising", "Trough passed; firms rehire slowly"],
                ["Expansion", "Above potential, growing", "Hiring, capital spending, inflation picks up"],
                ["Slowdown", "Growth slowing after the peak", "Inventories build up, confidence fades"],
                ["Contraction", "Output falling", "Layoffs, falling profits; a recession if severe"]),
              P("**Credit cycles** are expansions and contractions in the availability and cost of credit. "
                "Easy credit fuels asset prices, especially property, which supports more lending. When credit "
                "tightens, the process reverses. Credit cycles tend to be **longer and deeper** than business "
                "cycles and can amplify them."),
              FUN("A credit boom is a wedding season loan mela: everyone gets a loan, everyone buys gold, "
                  "and then the EMIs arrive.")),
        topic("Activity over the cycle",
              L("**Businesses**: as sales slow, unsold inventory piles up and the **inventory-to-sales ratio** "
                "rises, so production is cut. In recovery, inventories are rebuilt.",
                "**Labour**: firms first cut overtime and hours, then lay off workers. In recovery they first "
                "add hours, then hire. Unemployment therefore lags the cycle.",
                "**Consumers**: spending on **durables** (cars, appliances) swings most, because purchases "
                "can be postponed. Spending on services and staples is steadier.",
                "**Housing**: very sensitive to **mortgage rates** and incomes.",
                "**External trade**: imports rise with domestic GDP; exports depend on trading partners' GDP "
                "and the exchange rate."),
              EX("Ganga Retail: inventories ₹120 crore against monthly sales of ₹100 crore, so the "
                 "inventory-to-sales ratio is **1.2**, up from 1.0. That unwanted stock build-up usually means "
                 "production cuts are coming.")),
        topic("Economic indicators",
              T(["Type", "Moves", "Examples"],
                ["Leading", "Before the cycle", "Building permits, new orders, average weekly hours, stock prices, "
                                                "yield spread, consumer expectations"],
                ["Coincident", "With the cycle", "Industrial production, payroll employment, personal income, "
                                                 "manufacturing sales"],
                ["Lagging", "After the cycle", "Average duration of unemployment, inventory-to-sales ratio, "
                                               "unit labour costs, bank lending rates"]),
              WO("A rising **inventory-to-sales ratio** is a **lagging** indicator, but reading it with sales "
                 "data helps explain where the cycle is heading.")),
    ],
    revision=sheet("Recovery → Expansion → Slowdown → Contraction · Leading → Coincident → Lagging",
                   ("Recovery", "Output below potential, rising"),
                   ("Inventory/sales ↑", "Weak sales, production cuts ahead"),
                   ("Labour adjustment", "Hours first, then headcount"),
                   ("Most cyclical spending", "Durables and housing"),
                   ("Credit cycle", "Longer, deeper; amplifies the business cycle"),
                   ("Leading", "Permits, new orders, stock prices, yield spread"),
                   ("Lagging", "Unemployment duration, unit labour cost")),
    questions=[
        q("E", "The phase in which activity is rising but output is still below potential is the:",
          ["Recovery", "Slowdown", "Contraction"], 0,
          "Recovery starts at the trough, with output growing but still below potential.", "2.a"),
        q("M", "Spending on durable goods is the most cyclical type of consumer spending because:",
          ["Durables are necessities", "Purchases can be postponed when incomes fall",
           "Durable prices never change"], 1,
          "Households delay buying cars and appliances in bad times and catch up in good times.", "2.c"),
        q("M", "Which is a leading economic indicator?",
          ["Average duration of unemployment", "Building permits for new private housing",
           "Industrial production"], 1,
          "Permits come before construction activity; unemployment duration lags; production is coincident.",
          "2.c"),
        q("M", "Which is a lagging economic indicator?",
          ["Stock prices", "New orders for consumer goods", "Average duration of unemployment"], 2,
          "Unemployment duration keeps rising after the economy has turned.", "2.c"),
        q("E", "Industrial production is best classified as a(n):",
          ["Coincident indicator", "Leading indicator", "Lagging indicator"], 0,
          "Industrial output moves in step with the overall cycle.", "2.c"),
        q("H", "A rising inventory-to-sales ratio late in an expansion most likely signals:",
          ["Weaker sales than expected and production cuts ahead", "Demand that firms cannot keep up with",
           "Falling interest rates"], 0,
          "Unsold stock builds up when sales slow, so firms cut output to clear it.", "2.c"),
        q("M", "Credit cycles are best described as:",
          ["Seasonal changes in bank deposits", "Changes in a currency's value",
           "Expansions and contractions in credit availability that can amplify business cycles"], 2,
          "Easy credit lifts asset prices and spending; tight credit reverses both.", "2.b"),
        q("H", "When demand first weakens, firms typically adjust labour by:",
          ["Hiring more permanent staff", "Cutting overtime and hours before laying off workers",
           "Raising wages"], 1,
          "Cutting hours is cheaper and easier to reverse than firing and later rehiring.", "2.c"),
        q("H", "Other things equal, faster GDP growth in India's main trading partners most likely:",
          ["Raises Indian exports", "Reduces Indian exports", "Has no effect on Indian trade"], 0,
          "Richer trading partners buy more imports, which are India's exports.", "2.c"),
        q("H", "Housing activity is especially sensitive to:",
          ["Corporate tax rates on exporters", "Dividend payments", "Mortgage interest rates"], 2,
          "Most homes are bought with loans, so EMIs and affordability move with mortgage rates.", "2.c"),
    ],
    flashcards=[
        fc("Four business cycle phases", "Recovery, expansion, slowdown, contraction."),
        fc("Credit cycle", "Swings in credit availability; longer and deeper than business cycles."),
        fc("How firms adjust labour first", "Cut or add hours and overtime before changing headcount."),
        fc("Most cyclical consumer spending", "Durable goods, because purchases can be postponed."),
        fc("Leading indicators (examples)", "Building permits, new orders, weekly hours, stock prices, yield "
                                            "spread."),
        fc("Lagging indicators (examples)", "Unemployment duration, inventory-to-sales ratio, unit labour costs."),
    ],
))

# ---------------------------------------------------------------- LM3
LMS.append(dict(
    lm_no=3, title="Fiscal Policy",
    summary="Fiscal vs monetary policy, fiscal tools, the multiplier, deficits and debt, implementation lags.",
    los=[("3.a", "compare", "Compare monetary and fiscal policy."),
         ("3.b", "describe", "Describe the roles and objectives of fiscal policy and arguments about whether "
                             "the size of national debt matters."),
         ("3.c", "describe", "Describe the tools of fiscal policy and their advantages and disadvantages."),
         ("3.d", "explain", "Explain fiscal policy implementation, its difficulties, and whether a stance is "
                            "expansionary or contractionary.")],
    topics=[
        topic("Roles and tools of fiscal policy",
              P("**Fiscal policy** is the government's use of **spending and taxation** to influence the "
                "economy. **Monetary policy** is the central bank's use of interest rates and the money supply."),
              L("**Roles**: stabilise aggregate demand, redistribute income and wealth, allocate resources to "
                "public goods.",
                "**Automatic stabilisers** work without new decisions: progressive taxes and unemployment "
                "benefits cushion a downturn on their own.",
                "**Discretionary policy** needs a deliberate decision, e.g. a stimulus package."),
              T(["Spending tools", "Revenue tools"],
                ["Transfer payments (pensions, subsidies)", "Direct taxes: income, corporate, wealth"],
                ["Current spending (salaries, services)", "Indirect taxes: GST, excise, customs"],
                ["Capital spending (roads, railways)", ""]),
              P("A good tax is **simple**, **efficient** (distorts little), **fair** and raises **enough "
                "revenue**. **Horizontal equity**: people in similar situations pay the same. **Vertical "
                "equity**: those more able to pay pay more."),
              WO("Indirect taxes can be changed quickly; capital projects take years to plan and build, so "
                 "they act slowly.")),
        topic("The multiplier, deficits and debt",
              FX("Fiscal multiplier = 1 ÷ [1 − MPC × (1 − t)]"),
              EX("MPC = 0.8 and t = 25%. Multiplier = 1 ÷ (1 − 0.8 × 0.75) = 1 ÷ 0.4 = **2.5**. Extra spending of "
                 "₹10,000 crore can lift GDP by about ₹25,000 crore."),
              T(["Debt matters because…", "Debt may not matter because…"],
                ["Future taxes must rise to service it", "Debt owed to citizens is a transfer within the country"],
                ["Borrowing can **crowd out** private investment", "**Ricardian equivalence**: people save to "
                                                                  "pay future taxes"],
                ["It may be financed by printing money (inflation)", "It may fund productive capital spending"],
                ["High debt limits room for future stimulus", "It can push governments to reform taxes"])),
        topic("Implementation and stance",
              L("**Recognition lag**: time to realise action is needed.",
                "**Action lag**: time to decide and pass the measure.",
                "**Impact lag**: time for the measure to affect the economy."),
              P("To judge the stance, use the **structural (cyclically adjusted) budget balance**, which strips "
                "out the effect of the cycle. A rising structural deficit means policy is **expansionary**; a "
                "falling one means **contractionary**."),
              FUN("Fiscal stimulus with long lags is like ordering an umbrella online during the monsoon. "
                  "By the time it arrives, it's Diwali.")),
    ],
    revision=sheet("Multiplier = 1 / [1 − MPC(1 − t)] · Stance: structural deficit ↑ = expansionary",
                   ("Fiscal policy", "Government spending and taxes"),
                   ("Automatic stabilisers", "Progressive taxes, unemployment benefits"),
                   ("Direct vs indirect", "Income tax vs GST"),
                   ("Vertical equity", "Higher ability to pay, more tax"),
                   ("Crowding out", "Govt borrowing raises rates, cuts private investment"),
                   ("Ricardian equivalence", "Tax cut saved for future taxes"),
                   ("Lags", "Recognition, action, impact")),
    questions=[
        q("E", "Fiscal policy refers to a government's use of:",
          ["Spending and taxation to influence the economy", "Interest rates and the money supply",
           "Exchange rate intervention only"], 0,
          "Monetary policy uses rates and money; fiscal policy uses the budget.", "3.a"),
        q("M", "Which is an automatic stabiliser?",
          ["A one-time infrastructure package", "A progressive income tax system", "A central bank rate cut"], 1,
          "Tax collections fall automatically as incomes fall, supporting spending without new decisions.",
          "3.b"),
        q("M", "The marginal propensity to consume is 0.8 and the tax rate is 25%. The fiscal multiplier is:",
          ["5.0", "2.5", "1.25"], 1, "1 ÷ (1 − 0.8 × 0.75) = 1 ÷ 0.4 = 2.5.", "3.c"),
        q("M", "Ricardian equivalence suggests that a debt-financed tax cut:",
          ["Always raises consumption by the full amount of the tax cut", "Causes immediate inflation",
           "Has little effect on demand, because people save to pay future taxes"], 2,
          "If households expect higher taxes later, they save the tax cut instead of spending it.", "3.b"),
        q("E", "Which is an indirect tax?",
          ["Personal income tax", "Goods and services tax (GST)", "Corporate income tax"], 1,
          "Indirect taxes are levied on spending; direct taxes on income or wealth.", "3.c"),
        q("H", "Crowding out occurs when government borrowing:",
          ["Raises interest rates and reduces private investment",
           "Lowers interest rates and raises private investment", "Increases exports"], 0,
          "The government competes with firms for savings, pushing rates up.", "3.b"),
        q("M", "The time it takes policymakers to realise the economy needs stimulus is the:",
          ["Action lag", "Recognition lag", "Impact lag"], 1,
          "Data arrive with a delay, so recognising a slowdown takes time.", "3.d"),
        q("H", "An increase in the structural (cyclically adjusted) budget deficit indicates fiscal policy is:",
          ["Expansionary", "Contractionary", "Neutral"], 0,
          "Removing cyclical effects isolates deliberate policy; a larger deficit means more stimulus.", "3.d"),
        q("H", "Vertical equity in taxation means that:",
          ["People in similar situations pay the same tax", "Everyone pays the same amount",
           "People with a greater ability to pay pay more"], 2,
          "Horizontal equity is equal treatment of equals; vertical equity is about ability to pay.", "3.c"),
        q("M", "Compared with new capital spending, changes in indirect taxes:",
          ["Take years to plan", "Cannot affect spending", "Can be implemented quickly"], 2,
          "Rate changes can take effect almost at once; infrastructure needs planning and construction.", "3.c"),
    ],
    flashcards=[
        fc("Fiscal vs monetary policy", "Government spending and taxes vs central bank rates and money supply."),
        fc("Fiscal multiplier", "1 ÷ [1 − MPC × (1 − t)]"),
        fc("Automatic stabilisers", "Progressive taxes and unemployment benefits; no new decision needed."),
        fc("Ricardian equivalence", "Debt-funded tax cuts are saved to pay expected future taxes."),
        fc("Crowding out", "Government borrowing raises rates and displaces private investment."),
        fc("Three fiscal lags", "Recognition, action, impact."),
    ],
))

# ---------------------------------------------------------------- LM4
LMS.append(dict(
    lm_no=4, title="Monetary Policy",
    summary="Central bank roles and tools, transmission, targeting regimes, policy stance, policy mix.",
    los=[("4.a", "describe", "Describe the roles and objectives of central banks."),
         ("4.b", "describe", "Describe monetary policy tools and the transmission mechanism, and explain "
                             "links between monetary policy and growth, inflation, interest and exchange "
                             "rates."),
         ("4.c", "describe", "Describe qualities of effective central banks and contrast inflation, interest "
                             "rate and exchange rate targeting."),
         ("4.d", "determine", "Determine whether a monetary policy is expansionary or contractionary."),
         ("4.e", "describe", "Describe the interaction of monetary and fiscal policy.")],
    topics=[
        topic("Roles, objectives and tools",
              L("**Roles**: sole issuer of currency, banker to the government and banks, lender of last resort, "
                "supervisor of banks and payment systems, manager of foreign exchange reserves.",
                "**Main objective**: price stability. The RBI, for example, targets CPI inflation of 4% within a "
                "band of 2% to 6%."),
              T(["Tool", "Expansionary use", "Effect"],
                ["Policy rate (repo rate)", "Cut it", "Cheaper borrowing across the economy"],
                ["Reserve requirement (CRR)", "Lower it", "Banks can lend more"],
                ["Open market operations", "Buy government bonds", "Adds reserves and money"]),
              P("**Transmission**: a policy rate change moves bank rates, asset prices, expectations and the "
                "exchange rate, which in turn change spending, output and inflation."),
              WO("A higher policy rate usually **strengthens** the currency, as foreign investors seek higher "
                 "returns. That makes imports cheaper and hurts exporters.")),
        topic("Effective central banks and targeting",
              L("Effective central banks are **independent**, **credible** and **transparent**.",
                "**Inflation targeting**: publicly announced inflation target, policy rate set to meet it.",
                "**Interest rate targeting**: steer a short-term market rate.",
                "**Exchange rate targeting**: hold a peg to another currency. The country effectively **imports "
                "the anchor country's monetary policy**."),
              P("Limits of monetary policy: in a **liquidity trap**, extra money is simply held and rates "
                "near zero fail to stimulate. Central banks may then use **quantitative easing**, buying assets "
                "on a large scale.")),
        topic("Stance and policy mix",
              FX("Neutral policy rate = trend real growth + inflation target. Policy rate above neutral = "
                 "contractionary; below = expansionary."),
              EX("Trend real growth is 3% and the inflation target is 4%, so the neutral rate is **7%**. A policy "
                 "rate of 6.5% is below neutral, so policy is **expansionary**."),
              T(["", "Easy fiscal", "Tight fiscal"],
                ["Easy monetary", "Strong stimulus; demand rises", "Low rates; private sector grows as a share"],
                ["Tight monetary", "High rates; public sector grows as a share", "Demand falls; contraction"]),
              FUN("Monetary policy is like a pressure cooker whistle: the RBI raises rates to let out steam "
                  "before inflation blows the lid off.")),
    ],
    revision=sheet("Neutral rate = trend real growth + inflation target · above = tight, below = easy",
                   ("Main objective", "Price stability"),
                   ("Expansionary tools", "Cut repo/CRR, buy bonds"),
                   ("Effective CB", "Independent, credible, transparent"),
                   ("Peg", "Imports anchor country's policy"),
                   ("Liquidity trap", "Rate cuts and extra money don't stimulate"),
                   ("Tight money + easy fiscal", "High rates, bigger public sector"),
                   ("Higher policy rate", "Stronger currency")),
    questions=[
        q("E", "Which is the primary objective of most central banks?",
          ["Price stability", "Maximising tax revenue", "Fixing stock prices"], 0,
          "Most central banks target low, stable inflation.", "4.a"),
        q("M", "A central bank that buys government bonds through open market operations:",
          ["Reduces bank reserves and the money supply", "Increases bank reserves and the money supply",
           "Has no effect on reserves"], 1,
          "Paying for the bonds credits banks' reserve accounts, adding liquidity.", "4.b"),
        q("M", "Trend real growth is 3% and the inflation target is 4%. With a policy rate of 6.5%, monetary "
               "policy is:", ["Contractionary", "Neutral", "Expansionary"], 2,
          "Neutral = 3% + 4% = 7%; a rate below neutral is expansionary.", "4.d"),
        q("E", "In India, the main policy rate set by the RBI's Monetary Policy Committee is the:",
          ["Repo rate", "Banks' prime lending rate", "Government bond coupon"], 0,
          "The repo rate is the rate at which the RBI lends to banks against government securities.", "4.b"),
        q("M", "Raising the reserve requirement most likely:",
          ["Increases bank lending", "Reduces the money multiplier and bank lending", "Lowers the policy rate"],
          1, "Banks must hold more reserves, so less of each deposit can be lent out.", "4.b"),
        q("H", "Which is least likely a quality of an effective central bank?",
          ["Independence", "Transparency", "Frequent unexplained changes to its target"], 2,
          "Credibility depends on clear, consistent and well-explained policy.", "4.c"),
        q("M", "A country that pegs its currency to the US dollar effectively:",
          ["Imports US monetary policy", "Gains full monetary independence", "Must run a budget surplus"], 0,
          "To hold the peg its interest rates must follow US policy.", "4.c"),
        q("H", "A liquidity trap describes a situation in which:",
          ["Inflation is very high", "Lower rates or more money fail to stimulate spending",
           "Banks have too few reserves to lend"], 1,
          "Demand for cash is so high that extra money is hoarded, not spent.", "4.c"),
        q("H", "Tight monetary policy combined with loose fiscal policy most likely leads to:",
          ["Higher interest rates and a larger public sector share of GDP",
           "Lower interest rates and a smaller public sector", "Falling demand from both sides"], 0,
          "Government spending rises while high rates squeeze private borrowing.", "4.e"),
        q("M", "A higher policy rate typically affects the domestic currency by:",
          ["Weakening it", "Leaving it unchanged", "Strengthening it"], 2,
          "Higher returns attract foreign capital, raising demand for the currency.", "4.b"),
    ],
    flashcards=[
        fc("Central bank's main objective", "Price stability (e.g. RBI: 4% CPI, band 2–6%)."),
        fc("Three monetary tools", "Policy rate, reserve requirements, open market operations."),
        fc("Neutral policy rate", "Trend real growth + inflation target."),
        fc("Qualities of an effective central bank", "Independence, credibility, transparency."),
        fc("Liquidity trap", "Rate cuts and more money fail to stimulate; cash is hoarded."),
        fc("Tight money + loose fiscal", "Higher rates; public sector takes a bigger share of GDP."),
    ],
))

# ---------------------------------------------------------------- LM5
LMS.append(dict(
    lm_no=5, title="Introduction to Geopolitics",
    summary="Cooperation vs competition, globalization, tools of geopolitics, geopolitical risk.",
    los=[("5.a", "describe", "Describe geopolitics from a cooperation versus competition perspective."),
         ("5.b", "describe", "Describe geopolitics and its relationship with globalization."),
         ("5.c", "describe", "Describe the tools of geopolitics and their impact on regions and economies."),
         ("5.d", "describe", "Describe geopolitical risk and its impact on investments.")],
    topics=[
        topic("Cooperation, competition and globalization",
              P("**Geopolitics** studies how geography, politics and economics shape relations between "
                "**state actors** (governments) and **non-state actors** (companies, NGOs, individuals)."),
              L("Countries **cooperate** when it serves national interests: security, access to resources, "
                "common standards and rules.",
                "They **compete** when interests clash, especially over strategic resources and technology.",
                "**Globalization** spreads trade, capital, people and ideas across borders. Its opposite, "
                "**nationalism**, puts domestic interests and self-reliance first."),
              T(["Approach", "What it looks like"],
                ["Autarky", "Self-sufficiency; minimal trade; strong state control (non-cooperative, nationalist)"],
                ["Multilateralism", "Many countries cooperating under shared rules (cooperative, globalized)"],
                ["Bilateralism", "Agreements negotiated between two countries at a time"],
                ["Hegemony", "A dominant power shapes the rules others follow"]),
              WO("Globalization lowers costs and widens markets, but it also **transmits shocks** across borders "
                 "faster.")),
        topic("Tools of geopolitics",
              T(["Tool", "Examples"],
                ["National security", "Armed conflict, alliances, espionage, military presence"],
                ["Economic", "Trade agreements, tariffs, quotas, nationalisation, export controls"],
                ["Financial", "Currency arrangements, capital controls, sanctions on financial transactions, "
                              "limits on foreign investment"]),
              P("Non-cooperation raises business costs: firms may duplicate supply chains, face tariffs and lose "
                "access to markets or technology."),
              FUN("Supply chains in a trade war are like a joint family splitting the kitchen: everyone "
                  "suddenly needs their own pressure cooker.")),
        topic("Geopolitical risk",
              T(["Type", "Meaning", "Example"],
                ["Event risk", "Known date, uncertain outcome", "A scheduled national election"],
                ["Exogenous risk", "Sudden and unanticipated", "An unexpected invasion"],
                ["Thematic risk", "Builds over a long period", "Cyber threats, climate-related conflict"]),
              L("Assess each risk's **likelihood**, **velocity** (how fast it hits markets) and **size and "
                "nature** of impact.",
                "High-velocity risks hit prices immediately; low-velocity risks change fundamentals over years.",
                "Respond with scenario analysis, diversification and risk premia in valuation.")),
    ],
    revision=sheet("Risk = likelihood × velocity × size of impact (assess all three)",
                   ("Geopolitics", "Geography + politics + economics"),
                   ("Autarky", "Self-sufficient, nationalist, non-cooperative"),
                   ("Multilateralism", "Many countries, shared rules"),
                   ("Financial tools", "Capital controls, sanctions, FX arrangements"),
                   ("Event risk", "Known date (elections)"),
                   ("Exogenous risk", "Sudden shock"),
                   ("Thematic risk", "Long-running (cyber, climate)")),
    questions=[
        q("E", "Geopolitics is best described as the study of how:",
          ["Geography, politics and economics affect relations between countries and other actors",
           "Companies allocate capital", "Central banks manage balance sheets"], 0,
          "Geopolitics looks at how these forces shape cooperation and competition.", "5.a"),
        q("M", "A country that aims to produce everything it needs and keeps trade to a minimum follows:",
          ["Multilateralism", "Autarky", "Hegemony"], 1,
          "Autarky is self-sufficiency with minimal external dependence.", "5.b"),
        q("M", "Multilateralism is characterised by:",
          ["Many countries cooperating under common rules", "Self-sufficiency with no trade",
           "A single country acting alone"], 0,
          "Multilateral frameworks bind many countries to shared rules, e.g. on trade.", "5.b"),
        q("M", "Which is a financial tool of geopolitics?",
          ["Military alliances", "Capital controls and sanctions on financial transactions", "Espionage"], 1,
          "Alliances and espionage are national security tools.", "5.c"),
        q("E", "A national election on a scheduled date is an example of:",
          ["Exogenous risk", "Thematic risk", "Event risk"], 2,
          "The date is known in advance; only the outcome is uncertain.", "5.d"),
        q("H", "A sudden, unanticipated invasion is best classified as:",
          ["Exogenous risk", "Event risk", "Thematic risk"], 0,
          "Exogenous risks arrive without warning and shock markets.", "5.d"),
        q("H", "Thematic geopolitical risks are those that:",
          ["Occur on a known date", "Evolve and expand over a long period, such as cyber threats",
           "Affect only one company"], 1,
          "Thematic risks build gradually and persist.", "5.d"),
        q("M", "The velocity of a geopolitical risk refers to:",
          ["The probability that it occurs", "The number of countries involved",
           "How quickly it affects markets or the economy"], 2,
          "High-velocity risks hit asset prices almost immediately.", "5.d"),
        q("H", "Rising non-cooperation between countries most likely leads companies to face:",
          ["Higher costs from duplicating supply chains and lower efficiency", "Lower tariffs",
           "Greater access to foreign markets"], 0,
          "Firms must source from more places and lose economies of scale.", "5.c"),
        q("M", "Globalization most likely brings:",
          ["Complete independence from foreign shocks",
           "Wider access to markets and capital, and lower costs, but more exposure to foreign shocks",
           "Higher tariffs"], 1,
          "Closer integration brings benefits but transmits shocks across borders.", "5.b"),
    ],
    flashcards=[
        fc("State vs non-state actors", "Governments vs companies, NGOs and individuals."),
        fc("Autarky", "Self-sufficiency, minimal trade, nationalist and non-cooperative."),
        fc("Three groups of geopolitical tools", "National security, economic, financial."),
        fc("Event vs exogenous vs thematic risk", "Known date vs sudden shock vs long-running."),
        fc("Velocity of geopolitical risk", "How fast the risk affects markets or the economy."),
        fc("Cost of non-cooperation for firms", "Duplicate supply chains, tariffs, lost market access."),
    ],
))

# ---------------------------------------------------------------- LM6
LMS.append(dict(
    lm_no=6, title="International Trade",
    summary="Comparative advantage, benefits and costs of trade, trade restrictions, trading blocs.",
    los=[("6.a", "describe", "Describe the benefits and costs of international trade, including comparative "
                             "advantage."),
         ("6.b", "compare", "Compare types of trade restrictions and their economic implications."),
         ("6.c", "explain", "Explain motivations for and advantages of trading blocs, common markets and "
                            "economic unions.")],
    topics=[
        topic("Comparative advantage, benefits and costs",
              P("A country has an **absolute advantage** if it produces a good using fewer resources. It has a "
                "**comparative advantage** if its **opportunity cost** of producing the good is lower. Trade "
                "follows comparative advantage."),
              EX("Per worker-day, Country A makes 6 cloth or 3 wheat; Country B makes 2 cloth or 2 wheat. A has "
                 "an absolute advantage in both. But a cloth costs A 0.5 wheat and B 1 wheat, so **A has the "
                 "comparative advantage in cloth**. A wheat costs A 2 cloth and B 1 cloth, so **B specialises "
                 "in wheat**."),
              T(["Benefits", "Costs"],
                ["Gains from specialisation and exchange", "Job losses in import-competing industries"],
                ["Economies of scale, more variety", "Wider income inequality"],
                ["Competition and technology transfer", "Adjustment costs for workers and regions"])),
        topic("Trade restrictions",
              T(["Restriction", "How it works", "Who gains"],
                ["Tariff", "Tax on imports", "Domestic producers and the government (revenue)"],
                ["Import quota", "Limit on import quantity", "Holders of import licences (quota rents)"],
                ["Voluntary export restraint", "Exporting country limits its exports",
                 "Foreign producers capture the rents"],
                ["Export subsidy", "Government pays exporters", "Exporters; domestic price rises"]),
              P("Compared with free trade, a tariff **raises the domestic price**, **increases domestic "
                "production**, **reduces consumption and imports**, raises government revenue and creates a "
                "**deadweight loss**. A large country may gain if the tariff improves its terms of trade."),
              WO("A quota's rents go to whoever holds the import licences, not to the government, unless the "
                 "licences are auctioned.")),
        topic("Trading blocs",
              T(["Level", "What it adds"],
                ["Free trade area", "No barriers among members; each keeps its own external policy"],
                ["Customs union", "+ common external trade policy"],
                ["Common market", "+ free movement of labour and capital"],
                ["Economic union", "+ common economic institutions and policy coordination"],
                ["Monetary union", "+ a common currency"]),
              P("Blocs widen markets, raise competition and attract investment. But they can cause **trade "
                "diversion**: imports shift from a cheaper non-member to a costlier member because only the "
                "non-member pays tariffs."),
              FUN("A customs union is a housing society that agrees on one rule for all outside vendors, "
                  "while members borrow each other's ladders for free.")),
    ],
    revision=sheet("Comparative advantage = lower opportunity cost (not lower absolute cost)",
                   ("Tariff effects", "Price ↑, domestic output ↑, imports ↓, revenue ↑, deadweight loss"),
                   ("Quota rent", "Goes to licence holders"),
                   ("VER", "Exporter limits; foreign producers gain rents"),
                   ("Export subsidy", "Raises price in exporting country"),
                   ("Customs union", "FTA + common external policy"),
                   ("Common market", "+ free labour and capital movement"),
                   ("Trade diversion", "Switch to higher-cost member")),
    questions=[
        q("E", "A country has a comparative advantage in a good when it:",
          ["Has a lower opportunity cost of producing it", "Produces more of it per worker",
           "Exports more of it than any other country"], 0,
          "Comparative advantage is about opportunity cost, not output per worker.", "6.a"),
        q("M", "Per worker-day, Country A makes 6 cloth or 3 wheat and Country B makes 2 cloth or 2 wheat. "
               "Country A has a comparative advantage in:", ["Wheat", "Cloth", "Neither good"], 1,
          "A cloth costs A 0.5 wheat but B 1 wheat, so A should specialise in cloth.", "6.a"),
        q("M", "Compared with free trade, an import tariff most likely:",
          ["Lowers the domestic price", "Raises domestic production and government revenue",
           "Raises domestic consumption"], 1,
          "The higher price encourages local output and the tax raises revenue; consumption falls.", "6.b"),
        q("M", "Under an import quota, the gain from the higher domestic price that is not government revenue "
               "is called:", ["Tariff revenue", "A deadweight gain", "Quota rent"], 2,
          "Licence holders buy at the world price and sell at the higher domestic price.", "6.b"),
        q("E", "A free trade area removes trade barriers among members, but:",
          ["Each member keeps its own trade policy toward non-members", "Members share a common currency",
           "Labour moves freely between members"], 0,
          "A common external policy would make it a customs union.", "6.c"),
        q("H", "A common market adds which feature to a customs union?",
          ["A common currency", "Free movement of labour and capital", "A common fiscal policy"], 1,
          "Currency and fiscal coordination come at the monetary and economic union stages.", "6.c"),
        q("H", "Trade diversion occurs when a trading bloc causes imports to:",
          ["Shift from a low-cost non-member to a higher-cost member", "Stop between members",
           "Face higher tariffs between members"], 0,
          "Removing tariffs only for members can make a less efficient member's goods look cheaper.", "6.c"),
        q("M", "A voluntary export restraint differs from an import quota in that:",
          ["The importing government collects tariff revenue", "The quantity of trade is unlimited",
           "The exporting country imposes the limit and its producers capture the rents"], 2,
          "With a VER, foreign exporters sell less but at a higher price, keeping the rents.", "6.b"),
        q("H", "An export subsidy most likely affects the exporting country by:",
          ["Lowering the domestic price there", "Raising the domestic price there and creating a deadweight loss",
           "Having no welfare cost"], 1,
          "Producers divert output to export, so domestic consumers pay more.", "6.b"),
        q("M", "A cost of international trade for an economy is that:",
          ["Consumers have less variety", "Firms lose economies of scale",
           "Workers in import-competing industries may lose jobs"], 2,
          "Trade's gains are broad but its losses are concentrated in exposed industries.", "6.a"),
    ],
    flashcards=[
        fc("Absolute vs comparative advantage", "Fewer resources vs lower opportunity cost."),
        fc("Effects of a tariff", "Domestic price, output and govt revenue rise; imports and consumption fall."),
        fc("Who gets quota rents?", "Holders of import licences."),
        fc("Voluntary export restraint", "The exporter limits sales; foreign producers keep the rents."),
        fc("Trading bloc ladder", "FTA → customs union → common market → economic union → monetary union."),
        fc("Trade diversion", "Imports switch from a cheaper non-member to a costlier member."),
    ],
))

# ---------------------------------------------------------------- LM7
LMS.append(dict(
    lm_no=7, title="Capital Flows and the FX Market",
    summary="FX market participants, nominal and real exchange rates, regimes, capital restrictions.",
    los=[("7.a", "calculate", "Describe the FX market and its participants, distinguish nominal and real "
                              "exchange rates, and calculate the percentage change in a currency."),
         ("7.b", "describe", "Describe exchange rate regimes and the effects of exchange rates on trade and "
                             "capital flows."),
         ("7.c", "describe", "Describe common objectives of capital restrictions imposed by governments.")],
    topics=[
        topic("The FX market and exchange rates",
              L("**Sell side**: large dealing banks that make prices.",
                "**Buy side**: corporations (exporters, importers), real-money investors (pension funds, "
                "insurers), leveraged funds, governments, central banks, sovereign wealth funds, retail.",
                "Instruments: **spot**, **forwards**, **FX swaps** and options."),
              P("Quotes here are written as **rupees per US dollar**. If the rate rises, the dollar has "
                "strengthened and the rupee has weakened."),
              EX("The rate moves from ₹80 to ₹84 per $. The **dollar appreciates 5%** (84 ÷ 80 − 1). In dollar "
                 "terms the rupee goes from 1/80 to 1/84, so it **depreciates 4.76%** (80 ÷ 84 − 1)."),
              FX("Real exchange rate (₹ per $) = nominal rate × (US price level ÷ Indian price level)"),
              EX("Nominal rate stays ₹80 per $. US prices rise 2%, Indian prices 6%. Real rate = 80 × 1.02 ÷ 1.06 "
                 "= **₹76.98**. In real terms the rupee has **appreciated**: Indian goods became relatively "
                 "dearer."),
              WO("Appreciation of one currency and depreciation of the other are **not equal percentages**. "
                 "Always compute each from its own base.")),
        topic("Exchange rate regimes",
              T(["Regime (hardest to most flexible)", "Feature"],
                ["No separate legal tender (dollarisation)", "Uses another country's currency"],
                ["Monetary union", "Shared currency, e.g. the euro"],
                ["Currency board", "Legal commitment to a fixed rate, backed by reserves"],
                ["Conventional peg", "Fixed rate within a narrow band"],
                ["Target zone", "Fixed central rate, wider band"],
                ["Crawling peg", "Peg adjusted periodically in small steps"],
                ["Managed float", "Market-set, with intervention"],
                ["Independent float", "Set by the market"]),
              P("A weaker currency makes exports cheaper and imports dearer, which can improve the trade "
                "balance over time. Exchange rate expectations also drive **capital flows**.")),
        topic("Capital restrictions",
              L("**Objectives**: reduce volatility in domestic asset prices, maintain a fixed exchange rate, "
                "keep domestic interest rates low, protect strategic industries from foreign ownership.",
                "**Forms**: taxes on flows (price controls), limits or outright bans (quantity controls)."),
              WO("Capital controls are least likely used to **encourage** foreign ownership of strategic "
                 "industries; they usually restrict it."),
              FUN("Capital controls are the society watchman at the gate: great for keeping trouble out, "
                  "but the pizza delivery takes longer too.")),
    ],
    revision=sheet("% change = new ÷ old − 1 (compute each currency from its own base) · "
                   "Real ₹/$ = nominal × P_US ÷ P_India",
                   ("Sell side", "Dealing banks"),
                   ("Rate ↑ (₹ per $)", "Dollar stronger, rupee weaker"),
                   ("Real rate", "Adjusts for relative prices"),
                   ("Currency board", "Fixed rate backed by reserves"),
                   ("Crawling peg", "Small periodic adjustments"),
                   ("Depreciation", "Exports cheaper, imports dearer"),
                   ("Capital controls aim to", "Cut volatility, hold peg, keep rates low, protect industry")),
    questions=[
        q("E", "The exchange rate moves from ₹80 to ₹84 per US dollar. The US dollar has:",
          ["Appreciated 5% against the rupee", "Depreciated 5% against the rupee",
           "Appreciated 4.76% against the rupee"], 0, "84 ÷ 80 − 1 = 5%.", "7.a"),
        q("M", "For the same move (₹80 to ₹84 per $), the rupee's change against the dollar is closest to:",
          ["+5.00%", "−4.76%", "−5.00%"], 1, "In dollars per rupee: (1/84) ÷ (1/80) − 1 = 80 ÷ 84 − 1 = −4.76%.",
          "7.a"),
        q("M", "The nominal rate stays at ₹80 per $. US prices rise 2% and Indian prices 6%. The real exchange "
               "rate (₹ per $) is closest to:", ["83.14", "80.00", "76.98"], 2,
          "80 × 1.02 ÷ 1.06 = 76.98.", "7.a"),
        q("M", "A real exchange rate adjusts the nominal exchange rate for:",
          ["Relative price levels in the two countries", "Interest rate differences only", "Transaction costs"],
          0, "It measures the relative purchasing power of the two currencies.", "7.a"),
        q("E", "Which participant is on the sell side of the FX market?",
          ["Exporters", "Large dealing banks", "Pension funds"], 1,
          "Dealing banks quote prices; the others are buy-side users.", "7.a"),
        q("M", "A currency board arrangement:",
          ["Commits by law to exchanging domestic currency for a foreign currency at a fixed rate, backed by "
           "reserves", "Lets the currency float freely", "Needs no foreign reserves"], 0,
          "The board can issue domestic currency only when backed by foreign reserves.", "7.b"),
        q("H", "Under a crawling peg, the exchange rate:",
          ["Floats freely", "Is replaced by a foreign currency", "Is adjusted periodically in small steps"], 2,
          "The peg 'crawls', often to offset inflation differences.", "7.b"),
        q("H", "A government is least likely to impose capital restrictions in order to:",
          ["Reduce volatility in domestic asset prices", "Maintain a fixed exchange rate",
           "Encourage foreign ownership of strategic industries"], 2,
          "Restrictions usually limit foreign ownership of strategic industries.", "7.c"),
        q("M", "Other things equal, a depreciation of the rupee most likely:",
          ["Makes Indian exports cheaper for foreign buyers", "Makes imports cheaper for Indian buyers",
           "Has no effect on trade"], 0,
          "Foreign buyers need fewer units of their own currency to buy Indian goods.", "7.b"),
        q("H", "Dollarisation is an exchange rate regime in which a country:",
          ["Pegs within a wide band", "Uses another country's currency as legal tender", "Floats freely"], 1,
          "It gives up its own currency and monetary policy entirely.", "7.b"),
    ],
    flashcards=[
        fc("Sell side vs buy side in FX", "Dealing banks vs corporates, investors, governments, retail."),
        fc("Rupee change when ₹/$ goes 80 → 84", "80 ÷ 84 − 1 = −4.76% (the dollar rises 5%)."),
        fc("Real exchange rate (₹ per $)", "Nominal × US prices ÷ Indian prices."),
        fc("Currency board", "Legal commitment to a fixed rate, fully backed by foreign reserves."),
        fc("Crawling peg", "Peg adjusted in small, periodic steps."),
        fc("Objectives of capital controls", "Cut asset volatility, hold a peg, keep rates low, protect "
                                             "strategic industries."),
    ],
))

# ---------------------------------------------------------------- LM8
LMS.append(dict(
    lm_no=8, title="Exchange Rate Calculations",
    summary="Cross rates, covered interest rate parity, forward points and forward premiums or discounts.",
    los=[("8.a", "calculate", "Calculate and interpret currency cross-rates."),
         ("8.b", "calculate", "Explain the arbitrage link between spot rates, forward rates and interest rates; "
                              "calculate a forward rate using points or percentages and interpret a forward "
                              "premium or discount.")],
    topics=[
        topic("Cross rates",
              P("A **cross rate** is an exchange rate between two currencies derived through a third, usually "
                "the US dollar or here the rupee."),
              EX("₹/$ = 83.00 and ₹/€ = 90.00. Dollars per euro = 90.00 ÷ 83.00 = **1.0843**. Euros per dollar = "
                 "83.00 ÷ 90.00 = **0.9222**. Check: 1.0843 × 0.9222 ≈ 1."),
              WO("Line the quotes up so the common currency **cancels**. ₹ per € ÷ ₹ per $ = $ per €."),
              FUN("Cross rates are like converting cricket runs to football goals through the canteen's "
                  "samosa price: the common unit cancels and the answer pops out.")),
        topic("Forward rates and interest rate parity",
              FX("Covered interest parity: F = S × (1 + i_price × days/360) ÷ (1 + i_base × days/360), where S "
                 "and F are quoted as price currency per unit of base currency"),
              EX("S = ₹83.00 per $. One-year rates: 7% in India, 5% in the US. F = 83.00 × 1.07 ÷ 1.05 = "
                 "**₹84.58 per $**. The dollar trades at a **forward premium** of 84.58 ÷ 83.00 − 1 ≈ **1.90%**, "
                 "because US rates are lower."),
              L("The **higher-interest currency trades at a forward discount**; the lower-interest currency at a "
                "premium. The forward rate offsets the interest gain, so there is no riskless profit.",
                "If the market forward differs from the parity rate, traders can earn **riskless arbitrage** "
                "until prices realign.",
                "**Forward points** are added to spot: S = 1.1000 $ per € with +25 points (4-decimal quote) gives "
                "F = 1.1000 + 0.0025 = **1.1025**."),
              EX("S = 1.2000 $ per £; 180-day rates: USD 4%, GBP 5% (actual/360). F = 1.2000 × (1 + 0.04 × 0.5) "
                 "÷ (1 + 0.05 × 0.5) = 1.2000 × 1.02 ÷ 1.025 = **1.1941**: sterling, the higher-yielding currency, "
                 "trades at a forward discount.")),
    ],
    revision=sheet("F/S = (1 + i_price τ) ÷ (1 + i_base τ) · Forward premium % = F ÷ S − 1",
                   ("Cross rate", "Divide quotes so the common currency cancels"),
                   ("₹/€ ÷ ₹/$", "= $ per €"),
                   ("Higher interest currency", "Forward discount"),
                   ("Lower interest currency", "Forward premium"),
                   ("Forward points", "Add to spot (÷10,000 for 4-decimal quotes)"),
                   ("Parity breaks", "Riskless arbitrage until it holds")),
    questions=[
        q("E", "₹/$ = 83.00 and ₹/€ = 90.00. The dollars-per-euro cross rate is closest to:",
          ["1.0843", "0.9222", "7.00"], 0, "90.00 ÷ 83.00 = 1.0843.", "8.a"),
        q("M", "From the same quotes, the euros-per-dollar rate is closest to:",
          ["1.0843", "0.9222", "0.9000"], 1, "83.00 ÷ 90.00 = 0.9222.", "8.a"),
        q("M", "Covered interest rate parity says the forward premium or discount reflects:",
          ["Expected inflation only", "Current account balances",
           "The interest rate differential between the two currencies"], 2,
          "The forward rate offsets the interest gain from holding the higher-yielding currency.", "8.b"),
        q("M", "Spot is ₹83.00 per $. One-year rates are 7% in India and 5% in the US. The no-arbitrage one-year "
               "forward rate (₹ per $) is closest to:", ["84.58", "81.45", "83.00"], 0,
          "83.00 × 1.07 ÷ 1.05 = 84.58. 81.45 inverts the interest ratio.", "8.b"),
        q("M", "In that example, the US dollar trades at a forward:",
          ["Discount, because US rates are lower", "Premium, because US rates are lower",
           "Premium, because US rates are higher"], 1,
          "The lower-interest currency trades at a forward premium.", "8.b"),
        q("E", "A currency with higher interest rates typically trades at a forward:",
          ["Discount", "Premium", "Par"], 0,
          "The forward discount offsets its interest advantage.", "8.b"),
        q("H", "Spot is 1.1000 US dollars per euro and 3-month forward points are +25 (4-decimal quote). The "
               "3-month forward rate is:", ["1.1250", "1.0975", "1.1025"], 2,
          "25 points = 0.0025, so F = 1.1000 + 0.0025 = 1.1025.", "8.b"),
        q("H", "Spot is ₹83.00 per $ and the forward is ₹84.58. The dollar's forward premium as a percentage of "
               "spot is closest to:", ["1.90%", "1.58%", "0.19%"], 0, "84.58 ÷ 83.00 − 1 = 1.90%.", "8.b"),
        q("H", "Spot is 1.2000 USD per GBP. 180-day rates (actual/360): USD 4%, GBP 5%. The 180-day forward (USD "
               "per GBP) is closest to:", ["1.2059", "1.1941", "1.2000"], 1,
          "1.2000 × 1.02 ÷ 1.025 = 1.1941; sterling trades at a forward discount.", "8.b"),
        q("M", "If the market forward rate differs from the rate implied by covered interest parity, traders "
               "can earn:", ["Only a risky speculative return", "A riskless arbitrage profit",
                             "Nothing, because forwards cannot be traded"], 1,
          "Borrowing in one currency, converting, investing and locking in the forward gives a riskless gain.",
          "8.b"),
    ],
    flashcards=[
        fc("Cross rate $ per €", "(₹ per €) ÷ (₹ per $)."),
        fc("Covered interest parity", "F = S × (1 + i_price τ) ÷ (1 + i_base τ)."),
        fc("Which currency trades at a forward discount?", "The one with the higher interest rate."),
        fc("Forward premium %", "F ÷ S − 1."),
        fc("Forward points on a 4-decimal quote", "Divide by 10,000 and add to spot (e.g. +25 = +0.0025)."),
        fc("What if parity fails?", "Riskless (covered) interest arbitrage until it holds."),
    ],
))


if __name__ == "__main__":
    write_pack("ec", "Economics", LMS)
