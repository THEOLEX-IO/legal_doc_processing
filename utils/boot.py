from legal_doc_processing.pr import read_PressRelease as rr

ob = rr("./data/boot/press_release.txt")
pp = ob.predict_all()
print(pp)

from legal_doc_processing.ld import read_LegalDoc as rr

ob = rr("./data/boot/order.txt")
pp = ob.predict_all()
print(pp)