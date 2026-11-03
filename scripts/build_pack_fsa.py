"""Financial Statement Analysis content pack.  python scripts/build_pack_fsa.py, then re-seed."""

from packlib import EX, FUN, FX, OL, WO, H, L, P, T, fc, q, sheet, topic, write_pack

LMS = []

# ---------------------------------------------------------------- LM1
LMS.append(
    dict(
        lm_no=1,
        title="Introduction to Financial Statement Analysis",
        summary="Roles of the statements and other sources, standard-setters, the conceptual framework and the "
        "analysis process.",
        los=[
            (
                "1.a",
                "describe",
                "Describe the roles of financial statement analysis and of the key financial statements.",
            ),
            ("1.b", "describe", "Describe the importance of notes, MD&A and the audit report."),
            (
                "1.c",
                "describe",
                "Describe the roles of standard-setting bodies and regulators, and the qualitative "
                "characteristics of financial reports.",
            ),
            ("1.d", "describe", "Describe the steps in the financial statement analysis framework."),
        ],
        topics=[
            topic(
                "The statements and other sources",
                T(
                    ["Statement", "Shows"],
                    [
                        "Statement of financial position (balance sheet)",
                        "Assets, liabilities, equity at a point in time",
                    ],
                    ["Income statement / comprehensive income", "Revenue, expenses, profit over a period"],
                    ["Statement of changes in equity", "Movements in each equity component"],
                    ["Cash flow statement", "Operating, investing and financing cash flows"],
                ),
                L(
                    "**Notes** explain policies, estimates and details behind the numbers.",
                    "**MD&A** (management commentary): results, trends, risks and outlook in management's words.",
                    "**Auditor's report**: opinion on whether statements are fairly presented. **Unqualified** "
                    "(clean), "
                    "**qualified** (except for…), **adverse** (not fair), or **disclaimer** (unable to form an "
                    "opinion).",
                    "Other sources: earnings calls, industry data, economic data, press releases.",
                ),
                WO("An audit gives **reasonable** assurance, not a guarantee that there is no fraud."),
            ),
            topic(
                "Standards and the framework",
                L(
                    "**Standard-setters** write the rules: IASB (IFRS) and FASB (US GAAP). India's Ind AS are "
                    "converged with IFRS.",
                    "**Regulators** enforce them and require filing: SEC in the US, SEBI in India.",
                    "**Fundamental qualitative characteristics**: **relevance** (including materiality) and "
                    "**faithful representation** (complete, neutral, free from error).",
                    "**Enhancing**: comparability, verifiability, timeliness, understandability.",
                    "Constraint: benefits of information should exceed its cost.",
                ),
                FUN(
                    "Standard-setters write the cricket rulebook; regulators are the umpires; auditors are the third "
                    "umpire checking the replay."
                ),
            ),
            topic(
                "The analysis framework",
                OL(
                    "Define the **purpose** and context.",
                    "**Collect** data.",
                    "**Process** data (adjust, compute ratios, common-size).",
                    "**Analyse and interpret**.",
                    "**Communicate** conclusions.",
                    "**Follow up** and update.",
                ),
                EX(
                    "A bank evaluating a ₹50 crore loan to a textile firm: purpose = repayment ability; collect five "
                    "years of statements; compute interest coverage and debt/EBITDA; conclude and write a credit "
                    "note; review each quarter."
                ),
            ),
        ],
        revision=sheet(
            "Framework: purpose → collect → process → analyse → communicate → follow up",
            ("Balance sheet", "Point in time"),
            ("Income statement", "Over a period"),
            ("Notes / MD&A", "Policies and management's commentary"),
            ("Unqualified opinion", "Clean audit report"),
            ("Standard-setters", "IASB, FASB"),
            ("Regulators", "SEC, SEBI"),
            ("Fundamental qualities", "Relevance, faithful representation"),
        ),
        questions=[
            q(
                "E",
                "Which statement reports a company's financial position at a point in time?",
                ["Income statement", "Balance sheet", "Cash flow statement"],
                1,
                "The balance sheet is a snapshot.",
                "1.a",
            ),
            q(
                "M",
                "An auditor's opinion stating the statements are fairly presented except for one matter is:",
                ["Qualified", "Unqualified", "Adverse"],
                0,
                "Qualified = 'except for'.",
                "1.b",
            ),
            q(
                "E",
                "The body that issues IFRS is the:",
                ["SEC", "IASB", "FASB"],
                1,
                "The IASB writes IFRS; FASB writes US GAAP.",
                "1.c",
            ),
            q(
                "M",
                "The two fundamental qualitative characteristics of useful financial information are:",
                ["Timeliness and comparability", "Relevance and faithful representation", "Verifiability and cost"],
                1,
                "The others are enhancing characteristics.",
                "1.c",
            ),
            q(
                "M",
                "The role of a securities regulator such as SEBI is mainly to:",
                ["Write accounting standards", "Enforce reporting requirements and oversee markets", "Audit companies"],
                1,
                "Regulators enforce; standard-setters write.",
                "1.c",
            ),
            q(
                "E",
                "Management's discussion of results, risks and outlook is found in the:",
                ["MD&A", "Auditor's report", "Statement of changes in equity"],
                0,
                "MD&A gives management's view.",
                "1.b",
            ),
            q(
                "M",
                "The first step in the financial statement analysis framework is to:",
                ["Collect data", "Compute ratios", "Define the purpose and context"],
                2,
                "The purpose shapes everything after.",
                "1.d",
            ),
            q(
                "H",
                "An audit provides:",
                [
                    "Absolute assurance that there is no fraud",
                    "Reasonable assurance that statements are free of material misstatement",
                    "No assurance at all",
                ],
                1,
                "Audits test samples and judgements; assurance is reasonable.",
                "1.b",
            ),
            q(
                "M",
                "Computing ratios and preparing common-size statements belongs to which step?",
                ["Collect", "Process", "Follow up"],
                1,
                "Processing turns raw data into analysable form.",
                "1.d",
            ),
            q(
                "E",
                "Information is material if:",
                ["It is in the notes", "Omitting or misstating it could influence users' decisions", "It is audited"],
                1,
                "Materiality is part of relevance.",
                "1.c",
            ),
        ],
        flashcards=[
            fc("Four main statements", "Financial position, comprehensive income, changes in equity, cash flows."),
            fc("Audit opinion types", "Unqualified, qualified, adverse, disclaimer."),
            fc("Standard-setters vs regulators", "IASB/FASB write rules; SEC/SEBI enforce."),
            fc("Fundamental qualities", "Relevance and faithful representation."),
            fc("Enhancing qualities", "Comparability, verifiability, timeliness, understandability."),
            fc("Analysis framework", "Purpose, collect, process, analyse, communicate, follow up."),
        ],
    )
)

