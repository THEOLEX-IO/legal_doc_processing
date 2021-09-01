from legal_doc_processing.utils import get_pipeline, get_spacy
from legal_doc_processing.press_release.press_release import PressRelease


def press_release() : 


    try : 
        with open("./data/boot/press_release.txt") as f : 
            return f.read()
        with open("./app/data/boot/press_release.txt") as f : 
            return f.read()
    except Exception as e : 
        txt =  """Release Number 7100-15

 

January 12, 2015

Federal Court in Florida Enters Order Freezing Assets in CFTC Foreign Currency Anti-
Fraud Action against Allied Markets LLC and its Principals Joshua Gilliland and Chawalit
Wongkhiao

CFIC Charges Jacksonville, Florida, Defendants with Operating a
Fraudulent Forex Pool and Misappropriating Customer Funds to Pay
Personal Expenses

Washington, DC — The U.S. Commodity Futures Trading Commission (CFTC) today announced that it filed a civil
enforcement Complaint in the U.S. District Court for the Middle District of Florida, charging Defendants Allied Markets
LLC, and its principals Joshua Gilliland and Chawalit Wongkhiao, all of Jacksonville, Florida, with operating a
fraudulent foreign currency (forex) commodity pool in violations of the Commodity Exchange Act (CEA) and CFTC
Regulations. In addition, none of the Defendants has ever been registered with the CFTC, as required.

On January 7, 2015, the day after the CFTC Complaint was filed under seal, U.S. District Judge Marcia Morales Howard
issued an emergency Order freezing and preserving assets under the Defendants’ control and prohibiting them from
destroying documents or denying CFTC staff access to their books and records. The Court has scheduled a hearing for
January 21, 2015, on the CFTC’s motion for a preliminary injunction.

The CFTC Complaint charges that, as early as January 2012, the Defendants fraudulently solicited more than $1 million
from members of the public to trade forex in a commodity pool. As alleged, Defendants Gilliland and Wongkhiao
misappropriated funds to pay their personal expenses. For example, instead of trading forex as promised, they allegedly
withdrew approximately $850,000 in pool participant funds from the Allied Markets forex account, spending more than
$64,000 of the stolen funds on restaurants and entertainment; approximately $33,000 on travel, hotels and rental cars;
and approximately $66,000 on rent for their residence in Jacksonville Beach, Florida. They also transferred at least
$83,200 to their personal bank accounts and withdrew approximately $139,000 in cash from automated teller machines
and at bank branches, the Complaint charges.

Defendants also used pool participant funds to pay purported trading profits and supposedly returned pool participants’
principal in the manner of a Ponzi scheme, according to the Complaint.

Specifically, according to the Complaint, the Defendants solicited members of the public to send them money for forex
trading by fraudulently guaranteeing specific trading returns and by making material misrepresentations regarding their
trading expertise and results, including that Defendants’ forex trading was generating large profits.

In its continuing litigation, the CFTC seeks full restitution to defrauded pool participants, disgorgement of any ill-gotten
gains, a civil monetary penalty, permanent registration and trading bans, and a permanent injunction against future
violations of the CEA and CFTC Regulations, as charged.

The CFTC appreciates the assistance of the Jacksonville Beach Police Department, the Jacksonville Sheriff's Office, the
Florida Office of Financial Regulation, the United States Marshals Service, and the National Futures Association.

CFTC Division of Enforcement staff members responsible for this action are Jonah McCarthy, Patricia Gomersall, Dmitriy
Vilenskiy, Jonathan Robell, John Einstman, and Paul Hayeck.

(See Complaint and Asset Freeze Order under Related Links.)
2K OK OOK OK OK KOK
CFTC’s Foreign Currency (Forex) Fraud and Commodity Pool Fraud Advisories

The CFTC has issued several customer protection Fraud Advisories that provide the warning signs of fraud, including the
Foreign Currency Trading (Forex) Fraud Advisory, which states that the CFTC has witnessed a sharp rise in Forex trading
scams in recent years and helps customers identify this potential fraud.

The CFTC has also issued a Commodity Pool Fraud Advisory, which warns customers about a type of fraud that involves
individuals and firms, often unregistered, offering investments in commodity pools.

Customers can report suspicious activities or information, such as possible violations of commodity trading laws, to the
CFTC Division of Enforcement via a Toll-Free Hotline 866-FON-CFTC (866-366-2382) or file a tip or complaint online.
Media Contact
Dennis Holden
202-418-5088

Last Updated: January 12, 2015"""

        return txt


