"""Corporate Finance (CFA "Corporate Issuers") content pack.  python scripts/build_pack_cf.py, then re-seed."""

from packlib import EX, FUN, FX, OL, WO, H, L, P, T, fc, q, sheet, topic, write_pack

LMS = []

# ---------------------------------------------------------------- LM1
LMS.append(dict(
    lm_no=1, title="Organizational Forms",
    summary="Business forms, features of corporations, and public versus private ownership.",
    los=[("1.a", "compare", "Compare the main organizational forms of businesses."),
         ("1.b", "describe", "Describe the key features of corporate issuers."),
         ("1.c", "compare", "Compare publicly and privately owned corporate issuers.")],
    topics=[
        topic("Forms of business",
              P("Every business has to answer four questions: who owns it, who runs it, who is liable for its debts, "
                "and how its profits are taxed. The answers define its **organizational form**."),
              T(["Form", "Owner liability", "Who runs it", "Taxation"],
                ["Sole proprietorship", "Unlimited", "The owner", "Owner level only (pass-through)"],
                ["General partnership", "Unlimited, shared", "The partners", "Partner level only"],
                ["Limited partnership", "GP unlimited; LPs limited", "General partner", "Partner level only"],
                ["Corporation", "Limited", "Professional managers, overseen by a board",
                 "Company level, then dividends taxed again"]),
              WO("In a limited partnership, the **general partner** runs the business and carries unlimited "
                 "liability. Limited partners only supply capital, so their loss is capped at what they put in."),
              FUN("A sole proprietor is like a home tiffin service: the cook, the cashier and the person "
                  "the customer shouts at are all the same person.")),
        topic("Features of corporations",
              L("**Separate legal entity**: the company can own assets, sign contracts, sue and be sued.",
                "**Limited liability**: shareholders can lose at most what they invested.",
                "**Separation of ownership and control**: owners elect a board, the board hires managers. This "
                "makes raising capital easy but creates principal–agent conflicts.",
                "**Double taxation** in many countries: profit is taxed at the company and dividends are taxed "
                "again in shareholders' hands."),
              EX("Sagar Ltd earns ₹100 of profit. Corporate tax is 25%, so ₹75 is left and paid out as dividends. "
                 "Dividend tax is 20%, so the shareholder keeps 75 × 0.80 = ₹60. The **effective tax rate is "
                 "40%**. A pass-through firm taxed once at 30% would leave ₹70."),
              WO("Limited liability protects shareholders, not managers who commit fraud, and not partners in a "
                 "general partnership.")),
        topic("Public and private companies",
              P("A **public company** has shares listed and traded on an exchange. A **private company** does "
                "not, so its shares are harder to sell and its disclosure obligations are lighter."),
              T(["", "Public", "Private"],
                ["Share liquidity", "High (exchange-traded)", "Low (negotiated sales)"],
                ["Disclosure and regulation", "Extensive, periodic", "Limited"],
                ["Access to capital", "Broad, from many investors", "Narrower: founders, VC, PE"],
                ["Ownership", "Dispersed", "Concentrated"]),
              H("Ways to go public or private"),
              L("**IPO**: the company issues new shares to the public with investment-bank underwriting.",
                "**Direct listing**: existing shares start trading; no new capital is raised.",
                "**SPAC**: a listed shell raises cash in its own IPO, then merges with a private company.",
                "**Going private / LBO**: a buyer, often private equity funded largely with debt, buys all "
                "public shares and delists the company."),
              WO("A direct listing raises **no new money**. It only gives existing holders a market to sell "
                 "into.")),
    ],
    revision=sheet("Effective tax under double taxation = 1 − (1 − t_corp) × (1 − t_div)",
                   ("Sole proprietor", "Unlimited liability, owner-run, pass-through tax"),
                   ("General partner", "Runs the LP, unlimited liability"),
                   ("Limited partner", "Capital only, limited liability"),
                   ("Corporation", "Separate entity, limited liability, double tax"),
                   ("Direct listing", "Listing without raising capital"),
                   ("SPAC", "Listed shell that acquires a private company"),
                   ("LBO", "Debt-funded buyout that takes a company private")),
    questions=[
        q("E", "Which business form gives its owner unlimited personal liability and taxes profit only at the "
               "owner level?", ["Sole proprietorship", "Corporation", "A limited partner's interest"], 0,
          "A sole proprietor is personally liable for all business debts and the profit is taxed as the "
          "owner's income.", "1.a"),
        q("E", "In a limited partnership, the general partner:",
          ["Has limited liability and no management role", "Manages the business and has unlimited liability",
           "Must be a listed company"], 1,
          "The GP runs the partnership and bears unlimited liability; limited partners only contribute capital.",
          "1.a"),
        q("M", "A key feature that distinguishes a corporation from a partnership is that a corporation:",
          ["Pays tax only at the owner level", "Is a legal entity separate from its owners",
           "Must be run by its owners"], 1,
          "A corporation has its own legal identity: it owns assets, signs contracts and can be sued.", "1.b"),
        q("M", "A company earns ₹100 of profit. Corporate tax is 25% and all after-tax profit is paid as "
               "dividends taxed at 20%. The effective tax rate on the profit is closest to:",
          ["40%", "45%", "25%"], 0,
          "100 × (1 − 0.25) = 75; 75 × (1 − 0.20) = 60 kept, so 40% goes in tax.", "1.b"),
        q("M", "Separation of ownership and control in a corporation most likely leads to:",
          ["Unlimited liability for shareholders", "Shareholders running daily operations",
           "Potential conflicts between managers and shareholders"], 2,
          "Owners delegate decisions to managers whose interests may differ: the principal–agent problem.",
          "1.b"),
        q("E", "Compared with private companies, publicly listed companies typically face:",
          ["Greater regulatory and disclosure requirements", "Fewer reporting obligations",
           "No access to equity markets"], 0,
          "Listed companies must publish periodic financial reports and follow exchange and regulator rules.",
          "1.c"),
        q("M", "A company whose existing shares begin trading on an exchange without issuing new shares or "
               "using underwriters is using a(n):", ["IPO", "SPAC merger", "Direct listing"], 2,
          "A direct listing only lists existing shares; no new capital is raised.", "1.c"),
        q("H", "A special purpose acquisition company (SPAC) is best described as:",
          ["A listed shell that raises cash in an IPO to acquire a private company",
           "A private equity fund that buys listed companies", "A regulator that approves listings"], 0,
          "A SPAC goes public first with only cash, then merges with a private target, which becomes listed.",
          "1.c"),
        q("H", "A public company is most likely to go private through a leveraged buyout in order to:",
          ["Increase its public disclosure", "Restructure away from short-term market scrutiny",
           "Give retail investors more liquidity"], 1,
          "Going private removes listing obligations and quarterly pressure while new owners restructure.",
          "1.c"),
        q("H", "Which statement about pass-through business forms is most accurate?",
          ["Profit is taxed at the entity and again at the owner", "They are exempt from all tax",
           "Profit is taxed only at the owner level"], 2,
          "Partnerships and proprietorships pass profit through to owners, who pay tax once.", "1.a"),
    ],
    flashcards=[
        fc("Which owners have unlimited liability?", "Sole proprietors, general partners and the GP of a limited "
                                                     "partnership."),
        fc("What does a limited partner contribute?", "Capital only. No management role; liability capped at "
                                                      "the investment."),
        fc("Double taxation", "Profit taxed at the company, then dividends taxed again for shareholders."),
        fc("Separation of ownership and control", "Shareholders own, board oversees, managers run: the source of "
                                                  "agency conflicts."),
        fc("Direct listing vs IPO", "Direct listing: existing shares trade, no new money. IPO: new shares sold, "
                                    "capital raised."),
        fc("What is a SPAC?", "A listed cash shell that later merges with a private company to take it public."),
    ],
))