# ---------------------------------------------------------------- LM2
LMS.append(
    dict(
        lm_no=2,
        title="Analyzing Income Statements",
        summary="Revenue and expense recognition, non-recurring items, EPS and common-size analysis.",
        los=[
            ("2.a", "evaluate", "Evaluate the revenue recognition and expense recognition policies of a company."),
            (
                "2.b",
                "describe",
                "Describe non-recurring items, discontinued operations and changes in accounting policy.",
            ),
            ("2.c", "calculate", "Calculate and interpret basic and diluted earnings per share."),
            (
                "2.d",
                "evaluate",
                "Evaluate a company's financial performance using common-size income statements and margins.",
            ),
        ],
        topics=[
            topic(
                "Revenue and expense recognition",
                P(
                    "Under **accrual accounting**, revenue is recognised when it is earned (control of goods or "
                    "services "
                    "passes to the customer), not when cash arrives. The five-step model:"
                ),
                OL(
                    "Identify the contract.",
                    "Identify the performance obligations.",
                    "Determine the transaction price.",
                    "Allocate the price to each obligation.",
                    "Recognise revenue as each obligation is satisfied.",
                ),
                L(
                    "Expenses are matched to the revenue they help generate, or to the period.",
                    "**Principal vs agent**: a principal reports gross revenue; an agent reports only its commission.",
                ),
                EX(
                    "A software firm sells a ₹12 lakh package: licence (₹8 lakh value) and one-year support (₹4 lakh). "
                    "It recognises ₹8 lakh at delivery and ₹4 lakh evenly over 12 months."
                ),
            ),
            topic(
                "Non-recurring items and EPS",
                L(
                    "**Discontinued operations** are shown separately, net of tax, below continuing profit.",
                    "Unusual or infrequent items are in continuing operations but disclosed; analysts often exclude "
                    "them when forecasting.",
                    "Policy changes are applied **retrospectively**; changes in estimates **prospectively**.",
                ),
                FX("Basic EPS = (Net income − preferred dividends) ÷ weighted average shares"),
                EX(
                    "Net income ₹1,000 crore, preferred dividends ₹100 crore, weighted shares 300 crore: basic EPS = "
                    "**₹3.00**. Convertible preferred would add 50 crore shares; diluted EPS = 1,000 ÷ 350 = ₹2.86, "
                    "lower, so it is dilutive."
                ),
                H("Treasury stock method for options"),
                EX(
                    "100 options at exercise price ₹20, average share price ₹25. Proceeds 2,000 buy back 2,000 ÷ 25 = "
                    "80 "
                    "shares. Net new shares = **20**."
                ),
                WO("A security is **antidilutive** if including it raises EPS; it is then left out of diluted EPS."),
            ),
            topic(
                "Common-size analysis and margins",
                P("Express every line as a **percentage of revenue** to compare across years and companies."),
                T(
                    ["Margin", "Formula"],
                    ["Gross margin", "Gross profit ÷ revenue"],
                    ["Operating margin", "Operating profit ÷ revenue"],
                    ["Pre-tax margin", "EBT ÷ revenue"],
                    ["Net margin", "Net income ÷ revenue"],
                ),
                FUN(
                    "A common-size income statement is like comparing two thalis by the share of rice, dal and "
                    "sweets, so a giant wedding thali and a small office one can be judged fairly."
                ),
            ),
        ],
        revision=sheet(
            "Basic EPS = (NI − pref div) ÷ weighted shares · Treasury stock: new shares = N − N×X/avg P",
            ("Revenue recognition", "When control passes to the customer"),
            ("Five steps", "Contract, obligations, price, allocate, recognise"),
            ("Principal vs agent", "Gross vs net revenue"),
            ("Discontinued ops", "Separate, net of tax"),
            ("Policy change", "Retrospective"),
            ("Estimate change", "Prospective"),
            ("Antidilutive", "Raises EPS; excluded"),
        ),
        questions=[
            q(
                "E",
                "Under accrual accounting, revenue is recognised when:",
                ["Cash is received", "It is earned, as control passes to the customer", "The invoice is printed"],
                1,
                "Recognition follows the transfer of goods or services.",
                "2.a",
            ),
            q(
                "M",
                "Net income is ₹1,000 crore, preferred dividends ₹100 crore and weighted shares 300 crore. Basic EPS "
                "is:",
                ["₹3.33", "₹3.00", "₹2.86"],
                1,
                "(1,000 − 100)/300 = 3.00.",
                "2.c",
            ),
            q(
                "H",
                "100 options with exercise price ₹20 are outstanding; the average share price is ₹25. Under the "
                "treasury stock method, incremental shares are:",
                ["100", "80", "20"],
                2,
                "Proceeds buy back 80 shares, so 20 are net new.",
                "2.c",
            ),
            q(
                "M",
                "A convertible security whose conversion would raise EPS is:",
                ["Dilutive", "Antidilutive and excluded", "Always included"],
                1,
                "Antidilutive securities are excluded.",
                "2.c",
            ),
            q(
                "M",
                "Results of a business segment the company has sold are reported:",
                ["Within operating expenses", "As discontinued operations, net of tax", "Only in the notes"],
                1,
                "Shown separately so users can focus on continuing operations.",
                "2.b",
            ),
            q(
                "E",
                "Gross profit margin is calculated as:",
                ["Gross profit ÷ revenue", "Net income ÷ revenue", "Revenue ÷ total assets"],
                0,
                "Gross margin definition.",
                "2.d",
            ),
            q(
                "M",
                "A travel website that arranges hotel bookings without bearing inventory risk is an agent and reports:",
                ["The full booking value as revenue", "Only its commission as revenue", "No revenue"],
                1,
                "Agents report net revenue.",
                "2.a",
            ),
            q(
                "H",
                "A change in an accounting estimate, such as an asset's useful life, is applied:",
                ["Retrospectively", "Prospectively", "Never"],
                1,
                "Estimates change going forward.",
                "2.b",
            ),
            q(
                "M",
                "In a common-size income statement, each line is expressed as a percentage of:",
                ["Total assets", "Revenue", "Net income"],
                1,
                "Revenue is the base.",
                "2.d",
            ),
            q(
                "E",
                "The final step of the five-step revenue model is to:",
                ["Identify the contract", "Recognise revenue as obligations are satisfied", "Set the price"],
                1,
                "Revenue is recognised as each obligation is met.",
                "2.a",
            ),
        ],
        flashcards=[
            fc("Five-step revenue model", "Contract, obligations, price, allocate, recognise."),
            fc("Principal vs agent", "Gross revenue vs commission only."),
            fc("Basic EPS", "(NI − preferred dividends) ÷ weighted average shares."),
            fc("Treasury stock method", "Option proceeds buy back shares at the average price."),
            fc("Antidilutive security", "Would raise EPS; excluded from diluted EPS."),
            fc("Policy vs estimate change", "Retrospective vs prospective."),
        ],
    )
)

# ---------------------------------------------------------------- LM3
LMS.append(
    dict(
        lm_no=3,
        title="Analyzing Balance Sheets",
        summary="Classification and measurement of assets and liabilities, financial instruments, equity, and "
        "liquidity and solvency ratios.",
        los=[
            (
                "3.a",
                "explain",
                "Explain the classification and measurement of current and non-current assets and liabilities.",
            ),
            ("3.b", "describe", "Describe the measurement of financial instruments, intangibles and goodwill."),
            ("3.c", "describe", "Describe the components of equity."),
            (
                "3.d",
                "calculate",
                "Calculate and interpret common-size balance sheets and liquidity and solvency ratios.",
            ),
        ],
        topics=[
            topic(
                "Classification and measurement",
                L(
                    "**Current** items are expected to be realised or settled within one year (or the operating "
                    "cycle). The rest are **non-current**.",
                    "Measurement bases: **historical cost**, **amortised cost**, **fair value**.",
                    "**Goodwill** = price paid in an acquisition − fair value of net identifiable assets. Not "
                    "amortised; "
                    "tested for impairment.",
                    "Internally generated brands and goodwill are **not** recognised as assets.",
                ),
                T(
                    ["Financial asset category", "Measured at", "Changes in value go to"],
                    ["Amortised cost (hold to collect)", "Amortised cost", "Not recognised"],
                    ["FVOCI", "Fair value", "Other comprehensive income"],
                    ["FVPL", "Fair value", "Profit or loss"],
                ),
                EX(
                    "Ganga Retail pays ₹900 crore for a company whose identifiable net assets are worth ₹700 crore at "
                    "fair "
                    "value. Goodwill = **₹200 crore**."
                ),
            ),
            topic(
                "Equity",
                L(
                    "Share capital and share premium (contributed capital).",
                    "**Retained earnings**.",
                    "**Accumulated other comprehensive income**.",
                    "Treasury shares (bought back, deducted).",
                    "**Non-controlling interest**: the part of subsidiaries not owned by the parent.",
                ),
            ),
            topic(
                "Ratios",
                T(
                    ["Ratio", "Formula", "Tells you"],
                    ["Current ratio", "Current assets ÷ current liabilities", "Short-term liquidity"],
                    ["Quick ratio", "(Cash + marketable securities + receivables) ÷ CL", "Liquidity without inventory"],
                    ["Cash ratio", "(Cash + marketable securities) ÷ CL", "Strictest liquidity test"],
                    ["Debt-to-equity", "Total debt ÷ total equity", "Solvency, leverage"],
                    ["Financial leverage", "Total assets ÷ total equity", "Leverage"],
                ),
                EX(
                    "Current assets ₹500 crore (inventory 200), current liabilities ₹250 crore. Current ratio = "
                    "**2.0**; "
                    "quick ratio = 300 ÷ 250 = **1.2**."
                ),
                WO("A high current ratio can hide slow-moving inventory. The quick ratio strips it out."),
                FUN(
                    "Goodwill is the extra money you pay for a sweet shop because the queue outside is long. You "
                    "can't sell the queue separately, but you paid for it."
                ),
            ),
        ],
        revision=sheet(
            "Current ratio = CA/CL · Quick = (cash + MS + AR)/CL · Goodwill = price − FV net assets",
            ("Current", "Within one year or operating cycle"),
            ("Amortised cost", "Hold-to-collect debt"),
            ("FVOCI", "Value changes to OCI"),
            ("FVPL", "Value changes to profit"),
            ("Goodwill", "Not amortised; impairment test"),
            ("NCI", "Minority share of subsidiaries"),
        ),
        questions=[
            q(
                "M",
                "A company pays ₹900 crore for a business with identifiable net assets at fair value of ₹700 crore. "
                "Goodwill is:",
                ["₹200 crore", "₹900 crore", "₹1,600 crore"],
                0,
                "900 − 700 = 200.",
                "3.b",
            ),
            q(
                "E",
                "Goodwill acquired in a business combination is:",
                ["Amortised over 5 years", "Not amortised but tested for impairment", "Expensed immediately"],
                1,
                "Goodwill is tested at least annually for impairment.",
                "3.b",
            ),
            q(
                "M",
                "Current assets ₹500 crore including ₹200 crore inventory; current liabilities ₹250 crore. The quick "
                "ratio (assume no prepaid items) is:",
                ["2.0", "1.2", "0.8"],
                1,
                "(500 − 200)/250 = 1.2.",
                "3.d",
            ),
            q(
                "M",
                "Changes in the fair value of an equity investment classified at FVPL are reported in:",
                ["Profit or loss", "Other comprehensive income", "Retained earnings directly"],
                0,
                "FVPL means through profit or loss.",
                "3.b",
            ),
            q(
                "E",
                "A debt investment held only to collect contractual cash flows is measured at:",
                ["Fair value through profit or loss", "Amortised cost", "Replacement cost"],
                1,
                "Hold-to-collect → amortised cost.",
                "3.b",
            ),
            q(
                "H",
                "Which is not recognised as an asset on the balance sheet?",
                ["Purchased patents", "Goodwill from an acquisition", "Internally generated brand value"],
                2,
                "Internally created brands cannot be capitalised.",
                "3.b",
            ),
            q(
                "M",
                "The part of a subsidiary's equity not owned by the parent is:",
                ["Treasury stock", "Non-controlling interest", "Retained earnings"],
                1,
                "NCI is shown within equity.",
                "3.c",
            ),
            q(
                "E",
                "Liabilities due to be settled within one year are classified as:",
                ["Non-current", "Current", "Contingent"],
                1,
                "One year or the operating cycle.",
                "3.a",
            ),
            q(
                "M",
                "Debt-to-equity is a measure of:",
                ["Liquidity", "Solvency", "Profitability"],
                1,
                "It shows the reliance on debt financing.",
                "3.d",
            ),
            q(
                "H",
                "A company's current ratio is high but its quick ratio is low. This suggests:",
                [
                    "Large inventories relative to other current assets",
                    "Very high cash balances",
                    "No current liabilities",
                ],
                0,
                "Inventory explains the gap.",
                "3.d",
            ),
        ],
        flashcards=[
            fc("Current vs non-current", "Within one year/operating cycle vs longer."),
            fc("Financial asset categories", "Amortised cost, FVOCI, FVPL."),
            fc("Goodwill", "Price paid − fair value of net identifiable assets; impairment-tested."),
            fc("Current ratio", "Current assets ÷ current liabilities."),
            fc("Quick ratio", "(Cash + marketable securities + receivables) ÷ CL."),
            fc("Non-controlling interest", "Share of subsidiaries owned by outsiders."),
        ],
    )
)