def order() : 
    """ """

    try : 
        with open("./data/boot/order.txt") as f : 
            return f.read()
        with open("./app/data/boot/order.txt") as f : 
            return f.read()
    except Exception as e : 

        txt =   """UNITED STATES DISTRICT COURT
MIDDLE DISTRICT OF FLORIDA
Jacksonville Division

U.S. COMMODITY FUTURES
TRADING COMMISSION,
Plaintiff,
v. Case No. 3:15-cv-5-J-34MCR
ALLIED MARKETS LLC,
JOSHUA GILLILAND, and
CHAWALIT WONGKHIAOQO,

Defendants.

 

 

 

ORDER GRANTING PLAINTIFF’S EX PARTE
MOTION FOR STATUTORY RESTRAINING ORDER AND SCHEDULING
PRELIMINARY INJUNCTION HEARING

THIS CAUSE is before the Court on Plaintiff's Ex Parte Motion for Statutory
Restraining Order and Motion for Preliminary Injunction (Doc. S-4; Motion), filed on
January 5, 2015. Simultaneously with the Motion, the United States Commodity Futures
Trading Commission (Plaintiff or CFTC) filed a Complaint for Injunctive Relief, Civil
Monetary Penalty, and Other Equitable Relief (Doc. S-3) against Defendants Allied Markets
LLC, Joshua Gilliland, and Chawalit Wongkhiao (collectively, Defendants). In the Motion,
the CFTC moves, pursuant to Section 6c(a) of the Commodity Exchange Act (CEA), 7
U.S.C. § 13a-1(a) (2012), for an ex parte statutory restraining order freezing assets and
prohibiting the destruction of books, records, or other documents; and for an order requiring

Defendants to show cause why a preliminary injunction should not issue.
 

 

 

The Court has considered the pleadings, declarations, exhibits, and memorandum
filed in support of the CFTC’s Motion, and now, being fully advised, finds as follows:

l. The Court possesses jurisdiction over the parties and over the subject matter
of this action pursuant to Section 6c of the CEA, 7 U.S.C. § 13a-1 (2012).

om Venue properly lies in this District, pursuant to Section 6c(e) of the CEA,
7 U.S.C. § 13a-1(e) (2012).

as There is good cause to believe that Defendant Allied Markets LLC (“Allied
Markets”), by and through its agents, principals and control persons, Defendants Joshua
Gilliland and Chawalit Wongkhiao have engaged in, are engaging in, and may continue to
engage in violations of Sections 2(c)(2)(C)Gii)(D(cc), 4b(a)(2)(A) and (C), 4k(2), 4m(1), and
40(1) of the CEA, 7 U.S.C. §§ 2(c)(2)(C)Gu)(D(cc), 6b(a)(2)(A), (C), 6k(2), 6m(1), 60(1)
(2012); and CFTC Regulations 3.12, 4.20(a)-(c), 4.41(a), 5.2(b)(1) and (3), 5.3(a)(2)@), and
5.3(a)(2)(ii), 17 C.F.R. §§ 3.12, 4.20(a)-(c), 4.41 (a), 5.2(b)(1), (3), 5.3(a)(2)G), (41) (2014).

4, The CFTC has presented evidence that, since at least January 2012,
Defendants fraudulently solicited more than $1 million from members of the public to
participate in a supposed commodity pool purportedly trading leveraged or margined retail
off-exchange foreign currency contracts, commonly known as “forex.” The CFTC has also
presented evidence that Defendants misappropriated pool participants’ funds to pay
Defendants Gilliland’s and Wongkhiao’s personal expenses. Additionally, the CFTC has
presented evidence that Defendants failed to register with the CFTC as required, failed to

segregate customer funds, and failed to operate the commodity pool as a separate entity, and
 

 

failed to accurately report or disclose the performance of the relevant investments, as
required by the CEA and CFTC Regulations.

» There is good cause to believe that immediate and irreparable damage to the
Court’s ability to grant effective final relief in the form of monetary redress will occur from
the sale, transfer, assignment, or other disposition by Defendants of assets or records unless
Defendants are immediately restrained and enjoined by order of this Court;

6. There is good cause for entry of an order freezing assets owned, controlled,
managed, or held by or on behalf of, or for the benefit of, Defendants.

7: There is good cause for entry of an order prohibiting Defendants, their agents,
servants, employees, assigns, attorneys, and persons in active concert or participation with
Defendants, including any successor thereof, from destroying records and/or denying agents
of the CFTC immediate and complete access to Defendants’ books and records for inspection
and copying.

8. Absent the entry of this order, Defendants would have the ability to dissipate
or transfer assets and destroy books and records.

9. An ex parte statutory restraining order is warranted here to preserve the status
quo, protect customers from loss and damage, and enable the CFTC to fulfill its statutory
duties.

Accordingly, it is ORDERED:

10. ‘Plaintiff's Ex Parte Motion for Statutory Restraining Order and Motion for
Preliminary Injunction (Doc. S-4) is GRANTED, in part, and TAKEN UNDER

ADVISEMENT, in part.
A. To the extent the CFTC requests an ex parte statutory restraining order,
the Motion is GRANTED as set forth below.
B. To the extent the CFTC requests the entry of a preliminary injunction, the
Motion is TAKEN UNDER ADVISEMENT.
RELIEF GRANTED

I. ASSET! FREEZE

IT IS HEREBY ORDERED that:

11. Defendants? and their agents, servants, employees, assigns, attorneys,
including any successor thereof, and persons in active concert or participation with them,
who receive actual notice of this Order by personal service or otherwise, are immediately
restrained and enjoined from directly or indirectly transferring, selling, alienating,
liquidating, encumbering, pledging, leasing, loaning, assigning, concealing, dissipating,
converting, withdrawing, or otherwise disposing of any assets, wherever located, including

Defendants’ assets held outside the United States, except as otherwise ordered by the Court.

 

' For the purposes of this Order, the term “Assets” means any legal or equitable interest in, right to, or
claim to, any real or personal property, whether individually or jointly, directly or indirectly controlled, and
wherever located, including, but not limited to: chattels, goods, instruments, equipment, fixtures, general
intangibles, effects, leaseholds mail or other deliveries, inventory, checks, notes, accounts (including, but not
limited to, bank accounts and accounts at other financial institutions), credits, receivables, lines of credit,
contracts (including spot, futures, options, or swaps contracts), insurance policies, and all cash, wherever
located, whether within or outside the United States.

2 For purposes of this Order, the term “Defendants” refers to Allied Markets LLC, Joshua Gilliland,
and Chawalit Wongkhiao, and any person insofar as he or she is acting in the capacity of an officer, agent
servant, employee, or attorney of Defendants and any person who receives actual notice of this Order by
personal service or otherwise insofar as he or she is acting in concert or participation with Defendants.
“Defendants” also refers to any d/b/a, successor, affiliate, subsidiary, or other entity owned, controlled,
managed, or held by, on behalf of, or for the benefit of Allied Markets, Joshua Gilliland, or Chawalit
Wongkhiao.
 

12; This Order shall apply to any assets derived from or otherwise related to the
activities alleged in the CFTC’s complaint, regardless of when the asset is obtained.
However, the assets affected by this Order shall not include assets obtained after the effective
date of this Order, to the extent such assets are not derived from or otherwise related to the
activities alleged in the CFTC’s complaint.

Il. NOTICE TO FINANCIAL INSTUTIONS AND OTHERS

[3. Any financial or brokerage institution, business entity, or person that holds,
controls, or maintains custody of any account or asset titled in the name of, held for the
benefit of, or otherwise under the control of any Defendant, or has held, controlled, or
maintained custody of any such account or asset of any Defendant at any time since January
1, 2012 are hereby notified that this Order prohibits any Defendant and all other persons from
withdrawing, removing, assigning, transferring, pledging, encumbering, disbursing,
dissipating, converting, selling or otherwise disposing of Defendants’ assets, except as
directed by further order of the Court; provided, however, nothing in this Order shall limit the
discretion of any compliance official of any retail foreign exchange dealer or futures
commission merchant with which Defendants maintain an account to liquidate, or close out,
any and all open positions in Defendants’ account, in a prompt and orderly fashion in order
to avoid losses due to the asset freeze required by this Order.

Il. MAINTENANCE OF AND ACCESS TO BUSINESS RECORDS

IT IS FURTHER ORDERED that:
14. Defendants and all persons or entities who receive notice of this Order by

personal service or otherwise, are restrained from directly or indirectly destroying,
mutilating, erasing, altering, concealing or disposing of, in any manner, directly or indirectly,
any documents? that relate to the business practices or business or personal finances of any
Defendant.

IV. BOND NOT REQUIRED OF PLAINTIFF
IT IS FURTHER ORDERED that:

Ibs Because Plaintiff CFTC is an agency of the United States of America and has
made a proper showing under Section 6c(b) of the CEA, 7 U.S.C. § 13a-1(b) (2012), this
restraining order is granted without bond.

V. INSPECTION AND COPYING OF BOOKS AND RECORDS
IT IS FURTHER ORDERED that:

16. Defendants shall immediately allow representatives of the CFTC to inspect
the books, records, and other documents of Defendants and their agents including, but not
limited to, paper documents, electronically stored information, tape recordings, and computer
discs, wherever they may be situated and whether they are in the possession of Defendants or
others, and to copy said documents, data and records, either on or off the premises where
they may be situated.

VI. SERVICE OF ORDER AND ASSISTANCE OF UNITED STATES
MARSHALS SERVICE

IT IS FURTHER ORDERED that:
17. Copies of this Order may be served by any means, including facsimile

transmission, upon any financial institution or other entity or person that may have

 

3 For purposes of this Order, the term “document” is synonymous in meaning and equal in scope to the broad
usage of the term in Federal Rule of Civil Procedure 34(a).
 

possession, custody, or control of any documents or assets of any Defendant, or that may be
subject to any provision of this Order.

18. Representatives of the CFTC, the United States Marshals Service, the Florida
Office of Financial Regulation, and the police departments of Jacksonville and Jacksonville
Beach, Florida are specially appointed by the Court to effect service of this Order.

19, The United States Marshals Service, the Florida Office of Financial
Regulation, and the police departments of Jacksonville and Jacksonville Beach, Florida, in
order to ensure the safety of CFTC representatives, are authorized to accompany and assist
the CFTC in the service on Defendants of the summons, complaint, and supporting motions,
memoranda, and orders entered with this Order.

20. The CFTC shall immediately file proof of service with the Court once
accomplished.

VII. PRELIMINARY INJUNCTION HEARING

IT IS FURTHER ORDERED that:

21, This matter is set for a HEARING on Plaintiff's Motion for Preliminary
Injunction (Doc. S-4) on Wednesday, January 21, 2015, at 10:00 a.m., before the
undersigned at the Bryan Simpson United States Courthouse, 300 North Hogan Street,
Jacksonville, Florida, 32202, in Courtroom 10B. Counsel for Plaintiff and Defendants shall

appear in person and telephonic appearances will not be permitted.’

 

* All persons entering the Courthouse must present photo identification to Court Security Officers. Although
cell phones, laptop computers, and similar electronic devices generally are not permitted in the building,
attorneys may bring those items with them upon presentation to Court Security Officers of a Florida Bar card
(presentation of the Duval County Courthouse lawyer identification card will suffice) or Order of special
admission pro hac vice. However, all cell phones must be turned off while in the courtroom.
 

22. The following expedited briefing schedule shall govern this case:

A. Defendants shall have up to and including 5:00 p.m. on Thursday,

January 15, 2015, to file a memorandum in opposition to Plaintiffs Motion for

Preliminary Injunction (Doc. S-4), including any affidavits or declarations on which

they rely.

B. Plaintiff shall have up to and including 11:00 a.m. on Tuesday,

January 20, 2015, to file a reply, if mecessary, in support of its Motion for

Preliminary Injunction, which shall not exceed TEN (10) PAGES in length.

23, The hearing will be conducted in accordance with Local Rule 4.06, United
States District Court, Middle District of Florida, and Rule 65, Federal Rules of Civil
Procedure. The case does not appear to involve the exceptional situation wherein the Court
will allow the parties to submit evidence at the hearing. See Local Rule 4.06(b). Thus,
absent further order,’ the hearing will be limited to the written submissions and arguments of
counsel.

24. In issuing this Statutory Restraining Order, the Court understands that
Defendants have not yet been given an opportunity to be heard and emphasizes that it is not
making a final decision on any request for preliminary injunctive relief. However, the Court
is persuaded that issuing the Statutory Restraining Order until a full hearing can be held on

the CFTC’s request for preliminary injunctive relief is the lawful and proper action.

 

> McDonald’s Corp. v. Robertson, 147 F.3d 1301, 1312-13 (11th Cir. 1998) (“[W]here facts are bitterly
contested and credibility determinations must be made to decide whether injunctive relief should issue, an
evidentiary hearing must be held... . [W]here material facts are not in dispute, or where facts in dispute are not
material to the preliminary injunction sought, district courts need not hold an evidentiary hearing.”) In the
event either party believes such a hearing is warranted in this action, the party must, after conferring with
opposing counsel, file a motion requesting an evidentiary hearing and identifying the factual issues or dispute
which necessitate such relief,
 

Vill. FORCE AND EFFECT

IT IS FURTHER ORDERED that:
25. Unless earlier dissolved or extended by Order of the Court, the Statutory
Restraining Order granted herein shall expire at midnight on January 21, 2015.

IT IS SO ORDERED at Jacksonville, Florida on this 7th day of January, 2015, at

AO@.m.

aed

UNITED STATES DISTRICT JUDGE"""

        return txt

class Boot:
    """ """

    press_release = press_release()
    order = order()

    def boot() : 
        """boot module """ 

        nlpipe = get_pipeline()
        nlspa =  get_spacy()

        obj = PressRelease(text=press_release(), source="cftc",nlpipe=nlpipe, nlspa=nlspa)
        obj.predict_all()
        
        return obj