# ---------------------------------------------------------------- LM2
LMS.append(dict(
    lm_no=2, title="Investors and Stakeholders",
    summary="Debt and equity claims, stakeholder groups, and ESG in investment analysis.",
    los=[("2.a", "compare", "Compare the financial claims and motivations of lenders and shareholders."),
         ("2.b", "describe", "Describe a corporation's stakeholder groups and compare their interests."),
         ("2.c", "describe", "Describe environmental, social and governance (ESG) factors in investment "
                             "analysis.")],
    topics=[
        topic("Debt and equity claims",
              P("**Debt holders** have a fixed, contractual claim: interest and principal, ranked ahead of "
                "equity. **Equity holders** have the residual claim on whatever is left after debt is paid."),
              T(["", "Debt holders", "Equity holders"],
                ["Claim", "Fixed, contractual", "Residual"],
                ["Upside", "Capped at interest + principal", "Unlimited"],
                ["Maximum loss", "Amount lent", "Amount invested"],
                ["Preferred risk level", "Lower volatility", "Higher volatility can raise value"]),
              EX("Kaveri Motors has ₹100 crore of debt due next year. If its assets are then worth ₹150 crore, "
                 "lenders get ₹100 crore and **shareholders get ₹50 crore**. If assets are worth ₹80 crore, "
                 "lenders take all ₹80 crore and shareholders get nothing, but lose no more than their stake."),
              WO("Equity behaves like a **call option** on the company's assets with a strike price equal to the "
                 "debt. This is why shareholders may favour riskier projects than lenders do.")),
        topic("Stakeholder groups",
              L("**Shareholders**: want higher share value and dividends.",
                "**Creditors**: want timely interest and principal, so prefer stability.",
                "**Board of directors**: oversees management on behalf of shareholders.",
                "**Managers and employees**: pay, job security, career growth.",
                "**Customers and suppliers**: reliable products, fair prices, prompt payment.",
                "**Governments and regulators**: taxes, compliance, protection of the public."),
              P("**Shareholder theory** says management's main goal is to maximise shareholder value. "
                "**Stakeholder theory** says management should balance the interests of all groups affected by "
                "the company."),
              FUN("Running a company is like planning a family trip: shareholders want the best hotel, "
                  "creditors want you to stay within budget, and employees just want a day off.")),
        topic("ESG in investment analysis",
              P("ESG factors are environmental, social and governance issues that can affect a company's risk "
                "and value. Analysts focus on factors that are **material** to the business."),
              T(["Pillar", "Examples"],
                ["Environmental", "Carbon emissions, water use, waste, climate risk"],
                ["Social", "Workplace safety, labour practices, data privacy, community relations"],
                ["Governance", "Board independence, executive pay, shareholder rights, audit quality"]),
              H("ESG investment approaches"),
              L("**Negative (exclusionary) screening**: leave out sectors such as tobacco or weapons.",
                "**Positive / best-in-class screening**: favour leaders on ESG within each sector.",
                "**ESG integration**: build material ESG factors into valuation and risk analysis.",
                "**Thematic investing**: target a theme such as clean energy or water.",
                "**Impact investing**: seek measurable social or environmental outcomes plus a return.",
                "**Engagement / stewardship**: use voting and dialogue to change company behaviour."),
              WO("ESG integration does **not** replace financial analysis. It adds risks and opportunities "
                 "that traditional analysis may miss.")),
    ],
    revision=sheet("Equity payoff at maturity = max(0, assets − debt); debt payoff = min(debt, assets)",
                   ("Debt claim", "Fixed, ranked first, limited upside"),
                   ("Equity claim", "Residual, unlimited upside, loss capped"),
                   ("Risk preference", "Lenders prefer low risk; shareholders may accept more"),
                   ("Shareholder theory", "Maximise shareholder value"),
                   ("Stakeholder theory", "Balance all affected groups"),
                   ("Exclusionary screening", "Remove sectors on ESG grounds"),
                   ("Impact investing", "Measurable outcome plus financial return")),
    questions=[
        q("E", "Compared with equity holders, debt holders have:",
          ["A residual claim with unlimited upside", "A fixed contractual claim with limited upside",
           "No priority in liquidation"], 1,
          "Lenders are owed fixed interest and principal and rank ahead of shareholders.", "2.a"),
        q("M", "A shareholder's payoff resembles a call option on the company's assets because shareholders:",
          ["Gain all value above the debt but can lose at most their investment",
           "Receive fixed interest payments", "Rank first in liquidation"], 0,
          "Above the debt level each extra rupee of asset value goes to equity; below it, equity is worth zero.",
          "2.a"),
        q("M", "A company's assets are worth ₹150 crore when its ₹100 crore of debt matures. Shareholders "
               "receive:", ["₹100 crore", "₹150 crore", "₹50 crore"], 2,
          "Lenders are paid ₹100 crore first; the residual 150 − 100 = ₹50 crore belongs to shareholders.", "2.a"),
        q("M", "Which stakeholder group generally prefers lower company risk?",
          ["Shareholders", "Creditors", "Managers paid mainly in stock options"], 1,
          "Creditors' upside is capped, so extra risk only raises their chance of loss.", "2.b"),
        q("E", "Under shareholder theory, management's primary goal is to:",
          ["Maximise shareholder value", "Treat every stakeholder group equally", "Maximise employee wages"], 0,
          "Shareholder theory puts the owners' value first.", "2.b"),
        q("M", "Stakeholder theory differs from shareholder theory in that it:",
          ["Ignores shareholders entirely", "Requires no board of directors",
           "Considers employees, customers, suppliers and others alongside shareholders"], 2,
          "Stakeholder theory widens the objective to everyone the company affects.", "2.b"),
        q("E", "Which is a governance (G) factor in ESG analysis?",
          ["Carbon emissions", "Board independence", "Workplace safety"], 1,
          "Emissions are environmental and workplace safety is social; board independence is governance.", "2.c"),
        q("H", "An investor that removes tobacco and weapons companies from its portfolio is using:",
          ["Thematic investing", "Impact investing", "Negative (exclusionary) screening"], 2,
          "Excluding whole sectors on ESG grounds is negative screening.", "2.c"),
        q("H", "Impact investing is best described as investing that:",
          ["Seeks measurable social or environmental outcomes alongside a financial return",
           "Excludes every company with any ESG risk", "Ranks stocks by price momentum"], 0,
          "Impact investors target a specific, measurable positive outcome as well as a return.", "2.c"),
        q("H", "ESG integration in investment analysis means:",
          ["Investing only in green bonds", "Including material ESG factors in valuation and risk assessment",
           "Replacing financial analysis with ESG scores"], 1,
          "Integration adds material ESG risks and opportunities to normal fundamental analysis.", "2.c"),
    ],
    flashcards=[
        fc("Debt holder claim", "Fixed and contractual; ranks ahead of equity; upside capped."),
        fc("Equity holder claim", "Residual; unlimited upside; loss capped at the investment."),
        fc("Why is equity like a call option?", "Shareholders get max(0, assets − debt) at debt maturity."),
        fc("Shareholder vs stakeholder theory", "Maximise owner value vs balance all affected groups."),
        fc("Three ESG pillars", "Environmental, Social, Governance."),
        fc("Negative screening", "Excluding sectors or companies on ESG grounds, e.g. tobacco."),
    ],
))