# ---------------------------------------------------------------- LM4
LMS.append(
    dict(
        lm_no=4,
        title="Analyzing Statements of Cash Flows I",
        summary="Classifying cash flows, IFRS versus US GAAP, and the direct and indirect methods.",
        los=[
            ("4.a", "describe", "Describe the operating, investing and financing classifications of cash flows."),
            ("4.b", "contrast", "Contrast cash flow statements prepared under IFRS and US GAAP."),
            ("4.c", "contrast", "Contrast the direct and indirect methods of presenting operating cash flow."),
            ("4.d", "prepare", "Prepare an operating cash flow section using the indirect method."),
        ],
        topics=[
            topic(
                "The three sections",
                T(
                    ["Section", "Examples"],
                    ["Operating (CFO)", "Cash from customers, paid to suppliers, staff, taxes"],
                    ["Investing (CFI)", "Buying or selling PP&E, investments, acquisitions"],
                    ["Financing (CFF)", "Issuing or repaying debt, issuing shares, buybacks, dividends paid (US GAAP)"],
                ),
                T(
                    ["Item", "IFRS", "US GAAP"],
                    ["Interest paid", "CFO or CFF", "CFO"],
                    ["Interest received", "CFO or CFI", "CFO"],
                    ["Dividends paid", "CFO or CFF", "CFF"],
                    ["Dividends received", "CFO or CFI", "CFO"],
                    ["Taxes paid", "CFO unless linked to investing/financing", "CFO"],
                ),
                WO(
                    "Non-cash transactions, like converting debt to equity, do not appear in the cash flow statement; "
                    "they are disclosed in notes."
                ),
            ),
            topic(
                "Direct and indirect methods",
                P(
                    "The **direct method** lists actual cash receipts and payments. The **indirect method** starts "
                    "from "
                    "net income and adjusts it. Both give the same CFO; IFRS and US GAAP encourage direct but most "
                    "companies use indirect."
                ),
                OL(
                    "Start with **net income**.",
                    "Add back **non-cash expenses** (depreciation, amortisation).",
                    "Subtract **gains** / add losses on investing and financing items.",
                    "Adjust for working capital: **increase in current assets → subtract**; **increase in current "
                    "liabilities → add**.",
                ),
                EX(
                    "Net income ₹100 crore; depreciation ₹30 crore; gain on sale of machine ₹10 crore; receivables up "
                    "₹15 "
                    "crore; inventory down ₹5 crore; payables up ₹8 crore. CFO = 100 + 30 − 10 − 15 + 5 + 8 = **₹118 "
                    "crore**."
                ),
                FUN(
                    "Net income is the selfie with filters; CFO is the photo your aunt takes at the wedding. Same "
                    "person, very different look."
                ),
            ),
        ],
        revision=sheet(
            "Indirect CFO = NI + non-cash charges − gains + losses − ΔCA (non-cash) + ΔCL (operating)",
            ("CFO", "Day-to-day operations"),
            ("CFI", "Long-term assets, investments"),
            ("CFF", "Debt and equity financing"),
            ("US GAAP", "Interest paid/received and dividends received in CFO; dividends paid in CFF"),
            ("IFRS", "More choice for interest and dividends"),
            ("Increase in receivables", "Subtract"),
            ("Increase in payables", "Add"),
        ),
        questions=[
            q(
                "E",
                "Purchase of a new factory is classified as:",
                ["Operating cash flow", "Investing cash flow", "Financing cash flow"],
                1,
                "PP&E purchases are investing.",
                "4.a",
            ),
            q(
                "M",
                "Under US GAAP, dividends paid are classified as:",
                ["Operating", "Investing", "Financing"],
                2,
                "Dividends paid are CFF under US GAAP.",
                "4.b",
            ),
            q(
                "M",
                "Under IFRS, interest paid may be classified as:",
                ["Operating or financing", "Investing only", "Financing only"],
                0,
                "IFRS gives a choice.",
                "4.b",
            ),
            q(
                "H",
                "NI ₹100 crore, depreciation ₹30 crore, gain on asset sale ₹10 crore, receivables +₹15 crore, "
                "inventory "
                "−₹5 crore, payables +₹8 crore. CFO is:",
                ["₹118 crore", "₹138 crore", "₹98 crore"],
                0,
                "100 + 30 − 10 − 15 + 5 + 8 = 118.",
                "4.d",
            ),
            q(
                "M",
                "Under the indirect method, an increase in accounts receivable is:",
                ["Added to net income", "Subtracted from net income", "Ignored"],
                1,
                "Sales were not yet collected in cash.",
                "4.d",
            ),
            q(
                "E",
                "The direct method of presenting CFO:",
                ["Starts from net income", "Shows actual cash receipts and payments", "Is required under US GAAP only"],
                1,
                "It lists cash from customers, paid to suppliers, and so on.",
                "4.c",
            ),
            q(
                "M",
                "A gain on the sale of equipment is, in the indirect method:",
                ["Added back", "Subtracted", "Classified as CFF"],
                1,
                "The cash proceeds are in CFI, so the gain is removed from CFO.",
                "4.d",
            ),
            q(
                "M",
                "Converting bonds into common shares appears:",
                ["In CFF", "In CFI", "Only in the notes as a non-cash transaction"],
                2,
                "No cash changes hands.",
                "4.a",
            ),
            q(
                "E",
                "Depreciation is added back in the indirect method because it is:",
                ["A cash inflow", "A non-cash expense", "A financing item"],
                1,
                "It reduced net income without using cash.",
                "4.d",
            ),
            q(
                "H",
                "Both methods of presenting operating cash flow produce:",
                ["Different CFO totals", "The same CFO total", "The same net income only"],
                1,
                "Only the presentation differs.",
                "4.c",
            ),
        ],
        flashcards=[
            fc("CFO / CFI / CFF", "Operations / long-term assets and investments / debt and equity."),
            fc(
                "US GAAP interest and dividends",
                "Interest paid/received and dividends received: CFO. Dividends paid: CFF.",
            ),
            fc("IFRS flexibility", "Interest and dividends can be CFO, CFI or CFF depending on type."),
            fc("Indirect method start", "Net income."),
            fc("Increase in current assets", "Subtract in indirect CFO."),
            fc("Increase in current liabilities", "Add in indirect CFO."),
        ],
    )
)

