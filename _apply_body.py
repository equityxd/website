p = "gen_cv_typ.py"
s = open(p, encoding="utf-8").read()


def rep(old, new, label):
    global s
    c = s.count(old)
    if c != 1:
        print(f"[FAIL] {label}: expected 1, found {c}")
        raise SystemExit(1)
    s = s.replace(old, new, 1)
    print(f"[ok] {label}")


# --- GRID: MS PowerPoint after Workshops ---
rep(
    "            - Cross-functional workshops\\n",
    "            - Cross-functional workshops\\n            - MS PowerPoint (workshop presentations)\\n",
    "rec4: MS PowerPoint in workshops grid")

# --- GRID: Qlik Sense after MS Power BI (BI column) ---
rep(
    "            - QlikSense\\n",
    "            - Qlik Sense\\n",
    "rec9-grid: Qlik Sense spelling fix in BI column")

# --- Engie SEM bullet: GL close (rec1) ---
rep(
    '    - Led finance-accounting (GL) as core Business Analyst on the SAP S/4HANA ERP migration pilot "\n        "across French subsidiaries, bridging IT architecture and business stakeholders.\\n',
    '    - Led month-end/year-end GL close for up to 6 BE/FR/NL entities (ERP replacing legacy AS/400), strengthening financial-close control across the multi-entity group.\\n',
    "rec1: Engie GL close quantified")

# --- Engie SEM bullet: training / UAT (rec5) ---
rep(
    '    - Reconciled middle-office (IVDB) to SAP S/4HANA and streamlined WTS project coding to "\n        "improve portfolio monitoring.\\n',
    '    - Trained end-users on Infor M3 and validated UAT for finance sub-processes before go-live, documenting steering-committee sign-off.\\n',
    "rec5: Engie training + UAT sign-off")

# --- Engie SEM bullet: workshops stakeholder sign-off ---
rep(
    '    - Drove AS-IS to TO-BE process design for finance sub-processes and coordinated cross-functional "\n        "workshops.\\n',
    '    - Drove AS-IS to TO-BE process design for finance sub-processes, coordinating cross-functional workshops and stakeholder sign-off.\\n',
    "Engie workshops sign-off")

# --- Engie SEM bullet: keep PowerQuery ETL ---
rep(
    '    - Automated the financial close with PowerQuery ETL, ingesting 1,500+ bookings per close "\n        "with zero manual intervention.\\n',
    '    - Automated the financial close with PowerQuery ETL, ingesting 1,500+ bookings per close with zero manual intervention.\\n',
    "Engie PowerQuery ETL (unchanged)")

# --- Holcim: Qlik Sense dashboards (rec9) ---
rep(
    "    - Rolled out Qliksense finance reporting, converting raw data into executive decision-support.\\n",
    "    - Rolled out Qlik Sense finance reporting, building 8 executive dashboards that shortened reporting cycles by 50% and enabled faster, evidence-based managerial decisions.\\n",
    "rec9-body: Holcim Qlik Sense dashboards")

# --- Holcim: rebate quantification (rec3) ---
rep(
    "    - Built rebate models (matrix & automated SAP) aligned to commercial strategy.\\n",
    "    - Built rebate models (matrix & automated SAP) aligned to commercial strategy, driving \u20ac150M annual rebate volume with 99.8% accuracy and resolving commercial disputes ~30% faster.\\n",
    "rec3: Holcim rebate \u20ac150M")

# --- Holcim: keep reliability bullet (unchanged) ---
rep(
    "    - Guaranteed data reliability and partnered with auditors on rebate matters.\\n",
    "    - Guaranteed data reliability and partnered with auditors on rebate matters.\\n",
    "Holcim reliability (unchanged)")

# --- Rexel: auto-sector prominence (rec2a) ---
rep(
    "    - Managed consolidated GL reporting across multi-country subsidiaries under IFRS / BE-GAAP.\\n",
    "    - Operated within automobile-parts distribution (\u20ac500M turnover, 12 entities / 3 countries), overseeing GL consolidated reporting and aligning AP/AR flows for strong financial-close control.\\n",
    "rec2a: Rexel auto-sector prominence")

# --- Rexel: keep SAP BPC / Cognos (unchanged) ---
rep(
    "    - Integrated SAP BPC and Cognos reporting, strengthening GL/AP consolidated reporting.\\n",
    "    - Integrated SAP BPC and Cognos reporting, strengthening GL/AP consolidated reporting.\\n",
    "Rexel SAP BPC/Cognos (unchanged)")

# --- Rexel: keep budgeting (unchanged) ---
rep(
    "    - Ran annual budgeting and monthly forecasting (actual vs. budget).\\n",
    "    - Ran annual budgeting and monthly forecasting (actual vs. budget).\\n",
    "Rexel budgeting (unchanged)")

# --- Engie Tractebel: filler purged / dashboards (rec10) ---
rep(
    "    - Built finance data models from SAP (HANA) and delivered Power BI executive reporting.\\n",
    "    - Engineered finance data models from SAP HANA, delivering 8 Power BI executive dashboards that turned raw transactions into decision-ready insights for finance leadership.\\n",
    "rec10: Engie Tractebel filler purged / dashboards")

open(p, "w", encoding="utf-8").write(s)
print("Wrote", p)