# ---------------------------------------------------------------- LM3
LMS.append(dict(
    lm_no=3, title="Corporate Governance",
    summary="Principal–agent conflicts, governance mechanisms, and analysing governance risk.",
    los=[("3.a", "describe", "Describe principal–agent relationships and conflicts between stakeholder groups."),
         ("3.b", "describe", "Describe mechanisms used to manage stakeholder relationships and reduce conflicts."),
         ("3.c", "describe", "Describe the risks and benefits of corporate governance and stakeholder "
                             "management."),
         ("3.d", "describe", "Describe factors relevant to analysing a company's corporate governance.")],
    topics=[
        topic("Principal–agent conflicts",
              P("A **principal–agent relationship** exists when one party (the agent) acts on behalf of another "
                "(the principal). Conflicts arise when the agent's interests differ."),
              T(["Conflict", "Typical behaviour"],
                ["Shareholders vs managers", "Insufficient effort, empire building, entrenchment, perks, too much "
                                             "or too little risk"],
                ["Controlling vs minority shareholders", "Dual-class voting, related-party transactions at "
                                                         "unfair prices"],
                ["Shareholders vs creditors", "Riskier projects, extra debt, large dividends that weaken "
                                              "lenders' security"],
                ["Company vs other stakeholders", "Cutting safety, delaying supplier payments, avoiding "
                                                  "regulation"]),
              WO("**Dual-class shares** give founders more votes than their economic ownership. Control and "
                 "cash-flow rights are no longer aligned, so minority holders carry more agency risk.")),
        topic("Governance mechanisms",
              H("Shareholders"),
              L("**General meetings**: an ordinary resolution needs a simple majority; an **extraordinary "
                "(special) resolution**, e.g. a merger or charter change, needs a supermajority.",
                "**Proxy voting** lets absent shareholders vote.",
                "**Straight voting**: one vote per share per seat, so a majority holder fills every seat. "
                "**Cumulative voting**: votes can be pooled on one candidate, which helps minorities win seats.",
                "**Activism, proxy fights and takeover threats** discipline poor managers."),
              EX("Under cumulative voting, the shares needed to guarantee one seat = shares ÷ (seats + 1) + 1. "
                 "With 1,000 shares and 3 seats: 1,000 ÷ 4 + 1 = **251 shares**. Under straight voting, you "
                 "would need 501 to win any seat."),
              H("Board of directors and committees"),
              L("**Audit**: financial reporting, internal controls, external auditor.",
                "**Remuneration (compensation)**: executive pay linked to long-term performance.",
                "**Nomination**: identifies and recommends board candidates.",
                "**Governance, risk and investment** committees in larger companies."),
              H("Other stakeholders"),
              L("Creditors: **covenants** in loan agreements and bond indentures.",
                "Employees: labour laws, contracts, share plans.",
                "Customers and suppliers: contracts; governments: regulation and laws.")),
        topic("Risks, benefits and analysis",
              T(["Weak governance risks", "Effective governance benefits"],
                ["Poor control systems and fraud", "Better operational efficiency"],
                ["Bad decisions and value destruction", "Lower cost of debt and equity"],
                ["Legal, regulatory and reputational damage", "Stronger financial performance"],
                ["Higher default risk", "Lower default and bankruptcy risk"]),
              H("What an analyst checks"),
              L("Ownership and voting structure (dual-class shares, controlling holders).",
                "Board composition: independence, skills, tenure, staggered terms.",
                "Management remuneration and how it links to strategy.",
                "Investor composition and shareholder activism.",
                "Strength of shareholder rights and takeover defences.",
                "Long-term risk management."),
              FUN("A board full of the promoter's relatives is like a cricket team where the captain's cousins "
                  "are also the umpires.")),
    ],
    revision=sheet("Cumulative voting: shares needed for one seat = shares ÷ (seats + 1) + 1",
                   ("Agent conflict", "Agent's interests differ from the principal's"),
                   ("Empire building", "Growth for its own sake, value-destroying deals"),
                   ("Dual-class shares", "Votes exceed economic ownership"),
                   ("Special resolution", "Mergers, charter changes: supermajority"),
                   ("Audit committee", "Reporting, controls, external auditor"),
                   ("Covenants", "Creditors' main protection"),
                   ("Good governance", "Lower cost of capital, fewer defaults")),
    questions=[
        q("E", "A principal–agent conflict arises when:",
          ["An agent acting for a principal has different interests", "Two companies merge",
           "A company pays taxes"], 0,
          "The conflict exists because the agent may act in its own interest rather than the principal's.",
          "3.a"),
        q("M", "Which is an example of a manager–shareholder conflict?",
          ["Paying suppliers on time", "Empire building through value-destroying acquisitions",
           "Publishing an annual report"], 1,
          "Managers may grow the firm for prestige and pay even when acquisitions destroy value.", "3.a"),
        q("M", "A related-party transaction at a non-market price most likely benefits:",
          ["Minority shareholders", "Controlling shareholders at minority shareholders' expense",
           "Bondholders only"], 1,
          "Controlling holders can move value to entities they own, hurting minority holders.", "3.a"),
        q("M", "A company with dual-class shares most likely:",
          ["Gives founders voting control out of proportion to their economic ownership",
           "Gives every shareholder one vote per rupee invested", "Prevents insiders from voting"], 0,
          "High-vote shares let founders control the company with a smaller equity stake.", "3.a"),
        q("H", "A company has 1,000 voting shares and 3 board seats are up for election under cumulative voting. "
               "The minimum shares needed to guarantee one seat is closest to:", ["334", "501", "251"], 2,
          "Shares ÷ (seats + 1) + 1 = 1,000 ÷ 4 + 1 = 251.", "3.b"),
        q("E", "Which board committee oversees financial reporting and the external auditor?",
          ["Remuneration committee", "Audit committee", "Nomination committee"], 1,
          "The audit committee monitors reporting quality, internal controls and auditor independence.", "3.b"),
        q("M", "Creditors primarily protect their interests through:",
          ["Proxy voting", "Electing the CEO", "Covenants in loan agreements and bond indentures"], 2,
          "Covenants restrict actions such as extra borrowing or large dividends.", "3.b"),
        q("M", "An extraordinary (special) resolution at a general meeting is typically required to:",
          ["Approve a merger or amend the corporate charter", "Reappoint the auditor",
           "Accept the annual accounts"], 0,
          "Major structural changes need a supermajority; routine items need a simple majority.", "3.b"),
        q("H", "Which is most likely a benefit of effective corporate governance?",
          ["A higher cost of capital", "A lower cost of capital and better operational efficiency",
           "Greater default risk"], 1,
          "Investors demand lower returns from well-governed firms, and controls improve operations.", "3.c"),
        q("H", "An analyst worried about management entrenchment would focus most on:",
          ["Dividend yield", "Inventory turnover", "A staggered board and strong takeover defences"], 2,
          "Staggered boards and defences make it hard to replace managers, protecting poor performers.", "3.d"),
    ],
    flashcards=[
        fc("Principal–agent problem", "An agent acting for a principal pursues its own interests."),
        fc("Straight vs cumulative voting", "Straight: majority fills every seat. Cumulative: votes pooled, "
                                            "helping minorities win seats."),
        fc("Cumulative voting: shares for one seat", "Shares ÷ (seats + 1) + 1"),
        fc("Audit committee", "Oversees financial reporting, internal controls and the external auditor."),
        fc("How do creditors protect themselves?", "Covenants in loan agreements and bond indentures."),
        fc("Benefits of good governance", "Better efficiency, lower cost of capital, lower default risk."),
    ],
))