# ---------------------------------------------------------------- LM5
LMS.append(
    dict(
        lm_no=5,
        title="Analyzing Statements of Cash Flows II",
        summary="Interpreting cash flows, common-size cash flow statements, free cash flow and cash flow ratios.",
        los=[
            ("5.a", "analyze", "Analyse and interpret a cash flow statement and its links to the other statements."),
            ("5.b", "calculate", "Calculate and interpret free cash flow to the firm and free cash flow to equity."),
            ("5.c", "calculate", "Calculate and interpret cash flow ratios."),
        ],
        topics=[
            topic(
                "Reading a cash flow statement",
                L(
                    "A healthy, mature firm: positive CFO that covers capex and dividends.",
                    "A growing firm: CFO may be below net income as working capital builds; heavy CFI outflows.",
                    "Red flag: CFO persistently below net income, or CFO propped up by stretching payables or selling "
                    "receivables.",
                    "**Common-size** cash flows: each item as % of revenue, or inflows/outflows as % of totals.",
                ),
                WO("Selling assets each year to fund dividends shows up as CFI inflows. It is not sustainable."),
            ),
            topic(
                "Free cash flow",
                FX("FCFF = CFO + interest × (1 − t) − capex · FCFE = CFO − capex + net borrowing"),
                EX(
                    "CFO ₹500 crore, interest paid ₹80 crore (in CFO), tax 25%, capex ₹200 crore, net borrowing ₹50 "
                    "crore. "
                    "FCFF = 500 + 80 × 0.75 − 200 = **₹360 crore**. FCFE = 500 − 200 + 50 = **₹350 crore**."
                ),
                WO("Under IFRS, if interest paid was put in CFF, do **not** add it back to CFO when computing FCFF."),
            ),
            topic(
                "Cash flow ratios",
                T(
                    ["Ratio", "Formula"],
                    ["Cash flow to revenue", "CFO ÷ revenue"],
                    ["Cash return on assets", "CFO ÷ average total assets"],
                    ["Cash flow to income", "CFO ÷ operating income"],
                    ["Debt coverage", "CFO ÷ total debt"],
                    ["Interest coverage", "(CFO + interest paid + taxes paid) ÷ interest paid"],
                    ["Reinvestment", "CFO ÷ cash paid for long-term assets"],
                    ["Dividend payment", "CFO ÷ dividends paid"],
                ),
                FUN(
                    "Profit is opinion, cash is fact. A company with great profits and no cash is like a groom with a "
                    "great horoscope who can't pay for the wedding."
                ),
            ),
        ],
        revision=sheet(
            "FCFF = CFO + Int(1 − t) − FCInv · FCFE = CFO − FCInv + net borrowing",
            ("CFO < NI persistently", "Earnings-quality red flag"),
            ("Common-size CF", "Items as % of revenue"),
            ("Debt coverage", "CFO ÷ total debt"),
            ("Reinvestment ratio", "CFO ÷ capex"),
            ("Dividend payment ratio", "CFO ÷ dividends"),
        ),
        questions=[
            q(
                "M",
                "CFO ₹500 crore (interest ₹80 crore paid in CFO), tax 25%, capex ₹200 crore. FCFF is:",
                ["₹360 crore", "₹300 crore", "₹380 crore"],
                0,
                "500 + 60 − 200 = 360.",
                "5.b",
            ),
            q(
                "M",
                "CFO ₹500 crore, capex ₹200 crore and net borrowing ₹50 crore. FCFE is:",
                ["₹250 crore", "₹350 crore", "₹750 crore"],
                1,
                "500 − 200 + 50 = 350.",
                "5.b",
            ),
            q(
                "E",
                "The cash flow to revenue ratio is:",
                ["CFO ÷ revenue", "Net income ÷ revenue", "Capex ÷ revenue"],
                0,
                "It measures cash generated per rupee of sales.",
                "5.c",
            ),
            q(
                "H",
                "A company reports net income well above CFO year after year. This most likely suggests:",
                [
                    "High earnings quality",
                    "Possible aggressive accruals or working capital build-up",
                    "Very conservative accounting",
                ],
                1,
                "Profits not turning into cash are a warning sign.",
                "5.a",
            ),
            q(
                "M",
                "The reinvestment ratio is:",
                ["CFO ÷ cash paid for long-term assets", "Dividends ÷ CFO", "Debt ÷ CFO"],
                0,
                "It shows whether operations fund capex.",
                "5.c",
            ),
            q(
                "M",
                "Under IFRS a company classifies interest paid in CFF. To compute FCFF from CFO you should:",
                ["Add after-tax interest to CFO", "Not add interest back", "Subtract interest twice"],
                1,
                "Interest was never deducted in CFO.",
                "5.b",
            ),
            q(
                "E",
                "Debt coverage is measured as:",
                ["CFO ÷ total debt", "Total debt ÷ equity", "EBIT ÷ interest"],
                0,
                "Higher is better.",
                "5.c",
            ),
            q(
                "M",
                "A company funding dividends by selling assets each year would show:",
                ["Large CFI inflows", "Large CFO inflows", "No change in CFI"],
                0,
                "Asset sales are investing inflows.",
                "5.a",
            ),
            q(
                "H",
                "Free cash flow to equity is the cash available to:",
                ["All capital providers", "Common shareholders after debt payments and reinvestment", "Lenders only"],
                1,
                "FCFE is after net borrowing and capex.",
                "5.b",
            ),
            q(
                "E",
                "A common-size cash flow statement often expresses items as a percentage of:",
                ["Revenue", "Total equity", "Share price"],
                0,
                "Revenue is a common base.",
                "5.a",
            ),
        ],
        flashcards=[
            fc("FCFF", "CFO + interest(1 − t) − capex."),
            fc("FCFE", "CFO − capex + net borrowing."),
            fc("Red flag", "CFO persistently below net income."),
            fc("Cash flow to revenue", "CFO ÷ revenue."),
            fc("Reinvestment ratio", "CFO ÷ cash paid for long-term assets."),
            fc("IFRS FCFF trap", "If interest paid sits in CFF, don't add it back."),
        ],
    )
)

# ---------------------------------------------------------------- LM6
LMS.append(
    dict(
        lm_no=6,
        title="Analysis of Inventories",
        summary="Cost formulas, LIFO and the LIFO reserve, write-downs, and inventory ratios.",
        los=[
            ("6.a", "describe", "Describe the measurement of inventory and the cost formulas."),
            (
                "6.b",
                "calculate",
                "Calculate and compare cost of sales, gross profit and ending inventory under different methods.",
            ),
            ("6.c", "explain", "Explain LIFO reserve and LIFO liquidation, and inventory write-downs."),
            ("6.d", "calculate", "Calculate and interpret inventory ratios."),
        ],
        topics=[
            topic(
                "Cost formulas",
                L(
                    "**Specific identification**: for unique items (jewellery, cars).",
                    "**FIFO**: first in, first out. Ending inventory at recent costs.",
                    "**Weighted average cost**.",
                    "**LIFO**: last in, first out. Allowed under **US GAAP only**, not IFRS.",
                ),
                EX(
                    "Opening: 100 units at ₹10. Bought 100 at ₹12. Sold 150. FIFO COGS = 100×10 + 50×12 = **₹1,600**; "
                    "ending inventory 50×12 = ₹600. Weighted average cost = 2,200 ÷ 200 = ₹11; COGS = **₹1,650**; "
                    "ending "
                    "₹550. LIFO COGS = 100×12 + 50×10 = **₹1,700**; ending ₹500."
                ),
                WO(
                    "When prices rise, **LIFO** gives the highest COGS, lowest profit, lowest taxes and lowest "
                    "inventory. "
                    "FIFO gives the opposite. Cash flow is higher under LIFO because of lower taxes."
                ),
            ),
            topic(
                "LIFO reserve, liquidation and write-downs",
                L(
                    "**LIFO reserve** = FIFO inventory − LIFO inventory. To convert LIFO to FIFO: inventory + reserve; "
                    "COGS − increase in reserve.",
                    "**LIFO liquidation**: selling more than is bought dips into old cheap layers; profit jumps for "
                    "one "
                    "year, which is not sustainable.",
                    "**IFRS**: lower of cost and **net realisable value**; write-downs **can be reversed**.",
                    "**US GAAP**: lower of cost and NRV (FIFO, average); lower of cost or market (LIFO); **no "
                    "reversals**.",
                ),
                FUN(
                    "A LIFO liquidation is like finally eating the sweets hidden at the back of the cupboard since "
                    "Diwali three years ago. Great day, not repeatable."
                ),
            ),
            topic(
                "Ratios",
                FX("Inventory turnover = COGS ÷ average inventory · Days of inventory on hand = 365 ÷ turnover"),
                EX("COGS ₹730 crore, average inventory ₹73 crore. Turnover = 10×; DOH = **36.5 days**."),
                WO("A very high turnover may also mean stock-outs and lost sales; compare with sales growth."),
            ),
        ],
        revision=sheet(
            "LIFO reserve = FIFO inv − LIFO inv · FIFO COGS = LIFO COGS − Δ reserve",
            ("Rising prices, LIFO", "Higher COGS, lower profit, lower tax, lower inventory"),
            ("Rising prices, FIFO", "Lower COGS, higher profit, current-cost inventory"),
            ("LIFO", "US GAAP only"),
            ("IFRS write-down", "Lower of cost and NRV; reversals allowed"),
            ("US GAAP write-down", "No reversals"),
            ("DOH", "365 ÷ inventory turnover"),
        ),
        questions=[
            q(
                "M",
                "Opening stock 100 units at ₹10, purchases 100 at ₹12, 150 sold. FIFO cost of goods sold is:",
                ["₹1,600", "₹1,650", "₹1,700"],
                0,
                "100×10 + 50×12 = 1,600.",
                "6.b",
            ),
            q(
                "M",
                "With the same data, weighted average COGS is:",
                ["₹1,600", "₹1,650", "₹1,700"],
                1,
                "Average cost 11; 150 × 11 = 1,650.",
                "6.b",
            ),
            q(
                "E",
                "LIFO is permitted under:",
                ["IFRS only", "US GAAP only", "Both IFRS and US GAAP"],
                1,
                "IFRS prohibits LIFO.",
                "6.a",
            ),
            q(
                "M",
                "In a period of rising prices, compared with FIFO, LIFO results in:",
                ["Higher gross profit", "Lower ending inventory and lower taxes", "Higher taxes"],
                1,
                "Recent, higher costs go to COGS.",
                "6.b",
            ),
            q(
                "H",
                "LIFO inventory is ₹400 crore and the LIFO reserve is ₹60 crore. FIFO inventory is:",
                ["₹460 crore", "₹340 crore", "₹400 crore"],
                0,
                "Add the reserve.",
                "6.c",
            ),
            q(
                "M",
                "Under IFRS, a previous inventory write-down:",
                [
                    "Can never be reversed",
                    "Can be reversed up to the original write-down",
                    "Must be reversed each year",
                ],
                1,
                "IFRS allows reversals; US GAAP does not.",
                "6.c",
            ),
            q(
                "H",
                "A LIFO liquidation in a period of rising prices will:",
                ["Lower reported profit", "Temporarily boost gross profit", "Raise COGS"],
                1,
                "Old low-cost layers flow into COGS.",
                "6.c",
            ),
            q(
                "M",
                "COGS ₹730 crore and average inventory ₹73 crore give days of inventory on hand of:",
                ["10 days", "36.5 days", "73 days"],
                1,
                "Turnover 10; 365/10 = 36.5.",
                "6.d",
            ),
            q(
                "E",
                "Inventory under IFRS is measured at the lower of cost and:",
                ["Market value", "Net realisable value", "Replacement cost"],
                1,
                "NRV = selling price − costs to complete and sell.",
                "6.a",
            ),
            q(
                "M",
                "Specific identification is most appropriate for:",
                ["Identical commodity goods", "Unique, high-value items", "Perishable goods only"],
                1,
                "Each item's actual cost is traceable.",
                "6.a",
            ),
        ],
        flashcards=[
            fc("Rising prices: LIFO effects", "Higher COGS, lower profit, lower taxes, lower inventory."),
            fc("LIFO reserve", "FIFO inventory − LIFO inventory."),
            fc("LIFO to FIFO COGS", "LIFO COGS − increase in LIFO reserve."),
            fc("LIFO allowed?", "US GAAP only."),
            fc("Write-down reversals", "IFRS yes; US GAAP no."),
            fc("Days of inventory on hand", "365 ÷ (COGS ÷ average inventory)."),
        ],
    )
)

