# Streamlit Interactive Case — Fever & Sore Throat → Travel → TB (Steps 1–8)
# ======================================================================================
# Additions in this version:
# • Step 7: Lost to follow-up from ART → disseminated TB presentation (SOB, LAD, headache)
# • Preloaded images via ./assets (Pillow)
# • use_container_width=True everywhere for images
# • Reset button retained
# • Dynamic background color per step

try:
    import streamlit as st
except ModuleNotFoundError:
    import sys
    sys.stderr.write(
        "\nERROR: The 'streamlit' package is not installed.\n"
        "Install with: pip install streamlit\n"
        "Run with: streamlit run app.py\n\n"
    )
    sys.exit(1)

from datetime import datetime
from PIL import Image
from pathlib import Path

# ==========================
# Page config
# ==========================
st.set_page_config(page_title="Interactive Micro Case: Fever & Sore Throat", page_icon="🦠")

# ==========================
# Preloaded image support
# ==========================
ASSETS_DIR = Path("assets")  # folder containing vignette.jpg, rash.jpg, etc.


def load_img(filename: str):
    if not filename:
        return None
    p = ASSETS_DIR / filename
    try:
        return Image.open(p)
    except Exception:
        return None


# ==========================
# Case data
# ==========================
CASE = {
    "images": {
        "vignette": "vignette.png",
        "rash": "rash.png",
        "ct": "ct_head.png",
        "csf": "lp_csf.jpg",
        "blood_smear": "blood_smear.png",
        "culture": "culture.png",
        "vignette_ams": "vignette_ams.png",
        "acute_hiv": "acute_hiv.png",
        "travel": "travel.png",
        "tb_cxr": "tb_cxr.png",
        "tb_ct_head": "ct_head_aids.png",
        "tb_vignette": "tb_vignette.png",
        # New (optional) TB images
        "cxr": "cxr_miliary.jpg",
        "ct_chest": "ct_chest_tb.jpg",
        "ln_fna": "lymph_node_fna.jpg",
        "urine_lam": "urine_lam.jpg",
    },

    # Core case (Steps 1–3)
    "title": "Fever & Sore Throat in a 46-year-old",
    "vignette": (
        "You are now a 4th year medical student working on your emergency department rotation.\n"
        "Your preceptor asks you to see the patient in Room B3 in the SHC ED.\n\n"
        "A 46-year-old man presents to the Emergency Department with a one-week history of fevers and sore throat.\n"
        "He also reports noticing some 'lumps' in his neck, a significant decrease in appetite, and extreme fatigue."
    ),
    "vitals": {
        "Temperature": "38.6°C",
        "Heart rate": "96/min",
        "Blood pressure": "122/74 mmHg",
        "Respiratory rate": "16/min",
        "SpO₂ (room air)": "99%",
    },
    "history": {
        "Where were you born?": "“I was born in San Francisco, CA and have lived in California my whole life, but I'm an avid traveler and I have been to all continents.”",
        "What do you do for work?": "“I work as a goat yoga teacher in Half Moon Bay.”",
        "Who do you live with and do you have any pets?": "“I live alone and I am a single dad to two kittens.”",
        "Are you currently sexually active?": "“Yes, I am currently sexually active with men and women with only occasional condom use.”",
        "Other relevant details": "No known sick contacts; no recent travel; no medications; No known allergies.",
    },
    "exam": [
        "**HEENT:** Posterior oropharyngeal and tonsillar erythema, no exudates. Enlarged anterior cervical lymph nodes, mobile, mildly tender to palpation.",
        "**Cardiovascular:** Tachycardic, normal S1, S2, no murmurs.",
        "**Lungs:** Clear to auscultation bilaterally.",
        "**Abdomen:** Soft, non-tender, non-distended.",
        "**Genitourinary:** No genital ulcers are noted, no urethral discharge.",
        "**Skin:** Diffuse, light pink maculopapular rash present over the trunk.",
    ],
    "labs": {
        "EBV antibody panel": "Negative",
        "CMV IgM and IgG": "Negative",
        "HIV antigen/antibody test": "Negative",
        "HIV RNA viral load": "Positive",
        "Syphilis screen": "Negative",
        "Blood cultures": "No growth",
        "Gonorrhea/Chlamydia NAAT": "Negative",
        "Toxoplasma IgM/IgG": "Negative",
        "GAS rapid antigen": "Negative",
    },

    # Step 4 follow-up episode (3 months later)
    "followup": {
        "vignette": (
            "Three months later, he is brought to the Emergency Department by a family member with fever, headache, and confusion.\n"
            "He is unable to provide a more detailed history. Since he appears unwell and needs more work-up, he is admitted to the hospital.\n"
            "You are doing an IM Sub-I, and help admit the patient.\n"
        ),
        "vitals": {
            "Temperature (°F)": "101.5",
            "Heart rate": "111 bpm",
            "Blood pressure": "135/85 mmHg",
        },
        "exam": {
            "General": "Unwell appearing, confused",
            "Neuro": "Alert and oriented to self only, no nuchal rigidity",
            "Skin": "No rashes or lesions",
            "Other": "Remainder of exam normal",
        },
        "recent_labs": {
            "CD4+ (cells/µL)": "650",
            "HIV viral load": "Undetectable",
        },
        # Gradual reveal objects
        "ct_head_result": "No mass lesion or contraindication to LP.",
        "lp_results": {
            "Opening pressure (cm H₂O)": "20",
            "WBC (cells/µL)": "100 (88% lymphocytes)",
            "Protein (mg/dL)": "42",
            "Glucose (mg/dL)": "50",
            "CSF Gram stain": "No organisms on gram stain, moderate mononuclear cells",
            "CSF culture": "Pending"
        },
    },

    # Step 6 travel episode data
    "travel": {
        "summary": (
            "After recovery from HSV encephalitis, he feels well and decides to take a **4-week trip to "
            "Southeast Asia and Oceania**, including time in **Thailand, Vietnam, Indonesia, and Papua New Guinea**.\n\n"
            "He goes **scuba diving** on coral reefs, **trekking** in humid jungle terrain, visits **rural villages**, "
            "**hikes volcanic landscapes**, swims in freshwater lagoons, and eats a wide variety of **local street food** "
            "and **undercooked meats and seafood** from night markets.\n\n"
            "On his way back to San Francisco, an intense **atmospheric river** closes Bay Area airports, and his flight "
            "is **diverted through Arizona**. During a long layover there, he eats a **half-cooked hamburger** at an airport diner."
        ),
        "diarrhea": {
            "vignette": (
                "Two days after returning to California, he presents to the **Emergency Department** where you are rotating "
                "with a complaint of **bloody diarrhea**. The illness began with **watery stools**, abdominal cramping, and "
                "low-grade fevers on the day after his layover in Arizona. Hoping to self-treat, he took one dose of leftover "
                "**ciprofloxacin** that he had at home, but the diarrhea has now progressed to **frankly bloody stools**.\n"
                "He has been taking ART as instructed"
            ),
        },
    },

    # Step 7 Fever in the returning traveler
    "fever": {
        "vignette": (
            "Approximately two weeks after his return from Southeast Asia and Oceania, and after improvement of "
            "his diarrheal illness, he now presents with **daily fevers** to 101.3°F, fatigue, and myalgias. He denies "
            "headache, cough, or current diarrhea, but endorses **abdominal pain** and notes a faint **macular rash over "
            "his torso**."
        ),
        "test_options": [
            "Peripheral blood smear",
            "Two sets of blood cultures",
            "Right upper quadrant ultrasound and stool O&P",
        ],
        "culture_result": "Blood cultures grow **gram-negative rods**.",
    },

    # Step 8: Lost to follow-up → disseminated TB scenario
    "tb": {
        "vignette": (
            "**Several years later:** The patient was **lost to follow-up** and has been **off ART**.\n"
            "They unfortunately lost their job and health insurance and have been off ART for an unknown period of time, likely years.\n"
            "He now presents with several months of **weight loss**, **generalized lymphadenopathy**, and a few weeks of **progressive shortness of breath** and a mild **headache**.\n"
        ),
        "vitals": {
            "Temperature (°F)": "100.8",
            "Heart rate": "108 bpm",
            "Respiratory rate": "22/min",
            "Blood pressure": "118/70 mmHg",
            "SpO₂ (room air)": "94%",
        },
        "exam": {
            "General": "Ill-appearing, mild respiratory distress",
            "Lungs": "Diffuse crackles",
            "Lymph nodes": "Cervical and supraclavicular nodes enlarged, non-suppurative",
            "Abdomen": "Mild hepatosplenomegaly",
            "Neuro": " No nuchal rigidity, No focal deficits",
        },
        "recent_labs": {
            "CD4+ (cells/µL)": "85",
            "HIV viral load": "> 500,000 copies/mL",
        },
        "test_options": [
            "Chest X-ray",
            "CT Chest",
            "Sputum AFB smear and culture",
            "Mycobacterium tuberculosis PCR/GeneXpert",
            "Urine LAM (lipoarabinomannan)",
            "Blood cultures for AFB",
            "Lymph node FNA for AFB stain/culture",
        ],
        "reveal": {
            "cxr": "Diffuse micronodular (miliary) pattern concerning for disseminated process.",
            "xpert": "Sputum MTB PCR (GeneXpert) **positive**, **rifampin susceptible**.",
            "ulam": "**Urine LAM positive**.",
            "fna": "Lymph node FNA: necrotizing granulomas with **AFB** on stain.",
        },
    },
}

