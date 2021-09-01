import os


def save_files(final_df, path="data/files/"):
    """ """

    for i, ser in final_df.iterrows():

        folder = ser.folder
        lenn = len(final_df)
        doc_filename = ser.document_link_new.split("/")[-1]
        press_filename = ser.press_release_link_new.split("/")[-1]
        doc_text = ser.legal_doc_text
        press_text = ser.press_release_text

        strize = lambda i: i[:30].replace("\n", "/n")

        try:
            print(f"i/I: {i}/{lenn}, folder : {folder}, path + folder : {path + folder}")
            print(f"doc_filename : {doc_filename}, press_filename : {press_filename}")
            print(f"doc_text : {strize(doc_text)} ||| press_text : {strize(press_text)}")
            print()

            # mkdir
            if not os.path.isdir(path + folder):
                os.mkdir(path + folder)

            # doc.txt and press .txt
            for fn, txt in [(doc_filename, doc_text), (press_filename, press_text)]:
                with open(path + folder + "/" + fn, "w") as f:
                    f.write(txt)

        except Exception as e:
            pass