# ---------------------------------------------------------------- LM7
LMS.append(
    dict(
        lm_no=7,
        title="Analysis of Long-Term Assets",
        summary="Capitalising versus expensing, intangibles, depreciation, impairment, revaluation and derecognition.",
        los=[
            ("7.a", "compare", "Compare the financial reporting of capitalised and expensed costs."),
            ("7.b", "describe", "Describe the accounting for intangible assets, including R&D."),
            ("7.c", "calculate", "Calculate depreciation and amortisation under different methods."),
            ("7.d", "explain", "Explain impairment, the revaluation model and derecognition of long-term assets."),
        ],
        topics=[
            topic(
                "Capitalise or expense?",
                T(
                    ["Effect (in the first year)", "Capitalise", "Expense"],
                    ["Net income", "Higher", "Lower"],
                    ["Total assets and equity", "Higher", "Lower"],
                    ["CFO", "Higher (outflow in CFI)", "Lower"],
                    ["Later years' income", "Lower (depreciation)", "Higher"],
                    ["Income variability", "Smoother", "More volatile"],
                ),
                P("Interest during construction of an asset is **capitalised** into its cost."),
                WO("Capitalising boosts CFO because the cash outflow is classified as investing, not operating."),
            ),
            topic(
                "Intangibles and depreciation",
                L(
                    "Purchased intangibles are capitalised. **IFRS**: research expensed; **development** capitalised "
                    "if feasibility criteria are met. **US GAAP**: R&D generally expensed (software has special "
                    "rules).",
                    "Intangibles with finite lives are amortised; indefinite-life ones (and goodwill) are tested for "
                    "impairment.",
                ),
                FX("Straight-line = (cost − residual) ÷ life · DDB = 2/life × opening book value (stop at residual)"),
                EX(
                    "Machine cost ₹100 lakh, residual ₹10 lakh, life 5 years. Straight-line = **₹18 lakh** a year. DDB "
                    "year 1 "
                    "= 40% × 100 = **₹40 lakh**; year 2 = 40% × 60 = ₹24 lakh. Units-of-production: if it will make "
                    "90,000 "
                    "units and makes 20,000 this year, depreciation = 90 × 20/90 = ₹20 lakh."
                ),
            ),
            topic(
                "Impairment, revaluation and derecognition",
                L(
                    "**IFRS** impairment: carrying amount vs **recoverable amount** = higher of fair value less costs "
                    "to sell and **value in use**. Reversals allowed (except goodwill).",
                    "**US GAAP** (held for use): **recoverability** test using undiscounted cash flows; if it fails, "
                    "write down to fair value. No reversals.",
                    "**Revaluation model** (IFRS only): carry PP&E at fair value; increases go to a revaluation "
                    "surplus "
                    "in OCI unless reversing a past loss.",
                    "On sale, gain or loss = proceeds − carrying amount.",
                ),
                FUN(
                    "Capitalising every cost is like calling your gym membership an 'asset'. Technically it will make "
                    "you stronger; your accountant may disagree."
                ),
            ),
        ],
        revision=sheet(
            "SL = (cost − residual)/life · DDB = 2/life × book value · IFRS recoverable = max(FVLCS, VIU)",
            ("Capitalise", "Higher NI and CFO now, lower later"),
            ("IFRS R&D", "Research expensed, development capitalised if criteria met"),
            ("US GAAP R&D", "Generally expensed"),
            ("IFRS impairment", "Reversals allowed (not goodwill)"),
            ("US GAAP impairment", "Undiscounted recoverability test; no reversals"),
            ("Revaluation model", "IFRS only"),
        ),
        questions=[
            q(
                "M",
                "A company capitalises a cost instead of expensing it. In the current year, net income will be:",
                ["Lower", "Higher", "Unchanged"],
                1,
                "Only depreciation is expensed this year.",
                "7.a",
            ),
            q(
                "M",
                "Capitalising rather than expensing an expenditure makes current-year CFO:",
                ["Higher", "Lower", "Unchanged"],
                0,
                "The outflow is classified in CFI.",
                "7.a",
            ),
            q(
                "E",
                "Under IFRS, research costs are:",
                ["Capitalised", "Expensed", "Recorded as goodwill"],
                1,
                "Development may be capitalised; research is expensed.",
                "7.b",
            ),
            q(
                "M",
                "Cost ₹100 lakh, residual ₹10 lakh, life 5 years. Annual straight-line depreciation is:",
                ["₹20 lakh", "₹18 lakh", "₹40 lakh"],
                1,
                "(100 − 10)/5 = 18.",
                "7.c",
            ),
            q(
                "H",
                "Using the same machine, double-declining-balance depreciation in year 2 is:",
                ["₹24 lakh", "₹40 lakh", "₹18 lakh"],
                0,
                "Year 1: 40; book 60; year 2: 40% × 60 = 24.",
                "7.c",
            ),
            q(
                "M",
                "Under IFRS, an asset's recoverable amount is the:",
                [
                    "Lower of fair value and cost",
                    "Higher of fair value less costs to sell and value in use",
                    "Undiscounted future cash flows",
                ],
                1,
                "Impairment compares carrying amount to recoverable amount.",
                "7.d",
            ),
            q(
                "H",
                "Which statement about impairment reversals is correct?",
                [
                    "US GAAP permits reversals of assets held for use",
                    "IFRS permits reversals except for goodwill",
                    "Neither permits reversals",
                ],
                1,
                "US GAAP prohibits reversals for assets held for use.",
                "7.d",
            ),
            q(
                "E",
                "The revaluation model for PP&E is permitted under:",
                ["US GAAP", "IFRS", "Both"],
                1,
                "US GAAP requires the cost model.",
                "7.d",
            ),
            q(
                "M",
                "An asset with carrying amount ₹30 lakh is sold for ₹35 lakh. The result is:",
                ["A ₹5 lakh gain", "A ₹5 lakh loss", "No gain or loss"],
                0,
                "Proceeds − carrying amount.",
                "7.d",
            ),
            q(
                "M",
                "Interest incurred while constructing an asset for own use is generally:",
                ["Expensed immediately", "Capitalised into the asset's cost", "Recorded in equity"],
                1,
                "Capitalised interest becomes part of the asset.",
                "7.a",
            ),
        ],
        flashcards=[
            fc("Capitalising effects", "Higher NI, assets, CFO now; more depreciation later."),
            fc("IFRS vs US GAAP R&D", "IFRS capitalises development if criteria met; US GAAP expenses."),
            fc("DDB rate", "2 ÷ useful life, applied to opening book value."),
            fc("IFRS recoverable amount", "Higher of FV less costs to sell and value in use."),
            fc("US GAAP impairment test", "Undiscounted cash flows; write down to fair value; no reversal."),
            fc("Revaluation model", "IFRS only; surplus to OCI."),
        ],
    )
)