# Resolve preloaded images once from disk
IMAGES = {k: load_img(v) for k, v in CASE.get("images", {}).items()}

# ==========================
# Session state (progress gating + reveal flags)
# ==========================
if "step" not in st.session_state:
    st.session_state.step = 1  # 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8
if "viewed" not in st.session_state:
    st.session_state.viewed = {"history": False, "exam": False, "vitals": False}
if "responses" not in st.session_state:
    st.session_state.responses = {}
if "final_interpretation" not in st.session_state:
    st.session_state.final_interpretation = ""
if "followup_responses" not in st.session_state:
    st.session_state.followup_responses = {}
# Step 3
if "step3_teaching" not in st.session_state:
    st.session_state.step3_teaching = False
# Step 4 reveal flags
if "lp_revealed" not in st.session_state:
    st.session_state.lp_revealed = False
if "lp_interpretation" not in st.session_state:
    st.session_state.lp_interpretation = ""
if "lp_success" not in st.session_state:
    st.session_state.lp_success = False
if "step4_choice" not in st.session_state:
    st.session_state.step4_choice = None

# Step 5
if "step5_teaching" not in st.session_state:
    st.session_state.step5_teaching = False
# Step 6
if "diarrhea_choice" not in st.session_state:
    st.session_state.diarrhea_choice = None
if "step6_correct" not in st.session_state:
    st.session_state.step6_correct = False
if "fever_tests" not in st.session_state:
    st.session_state.fever_tests = []
if "culture_revealed" not in st.session_state:
    st.session_state.culture_revealed = False
if "step6_answers" not in st.session_state:
    st.session_state.step6_answers = {}

# Step 7 – fever after travel
if "step7_labs" not in st.session_state:
    st.session_state.step7_labs = {
        "cbc": False,
        "cmp": False,
        "smear": False,
        "global_pcr": False,
        "hepA": False,
        "hepB": False,
        "hepC": False,
        "dengue": False,
        "zika": False,
        "chik": False,
        "blood_culture": False,
        "rick": False,
    }

if "step7_dx" not in st.session_state:
    st.session_state.step7_dx = ""

if "step7_teaching" not in st.session_state:
    st.session_state.step7_teaching = False

# Step 8 – disseminated TB / advanced HIV workup
if "step8_labs" not in st.session_state:
    st.session_state.step8_labs = {
        "cbc": False,
        "cmp": False,
        "cxr": False,
        "ct_head": False,
    }

if "step8_oi_selected" not in st.session_state:
    st.session_state.step8_oi_selected = []

if "step8_dx" not in st.session_state:
    st.session_state.step8_dx = ""

if "step8_ready" not in st.session_state:
    st.session_state.step8_ready = False

if "step8_teaching" not in st.session_state:
    st.session_state.step8_teaching = False

if "show_all_answers" not in st.session_state:
    st.session_state.show_all_answers = False


# ==========================
# Dynamic Background Styling (whole app)
# ==========================
STEP_BACKGROUNDS = {
    1: "#F9FAFB",  # NEJM light grey
    2: "#FFF7F2",  # Stanford sandstone
    3: "#F4F7FB",  # medical blue-grey
    4: "#FFF9F5",  # NEJM off-white
    5: "#F2F6FA",  # blue-tinted
    6: "#FFF5ED",  # travel warm
    7: "#FDF3F2",  # pale clay
    8: "#F3FAF5",  # TB green
}


