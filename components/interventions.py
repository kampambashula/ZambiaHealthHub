import streamlit as st

def show_interventions():
    st.header("Strategic Intervention Areas and Goals")

    intervention_data = {
        "Primary Health Care": "Contribute to Universal Health Coverage (UHC) by providing comprehensive essential PHC services.",
        "Health Promotion & Education": "Empower communities to achieve highest health and well-being.",
        "RMNCAH-N": ("Reduce Maternal Mortality from 278 to <100/100,000 live births by 2026, "
                     "reduce Neonatal Mortality Rate from 27 to 12/1000 live births, "
                     "reduce Under-5 Mortality from 61 to 25/1000 live births."),
        "Communicable Diseases": ("Reduce malaria incidence from 340 to 201/1000, "
                                 "HIV incidence from 28,000 to 15,000, "
                                 "TB incidence from 319 to 169/100,000 population by 2026."),
        "Non-Communicable Diseases": ("Reduce morbidity and mortality due to NCDs and promote mental health and well-being."),
        "Health Workforce": ("Increase availability of skilled and motivated health staff to improve service delivery."),
        "Health Infrastructure & Supplies": ("Improve availability of medicines, equipment, and infrastructure."),
        "Health Information & Research": ("Strengthen integrated health information systems and research."),
        "Health Financing": ("Attain adequate, sustainable, and predictable financing for health sector.")
    }

    for area, goal in intervention_data.items():
        st.markdown(f"**{area}**: {goal}")