# ---------------------------------------------------------------- LM8
LMS.append(
    dict(
        lm_no=8,
        title="Topics in Long-Term Liabilities and Equity",
        summary="Bonds at amortised cost, leases, pensions and share-based compensation.",
        los=[
            (
                "8.a",
                "explain",
                "Explain the accounting for bonds issued at par, a premium or a discount, using the "
                "effective interest method.",
            ),
            ("8.b", "explain", "Explain lease accounting from the lessee's perspective."),
            ("8.c", "describe", "Describe defined contribution and defined benefit pension plans and their reporting."),
            ("8.d", "describe", "Describe the reporting of share-based compensation."),
        ],
        topics=[
            topic(
                "Bonds payable",
                P(
                    "A bond is recorded at the cash received (its fair value at issue). Interest expense = **market "
                    "rate "
                    "at issue × opening carrying amount** (effective interest method). The coupon paid is cash."
                ),
                EX(
                    "Sagar Ltd issues 3-year bonds with face ₹1,000 lakh and a 5% coupon when market yields are 6%, "
                    "raising "
                    "₹973.3 lakh (a discount). Year 1 interest expense = 6% × 973.3 = **₹58.4 lakh**; coupon paid = "
                    "50; "
                    "the ₹8.4 lakh difference increases the carrying amount towards face value."
                ),
                WO("Discount bond: interest expense > coupon. Premium bond: interest expense < coupon."),
            ),
            topic(
                "Leases (lessee)",
                L(
                    "At commencement the lessee records a **right-of-use (ROU) asset** and a **lease liability** = PV "
                    "of "
                    "lease payments (short-term and low-value leases can be exempted).",
                    "**IFRS**: single model: depreciation of ROU asset + interest on liability; principal repayment in "
                    "CFF.",
                    "**US GAAP**: **finance lease** (like IFRS) or **operating lease** (single straight-line lease "
                    "expense, all in CFO).",
                ),
                WO("Lease accounting puts the debt on the balance sheet, raising debt-to-equity and assets."),
            ),
            topic(
                "Pensions and share-based pay",
                L(
                    "**Defined contribution**: expense = contribution owed; no further obligation.",
                    "**Defined benefit**: net pension liability (asset) = obligation − plan assets. Service cost and "
                    "net "
                    "interest in P&L (IFRS); **remeasurements** in OCI.",
                    "**Share-based compensation**: fair value at **grant date**, expensed over the **vesting period**.",
                    "Stock options increase equity, not liabilities; cash-settled awards (SARs) are liabilities.",
                ),
                EX(
                    "Options with a grant-date fair value of ₹12 crore vest over three years. Expense = **₹4 crore a "
                    "year**."
                ),
                FUN(
                    "A DB pension is like promising your grandchildren a fixed pocket money for life. Better hope "
                    "your investments grow faster than their appetite."
                ),
            ),
        ],
        revision=sheet(
            "Interest expense = market rate at issue × carrying amount · Lease liability = PV of payments",
            ("Discount bond", "Expense > coupon; carrying amount rises"),
            ("Premium bond", "Expense < coupon; carrying amount falls"),
            ("Lessee", "ROU asset + lease liability"),
            ("US GAAP operating lease", "Straight-line expense, CFO"),
            ("DC plan", "Expense = contribution"),
            ("DB net liability", "Obligation − plan assets"),
            ("Share-based pay", "Grant-date fair value over vesting"),
        ),
        questions=[
            q(
                "M",
                "A bond is issued at a discount. Each period, interest expense under the effective interest method is:",
                ["Less than the coupon paid", "Greater than the coupon paid", "Equal to the coupon paid"],
                1,
                "The market rate exceeds the coupon rate.",
                "8.a",
            ),
            q(
                "H",
                "A bond is issued for ₹973.3 lakh, with a 5% coupon on ₹1,000 lakh face and a 6% market yield. Year 1 "
                "interest expense is closest to:",
                ["₹50.0 lakh", "₹58.4 lakh", "₹60.0 lakh"],
                1,
                "6% × 973.3 = 58.4.",
                "8.a",
            ),
            q(
                "E",
                "When a lessee signs a five-year lease, it typically records:",
                ["Only rent expense", "A right-of-use asset and a lease liability", "Revenue"],
                1,
                "Both IFRS and US GAAP put leases on the balance sheet.",
                "8.b",
            ),
            q(
                "M",
                "Under US GAAP, an operating lease is reported in the income statement as:",
                ["Depreciation plus interest", "A single straight-line lease expense", "Nothing"],
                1,
                "Finance leases show depreciation and interest; operating leases a single cost.",
                "8.b",
            ),
            q(
                "M",
                "Under IFRS, the lessee's repayments of lease principal appear in:",
                ["CFO", "CFI", "CFF"],
                2,
                "Principal is financing; interest follows the company's policy.",
                "8.b",
            ),
            q(
                "E",
                "In a defined contribution plan, the employer's pension expense equals:",
                ["Its required contribution", "The change in plan assets", "Benefits paid"],
                0,
                "There is no further obligation.",
                "8.c",
            ),
            q(
                "M",
                "A defined benefit plan has an obligation of ₹500 crore and plan assets of ₹420 crore. It reports:",
                ["A net pension asset of ₹80 crore", "A net pension liability of ₹80 crore", "No balance"],
                1,
                "Obligation exceeds assets.",
                "8.c",
            ),
            q(
                "M",
                "Options with a grant-date fair value of ₹12 crore vest over three years. Annual compensation expense "
                "is:",
                ["₹12 crore", "₹4 crore", "₹3 crore"],
                1,
                "12 ÷ 3 = 4.",
                "8.d",
            ),
            q(
                "H",
                "Under IFRS, remeasurements of a defined benefit plan (actuarial gains and losses) are reported in:",
                ["Profit or loss", "Other comprehensive income", "Retained earnings directly"],
                1,
                "Remeasurements go to OCI.",
                "8.c",
            ),
            q(
                "E",
                "Share-based compensation is measured at fair value on the:",
                ["Exercise date", "Grant date", "Balance sheet date"],
                1,
                "Grant-date fair value is expensed over vesting.",
                "8.d",
            ),
        ],
        flashcards=[
            fc("Effective interest method", "Expense = market rate at issue × carrying amount."),
            fc("Discount vs premium bond expense", "Above coupon vs below coupon."),
            fc("Lessee accounting", "ROU asset + lease liability = PV of payments."),
            fc("US GAAP operating lease", "Single straight-line expense, all in CFO."),
            fc("DB net pension liability", "Obligation − plan assets."),
            fc("Share-based pay", "Grant-date fair value spread over vesting."),
        ],
    )
)

# ---------------------------------------------------------------- LM9
LMS.append(
    dict(
        lm_no=9,
        title="Analysis of Income Taxes",
        summary="Accounting profit versus taxable income, deferred tax assets and liabilities, and effective tax "
                "rates.",
        los=[
            ("9.a", "describe", "Describe the differences between accounting profit and taxable income."),
            ("9.b", "explain", "Explain how deferred tax liabilities and assets are created."),
            ("9.c", "calculate", "Calculate the tax base of assets and liabilities and deferred tax amounts."),
            ("9.d", "explain", "Explain permanent differences, valuation allowances and the effective tax rate."),
        ],
        topics=[
            topic(
                "Two sets of books",
                L(
                    "**Accounting profit** (pre-tax income) follows accounting standards; **taxable income** follows "
                    "tax law.",
                    "**Income tax expense** = taxes payable + change in deferred tax liability − change in deferred "
                    "tax "
                    "asset.",
                    "**Temporary differences** reverse over time and create deferred taxes; **permanent differences** "
                    "never reverse.",
                ),
                FX("Income tax expense = taxes payable + ΔDTL − ΔDTA"),
            ),
            topic(
                "Deferred tax liabilities and assets",
                L(
                    "**DTL**: taxes deferred to the future. Usually because **tax depreciation is faster** than book "
                    "depreciation, so the asset's carrying amount > its tax base.",
                    "**DTA**: taxes paid early. E.g. warranty expense recognised in the books before it is "
                    "tax-deductible, "
                    "or tax losses carried forward.",
                    "Asset: carrying amount > tax base → DTL. Liability: carrying amount > tax base → DTA.",
                ),
                EX(
                    "An asset cost ₹300 lakh. After year 1 the book carrying amount is ₹200 lakh, but the tax base is "
                    "₹150 lakh "
                    "(faster tax depreciation). Temporary difference = 50; at 25% tax, **DTL = ₹12.5 lakh**."
                ),
                WO(
                    "Under US GAAP, a **valuation allowance** reduces a DTA if it is more likely than not that it will "
                    "not "
                    "be realised. Watch for companies releasing allowances to boost profit."
                ),
            ),
            topic(
                "Effective tax rate",
                P(
                    "Effective tax rate = income tax expense ÷ pre-tax income. It differs from the statutory rate "
                    "because of permanent differences (tax-free income, non-deductible fines), tax credits, and "
                    "foreign "
                    "rates."
                ),
                FUN(
                    "A DTL is the government letting you pay later because you bought a shiny new machine. The "
                    "bill still comes; it just waits politely."
                ),
            ),
        ],
        revision=sheet(
            "Tax expense = taxes payable + ΔDTL − ΔDTA · DTL = (carrying amount − tax base) × t for assets",
            ("Temporary difference", "Reverses; creates deferred tax"),
            ("Permanent difference", "Never reverses; changes effective rate"),
            ("DTL source", "Accelerated tax depreciation"),
            ("DTA source", "Warranty provisions, tax-loss carryforwards"),
            ("Valuation allowance", "US GAAP reduction of DTA"),
            ("Effective rate", "Tax expense ÷ pre-tax income"),
        ),
        questions=[
            q(
                "E",
                "A deferred tax liability most commonly arises when:",
                [
                    "Tax depreciation is faster than book depreciation",
                    "Warranty costs are accrued",
                    "A company has tax losses",
                ],
                0,
                "Lower taxable income now means higher taxes later.",
                "9.b",
            ),
            q(
                "M",
                "An asset's carrying amount is ₹200 lakh and its tax base is ₹150 lakh. At a 25% tax rate the deferred "
                "tax "
                "position is:",
                ["DTA of ₹12.5 lakh", "DTL of ₹12.5 lakh", "DTL of ₹50 lakh"],
                1,
                "(200 − 150) × 25% = 12.5 DTL.",
                "9.c",
            ),
            q(
                "M",
                "Income tax expense equals:",
                ["Taxes payable + ΔDTL − ΔDTA", "Taxes payable − ΔDTL", "Pre-tax income × statutory rate"],
                0,
                "Expense includes the change in deferred taxes.",
                "9.b",
            ),
            q(
                "M",
                "Warranty expense recognised in the books before it is deductible for tax creates:",
                ["A deferred tax liability", "A deferred tax asset", "A permanent difference"],
                1,
                "Taxes are paid earlier than the book expense suggests.",
                "9.b",
            ),
            q(
                "H",
                "Under US GAAP, a valuation allowance is established when:",
                [
                    "DTLs are large",
                    "It is more likely than not that some of a DTA will not be realised",
                    "Tax rates rise",
                ],
                1,
                "It reduces the DTA's carrying amount.",
                "9.d",
            ),
            q(
                "E",
                "A difference between book and taxable income that will never reverse is a:",
                ["Temporary difference", "Permanent difference", "Valuation allowance"],
                1,
                "E.g. tax-exempt income.",
                "9.d",
            ),
            q(
                "M",
                "Tax-exempt interest income will cause the effective tax rate to be:",
                ["Higher than the statutory rate", "Lower than the statutory rate", "Equal to the statutory rate"],
                1,
                "Income in the denominator is not taxed.",
                "9.d",
            ),
            q(
                "H",
                "Taxes payable are ₹40 crore, the DTL rises by ₹5 crore and the DTA rises by ₹2 crore. Income tax "
                "expense is:",
                ["₹43 crore", "₹47 crore", "₹37 crore"],
                0,
                "40 + 5 − 2 = 43.",
                "9.b",
            ),
            q(
                "M",
                "Taxable income is calculated under:",
                ["Accounting standards", "Tax law", "Auditor guidance"],
                1,
                "Tax authorities set the rules.",
                "9.a",
            ),
            q(
                "E",
                "Tax losses carried forward to offset future taxable profit create:",
                ["A deferred tax asset", "A deferred tax liability", "No deferred tax"],
                0,
                "They reduce future taxes.",
                "9.b",
            ),
        ],
        flashcards=[
            fc("Income tax expense", "Taxes payable + ΔDTL − ΔDTA."),
            fc("DTL arises when", "Asset carrying amount > tax base (e.g. accelerated tax depreciation)."),
            fc("DTA arises when", "Expenses booked before deductible, or tax losses carried forward."),
            fc("Temporary vs permanent difference", "Reverses vs never reverses."),
            fc("Valuation allowance", "US GAAP reduction of DTA unlikely to be realised."),
            fc("Effective tax rate", "Tax expense ÷ pre-tax income."),
        ],
    )
)

