# #!/usr/bin/env python
# # coding: utf-8

# # ## 1 - Impots
# # --------------------


# import legal_doc_processing as ldp
# from legal_doc_processing.information_extraction import *
# from legal_doc_processing.segmentation import *
# from legal_doc_processing.utils import *

# from notebooks.packages import *


# # ## Extracted authorities


# """
# UNITED STATES DISTRICT COURT
# FOR THE MIDDLE DISTRICT OF FLORIDA
# """

# # ## Code law violation


# """
# violated Section 4c(a)(5)(C) of the Commodity Exchange Act ("Act"), 7 U.S.C.
# § 6c(a)(5)(C) (2018).
# """


# """
# Section 4c(a)(5) of the Act, 7 U.S.C.
# § 6c(a)(5) (2012).
# """

# # ## Violation period


# line = 'The Commodity Futures Trading Commission ("Commission") has reason to believe that from at least July 2012 through March 2017 ("Relevant Period"), Propex Derivatives Pty Ltd. ("Propex") violated Section 4c(a)(5)(C) of the Commodity Exchange Act ("Act"), 7 U.S.C. 6c(a)(5)(C) (2018). Therefore, the Commission deems it appropriate and in the public interest that public administrative proceedings be, and hereby are, instituted to determine whether Propex engaged in the violations set forth herein and to determine whether any order should be issued imposing remedial sanctions.'


# ("Relevant Period")


# # ## Transaction amount


# """
# pour complaint tous les montants vers Transaction amounts
# """

# # ## Defendant


# """
# Propex Derivatives Pty Ltd, Respondent.
# """


# #!pip install -U spacy
# #!python -m spacy download en_core_web_sm


# # ## Nature of violations


# """
# II. FINDINGS
# The Commission finds the following:
# A. SUMMARY
# During the Relevant Period, Propex, by and through a Propex trader ("Trader A"),·
# engaged in thousands of instances of the disruptive trading practice known as "spoofing"
# (bidding or offering with the intent to cancel the bid or offer before execution) in the E-mini
# S&P 500 futures contracts traded on the Chicago Mercantile Exchange ("CME"), a futures
# exchange and designated contract market which is owned and operated by CME Group Inc. This
# conduct violated Section 4c(a)(5)(C) of the Act, 7 U.S.C. § 6c(a)(5)(C) (2018).
# """


# # cftc_full_list = pd.read_excel("cftc_full_list.xlsx")


# def gen_line_rep(rep):
#     original_path = f"./cftc/original/{rep}"
#     text_path = f"./cftc/text/{rep}"
#     meta_path = f"./cftc/meta-data/{rep}"
#     lines = []
#     for file in glob.glob(f"{meta_path}/*.json"):
#         filename = os.path.basename(file)

#         with open(file) as json_file:
#             data = json.load(json_file)

#         data["filename"] = filename.replace(".json", "")
#         data["folder"] = rep
#         with open(f"{text_path}/{filename.replace('.json','.txt')}") as f:
#             data["doc_text"] = f.read()

#         lines.append(data)
#     return lines


# meta_data = []
# for index, row in cftc_full_list[~cftc_full_list.scraped_folder.isnull()].iterrows():
#     try:
#         meta_data.extend(gen_line_rep(row["scraped_folder"]))
#     except:
#         print("error on", row["scraped_folder"])
# len(meta_data)


# df_meta_data = pd.DataFrame(meta_data)


# df_meta_data["doc_clean"] = df_meta_data.doc_text.apply(clean_doc)


# df_meta_data["first_page"] = df_meta_data["doc_clean"].str[0]


# df_meta_data = df_meta_data[~df_meta_data["first_page"].isnull()]


# # ## Get reference


# # df_meta_data["reference"] = df_meta_data.first_page.apply(get_case)


# # # ## Get defendant


# # first_page = [text for text in df_meta_data.first_page.values[3] if len(text) > 100]


# # first_page


# # print(nlp(question="Who violeted?", context=".".join(first_page)))


# # print(nlp(question="Who is the defendant?", context=".".join(first_page), topk=3))


# # df_meta_data[['reference', 'folder', 'filename']][df_meta_data.reference.isnull()]


# # ## Type


# # df_meta_data["is_order"] = df_meta_data.filename.str.contains("order")
# # df_meta_data["is_complaint"] = df_meta_data.filename.str.contains("complaint")


# # df_meta_data["type"] = np.where(
# #     df_meta_data["is_order"],
# #     "Order CFTC",
# #     np.where(df_meta_data["is_complaint"], "Complaint CFTC", None),
# # )