# ---------------------------------------------------------------- LM4
LMS.append(dict(
    lm_no=4, title="Working Capital and Liquidity",
    summary="The cash conversion cycle, sources of liquidity, and short-term financing choices.",
    los=[("4.a", "explain", "Explain the cash conversion cycle and compare issuers' cash conversion cycles."),
         ("4.b", "explain", "Explain liquidity and compare issuers' liquidity levels."),
         ("4.c", "describe", "Describe issuers' objectives and compare methods for managing working capital "
                             "and liquidity.")],
    topics=[
        topic("Cash conversion cycle",
              P("The **cash conversion cycle (CCC)** is the number of days cash is tied up between paying "
                "suppliers and collecting from customers. A shorter cycle needs less working capital."),
              FX("CCC = DIO + DSO − DPO · DIO = 365 ÷ inventory turnover (COGS ÷ avg inventory) · "
                 "DSO = 365 ÷ receivables turnover (sales ÷ avg receivables) · "
                 "DPO = 365 ÷ payables turnover (purchases ÷ avg payables)"),
              EX("Meera Textiles: DIO 45 days, DSO 30 days, DPO 40 days. CCC = 45 + 30 − 40 = **35 days**. "
                 "If it negotiates DPO up to 50 days, CCC falls to 25 days and frees cash."),
              WO("A **negative CCC** is possible: retailers that sell before they pay suppliers are effectively "
                 "financed by those suppliers."),
              H("Working capital approaches"),
              L("**Conservative**: finance current assets mostly with long-term funds; safer but costlier.",
                "**Aggressive**: finance current assets with short-term debt; cheaper but more refinancing risk.",
                "**Moderate**: match the maturity of financing with the assets.")),
        topic("Liquidity",
              P("**Liquidity** is the ability to meet short-term obligations on time without large losses."),
              T(["Primary sources (normal operations)", "Secondary sources (may signal stress)"],
                ["Cash and short-term investments", "Selling long-term assets"],
                ["Cash flow from operations", "Renegotiating debt agreements"],
                ["Short-term funding: bank lines, trade credit", "Filing for bankruptcy protection"]),
              L("**Drags** on liquidity slow cash inflows: uncollected receivables, obsolete inventory, tight "
                "credit markets.",
                "**Pulls** on liquidity speed up outflows: paying suppliers early, reduced credit limits."),
              FX("Current ratio = current assets ÷ current liabilities · Quick ratio = (cash + short-term "
                 "investments + receivables) ÷ current liabilities · Cash ratio = (cash + short-term "
                 "investments) ÷ current liabilities"),
              WO("The quick ratio leaves out **inventory** because it is usually the least liquid current "
                 "asset.")),
        topic("Managing working capital",
              H("Trade credit discounts"),
              FX("Cost of forgoing the discount = (1 + d ÷ (1 − d))^(365 ÷ (credit days − discount days)) − 1"),
              EX("Terms of 2/10, net 30: 2% off if paid within 10 days, otherwise pay in full by day 30. "
                 "Cost of skipping = (1 + 0.02 ÷ 0.98)^(365 ÷ 20) − 1 = **44.6%** a year. Unless the company "
                 "can borrow above 44.6%, it should take the discount."),
              H("Short-term financing"),
              L("**Uncommitted line of credit**: the bank may refuse to lend; no fee, least reliable.",
                "**Committed (regular) line**: the bank commits for a fee; counts as reliable liquidity.",
                "**Revolving credit**: a committed line that can be drawn and repaid repeatedly over years.",
                "**Commercial paper**: short-term unsecured notes issued by large, creditworthy companies.",
                "**Factoring**: selling receivables to a third party at a discount for immediate cash.",
                "**Secured loans** backed by inventory or receivables."),
              FUN("Skipping a 2/10, net 30 discount is like declining a ₹2 cashback every 20 days on a ₹100 "
                  "bill. That is a 44.6% annual return you turned down.")),
    ],
    revision=sheet("CCC = DIO + DSO − DPO · Cost of trade credit = (1 + d/(1 − d))^(365/(N − n)) − 1",
                   ("Shorter CCC", "Less cash tied up"),
                   ("Conservative policy", "Long-term funds for current assets"),
                   ("Aggressive policy", "Short-term funds; refinancing risk"),
                   ("Primary liquidity", "Cash, operating cash flow, short-term funding"),
                   ("Secondary liquidity", "Asset sales, renegotiation, bankruptcy"),
                   ("Quick ratio", "Excludes inventory"),
                   ("2/10, net 30", "Forgoing the discount costs about 44.6% a year")),
    questions=[
        q("E", "The cash conversion cycle equals:", ["DIO + DSO − DPO", "DIO − DSO + DPO", "DSO + DPO − DIO"], 0,
          "Days of inventory plus days to collect, minus days the company takes to pay suppliers.", "4.a"),
        q("M", "A company has DIO of 45 days, DSO of 30 days and DPO of 40 days. Its cash conversion cycle is:",
          ["115 days", "35 days", "55 days"], 1, "45 + 30 − 40 = 35 days.", "4.a"),
        q("M", "Annual credit sales are ₹730 crore and average receivables are ₹60 crore. DSO is closest to:",
          ["12 days", "60 days", "30 days"], 2,
          "Receivables turnover = 730 ÷ 60 = 12.17; DSO = 365 ÷ 12.17 = 30 days.", "4.a"),
        q("M", "A conservative working capital approach is characterised by:",
          ["Financing current assets mostly with long-term funds",
           "Financing current assets mostly with short-term debt", "Holding minimal cash and inventory"], 0,
          "Long-term funding reduces refinancing risk at a higher cost.", "4.c"),
        q("E", "Which is a primary source of liquidity?",
          ["Selling a factory", "Cash balances and short-term investments", "Filing for bankruptcy protection"], 1,
          "Primary sources come from normal operations; asset sales and bankruptcy are secondary.", "4.b"),
        q("M", "The quick ratio excludes inventory from current assets because inventory:",
          ["Is the most liquid current asset", "Is usually the least liquid current asset",
           "Is classified as a liability"], 1,
          "Inventory must first be sold and then collected before it becomes cash.", "4.b"),
        q("H", "A supplier offers terms of 2/10, net 30. The annualised cost of not taking the discount and "
               "paying on day 30 is closest to:", ["24.5%", "36.7%", "44.6%"], 2,
          "(1 + 0.02 ÷ 0.98)^(365 ÷ 20) − 1 = 44.6%.", "4.c"),
        q("H", "Which is a drag on liquidity?",
          ["Faster customer collections", "Longer credit from suppliers", "Uncollected receivables"], 2,
          "Drags slow cash inflows; uncollected receivables delay cash coming in.", "4.b"),
        q("H", "Compared with an uncommitted line of credit, a committed (regular) line of credit:",
          ["Is a firm bank commitment, usually for a fee", "Can be withdrawn by the bank at any time",
           "Must be secured by receivables"], 0,
          "The commitment fee buys reliability, so committed lines count as dependable liquidity.", "4.c"),
        q("M", "Factoring receivables means:",
          ["Borrowing from shareholders", "Selling receivables to a third party at a discount",
           "Delaying payments to suppliers"], 1,
          "The factor pays cash now for the receivables, less a discount, and collects from customers.", "4.c"),
    ],
    flashcards=[
        fc("Cash conversion cycle", "DIO + DSO − DPO: days cash is tied up in operations."),
        fc("DSO", "365 ÷ (sales ÷ average receivables)"),
        fc("Conservative vs aggressive working capital", "Long-term funds (safer, costlier) vs short-term funds "
                                                         "(cheaper, refinancing risk)."),
        fc("Drag vs pull on liquidity", "Drag slows inflows (bad receivables); pull speeds outflows (early "
                                        "payments)."),
        fc("Cost of 2/10, net 30", "(1 + 2/98)^(365/20) − 1 ≈ 44.6% a year."),
        fc("Committed vs uncommitted line", "Committed: bank must lend, fee charged. Uncommitted: bank may "
                                            "refuse."),
    ],
))