# ---------------------------------------------------------------- LM10
LMS.append(
    dict(
        lm_no=10,
        title="Financial Reporting Quality",
        summary="The quality spectrum, why managers distort reports, and the warning signs to look for.",
        los=[
            ("10.a", "compare", "Compare financial reporting quality with the quality of reported results."),
            ("10.b", "describe", "Describe a spectrum for assessing financial reporting quality."),
            (
                "10.c",
                "explain",
                "Explain conditions conducive to low-quality reporting, and the role of regulators and auditors.",
            ),
            ("10.d", "describe", "Describe accounting warning signs and methods for detecting manipulation."),
        ],
        topics=[
            topic(
                "Two kinds of quality",
                P(
                    "**Reporting quality**: are the statements decision-useful and faithful? **Earnings (results) "
                    "quality**: are the earnings sustainable and adequate? A company can report its poor results "
                    "honestly (high reporting quality, low earnings quality)."
                ),
                OL(
                    "GAAP, decision-useful, sustainable and adequate returns (best).",
                    "GAAP, decision-useful, but sustainable earnings are not adequate.",
                    "GAAP-compliant but biased choices (aggressive or conservative).",
                    "Within GAAP but 'managed' earnings.",
                    "Departures from GAAP.",
                    "Fictitious transactions (fraud).",
                ),
            ),
            topic(
                "Why it happens",
                L(
                    "**Motivation**: hit analyst targets, bonuses, debt covenants, raise capital.",
                    "**Opportunity**: weak controls, weak board, complex rules with lots of judgement.",
                    "**Rationalisation**: 'everyone does it', 'it's only temporary'.",
                    "Defences: regulators (registration, disclosure, enforcement), auditors, audit committees, and "
                    "private contracts (lenders' covenants).",
                ),
                WO(
                    "**Conservative** is not automatically good: big write-offs today ('cookie jar' reserves) can be "
                    "released later to inflate profit."
                ),
            ),
            topic(
                "Warning signs",
                L(
                    "Revenue: changes in recognition policy, bill-and-hold, **receivables growing faster than sales**, "
                    "channel stuffing.",
                    "**Inventory growing faster than sales**; falling inventory turnover.",
                    "**CFO persistently below net income**.",
                    "Capitalising costs that peers expense; lengthening depreciation lives.",
                    "Frequent 'one-off' charges; heavy reliance on **non-GAAP** measures.",
                    "Related-party deals; auditor changes; late filings.",
                ),
                EX(
                    "Kamal Electronics grows sales 10% but receivables 45% and inventory 30%. CFO falls while net "
                    "income "
                    "rises. Likely: pushing goods onto dealers at year-end with easy credit terms."
                ),
                FUN("When a company's 'one-time' charge appears every year, it isn't one-time. It is a subscription."),
            ),
        ],
        revision=sheet(
            "Fraud triangle: motivation · opportunity · rationalisation",
            ("Reporting quality", "Faithful, decision-useful reports"),
            ("Earnings quality", "Sustainable, adequate results"),
            ("Spectrum top", "GAAP + sustainable, adequate returns"),
            ("Spectrum bottom", "Fictitious transactions"),
            ("Red flags", "AR or inventory > sales growth; CFO < NI; recurring 'one-offs'"),
            ("Cookie jar", "Over-conservative reserves released later"),
        ),
        questions=[
            q(
                "E",
                "The lowest point on the financial reporting quality spectrum is:",
                ["Biased accounting choices", "Fictitious transactions", "Earnings management within GAAP"],
                1,
                "Fraudulent reporting is the worst case.",
                "10.b",
            ),
            q(
                "M",
                "A company honestly reports a large, sustainable decline in profit. It has:",
                [
                    "Low reporting quality and high earnings quality",
                    "High reporting quality and low earnings quality",
                    "Low reporting and earnings quality",
                ],
                1,
                "The report is faithful; the results are poor.",
                "10.a",
            ),
            q(
                "M",
                "The three conditions that make low-quality reporting more likely are:",
                [
                    "Motivation, opportunity and rationalisation",
                    "Revenue, expenses and assets",
                    "Audit, review and filing",
                ],
                0,
                "These form the fraud triangle.",
                "10.c",
            ),
            q(
                "M",
                "Receivables growing much faster than sales is a warning sign of:",
                ["Conservative accounting", "Aggressive revenue recognition", "Strong cash collection"],
                1,
                "Sales may be booked before they are really earned or collectable.",
                "10.d",
            ),
            q(
                "H",
                "Why might very conservative accounting also be a concern?",
                [
                    "It always overstates profit",
                    "Excess reserves can be released later to boost earnings",
                    "It is never allowed",
                ],
                1,
                "Cookie-jar reserves smooth or inflate later earnings.",
                "10.c",
            ),
            q(
                "E",
                "Which is a warning sign of low earnings quality?",
                ["CFO consistently above net income", "CFO persistently below net income", "Stable margins"],
                1,
                "Profits not turning into cash.",
                "10.d",
            ),
            q(
                "M",
                "Lengthening the estimated useful lives of assets will:",
                ["Raise depreciation", "Lower depreciation and raise reported profit", "Not affect profit"],
                1,
                "A common way to flatter earnings.",
                "10.d",
            ),
            q(
                "M",
                "Debt covenants and bonus plans tied to profit targets mainly create:",
                ["Opportunity", "Motivation", "Rationalisation"],
                1,
                "They give managers reasons to manipulate.",
                "10.c",
            ),
            q(
                "H",
                "A company reports large 'non-recurring' restructuring charges in four of the last five years. An "
                "analyst should:",
                ["Exclude them as truly one-off", "Treat them as recurring costs of the business", "Ignore them"],
                1,
                "Frequent charges are effectively ongoing.",
                "10.d",
            ),
            q(
                "E",
                "Which body enforces financial reporting requirements for listed companies?",
                ["Securities regulator", "Credit rating agency", "Stock exchange member"],
                0,
                "Regulators like SEBI or the SEC enforce disclosure.",
                "10.c",
            ),
        ],
        flashcards=[
            fc("Reporting vs earnings quality", "Faithful reports vs sustainable, adequate results."),
            fc("Quality spectrum ends", "Top: GAAP + sustainable returns. Bottom: fictitious transactions."),
            fc("Fraud triangle", "Motivation, opportunity, rationalisation."),
            fc("Revenue red flag", "Receivables growing faster than sales."),
            fc("Cash red flag", "CFO persistently below net income."),
            fc("Recurring one-offs", "Treat as ongoing costs."),
        ],
    )
)

# ---------------------------------------------------------------- LM11
LMS.append(
    dict(
        lm_no=11,
        title="Financial Analysis Techniques",
        summary="Ratio categories, DuPont analysis, and limits of ratio analysis.",
        los=[
            ("11.a", "describe", "Describe tools and techniques used in financial analysis."),
            (
                "11.b",
                "calculate",
                "Calculate and interpret activity, liquidity, solvency, profitability and valuation ratios.",
            ),
            ("11.c", "demonstrate", "Demonstrate the application of DuPont analysis of return on equity."),
            ("11.d", "describe", "Describe the limitations of ratio analysis."),
        ],
        topics=[
            topic(
                "Ratio families",
                T(
                    ["Category", "Examples"],
                    [
                        "Activity",
                        "Receivables turnover, DSO, inventory turnover, DOH, payables turnover, total asset turnover",
                    ],
                    ["Liquidity", "Current, quick, cash ratios; cash conversion cycle = DSO + DOH − DPO"],
                    ["Solvency", "Debt-to-equity, debt-to-assets, financial leverage, interest coverage"],
                    ["Profitability", "Gross, operating, net margins; ROA, ROE"],
                    ["Valuation", "P/E, P/B, P/S, dividend yield"],
                ),
                EX("DSO 45 days, DOH 60 days, DPO 35 days. Cash conversion cycle = 45 + 60 − 35 = **70 days**."),
            ),
            topic(
                "DuPont analysis",
                FX(
                    "ROE = Net margin × Asset turnover × Financial leverage = (NI/Sales) × (Sales/Assets) × "
                    "(Assets/Equity)"
                ),
                EX("Net margin 5%, asset turnover 1.2, leverage 2.5: ROE = 0.05 × 1.2 × 2.5 = **15%**."),
                FX(
                    "Five-way: ROE = (NI/EBT) × (EBT/EBIT) × (EBIT/Sales) × (Sales/Assets) × (Assets/Equity)",
                    "Extended DuPont",
                ),
                P(
                    "Tax burden × interest burden × EBIT margin × asset turnover × leverage. It shows whether ROE "
                    "comes "
                    "from operations or from borrowing."
                ),
                WO(
                    "An ROE rise driven only by more leverage is lower quality than one from better margins or "
                    "turnover."
                ),
            ),
            topic(
                "Limits of ratios",
                L(
                    "Different accounting choices (FIFO vs LIFO, IFRS vs US GAAP) distort comparisons.",
                    "Diversified companies are hard to compare with single-industry peers.",
                    "Ratios need context: trends, peers, industry norms and the business model.",
                    "Window dressing at year end can flatter balance sheet ratios.",
                ),
                FUN(
                    "A ratio alone is like knowing a batter's average without knowing the format. 45 in Tests is "
                    "great; 45 strike rate in T20 is a disaster."
                ),
            ),
        ],
        revision=sheet(
            "ROE = margin × turnover × leverage · CCC = DSO + DOH − DPO",
            ("Activity", "How efficiently assets are used"),
            ("Liquidity", "Short-term obligations"),
            ("Solvency", "Long-term obligations"),
            ("Tax burden", "NI ÷ EBT"),
            ("Interest burden", "EBT ÷ EBIT"),
            ("Leverage-driven ROE", "Lower quality"),
        ),
        questions=[
            q(
                "M",
                "Net margin 5%, asset turnover 1.2 and financial leverage 2.5 give an ROE of:",
                ["15%", "8.7%", "6%"],
                0,
                "0.05 × 1.2 × 2.5 = 15%.",
                "11.c",
            ),
            q(
                "M",
                "DSO 45 days, DOH 60 days and DPO 35 days give a cash conversion cycle of:",
                ["140 days", "70 days", "50 days"],
                1,
                "45 + 60 − 35 = 70.",
                "11.b",
            ),
            q(
                "E",
                "Interest coverage is a measure of:",
                ["Liquidity", "Solvency", "Activity"],
                1,
                "It shows ability to service debt.",
                "11.b",
            ),
            q(
                "M",
                "In the five-way DuPont, EBT ÷ EBIT is the:",
                ["Tax burden", "Interest burden", "EBIT margin"],
                1,
                "It shows how much of EBIT survives interest.",
                "11.c",
            ),
            q(
                "H",
                "ROE rose from 12% to 15% while margins and asset turnover were unchanged. The increase came from:",
                ["Better operations", "Higher financial leverage", "Lower taxes only"],
                1,
                "Only the leverage term moved.",
                "11.c",
            ),
            q(
                "E",
                "Receivables turnover is an example of a(n):",
                ["Activity ratio", "Valuation ratio", "Solvency ratio"],
                0,
                "It measures collection efficiency.",
                "11.b",
            ),
            q(
                "M",
                "Which is a limitation of ratio analysis?",
                [
                    "Ratios are always comparable across companies",
                    "Different accounting methods can distort comparisons",
                    "Ratios need no context",
                ],
                1,
                "Accounting choices affect ratios.",
                "11.d",
            ),
            q(
                "M",
                "A tax burden of 0.75 means:",
                ["75% of pre-tax income is kept after tax", "75% is paid in tax", "Interest is 75% of EBIT"],
                0,
                "NI ÷ EBT = 0.75.",
                "11.c",
            ),
            q(
                "E",
                "Price-to-earnings is a:",
                ["Profitability ratio", "Valuation ratio", "Liquidity ratio"],
                1,
                "It relates market price to earnings.",
                "11.b",
            ),
            q(
                "H",
                "Total asset turnover falls while net margin is stable. Other things equal, ROE will:",
                ["Rise", "Fall", "Stay the same"],
                1,
                "Lower turnover reduces ROE in DuPont.",
                "11.c",
            ),
        ],
        flashcards=[
            fc("Three-way DuPont", "Net margin × asset turnover × financial leverage."),
            fc("Five-way DuPont", "Tax burden × interest burden × EBIT margin × turnover × leverage."),
            fc("Cash conversion cycle", "DSO + DOH − DPO."),
            fc("Solvency ratios", "D/E, debt-to-assets, leverage, interest coverage."),
            fc("Leverage-driven ROE", "Riskier, lower-quality ROE."),
            fc("Ratio limitation", "Accounting differences and lack of context."),
        ],
    )
)

