import legal_doc_processing

from legal_doc_processing.pr import read_PressRelease as rr

ob = rr("./data/boot/press_release.txt")
ob.predict_all()

from legal_doc_processing.ld import read_LegalDoc as rr

ob = rr("./data/boot/order.txt")
ob.predict_all()