# ---------------------------------------------------------------- LM5
LMS.append(dict(
    lm_no=5, title="Capital Investments",
    summary="Types of capital projects, NPV, IRR and ROIC, allocation principles and pitfalls, real options.",
    los=[("5.a", "describe", "Describe the types of capital investments."),
         ("5.b", "calculate", "Describe the capital allocation process; calculate NPV, IRR and ROIC and contrast "
                              "their use."),
         ("5.c", "describe", "Describe principles of capital allocation and common pitfalls."),
         ("5.d", "describe", "Describe types of real options relevant to capital investments.")],
    topics=[
        topic("Types of capital investment",
              L("**Business maintenance (going concern)**: replace worn-out assets to keep operating.",
                "**Business growth**: expand capacity or enter new products and markets.",
                "**Regulatory and compliance**: required by law, e.g. pollution control; may have negative NPV "
                "but are unavoidable.",
                "**Other**: high-risk projects outside the core business, sometimes 'pet projects'."),
              H("The capital allocation process"),
              OL("**Idea generation**", "**Investment analysis**: forecast cash flows, compute NPV / IRR",
                 "**Planning and prioritisation**: fit with strategy and budget",
                 "**Monitoring and post-investment review**: compare actual with forecast to improve future "
                 "decisions")),
        topic("NPV, IRR and ROIC",
              FX("NPV = Σ CF_t ÷ (1 + r)^t − initial outlay · IRR = the rate at which NPV = 0 · "
                 "ROIC = NOPAT ÷ average invested capital"),
              EX("Godavari Packaging can invest ₹100 lakh to earn ₹45 lakh a year for 3 years. At 10%: PV = "
                 "45 × 2.4869 = ₹111.9 lakh, so **NPV = +₹11.9 lakh**. Setting NPV to zero gives **IRR ≈ "
                 "16.7%**, above the 10% cost of capital, so accept."),
              T(["", "NPV", "IRR"],
                ["Output", "Rupee value added", "Percentage return"],
                ["Reinvestment assumption", "At the cost of capital", "At the IRR (often unrealistic)"],
                ["Mutually exclusive projects", "Preferred rule", "Can rank wrongly (scale, timing)"],
                ["Unusual cash flow signs", "Still works", "Can give multiple or no IRRs"]),
              EX("ROIC: NOPAT ₹18 crore ÷ average invested capital ₹120 crore = **15%**. With a cost of capital "
                 "of 11%, the company is creating value."),
              WO("When NPV and IRR disagree on mutually exclusive projects, **choose the higher NPV**: it "
                 "measures the wealth actually added.")),
        topic("Principles, pitfalls and real options",
              H("Principles"),
              L("Use **incremental after-tax cash flows**, not accounting profit.",
                "Ignore **sunk costs**; include **opportunity costs** and **externalities** such as "
                "cannibalisation.",
                "Leave **financing costs** out of cash flows; they are in the discount rate.",
                "Timing matters: earlier cash is worth more."),
              H("Common pitfalls"),
              L("**Inertia**: rolling last year's budget forward.",
                "**Source-of-capital bias**: spending internal cash more freely than raised capital.",
                "Not considering alternatives; **pet projects**; judging projects by EPS, net income or ROE; "
                "optimistic internal forecasts."),
              H("Real options"),
              L("**Timing**: delay until more is known.",
                "**Sizing**: **abandon** if results disappoint, or **expand** if they succeed.",
                "**Flexibility**: change prices (price-setting) or switch inputs and outputs (production).",
                "**Fundamental**: the payoff depends on an underlying asset price, e.g. an oil field."),
              FUN("Including the interest cost in project cash flows and again in the discount rate is like "
                  "paying the auto driver twice for the same ride.")),
    ],
    revision=sheet("NPV = Σ CF/(1 + r)^t − outlay · IRR: NPV = 0 · ROIC = NOPAT / avg invested capital",
                   ("Accept if", "NPV > 0, IRR > cost of capital, ROIC > cost of capital"),
                   ("Conflict", "Mutually exclusive projects: choose higher NPV"),
                   ("IRR reinvestment", "Assumes reinvestment at the IRR"),
                   ("Ignore", "Sunk costs and financing costs"),
                   ("Include", "Opportunity costs, externalities, taxes"),
                   ("Pitfalls", "Inertia, source-of-capital bias, pet projects"),
                   ("Real options", "Timing, sizing (abandon/expand), flexibility, fundamental")),
    questions=[
        q("E", "A project required to comply with new pollution rules is a:",
          ["Regulatory/compliance project", "Business growth project", "Pet project"], 0,
          "Projects mandated by law are regulatory or compliance investments.", "5.a"),
        q("M", "A project costs ₹100 lakh and returns ₹45 lakh a year for 3 years. At a 10% discount rate its "
               "NPV is closest to:", ["₹35.0 lakh", "₹11.9 lakh", "−₹0.5 lakh"], 1,
          "PV = 45 × 2.4869 = 111.9; NPV = 111.9 − 100 = ₹11.9 lakh.", "5.b"),
        q("M", "For the same project (₹100 lakh outlay, ₹45 lakh a year for 3 years), the IRR is closest to:",
          ["10.0%", "35.0%", "16.7%"], 2,
          "The rate where 45 × annuity factor = 100 is about 16.7%.", "5.b"),
        q("E", "When NPV and IRR rank mutually exclusive projects differently, an analyst should generally "
               "prefer the project with the:", ["Higher NPV", "Higher IRR", "Lower initial cost"], 0,
          "NPV measures the rupee value added and assumes reinvestment at the cost of capital.", "5.b"),
        q("M", "NOPAT is ₹18 crore, average invested capital is ₹120 crore and the cost of capital is 11%. "
               "ROIC and the best conclusion are:",
          ["15%; the company is creating value", "15%; the company is destroying value",
           "6.7%; the company is destroying value"], 0,
          "18 ÷ 120 = 15%, above the 11% cost of capital, so value is being created.", "5.b"),
        q("M", "Which should be excluded from a project's incremental cash flows?",
          ["Opportunity costs", "Sunk costs", "Cannibalisation of existing sales"], 1,
          "Sunk costs have already been incurred and do not change with the decision.", "5.c"),
        q("M", "Interest expense is excluded from project cash flows because:",
          ["Interest is not tax-deductible", "Interest is a sunk cost",
           "The cost of financing is already in the discount rate"], 2,
          "Counting interest in cash flows and in the discount rate would double-count it.", "5.c"),
        q("H", "A manager who sets next year's capital budget by raising last year's by a fixed percentage is "
               "showing which pitfall?", ["Real option bias", "Source-of-capital bias", "Inertia"], 2,
          "Rolling forward last year's allocation regardless of opportunities is inertia.", "5.c"),
        q("H", "An option to stop a project and sell its assets if cash flows disappoint is a(n):",
          ["Timing option", "Abandonment option", "Price-setting option"], 1,
          "Abandonment is a sizing option that limits downside.", "5.d"),
        q("H", "The IRR method implicitly assumes interim cash flows are reinvested at:",
          ["The cost of capital", "The IRR itself", "The risk-free rate"], 1,
          "This assumption is one reason IRR can mislead when it is far above the cost of capital.", "5.b"),
    ],
    flashcards=[
        fc("Four types of capital project", "Maintenance, growth, regulatory/compliance, other."),
        fc("NPV decision rule", "Accept if NPV > 0; for exclusive projects pick the highest NPV."),
        fc("IRR", "Discount rate that makes NPV zero; assumes reinvestment at the IRR."),
        fc("ROIC", "NOPAT ÷ average invested capital; compare with the cost of capital."),
        fc("Sunk vs opportunity cost", "Ignore sunk costs; include opportunity costs."),
        fc("Types of real options", "Timing, sizing (abandon/expand), flexibility, fundamental."),
    ],
))