# ---------------------------------------------------------------- LM12
LMS.append(
    dict(
        lm_no=12,
        title="Introduction to Financial Statement Modeling",
        summary="Building a forecast model, the effect of competition, inflation and technology, and biases in "
        "forecasting.",
        los=[
            ("12.a", "demonstrate", "Demonstrate the development of a sales-based pro forma company model."),
            ("12.b", "explain", "Explain how behavioural factors affect analyst forecasts."),
            (
                "12.c",
                "explain",
                "Explain how competitive factors, inflation and technological developments affect forecasts.",
            ),
            ("12.d", "explain", "Explain considerations in choosing an explicit forecast horizon."),
        ],
        topics=[
            topic(
                "Building a model",
                OL(
                    "Forecast **revenue** from its drivers.",
                    "Forecast **COGS** as a % of revenue (gross margin) and **SG&A** (often partly fixed).",
                    "Forecast **depreciation** and **capex**, interest and taxes.",
                    "Forecast **working capital** using days or turnover.",
                    "Build the balance sheet and cash flow; check they balance.",
                ),
                EX(
                    "Revenue ₹1,000 crore grows 10%. COGS 60% of sales; SG&A ₹150 crore rising 5%; depreciation ₹40 "
                    "crore; "
                    "tax 25%; no debt. Next year: revenue 1,100; gross profit 440; SG&A 157.5; EBIT 242.5; net income "
                    "**₹181.9 crore**."
                ),
            ),
            topic(
                "What moves the forecast",
                L(
                    "**Competition** (five forces) limits how long high margins last.",
                    "**Inflation**: firms with pricing power pass on costs; others see margins squeezed. Input costs "
                    "and selling prices may not move together.",
                    "**Technology**: can create new demand or destroy old products (substitution); a key source of "
                    "uncertainty in long forecasts.",
                ),
                H("Behavioural biases in forecasting"),
                L(
                    "**Overconfidence**: forecast ranges too narrow.",
                    "**Illusion of control**: too much detail in models.",
                    "**Conservatism**: slow to update after new information.",
                    "**Representativeness**: assuming recent trends continue.",
                    "**Confirmation**: seeking support for the existing view.",
                ),
                WO(
                    "A more detailed model is not necessarily a more accurate one. Focus on the few drivers that "
                    "matter."
                ),
            ),
            topic(
                "Choosing the forecast horizon",
                L(
                    "Match the investor's horizon and the strategy (short-term trading vs long-term holding).",
                    "Cover the full business cycle for cyclical firms.",
                    "Extend through any major change (acquisition, restructuring) until results normalise.",
                    "After the explicit period, use a terminal value assuming steady-state growth.",
                ),
                FUN(
                    "A 40-tab spreadsheet model with a typo in cell B7 is still a horoscope, just a very "
                    "well-formatted "
                    "one."
                ),
            ),
        ],
        revision=sheet(
            "Sales-based model: revenue → COGS → SG&A → EBIT → tax → NI → balance sheet → cash flow",
            ("Gross margin", "Often stable unless prices or input costs shift"),
            ("Inflation", "Hurts firms without pricing power"),
            ("Technology", "Substitution risk"),
            ("Overconfidence", "Ranges too narrow"),
            ("Illusion of control", "Excessive model detail"),
            ("Horizon", "Full cycle, through major changes, then terminal value"),
        ),
        questions=[
            q(
                "M",
                "Revenue ₹1,000 crore grows 10%; COGS is 60% of sales; SG&A ₹150 crore rises 5%; depreciation ₹40 "
                "crore. "
                "Next year's EBIT is closest to:",
                ["₹242.5 crore", "₹250.0 crore", "₹282.5 crore"],
                0,
                "1,100 − 660 − 157.5 − 40 = 242.5.",
                "12.a",
            ),
            q(
                "E",
                "A sales-based pro forma model starts by forecasting:",
                ["Revenue", "Dividends", "Share price"],
                0,
                "Most items are linked to revenue.",
                "12.a",
            ),
            q(
                "M",
                "An analyst whose forecast ranges are far too narrow most likely shows:",
                ["Overconfidence", "Conservatism", "Mental accounting"],
                0,
                "Overconfidence understates uncertainty.",
                "12.b",
            ),
            q(
                "M",
                "Building an extremely detailed model in the belief it will be more accurate is:",
                ["Illusion of control", "Anchoring", "Availability"],
                0,
                "Detail does not equal accuracy.",
                "12.b",
            ),
            q(
                "H",
                "During high input-cost inflation, which company is most likely to protect its margins?",
                [
                    "One with strong pricing power",
                    "One in a commodity market with many rivals",
                    "One with fixed-price long-term sales contracts",
                ],
                0,
                "Pricing power lets it pass costs on.",
                "12.c",
            ),
            q(
                "M",
                "For a cyclical company, the explicit forecast horizon should ideally:",
                ["Cover a full business cycle", "Be one quarter", "End at the peak"],
                0,
                "Normalised earnings need a full cycle.",
                "12.d",
            ),
            q(
                "E",
                "An analyst slow to revise forecasts after a surprise announcement shows:",
                ["Conservatism bias", "Overconfidence", "Framing"],
                0,
                "Conservatism is slow updating.",
                "12.b",
            ),
            q(
                "M",
                "A new technology that replaces a company's main product mainly affects forecasts through:",
                ["Substitution and lower future demand", "Lower tax rates", "Higher inventory turnover"],
                0,
                "Disruption can shrink the market.",
                "12.c",
            ),
            q(
                "H",
                "After an acquisition, the forecast horizon should extend:",
                [
                    "Only one year",
                    "Until the combined business's results have normalised",
                    "Indefinitely without a terminal value",
                ],
                1,
                "Integration effects need to work through first.",
                "12.d",
            ),
            q(
                "M",
                "Assuming last year's 30% growth will continue for ten years is an example of:",
                ["Representativeness", "Loss aversion", "Endowment bias"],
                0,
                "Extrapolating recent patterns.",
                "12.b",
            ),
        ],
        flashcards=[
            fc("Sales-based model steps", "Revenue → costs → EBIT → NI → BS → CF."),
            fc("Inflation and margins", "Pricing power protects; commodity sellers squeezed."),
            fc("Overconfidence in forecasts", "Ranges too narrow."),
            fc("Illusion of control", "Too much model detail."),
            fc("Conservatism bias", "Slow to update after news."),
            fc("Forecast horizon", "Full cycle; through major changes; then terminal value."),
        ],
    )
)


if __name__ == "__main__":
    # Prototype questions: accrual revenue and gross margin are income statement (LM2); capitalising is LM7.
    write_pack("fsa", "Financial Statement Analysis", LMS, {"46": 2, "47": 7, "48": 2}, balance_keys=True)
