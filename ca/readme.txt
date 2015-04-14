California Campaign Disclosure files:

Location:
http://www.sos.ca.gov/campaign-lobbying/cal-access-resources/raw-data-campaign-finance-and-lobbying-activity/

Download: http://campaignfinance.cdn.sos.ca.gov/dbwebexport.zip
  - Contains all the guides plus the data
  - Data is in the CalAccess/DATA directory

Notes:
 - Data seems to be renormalized, with id/name/address information for many entities (FILER, CANDIDATE) repeated in many tables


Main File for People/Organization: CVR_CAMPAIGN_DISCLOSURE_CD.TSV
 - "Cover page information for the campaign disclosure forms"
 - Filers: FILER_* fields: Names: FILER_NAML (organization or last name if individual), FILER_NAMF (first name if applicable), 
   FILER_NAMT (prefix or title individual), FILER_NAMS (suffix if individual), FILER_CITY, FILER_ST, FILER_ZIP4, FILER_PHON, 
   FILER_FAX, FILE_EMAIL, MAIL_CITY, MAIL_ST, MAIL_ZIP4
 - Candidates: CAND_NAML, CAND_NAMF, CAND_NAMT, CAND_NAMS, CAND_CITY, CAND_ST, CAND_ZIP4, CAND_PHON, CAND_FAX, CAND_EMAIL
 - While there are BAL_NAME and BAL_NUM fields, they do not seem to have an actual balance amount 


Receipts: RCPT_CD.TSV matching FILING_ID from CVR_CAMPAIGN_DISCLOSURE_CD.TSV 
 - "Receipts schedules for the Form 460 Schedules A, C, I, and A-1 and the Form 401 Schedule A."
 - Amount fields: 'FILING_ID','LINE_ITEM', 'AMOUNT', 'CUM_YTD', 'CUM_OTH'
 - NOT unique across FILING_ID/LINE_ITEM (don't know if this is duplicate or if another field required to make unique)