# ---------------------------------------------------------------- LM6
LMS.append(dict(
    lm_no=6, title="Capital Structure",
    summary="Life-cycle financing, Modigliani–Miller, trade-off and pecking order, target weights and WACC.",
    los=[("6.a", "explain", "Explain factors affecting capital structure."),
         ("6.b", "describe", "Describe how a company's capital structure may change over its life cycle."),
         ("6.c", "explain", "Explain the Modigliani–Miller propositions on capital structure."),
         ("6.d", "calculate", "Describe the use of target capital structure in estimating WACC, and calculate "
                              "target weights."),
         ("6.e", "describe", "Describe competing stakeholder interests in capital structure decisions.")],
    topics=[
        topic("Capital structure over the life cycle",
              T(["Stage", "Cash flows", "Typical financing"],
                ["Start-up", "Negative, unpredictable", "Equity (founders, VC); debt hard to get"],
                ["Growth", "Improving but reinvested", "Mostly equity, some secured debt"],
                ["Mature", "Stable, positive", "More debt capacity; investment-grade bonds"]),
              H("Factors affecting capital structure"),
              L("**Internal**: business model, cash flow predictability, asset tangibility (collateral), "
                "existing leverage, corporate tax rate, management policy and credit rating targets.",
                "**External**: market conditions and interest rates, regulation, industry norms."),
              WO("Asset-light companies with intangible assets (software, brands) usually carry **less debt** "
                 "because they have little collateral to pledge.")),
        topic("Modigliani–Miller and other theories",
              T(["", "No taxes", "With corporate taxes"],
                ["Proposition I (value)", "V_L = V_U", "V_L = V_U + tD"],
                ["Proposition II (cost of equity)", "r_e = r_0 + (r_0 − r_d)(D/E)",
                 "r_e = r_0 + (r_0 − r_d)(1 − t)(D/E)"]),
              EX("r_0 = 12%, r_d = 6%, D/E = 0.5, t = 25%. Cost of equity = 12 + (12 − 6) × 0.75 × 0.5 = "
                 "**14.25%**. More debt raises the cost of equity, but with taxes the debt shield still lowers "
                 "WACC."),
              L("**Static trade-off theory**: optimal debt balances the tax shield against the expected costs "
                "of financial distress.",
                "**Pecking order**: managers prefer internal funds, then debt, and new equity last, because "
                "issuing equity signals the shares may be overvalued.",
                "**Signalling**: taking on debt signals confidence in future cash flows.",
                "**Agency costs**: debt disciplines managers by committing cash to interest payments."),
              FUN("Under MM with no taxes, cutting a pizza into more slices doesn't give you more pizza. "
                  "Taxes are the only thing that makes the debt slice taste better.")),
        topic("Target structure, WACC and stakeholders",
              FX("WACC = w_d × r_d × (1 − t) + w_p × r_p + w_e × r_e, using target weights at market values"),
              EX("Target weights: debt 1/3, equity 2/3. After-tax cost of debt = 6% × 0.75 = 4.5%; cost of "
                 "equity 14.25%. WACC = 1/3 × 4.5 + 2/3 × 14.25 = 1.5 + 9.5 = **11.0%**."),
              P("If the target is not disclosed, analysts use the current market-value structure, trends in the "
                "company's structure, or peer averages."),
              H("Competing stakeholder interests"),
              L("Shareholders may favour more debt to boost returns and use the tax shield.",
                "Existing creditors lose when extra debt or a debt-funded special dividend raises default risk.",
                "Managers may prefer low debt to protect their jobs."),
              WO("Use **market values**, not book values, for the weights. Book equity can be far from what "
                 "investors actually pay.")),
    ],
    revision=sheet("MM with tax: V_L = V_U + tD · r_e = r_0 + (r_0 − r_d)(1 − t)D/E · "
                   "WACC = w_d r_d(1 − t) + w_e r_e",
                   ("Start-up", "Equity-funded, little debt"),
                   ("Mature", "Stable cash flows, more debt"),
                   ("MM I, no tax", "Value unaffected by leverage"),
                   ("MM II", "Cost of equity rises with D/E"),
                   ("Trade-off", "Tax shield vs distress costs"),
                   ("Pecking order", "Internal → debt → equity"),
                   ("Weights", "Target, at market values")),
    questions=[
        q("E", "A start-up company typically relies mostly on:",
          ["Equity financing", "Long-term bank debt", "Investment-grade bonds"], 0,
          "Negative, uncertain cash flows and little collateral make debt hard to obtain.", "6.b"),
        q("M", "Mature companies can usually support more debt because they have:",
          ["High cash burn", "Stable and predictable cash flows", "No tangible assets"], 1,
          "Predictable cash flows make it easier to service interest and principal.", "6.b"),
        q("M", "Under Modigliani–Miller Proposition I without taxes:",
          ["Firm value is independent of capital structure", "Firm value rises with debt",
           "The cost of equity stays constant as debt rises"], 0,
          "With no taxes or frictions, how the pie is sliced does not change its size.", "6.c"),
        q("H", "Unlevered cost of capital is 12%, cost of debt 6%, D/E 0.5 and tax rate 25%. Under MM with "
               "taxes, the cost of equity is closest to:", ["15.0%", "14.25%", "12.0%"], 1,
          "12 + (12 − 6) × (1 − 0.25) × 0.5 = 14.25%.", "6.c"),
        q("M", "With corporate taxes, MM Proposition I states that:",
          ["V_L = V_U", "V_L = V_U − tD", "V_L = V_U + tD"], 2,
          "The levered firm is worth more by the present value of the debt tax shield, tD.", "6.c"),
        q("M", "Under the pecking order theory, managers prefer to finance first with:",
          ["New equity", "New debt", "Internal funds"], 2,
          "Internal funds avoid issuance costs and negative signals; equity comes last.", "6.a"),
        q("H", "The static trade-off theory says the optimal capital structure balances:",
          ["The tax benefit of debt against the costs of financial distress", "Dividends against buybacks",
           "Equity issuance against share splits"], 0,
          "Beyond some point, extra distress costs outweigh the extra tax shield.", "6.a"),
        q("H", "Target weights are debt 1/3 and equity 2/3. After-tax cost of debt is 4.5% and cost of equity "
               "14.25%. WACC is closest to:", ["9.4%", "11.0%", "12.0%"], 1,
          "1/3 × 4.5 + 2/3 × 14.25 = 1.5 + 9.5 = 11.0%.", "6.d"),
        q("M", "When estimating WACC, analysts prefer weights based on:",
          ["Historical book values only", "Equal weights for each source",
           "The company's target capital structure at market values"], 2,
          "WACC applies to future projects, so target market-value weights are most relevant.", "6.d"),
        q("H", "Borrowing to pay a large special dividend most likely benefits:",
          ["Shareholders at the expense of existing creditors", "Existing creditors at shareholders' expense",
           "Neither group"], 0,
          "Cash goes to shareholders while creditors face higher leverage and default risk.", "6.e"),
    ],
    flashcards=[
        fc("MM Proposition I (no taxes)", "V_L = V_U: capital structure doesn't affect firm value."),
        fc("MM Proposition I (with taxes)", "V_L = V_U + tD"),
        fc("MM Proposition II (with taxes)", "r_e = r_0 + (r_0 − r_d)(1 − t)(D/E)"),
        fc("Static trade-off theory", "Tax shield of debt vs expected costs of financial distress."),
        fc("Pecking order", "Internal funds → debt → new equity."),
        fc("Which weights for WACC?", "Target capital structure at market values."),
    ],
))