def apply_background(step_number: int):
    bg = STEP_BACKGROUNDS.get(step_number, "#FFFFFF")
    st.markdown(
        f"""
        <style>
        html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewContainer"] > .main,
        [data-testid="stAppViewContainer"] > .main > div {{
            background-color: {bg} !important;
        }}
        [data-testid="stSidebar"] {{
            background-color: {bg}33 !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ==========================
# Helpers
# ==========================
def _all_viewed() -> bool:
    v = st.session_state.viewed
    return v["history"] and v["exam"] and v["vitals"]


def _reset_case():
    keys = list(st.session_state.keys())
    for k in keys:
        del st.session_state[k]
    st.rerun()


# ==========================
# Header & Progress bar
# ==========================
st.title("Mystery Case")
st.header("An Infectious Disease Adventure: A 46-year-old with Fever & Sore Throat")

st.markdown(
    """
- **Alvaro Ayala, MD**
- **David Dickson, MD, PhD**
- **Thomas Dieringer, MD**
- **Natalie Medvedeva, MD**
- **Andrew Nevins, MD**
"""
)

step = st.session_state.step
apply_background(step)  # change whole background based on current step
st.progress({1: 1 / 8, 2: 2 / 8, 3: 3 / 8, 4: 4 / 8, 5: 5 / 8, 6: 6 / 8, 7: 7 / 8, 8: 1.0}[step])

# ==========================
# Vignette (always visible)
# ==========================
st.header("Clinical Case")
st.markdown(CASE["vignette"])
if IMAGES.get("vignette"):
    st.image(IMAGES["vignette"], caption="Vignette image", use_container_width=True)

st.divider()

# ==========================
# STEP 1 — History / Exam / Vitals
# ==========================
if step >= 1:
    st.subheader("What would you like to know?")

    # Only show the envelope buttons while you are actively in Step 1
    if step == 1:
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            if st.button("📩 Vital Signs", key="btn_vitals"):
                st.session_state.viewed["vitals"] = True
                st.rerun()
        with c2:
            if st.button("📩 Additional History", key="btn_hist"):
                st.session_state.viewed["history"] = True
                st.rerun()
        with c3:
            if st.button("📩 Physical Exam", key="btn_exam"):
                st.session_state.viewed["exam"] = True
                st.rerun()

        st.markdown("---")

    # Render sections persistently once viewed (they remain visible in later steps)
    if st.session_state.viewed["vitals"]:
        st.subheader("Vital Signs")
        vitals = CASE["vitals"]
        st.table({"Measurement": list(vitals.keys()), "Value": list(vitals.values())})

    if st.session_state.viewed["history"]:
        st.subheader("Additional History")
        st.markdown("Below are pertinent history questions and responses:")
        for question, answer in CASE["history"].items():
            st.markdown(f"**{question}**")
            st.markdown(answer)
            st.markdown("")

    if st.session_state.viewed["exam"]:
        st.subheader("Physical Examination")
        for item in CASE["exam"]:
            st.markdown(f"- {item}")
        if IMAGES.get("rash"):
            st.image(IMAGES["rash"], caption="Skin: maculopapular rash", use_container_width=True)

    # Show a Continue button (no longer requires opening all envelopes)
    if step == 1:
        if st.button("➡️ I feel comfortable with the information I have obtained", key="btn_to_step2"):
            st.session_state.step = 2
            st.rerun()

# ==========================
# STEP 2 — Clinical reasoning
# ==========================
if step >= 2:
    st.divider()
    st.subheader("What do you think it might be going on?")
    st.markdown("Answer the questions below (all required) to unlock labs.")

    q1 = st.text_area(
        "1. What is the **clinical syndrome**?",
        value=st.session_state.responses.get("clinical_syndrome", ""),
        height=100,
    )
    q2 = st.text_area(
        "2. Which **pathogens** could potentially cause this clinical syndrome?",
        value=st.session_state.responses.get("likely_pathogen", ""),
        height=100,
    )
    q3 = st.text_area(
        "4. What **diagnostic tests** would you send?",
        value=st.session_state.responses.get("diagnostic_tests", ""),
        height=100,
    )

    def _save_responses():
        st.session_state.responses = {
            "clinical_syndrome": q1.strip(),
            "likely_pathogen": q2.strip(),
            "diagnostic_tests": q3.strip(),
        }
        missing = [k for k, v in st.session_state.responses.items() if not v]
        if missing:
            st.error("Please complete all four questions before continuing.")
        else:
            st.success("Responses recorded.")
            st.session_state.step = 3
            st.rerun()

    st.button("Do not click until instructed to do so", on_click=_save_responses)

# ==========================
# STEP 3 — Initial laboratory results
# ==========================
if step >= 3:
    st.divider()
    st.subheader("Laboratory Results")
    st.markdown("After sending your diagnostic tests, the following results are now available:")

    labs = CASE["labs"]
    st.table({"Test": list(labs.keys()), "Result": list(labs.values())})

    # Diagnosis prompt
    q4 = st.text_area(
        "5. What is your **diagnosis**?",
        value=st.session_state.responses.get("diagnosis_first", ""),
        height=120,
    )

    # Initialize teaching flag if missing
    if "step3_teaching" not in st.session_state:
        st.session_state.step3_teaching = False

    # First button — save diagnosis and show teaching notes
    def _save_step3_show_teaching():
        diagnosis = q4.strip()
        if not diagnosis:
            st.error("Please enter your diagnosis before continuing.")
            return

        # Store diagnosis (keep other response keys if present)
        st.session_state.responses["diagnosis_first"] = diagnosis
        st.session_state.final_interpretation = diagnosis  # optional, keeps things consistent

        # Unlock teaching notes/text for this step
        st.session_state.step3_teaching = True
        st.success("Diagnosis recorded. Review teaching notes below.")

    st.button("💾 Save diagnosis", on_click=_save_step3_show_teaching)

    # Teaching notes + narrative (only after first button click)
    if st.session_state.step3_teaching:
        # Narrative text about ART start & recovery
        st.info(
            "The patient recovers well and is successfully started on single-pill combination ART "
            "(bictegravir + emtricitabine + tenofovir alafenamide; integrase inhibitor + 2 NRTIs) "
            "without side effects."
        )

        with st.expander("💡 Teaching Notes"):
            col_img, col_txt = st.columns([1, 2])

            with col_img:
                if IMAGES.get("acute_hiv"):
                    st.image(
                        IMAGES["acute_hiv"],
                        caption="HIV Testing Curve",
                        use_container_width=True,
                    )

            with col_txt:
                st.markdown(
                    "**Key teaching points:**\n\n"
                    "- Primary HIV infection often presents with fever, pharyngitis, lymphadenopathy, and a "
                    "**truncal maculopapular rash**.\n"
                    "- A **negative HIV Ag/Ab** test with a **positive HIV RNA** is classic for **acute HIV infection** "
                    "before seroconversion.\n"
                    "- Early **ART initiation** improves outcomes and reduces transmission.\n"
                )

        # Second button — continue to Step 4
        if st.button("➡️ Case Continues"):
            st.session_state.step = 4
            st.rerun()

# ==========================
# STEP 4 — 3 months later (CT → LP gradual reveal with MCQ)
# ==========================
if step >= 4:
    st.divider()
    st.subheader("Case Continues... 3 Months Later...")
    fu = CASE["followup"]

    # If LP interpretation already saved, show persistent success
    if st.session_state.get("lp_success"):
        st.success("✅ Prompt antimicrobial therapy should be started in patients with high suspicion for Meningitis/Encephalitis.")

    # Vignette
    st.markdown(fu["vignette"])
    if IMAGES.get("vignette_ams"):
        st.image(IMAGES["vignette_ams"], use_container_width=True)

    # Vitals + HIV labs
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("**Vitals**")
        st.table({"Measurement": list(fu["vitals"].keys()), "Value": list(fu["vitals"].values())})
    with c2:
        st.markdown("**Recent HIV Labs**")
        st.table({"Test": list(fu["recent_labs"].keys()), "Result": list(fu["recent_labs"].values())})

    # Physical exam
    st.markdown("**Physical Examination**")
    st.table({"System": list(fu["exam"].keys()), "Finding": list(fu["exam"].values())})

    st.markdown("---")

    # Admission decision question
    st.subheader("You are admitting this patient… what would you like to do **first**?")

    options = [
        "CT head without contrast",
        "Immediate lumbar puncture",
        "Serum cryptococcal antigen and Toxoplasma serologies",
    ]

    # Preserve choice across reruns
    current_index = 0
    if st.session_state.step4_choice in options:
        current_index = options.index(st.session_state.step4_choice)

    choice = st.radio(
        "Select one option:",
        options,
        index=current_index,
        key="step4_choice_radio",
    )

    if choice:
        st.session_state.step4_choice = choice

    # Once a choice is made, show feedback and then CT + LP path
    if st.session_state.step4_choice:
        st.markdown("---")

        if st.session_state.step4_choice == "CT head without contrast":
            st.success(
                "✅ Correct. In a febrile patient with **altered mental status**, you should obtain **neuroimaging** "
                "before performing a lumbar puncture to reduce the risk of herniation."
            )
        elif st.session_state.step4_choice == "Immediate lumbar puncture":
            st.error(
                "🟥 LP is necessary in this patient, but it should be performed **after** obtaining head imaging "
                "given altered mental status."
            )
        else:  # Serum cryptococcal antigen and Toxoplasma serologies
            st.warning(
                "⚠️ Although this patient has HIV, his **well-controlled HIV with CD4 >500** makes cryptococcal "
                "meningitis and toxoplasma encephalitis less likely as the **first** test to send. "
                "Neuroimaging and CSF evaluation are more urgent."
            )

        st.markdown("---")
        st.subheader("Head CT (non-contrast)")

        # Show CT findings + image
        st.info(f"**CT Head:** {fu['ct_head_result']}")
        if IMAGES.get("ct"):
            st.image(IMAGES["ct"], caption="CT Head (non-contrast)", use_container_width=True)

        # LP reveal button
        if not st.session_state.lp_revealed:
            if st.button("📩 Show lumbar puncture (CSF) results", key="show_lp_btn"):
                st.session_state.lp_revealed = True
                st.rerun()

        # LP results + interpretation prompt + save button
        if st.session_state.lp_revealed:
            st.subheader("Lumbar Puncture Results")
            st.table({"CSF Test": list(fu["lp_results"].keys()), "Result": list(fu["lp_results"].values())})

            if IMAGES.get("csf"):
                st.image(IMAGES["csf"], caption="CSF / LP tubes", use_container_width=True)

            st.session_state.lp_interpretation = st.text_area(
                "9. Interpret these CSF findings",
                value=st.session_state.lp_interpretation,
                height=120,
                key="lp_interpretation_box",
            )

            # This button ONLY appears after LP results are shown
            if st.button("Save LP interpretation", key="save_lp_btn"):
                if not st.session_state.lp_interpretation.strip():
                    st.warning("Consider writing a brief CSF synthesis before proceeding.")
                else:
                    # Store a flag so success persists on future steps
                    st.session_state.lp_success = True

                # Advance to Step 5
                st.session_state.step = 5
                st.rerun()

# ==========================
# STEP 5 — Final questions after CSF
# ==========================
if step >= 5:
    st.divider()
    st.subheader("Some Questions")

    # Load any existing answers if they exist
    existing_step5 = st.session_state.get("step5_answers", {})

    f1 = st.text_area(
        "10. What is the **clinical syndrome**?",
        value=existing_step5.get("clinical_syndrome", ""),
        height=100,
    )
    f2 = st.text_area(
        "11. Which **pathogen** is the most likely cause?",
        value=existing_step5.get("likely_pathogen", ""),
        height=100,
    )
    f3 = st.text_area(
        "12. What **confirmatory test** would you send for diagnosis?",
        value=existing_step5.get("confirmatory_test", ""),
        height=100,
    )

    # Ensure flag exists
    if "step5_teaching" not in st.session_state:
        st.session_state.step5_teaching = False

    def _save_step5():
        st.session_state.step5_answers = {
            "clinical_syndrome": f1.strip(),
            "likely_pathogen": f2.strip(),
            "confirmatory_test": f3.strip(),
        }

        st.session_state.step5_teaching = True
        st.success("Final answers saved. Review the update and teaching notes below.")

    # Save button
    st.button("Save Final Answers (When instructed to do so)", on_click=_save_step5)

    # Only show the update paragraph + teaching notes *after* save
    if st.session_state.step5_teaching:
        # Narrative update
        st.info(
            "Update: CSF HSV PCR returns **positive**. He is started on **IV acyclovir** with "
            "complete recovery of neurological status."
        )

        # Teaching notes appear only after the save
        with st.expander("💡 Teaching Notes"):
            st.markdown(
                "**Model Answers:**\n\n"
                "- **Clinical syndrome:** Aseptic meningitis/encephalitis with altered mental status.\n"
                "- **Most likely pathogen:** **HSV-1** encephalitis is a key concern given AMS; other viral etiologies are possible.\n"
                "- **Confirmatory test:** **CSF HSV PCR** (rapid, sensitive). MRI with temporal lobe involvement can support the diagnosis.\n"
            )

        # Continue button to next part of the case
        if st.button("➡️ Case Continues..."):
            st.session_state.step = 6
            st.rerun()

# ==========================
# STEP 6 — Travel: Bloody Diarrhea
# ==========================
if step >= 6:
    st.divider()
    st.subheader("Travel: Bloody Diarrhea")

    tr = CASE["travel"]
    st.markdown(tr["summary"])

    st.markdown("**New complaint — Bloody diarrhea (2 days after return to California)**")
    st.markdown(tr["diarrhea"]["vignette"])
    if IMAGES.get("travel"):
        st.image(IMAGES["travel"], use_container_width=True)

    options = [
        "Start ciprofloxacin immediately",
        "Order a GI PCR panel and start IV fluids",
        "Obtain ova and parasite exam and start albendazole immediately",
        "Concern for inflammatory bowel disease; start sulfasalazine and budesonide",
    ]

    # Maintain previously selected choice on rerun
    current_index = None
    if st.session_state.diarrhea_choice in options:
        current_index = options.index(st.session_state.diarrhea_choice)

    choice = st.radio(
        "What would you like to do **first**?",
        options,
        index=current_index,
        key="diarrhea_choice_radio",
    )

    feedback = None

    if choice:
        st.session_state.diarrhea_choice = choice
        st.session_state.step6_correct = False  # reset unless correct

        if choice == "Start ciprofloxacin immediately":
            feedback = (
                "🟥 **Not recommended.** Empiric fluoroquinolones in **bloody diarrhea** may worsen "
                "**Shiga toxin–producing E. coli** infections and increase the risk of **hemolytic uremic syndrome (HUS)**. "
                "Choose another option."
            )

        elif choice == "Order a GI PCR panel and start IV fluids":
            feedback = (
                "✅ **Correct.** A GI PCR panel rapidly identifies the etiologic agent in **dysentery**, and supportive "
                "care with IV fluids is appropriate. Antibiotics may be indicated depending on the identified pathogen."
            )
            st.session_state.step6_correct = True

        elif choice == "Obtain ova and parasite exam and start albendazole immediately":
            feedback = (
                "🟨 **Partially reasonable, but not first-line.** Stool O&P may be useful in subacute/chronic symptoms, "
                "but **helminths are not common causes of acute bloody diarrhea**, and empiric albendazole is not indicated."
            )

        elif choice == "Concern for inflammatory bowel disease; start sulfasalazine and budesonide":
            feedback = (
                "🟨 **Premature.** Although IBD can cause bloody diarrhea, **infectious causes must be excluded first**—"
                "especially after high-risk travel and food exposures."
            )

    if feedback:
        st.markdown("---")
        st.info(feedback)

    # Teaching Notes (appear only after correct answer)
    if st.session_state.step6_correct:
        with st.expander("💡 Teaching Notes — Differential for Bloody Diarrhea"):
            st.markdown(
                "**Major Causes of Acute Dysentery (Bloody Diarrhea):**\n\n"
                "**1. *Shigella spp.*** — highly infectious, classic cause of bacillary dysentery.\n"
                "**2. *Campylobacter jejuni*** — often from undercooked poultry; can cause fever + abdominal pain.\n"
                "**3. *Salmonella* (non-typhoidal)** — from eggs, poultry, and undercooked meats.\n"
                "**4. STEC (E. coli O157:H7, others)** — associated with undercooked beef; **avoid antibiotics** → HUS risk.\n"
                "**5. *Entamoeba histolytica*** — consider in travelers; more subacute; treat with metronidazole + luminal agent.\n"
                "**6. C. difficile** — especially after antibiotic exposure (e.g., ciprofloxacin).\n\n"
                "**Diagnostic priorities:**\n"
                "- GI PCR for rapid etiologic identification\n"
                "- C. difficile NAAT/toxin if recent antibiotic exposure\n"
                "- Avoid empiric antibiotics until STEC is excluded\n\n"
                "**Key principle:** Dysentery = evaluate for pathogens that require targeted therapy and those "
                "where antibiotics could be harmful."
            )

        st.success("Great work — proceed to the next step when ready.")
        if st.button("➡️ There is more.. (Do not click until be instructed)"):
            st.session_state.step = 7
            st.rerun()

# ==========================
# STEP 7 — Travel: Fever after Diarrhea
# ==========================
if step >= 7:
    st.divider()
    st.subheader("Two weeks after returning:")

    tr = CASE["fever"]

    st.markdown("**New complaint — Fever (2 weeks after return)**")
    st.markdown(tr["vignette"])

    st.markdown("---")
    st.subheader("Which tests would you like to order?")

    # Buttons to 'order' each test; click → reveal result
    lab_buttons = [
        ("CBC with differential", "cbc"),
        ("Comprehensive metabolic panel (CMP)", "cmp"),
        ("Peripheral blood smear", "smear"),
        ("Global fever PCR panel", "global_pcr"),
        ("Hepatitis A serology", "hepA"),
        ("Hepatitis B serology", "hepB"),
        ("Hepatitis C serology", "hepC"),
        ("Dengue serologies / NS1", "dengue"),
        ("Zika serology", "zika"),
        ("Chikungunya serology", "chik"),
        ("Blood cultures", "blood_culture"),
        ("Rickettsial Antibodies", "rick"),
    ]

    cols = st.columns(3)
    for idx, (label, key) in enumerate(lab_buttons):
        col = cols[idx % 3]
        with col:
            if st.button(label, key=f"step7_{key}_btn"):
                st.session_state.step7_labs[key] = True
                st.rerun()

    st.markdown("---")
    st.subheader("Results")

    # 1) CBC
    if st.session_state.step7_labs["cbc"]:
        st.markdown("**CBC with differential**")
        cbc_data = {
            "Parameter": [
                "WBC",
                "RBC",
                "Hemoglobin",
                "Hematocrit",
                "Platelets",
                "Neutrophils",
                "Lymphocytes",
                "Monocytes",
                "Eosinophils",
            ],
            "Result": [
                "6.4 × 10³/µL",
                "4.1 × 10⁶/µL",
                "12.3 g/dL",
                "37%",
                "210 × 10³/µL",
                "68%",
                "22%",
                "8%",
                "2%",
            ],
        }
        st.table(cbc_data)

    # 2) CMP
    if st.session_state.step7_labs["cmp"]:
        st.markdown("**Comprehensive metabolic panel (CMP)**")
        cmp_data = {
            "Parameter": [
                "Sodium",
                "Potassium",
                "Chloride",
                "CO₂ (bicarbonate)",
                "BUN",
                "Creatinine",
                "Glucose",
                "Calcium",
                "AST",
                "ALT",
                "Alkaline phosphatase",
                "Total bilirubin",
                "Albumin",
            ],
            "Result": [
                "132 mmol/L",
                "4.0 mmol/L",
                "100 mmol/L",
                "24 mmol/L",
                "14 mg/dL",
                "0.9 mg/dL",
                "92 mg/dL",
                "9.1 mg/dL",
                "26 U/L",
                "22 U/L",
                "90 U/L",
                "0.8 mg/dL",
                "4.0 g/dL",
            ],
        }
        st.table(cmp_data)

    # 3) Peripheral smear
    if st.session_state.step7_labs["smear"]:
        st.markdown("**Peripheral blood smear**")
        if IMAGES.get("blood_smear"):
            st.image(IMAGES["blood_smear"], caption="Peripheral smear", use_container_width=True)
        else:
            st.info("Peripheral smear: no parasites identified; morphology otherwise unremarkable.")

    # 4) Global fever PCR
    if st.session_state.step7_labs["global_pcr"]:
        st.markdown("**Global fever PCR panel**")
        st.markdown(
            "Result: **Negative** for Chikungunya virus, Dengue virus (serotypes 1, 2, 3 and 4)\n"
            "Leptospira spp., Plasmodium spp. (including species differentiation of Plasmodium falciparum and Plasmodium vivax/ovale)."
        )

    # 5) Hepatitis A
    if st.session_state.step7_labs["hepA"]:
        st.markdown("**Hepatitis A serology**")
        st.markdown(
            "- Hepatitis A IgG: **Positive**  \n"
            "- Hepatitis A IgM: **Negative**"
        )

    # 6) Hepatitis B
    if st.session_state.step7_labs["hepB"]:
        st.markdown("**Hepatitis B serology**")
        st.markdown(
            "- HBsAg: **Negative**  \n"
            "- Anti–HBs: **Positive**  \n"
            "- Anti–HBc (total): **Negative**"
        )

    # 7) Hepatitis C
    if st.session_state.step7_labs["hepC"]:
        st.markdown("**Hepatitis C serology**")
        st.markdown(
            "- HCV antibody: **Positive**  \n"
            "- HCV RNA (reflex): **Not detected**"
        )

    # 8) Dengue
    if st.session_state.step7_labs["dengue"]:
        st.markdown("**Dengue testing**")
        st.markdown(
            "- NS1 rapid antigen: **Negative**  \n"
            "- Dengue IgM: **Negative**  \n"
            "- Dengue IgG: **Negative**"
        )

    # 9) Zika
    if st.session_state.step7_labs["zika"]:
        st.markdown("**Zika serology**")
        st.markdown(
            "- Zika IgM: **Negative**  \n"
            "- Zika IgG: **Negative**"
        )

    # 10) Chikungunya
    if st.session_state.step7_labs["chik"]:
        st.markdown("**Chikungunya serology**")
        st.markdown(
            "- Chikungunya IgM: **Negative**  \n"
            "- Chikungunya IgG: **Positive**"
        )

    # 11) Blood cultures
    if st.session_state.step7_labs["blood_culture"]:
        st.markdown("**Blood cultures**")
        st.markdown("After incubation gram stain demonstrates:")
        if IMAGES.get("culture"):
            st.image(IMAGES["culture"], caption="Gram stain of blood culture", use_container_width=True)

    # 12) Rickettsial antibodies
    if st.session_state.step7_labs["rick"]:
        st.markdown("**Rickettsial Antibodies**")
        st.markdown(
            "- RMSF IgG:	<1:64 \n"
            "- RMSF IgM:	<1:64"
)

    st.markdown("---")

    # Final diagnosis question
    dx_input = st.text_area(
        "16. Based on the travel history, clinical presentation, and results above, what is the **most likely diagnosis**?",
        value=st.session_state.step7_dx,
        height=120,
    )

    def _save_step7_dx():
        diagnosis = dx_input.strip()
        if not diagnosis:
            st.error("Please enter a diagnosis before continuing.")
            return
        st.session_state.step7_dx = diagnosis
        st.session_state.step7_teaching = True
        st.success("Diagnosis recorded. Review teaching notes below.")

    st.button("💾 This is my diagnosis", on_click=_save_step7_dx)

if st.session_state.step7_teaching:
    with st.expander("💡 Teaching Notes — Typhoidal vs. Non-Typhoidal Salmonella in Travelers"):
        st.markdown(
            "**Why *Salmonella Typhi* (typhoid fever) is the leading diagnosis:**\n\n"
            "**1. Salmonellosis exists in two major clinical categories:**\n"
            "- **Typhoidal Salmonella** (*Salmonella enterica* serovars **Typhi** and **Paratyphi A/B/C**)\n"
            "- **Non-typhoidal Salmonella (NTS)** – hundreds of serovars (e.g., *S. Enteritidis*, *S. Typhimurium*) typically causing **self-limited gastroenteritis**.\n\n"
            "**Key distinctions:**\n"
            "- **NTS** → usually acquired from animal reservoirs (poultry, eggs, reptiles), causes **fever + acute diarrhea**, rarely bacteremia in immunocompetent hosts.\n"
            "- **Typhoidal Salmonella** → **strictly human-adapted pathogens**, transmitted via **contaminated food/water**, capable of **systemic infection** with bacteremia and multiorgan involvement.\n\n"
            "**Why this traveler’s illness points to typhoid:**\n"
            "- **Endemic regions:** Southeast Asia and parts of Oceania (including Papua New Guinea) remain high-burden areas for *S. Typhi/Paratyphi*.\n"
            "- **Clinical pattern:** Stepwise fever, malaise, myalgias, abdominal pain, and a faint truncal rash (“rose spots”) are **classic for typhoid fever**, not NTS.\n"
            "- **Bacteremia:** Blood cultures growing **gram-negative rods** in a traveler with this syndrome are most consistent with **typhoidal Salmonella**, since NTS bacteremia is uncommon in immunocompetent adults.\n"
            "- **Laboratory clues:** Bland LFTs, mild hyponatremia, and minimal cytopenias early in the course are frequently seen in typhoid.\n"
            "- **Negative arboviral & broad fever testing** (dengue, Zika, chikungunya, viral PCR panel) help narrow to bacterial etiologies.\n\n"
            "**Why *Salmonella Typhi* is important not to miss:**\n"
            "- It can cause **severe systemic disease**, intestinal perforation, encephalopathy, and relapse if untreated.\n"
            "- Rising global rates of **extensively drug-resistant (XDR) Typhi** (notably in South Asia) require careful antibiotic selection.\n"
            "- Carriage in the gallbladder can lead to **chronic shedding** and community transmission.\n"
            "- It is a **vaccine-preventable illness** — crucial teaching point for future travelers.\n\n"
            "**Management pearls:**\n"
            "- Obtain **two sets of blood cultures**.\n"
            "- Start empiric **ceftriaxone** or **azithromycin**, adjusting based on susceptibilities.\n"
            "- Counsel on prevention and the role of **typhoid vaccination** for future trips.\n"
        )

    if st.button("➡️ Continue to next step"):
        st.session_state.step = 8
        st.rerun()

# ==========================
# STEP 8 — Lost to follow-up: disseminated TB / advanced HIV
# ==========================
if step >= 8:
    st.divider()
    st.subheader("Lost to Follow-up: Progressive Dyspnea, LAD, Headache")

    tb = CASE["tb"]

    st.markdown(tb["vignette"])
    if IMAGES.get("tb_vignette"):
        st.image(IMAGES["tb_vignette"], use_container_width=True)
    st.markdown(
        "You are now the **junior attending** admitting this patient. The intern has already obtained "
        "vitals, basic labs, and a focused physical exam."
    )

    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("**Vitals**")
        st.table({"Measurement": list(tb["vitals"].keys()), "Value": list(tb["vitals"].values())})
    with c2:
        st.markdown("**Recent HIV Labs**")
        st.table({"Test": list(tb["recent_labs"].keys()), "Result": list(tb["recent_labs"].values())})

    st.markdown("**Physical Examination**")
    st.table({"System": list(tb["exam"].keys()), "Finding": list(tb["exam"].values())})

    st.markdown("---")
    st.subheader("Which initial diagnostic tests would you like to review?")

    # Phase 1: CBC, CMP, CXR, CT head
    lab_buttons_8 = [
        ("CBC with differential", "cbc"),
        ("Comprehensive metabolic panel (CMP)", "cmp"),
        ("Chest X-ray", "cxr"),
        ("CT head (non-contrast)", "ct_head"),
    ]

    cols = st.columns(4)
    for idx, (label, key) in enumerate(lab_buttons_8):
        col = cols[idx % 4]
        with col:
            if st.button(label, key=f"step8_{key}_btn"):
                st.session_state.step8_labs[key] = True
                st.rerun()

    st.markdown("---")
    st.subheader("Results")

    # CBC
    if st.session_state.step8_labs["cbc"]:
        st.markdown("**CBC with differential**")
        cbc8 = {
            "Parameter": [
                "WBC",
                "Hemoglobin",
                "Hematocrit",
                "MCV",
                "Platelets",
                "Neutrophils",
                "Lymphocytes",
                "Monocytes",
                "Eosinophils",
            ],
            "Result": [
                "2.9 × 10³/µL",
                "7.8 g/dL",
                "24%",
                "76 fL",
                "190 × 10³/µL",
                "62%",
                "20% (absolute lymphopenia)",
                "15%",
                "3%",
            ],
        }
        st.table(cbc8)

    # CMP
    if st.session_state.step8_labs["cmp"]:
        st.markdown("**Comprehensive metabolic panel (CMP)**")
        cmp8 = {
            "Parameter": [
                "Sodium",
                "Potassium",
                "Chloride",
                "CO₂ (bicarbonate)",
                "BUN",
                "Creatinine",
                "Glucose",
                "Calcium",
                "AST",
                "ALT",
                "Alkaline phosphatase",
                "Total bilirubin",
                "Albumin",
            ],
            "Result": [
                "134 mmol/L",
                "4.1 mmol/L",
                "101 mmol/L",
                "23 mmol/L",
                "18 mg/dL",
                "1.0 mg/dL",
                "98 mg/dL",
                "8.5 mg/dL",
                "30 U/L",
                "25 U/L",
                "110 U/L",
                "0.9 mg/dL",
                "2.8 g/dL",
            ],
        }
        st.table(cmp8)

    # Chest X-ray
    if st.session_state.step8_labs["cxr"]:
        st.markdown("**Chest X-ray**")
        st.info("Diffuse micronodular (miliary) pattern throughout both lung fields, concerning for a disseminated process.")
        if IMAGES.get("tb_cxr"):
            st.image(IMAGES["tb_cxr"], caption="Chest radiograph", use_container_width=True)

    # CT head
    if st.session_state.step8_labs["ct_head"]:
        st.markdown("**CT head (non-contrast)**")
        st.info("Axial CT shows enhancing masses at the right frontal brain parenchyma.")
        if IMAGES.get("tb_ct_head"):
            st.image(IMAGES["tb_ct_head"], caption="CT head", use_container_width=True)

    st.markdown("---")
    st.subheader("You suspect an opportunistic infection — which additional tests would you like to order?")

    # Phase 2: OI-focused tests with green/yellow reasoning
    OI_TESTS = {
        "blood_cx": {
            "label": "Routine blood cultures",
            "result": "Pending.",
            "reason": "Reasonable: bacteremia should be ruled out in a patient with a likely systemic infection.",
            "reasonable": True,
        },
        "afb_blood": {
            "label": "AFB blood cultures",
            "result": "Pending.",
            "reason": "Reasonable: mycobacteremia (including disseminated TB or MAC) can occur in advanced HIV.",
            "reasonable": True,
        },
        "histo_ag": {
            "label": "Histoplasma antigen (serum and urine)",
            "result": "Negative in both serum and urine.",
            "reason": "Reasonable: disseminated histoplasmosis is an important OI in advanced HIV with systemic symptoms, depending on geographical risk factors.",
            "reasonable": True,
        },
        "pjp_pcr": {
            "label": "PJP PCR from plasma",
            "result": "Negative.",
            "reason": "Less appropriate: this presentation (chronic LAD, miliary pattern, weight loss, mild headache) is not classic for PJP pneumonia.",
            "reasonable": False,
        },
        "bdg": {
            "label": "1,3-β-D-glucan",
            "result": "Negative.",
            "reason": "Less appropriate: this presentation (chronic LAD, miliary pattern, weight loss, mild headache) is not classic for PJP.",
            "reasonable": False,
        },
        "sputum_cx": {
            "label": "Routine sputum culture",
            "result": "Mixed upper-respiratory flora; no predominant pathogen.",
            "reason": "Less appropriate: not a typical community-acquired pneumonia picture; routine sputum culture is low yield.",
            "reasonable": False,
        },
        "legionella": {
            "label": "Legionella PCR from plasma",
            "result": "Negative.",
            "reason": "Less appropriate: imaging and clinical course are not typical for Legionella pneumonia.",
            "reasonable": False,
        },
        "serum_crag": {
            "label": "Serum cryptococcal antigen (CrAg)",
            "result": "Negative.",
            "reason": "Reasonable: advanced HIV and headache warrant screening for cryptococcal disease.",
            "reasonable": True,
        },
        "toxo": {
            "label": "Toxoplasma IgG and PCR",
            "result": "IgG positive; PCR pending.",
            "reason": "Reasonable: CNS symptoms and lymphadenopathy in advanced HIV should prompt evaluation for toxoplasmosis.",
            "reasonable": True,
        },
        "afb_sputum": {
            "label": "AFB sputum ×3 and MTB PCR",
            "result": "Pending.",
            "reason": "Reasonable: pulmonary symptoms with miliary CXR strongly suggest TB; sputum AFB and MTB PCR are key tests.",
            "reasonable": True,
        },
        "ln_fna": {
            "label": "Lymph node FNA for AFB/fungal stain and culture",
            "result": "Interventional radiology defers until non-invasive tests result.",
            "reason": "Potentially reasonable: tissue diagnosis is useful, but may be pursued in the future if non-invasive tests are not diagnostic.",
            "reasonable": True,
        },
        "cocci": {
            "label": "Coccidioides antibody with reflex complement fixation",
            "result": "Pending.",
            "reason": "Reasonable: prior travel through Arizona and current residence in California make coccidioidomycosis a consideration.",
            "reasonable": True,
        },
    }

    oi_label_to_key = {v["label"]: k for k, v in OI_TESTS.items()}

    selected_labels = st.multiselect(
        "Select additional tests (you can choose more than one):",
        [v["label"] for v in OI_TESTS.values()],
        default=[OI_TESTS[k]["label"] for k in st.session_state.step8_oi_selected],
    )
    st.session_state.step8_oi_selected = [oi_label_to_key[l] for l in selected_labels]

    if st.session_state.step8_oi_selected:
        st.markdown("---")
        st.subheader("Additional test results and reasoning")
        for key in st.session_state.step8_oi_selected:
            test = OI_TESTS[key]
            text = f"**{test['label']}**\n\nResult: {test['result']}\n\n{test['reason']}"
            if test["reasonable"]:
                st.success(text)
            else:
                st.warning(text)

        # Learner indicates they are ready to synthesize
        if st.button("✅ I have the tests I need — I'm ready to continue"):
            st.session_state.step8_ready = True
            st.rerun()

    # Phase 3: Diagnosis, TB narrative, teaching, end-case
    if st.session_state.step8_ready:
        st.markdown("---")
        st.subheader("Synthesis")

        dx_input = st.text_area(
            "19. Based on all of the information above, what is the **most likely diagnosis**?",
            value=st.session_state.step8_dx,
            height=120,
        )

        def _save_step8_dx():
            diagnosis = dx_input.strip()
            if not diagnosis:
                st.error("Please enter a diagnosis before continuing.")
                return
            st.session_state.step8_dx = diagnosis
            st.session_state.step8_teaching = True
            st.success("Diagnosis recorded. Review the update and teaching notes below.")

        st.button("💾 I'm a master clinician, this is my diagnosis", on_click=_save_step8_dx)

    if st.session_state.step8_teaching:
        st.markdown("---")
        st.info(
            "Update: Sputum AFB smear returns **4+ positive**, **MTB PCR (GeneXpert) positive**, and **rpoB mutation "
            "testing negative**, consistent with **rifampin-susceptible Mycobacterium tuberculosis**.\n\n"
            "You start the patient on **rifampin, isoniazid (with pyridoxine), pyrazinamide, and ethambutol (RIPE)**.\n\n"
            "Given concern for possible **TB meningitis or CNS involvement** in advanced HIV, you plan to **re-initiate ART "
            "approximately 2–8 weeks after** starting TB therapy to balance immune recovery with the risk of CNS IRIS."
        )

        with st.expander("💡 Teaching Notes — Pulmonary & CNS Lesions in HIV by CD4 Count"):
            st.markdown(
                "**Pulmonary syndromes by CD4 count:**\n\n"
                "- **CD4 > 200 cells/µL**\n"
                "  - Similar to HIV-negative patients: **typical CAP** (e.g., *Streptococcus pneumoniae*, *H. influenzae*),\n"
                "    viral respiratory infections, **TB** can reactivate as well.\n\n"
                "- **CD4 <200 cells/µL**\n"
                "  - **Pneumocystis jirovecii pneumonia (PJP)** — subacute dyspnea, hypoxemia, diffuse interstitial infiltrates.\n"
                "  - **Reactivation TB** and atypical bacterial pneumonias.\n\n"
                "- **CD4 < 100 cells/µL**\n"
                "  - Higher risk of **disseminated TB** with miliary pattern, **disseminated fungal disease** (e.g., histoplasmosis).\n\n"
                "**CNS lesions by CD4 count:**\n\n"
                "- **CD4 < 200 cells/µL**\n"
                "  - **Cryptococcal meningitis**, **tuberculous meningitis**, **PML** (JC virus), HIV-associated neurocognitive disorder.\n\n"
                "- **CD4 < 100 cells/µL**\n"
                "  - **Toxoplasma encephalitis** — multiple ring-enhancing lesions in basal ganglia/gray–white junction.\n"
                "  - **CNS TB** (basilar meningitis, tuberculomas), **CMV encephalitis**, advanced HIV-associated dementia.\n"
                "  - **CNS lymphoma**.\n\n"
            )

        # End case: review all responses
        if st.button("🏁 End case — Review all your responses"):
            st.session_state.show_all_answers = True
            st.rerun()

    if st.session_state.show_all_answers:
        st.markdown("---")
        st.subheader("Case Review — Your Responses by Step")

        # Step 2
        if st.session_state.get("responses"):
            with st.expander("Step 2 — Initial clinical reasoning"):
                for k, v in st.session_state.responses.items():
                    st.markdown(f"**{k.replace('_', ' ').title()}:** {v or '*No answer entered*'}")

        # Step 3
        if "diagnosis_first" in st.session_state.get("responses", {}):
            with st.expander("Step 3 — Acute HIV diagnosis"):
                st.markdown(f"**Diagnosis after labs:** {st.session_state.responses.get('diagnosis_first', '*No answer*')}")

        # Step 4
        if st.session_state.get("followup_responses") or st.session_state.get("lp_interpretation"):
            with st.expander("Step 4 — HSV encephalitis workup"):
                for k, v in st.session_state.get("followup_responses", {}).items():
                    st.markdown(f"**{k.replace('_',' ').title()}:** {v or '*No answer*'}")
                st.markdown(f"**LP interpretation:** {st.session_state.get('lp_interpretation', '*No answer*')}")

        # Step 5
        if st.session_state.get("step5_answers"):
            with st.expander("Step 5 — Final HSV questions"):
                for k, v in st.session_state.step5_answers.items():
                    st.markdown(f"**{k.replace('_',' ').title()}:** {v or '*No answer*'}")

        # Step 6
        if st.session_state.get("step6_answers") or st.session_state.get("diarrhea_choice"):
            with st.expander("Step 6 — Bloody diarrhea after travel"):
                st.markdown(f"**Initial approach to dysentery:** {st.session_state.get('diarrhea_choice', '*No choice*')}")
                if st.session_state.get("step6_answers"):
                    for k, v in st.session_state.step6_answers.items():
                        st.markdown(f"**{k.replace('_',' ').title()}:** {v}")

        # Step 7
        if st.session_state.get("step7_dx"):
            with st.expander("Step 7 — Fever after travel (enteric fever)"):
                st.markdown(f"**Most likely diagnosis (your answer):** {st.session_state.step7_dx or '*No answer*'}")

        # Step 8
        with st.expander("Step 8 — Advanced HIV / disseminated TB"):
            st.markdown(f"**Most likely diagnosis (your answer):** {st.session_state.step8_dx or '*No answer*'}")
            if st.session_state.step8_oi_selected:
                st.markdown("**Additional OI tests you selected:**")
                for key in st.session_state.step8_oi_selected:
                    st.markdown(f"- {OI_TESTS[key]['label']}")

        st.success("End of case. You can scroll back through the steps or reset the app to run it again with a new learner.")

# ==========================
# Reset / Footer
# ==========================
with st.container():
    st.divider()
    if st.button("🔁 Reset case (start over)"):
        _reset_case()

st.caption(f" {datetime.now().year} Created for Educational Purposes Only")
