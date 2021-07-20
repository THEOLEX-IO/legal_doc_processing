import legal_doc_processing.press_release.information_extraction as press_inf_ext
import legal_doc_processing.legal_doc.information_extraction as legal_doc_inf_ext
import legal_doc_processing.decision.information_extraction as decision_inf_ext


def predict_handler(obj_name):
    """ container for predict function """

    if obj_name == "PressRelease":
        return {
            "compliance_obligations": press_inf_ext.predict_compliance_obligations,
            "cooperation_credit": press_inf_ext.predict_cooperation_credit,
            "court": press_inf_ext.predict_court,
            "country_of_violation": press_inf_ext.predict_country_of_violation,
            "currency": press_inf_ext.predict_currency,
            "decision_date": press_inf_ext.predict_decision_date,
            "defendant": press_inf_ext.predict_defendant,
            "extracted_authorities": press_inf_ext.predict_extracted_authorities,
            "extracted_sanctions": press_inf_ext.predict_extracted_sanctions,
            "extracted_violations": press_inf_ext.predict_extracted_violations,
            "folder": press_inf_ext.predict_folder,
            "judge": press_inf_ext.predict_judge,
            "justice_type": press_inf_ext.predict_justice_type,
            "monetary_sanction": press_inf_ext.predict_monetary_sanction,
            "monitor": press_inf_ext.predict_monitor,
            "nature_de_sanction": press_inf_ext.predict_nature_de_sanction,
            "nature_of_violations": press_inf_ext.predict_nature_of_violations,
            "penalty_details": press_inf_ext.predict_penalty_details,
            "reference": press_inf_ext.predict_reference,
            "type": press_inf_ext.predict_type,
            # "violation_date ": predict_violation_date,
        }
    if obj_name == "LegalDoc":
        return {
            "compliance_obligations": legal_doc_inf_ext.predict_compliance_obligations,
            "cooperation_credit": legal_doc_inf_ext.predict_cooperation_credit,
            "court": legal_doc_inf_ext.predict_court,
            "country_of_violation": legal_doc_inf_ext.predict_country_of_violation,
            "currency": legal_doc_inf_ext.predict_currency,
            "decision_date": legal_doc_inf_ext.predict_decision_date,
            "defendant": legal_doc_inf_ext.predict_defendant,
            "extracted_authorities": legal_doc_inf_ext.predict_extracted_authorities,
            "extracted_violations": legal_doc_inf_ext.predict_extracted_violations,
            "extracted_sanctions": legal_doc_inf_ext.predict_extracted_sanctions,
            "folder": legal_doc_inf_ext.predict_folder,
            "judge": legal_doc_inf_ext.predict_judge,
            "justice_type": legal_doc_inf_ext.predict_justice_type,
            "monetary_sanction": legal_doc_inf_ext.predict_monetary_sanction,
            "monitor": legal_doc_inf_ext.predict_monitor,
            "nature_de_sanction": legal_doc_inf_ext.predict_nature_de_sanction,
            "nature_of_violations": legal_doc_inf_ext.predict_nature_of_violations,
            "penalty_details": legal_doc_inf_ext.predict_penalty_details,
            "reference": legal_doc_inf_ext.predict_reference,
            "type": legal_doc_inf_ext.predict_type,
            # "violation_date ": predict_violation_date,
        }
    if obj_name == "Decision":
        return {
            "compliance_obligations": decision_inf_ext.predict_compliance_obligations,
            "cooperation_credit": decision_inf_ext.predict_cooperation_credit,
            "court": decision_inf_ext.predict_court,
            "country_of_violation": decision_inf_ext.predict_country_of_violation,
            "currency": decision_inf_ext.predict_currency,
            "decision_date": decision_inf_ext.predict_decision_date,
            "defendant": decision_inf_ext.predict_defendant,
            "extracted_authorities": decision_inf_ext.predict_extracted_authorities,
            "extracted_sanctions": decision_inf_ext.predict_extracted_sanctions,
            "extracted_violations": decision_inf_ext.predict_extracted_violations,
            "folder": decision_inf_ext.predict_folder,
            "judge": decision_inf_ext.predict_judge,
            "justice_type": decision_inf_ext.predict_justice_type,
            "monetary_sanction": decision_inf_ext.predict_monetary_sanction,
            "monitor": decision_inf_ext.predict_monitor,
            "nature_de_sanction": decision_inf_ext.predict_nature_de_sanction,
            "nature_of_violations": decision_inf_ext.predict_nature_of_violations,
            "penalty_details": decision_inf_ext.predict_penalty_details,
            "reference": decision_inf_ext.predict_reference,
            "type": decision_inf_ext.predict_type,
            # "violation_date ": predict_violation_date,
        }