# ---------------------------------------------------------------- LM7
LMS.append(dict(
    lm_no=7, title="Business Models",
    summary="Value proposition, channels, pricing and revenue models, and common business model types.",
    los=[("7.a", "describe", "Describe key features of business models."),
         ("7.b", "describe", "Describe various types of business models.")],
    topics=[
        topic("Key features of a business model",
              P("A **business model** explains how a company creates value for customers and captures some of "
                "it as profit. Analysts ask: **who** are the customers, **what** is sold, **where** and **how** "
                "it reaches them, and **how much** it costs."),
              L("**Value proposition**: target customers, the product or service, and why it beats "
                "alternatives.",
                "**Value chain**: the activities that deliver the value proposition.",
                "**Channels**: direct, indirect (distributors, retailers) or **omnichannel**, which blends "
                "online and physical stores into one experience.",
                "**Pricing and revenue model**: how and when money comes in."),
              H("Pricing approaches"),
              T(["Approach", "Idea", "Example"],
                ["Value-based", "Price what the customer will pay", "Premium brand"],
                ["Cost-based", "Cost plus a markup", "Commodity goods"],
                ["Tiered / price discrimination", "Different prices for different groups", "Student discounts"],
                ["Dynamic", "Price moves with demand", "Ride-hailing surge, airline fares"],
                ["Freemium", "Basic free, premium paid", "Music and cloud apps"],
                ["Razors-and-blades", "Cheap base, profitable refills", "Printers and ink"],
                ["Subscription", "Recurring fee for access", "OTT streaming"])),
        topic("Types of business models",
              L("**Conventional**: manufacturers, distributors, retailers, service firms.",
                "**Platform / network effects**: each extra user makes the service more valuable to others, "
                "e.g. marketplaces and payment apps.",
                "**Crowdsourcing**: users contribute content or ideas.",
                "**Asset-light**: outsource capital-intensive work and focus on brand, design or software.",
                "**Licensing and franchising**: the owner licenses its brand and system to operators for fees "
                "and royalties.",
                "**Private label / contract manufacturing**: making products sold under another brand."),
              EX("Swara Music charges ₹499 a month; serving each subscriber costs ₹149 a month, so the "
                 "contribution is ₹350. Acquiring a customer costs ₹2,100, so **payback = 2,100 ÷ 350 = 6 "
                 "months**. If subscribers stay well beyond 6 months, the model works."),
              WO("Network effects can make winners dominant, but they work in reverse too: if users leave, the "
                 "platform becomes less valuable to everyone left."),
              FUN("A food-delivery app is a perfect platform: restaurants join because hungry users are there, "
                  "and hungry users are there because the restaurants joined.")),
    ],
    revision=sheet("CAC payback (months) = customer acquisition cost ÷ monthly contribution per customer",
                   ("Business model", "How value is created and captured"),
                   ("Value proposition", "Who, what, why it beats alternatives"),
                   ("Omnichannel", "Online and physical channels combined"),
                   ("Dynamic pricing", "Price varies with demand"),
                   ("Razors-and-blades", "Cheap base, profitable consumables"),
                   ("Network effects", "More users, more value per user"),
                   ("Asset-light", "Outsource capital-heavy activities")),
    questions=[
        q("E", "A company's value proposition describes:",
          ["Its target customers and why they should choose its product", "Its loan covenants",
           "Its corporate tax rate"], 0,
          "The value proposition covers who the customer is, what is offered and why it is better.", "7.a"),
        q("M", "A company that sells printers cheaply and earns its profit on ink cartridges uses:",
          ["Dynamic pricing", "Razors-and-blades pricing", "Cost-plus pricing"], 1,
          "The base product is priced low to lock in recurring purchases of profitable consumables.", "7.a"),
        q("M", "Freemium pricing means that:",
          ["A basic version is free and premium features are paid for", "Every product is sold at cost",
           "Prices change by time of day"], 0,
          "Free users are the funnel; revenue comes from those who upgrade.", "7.a"),
        q("M", "A ride-hailing app that raises fares during peak demand is using:",
          ["Bundling", "Tiered pricing", "Dynamic pricing"], 2,
          "Prices that move with real-time demand are dynamic pricing.", "7.a"),
        q("H", "A platform business benefits from network effects when:",
          ["Each additional user makes the service more valuable to other users",
           "Unit costs rise as it grows", "It owns all the inventory it sells"], 0,
          "Network effects mean value per user rises with the number of users.", "7.b"),
        q("E", "A franchise business model typically involves:",
          ["The company owning and running every outlet",
           "The franchisor licensing its brand and system to independent operators for fees",
           "Government ownership of outlets"], 1,
          "Franchisees run outlets using the franchisor's brand and processes, paying fees and royalties.", "7.b"),
        q("M", "A subscription costs ₹499 a month, the variable cost per subscriber is ₹149 a month and customer "
               "acquisition cost is ₹2,100. The payback period on acquisition cost is:",
          ["4.2 months", "6 months", "14 months"], 1,
          "Monthly contribution = 499 − 149 = 350; 2,100 ÷ 350 = 6 months.", "7.a"),
        q("H", "An asset-light business model most likely:",
          ["Owns all its factories and logistics", "Requires the highest capital expenditure in its industry",
           "Outsources capital-intensive activities and keeps fixed assets low"], 2,
          "Asset-light firms focus on brand, design or software and outsource heavy assets.", "7.b"),
        q("H", "Charging students a lower price than corporate buyers for the same course is an example of:",
          ["Price discrimination (tiered pricing)", "Cost-based pricing", "Bundling"], 0,
          "Different prices for different customer groups for the same product is price discrimination.", "7.a"),
        q("M", "An omnichannel strategy:",
          ["Sells only through distributors", "Uses only a direct sales force",
           "Integrates online and physical channels into one customer experience"], 2,
          "Omnichannel blends store, web and app so customers can switch between them seamlessly.", "7.a"),
    ],
    flashcards=[
        fc("Business model questions", "Who, what, where, how, how much."),
        fc("Value-based vs cost-based pricing", "What the customer will pay vs cost plus a markup."),
        fc("Razors-and-blades", "Cheap base product, profit on consumables (printer and ink)."),
        fc("Network effects", "Each extra user makes the service more valuable to others."),
        fc("Asset-light model", "Outsource capital-intensive activities; keep fixed assets low."),
        fc("CAC payback", "Customer acquisition cost ÷ monthly contribution per customer."),
    ],
))


if __name__ == "__main__":
    # Prototype questions 43–45 are governance/ESG items that were filed under LM1.
    write_pack("cf", "Corporate Finance", LMS, {"43": 3, "44": 3, "45": 2})
