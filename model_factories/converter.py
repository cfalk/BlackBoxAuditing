import time
import csv

def expand_to_one_hot_general(data,cat_list):
    cat_columns = [val for val in range(len(data[0])) if type(data[0][val])==str]
    """
    cat_list = []
    for col in range(len(data[0])):
	cat_list.append([])
	if col in cat_columns: 
	    for row in data:
		if not row[col] in cat_list[col]:
		    cat_list[col].append(row[col])
    """

    new_data = []
    for entry in data:
	temp = []
	for j,val in enumerate(entry):
	    if not j in cat_columns:
		temp.append(val)
	    else:
		for cat in cat_list[j]:
		    if val == cat:
			temp.append(1)
		    else:
			temp.append(0)
	new_data.append(temp)

    return new_data
		
def test():
    data = [['hello','there','my'],['name','is','brandon']]
    print expand_to_one_hot_general(data)

def expand_to_one_hot(data,expand = True,use_alternative=False):
    header_dict = {'ALCABUS':0,'PRIRCAT':1,'TMSRVC':2,'SEX1':3,'RACE':4,'RELTYP':5,'age_1st_arrest':6,'DRUGAB':7,'Class':8,'RLAGE':9,'NFRCTNS':10}

    new_data = []
    for entry in data:
	temp = {}
	if expand == True:
	    if entry[header_dict["SEX1"]] == "FEMALE":
		temp['female'] = 1
	    else:
		temp['female'] = 0

	    if entry[header_dict["ALCABUS"]] == 'INMATE IS AN ALCOHOL ABUSER':
		temp['prior_alcohol_abuse'] = 1
	    else:
		temp['prior_alcohol_abuse'] = 0

	    if entry[header_dict['DRUGAB']] == 'INMATE IS A DRUG ABUSER':
		temp['prior_drug_abuse'] = 1
	    else:
		temp['prior_drug_abuse'] = 0

	    if entry[header_dict['NFRCTNS']] == 'INMATE HAS RECORD':
		temp['infraction_in_prison'] = 1
	    else:
		temp['infraction_in_prison'] = 0
    
	    race_cats = ['WHITE','BLACK','AMERICAN INDIAN/ALEUTIAN','ASIAN/PACIFIC ISLANDER','OTHER','UNKNOWN']

	    for cat in race_cats:
		if entry[header_dict['RACE']] == cat:
		    temp['race_'+cat] = 1
		else:
		    temp['race_'+cat] = 0

	    release_age_cats = ['14 TO 17 YEARS OLD','18 TO 24 YEARS OLD', '25 TO 29 YEARS OLD', \
	    '30 TO 34 YEARS OLD','35 TO 39 YEARS OLD','40 TO 44 YEARS OLD','45 YEARS OLD AND OLDER']
	    for cat in release_age_cats:
		if entry[header_dict['RLAGE']] == cat:
		    temp['release_age_'+cat] = 1
		else:
		    temp['release_age_'+cat] = 0
    
	    time_served_cats = ['None','1 TO 6 MONTHS','13 TO 18 MONTHS','19 TO 24 MONTHS','25 TO 30 MONTHS', \
			'31 TO 36 MONTHS','37 TO 60 MONTHS','61 MONTHS AND HIGHER','7 TO 12 MONTHS']
	    for cat in time_served_cats:
		if entry[header_dict['TMSRVC']] == cat:
		    temp['time_served_'+cat] = 1
		else:
		    temp['time_served_'+cat] = 0

	    prior_arrest_cats = ['None','1 PRIOR ARREST','11 TO 15 PRIOR ARRESTS','16 TO HI PRIOR ARRESTS','2 PRIOR ARRESTS', \
		'3 PRIOR ARRESTS','4 PRIOR ARRESTS','5 PRIOR ARRESTS','6 PRIOR ARRESTS','7 TO 10 PRIOR ARRESTS']
	    for cat in prior_arrest_cats:
		if entry[header_dict['PRIRCAT']] == cat:
		    temp['prior_arrest_'+cat] = 1
		else:
		    temp['prior_arrest_'+cat] = 0

	    conditional_release =['PAROLE BOARD DECISION-SERVED NO MINIMUM','MANDATORY PAROLE RELEASE', 'PROBATION RELEASE-SHOCK PROBATION', \
			'OTHER CONDITIONAL RELEASE']
	    unconditional_release = ['EXPIRATION OF SENTENCE','COMMUTATION-PARDON','RELEASE TO CUSTODY, DETAINER, OR WARRANT', \
			'OTHER UNCONDITIONAL RELEASE']
	    other_release = ['NATURAL CAUSES','SUICIDE','HOMICIDE BY ANOTHER INMATE','OTHER HOMICIDE','EXECUTION','OTHER TYPE OF DEATH', \
		    'TRANSFER','RELEASE ON APPEAL OR BOND','OTHER TYPE OF RELEASE','ESCAPE','ACCIDENTAL INJURY TO SELF','UNKNOWN']
	    if entry[header_dict['RELTYP']] in conditional_release:
		temp['released_conditional'] = 1
		temp['released_unconditional'] = 0
		temp['released_other'] = 0
	    elif entry[header_dict['RELTYP']] in unconditional_release:
		temp['released_conditional'] = 0
		temp['released_unconditional'] = 1
		temp['released_other'] = 0
	    else:
		temp['released_conditional'] = 0
		temp['released_unconditional'] = 0
		temp['released_other'] = 1
	    
	    first_arrest_cats = ['UNDER 17','BETWEEN 18 AND 24','BETWEEN 25 AND 29','BETWEEN 30 AND 39','OVER 40']
	    for cat in first_arrest_cats:
		if entry[header_dict['age_1st_arrest']] == cat:
		    temp['age_first_arrest_'+cat] = 1
		else:
		    temp['age_first_arrest_'+cat] = 0
	else:
	    temp['SEX1'] = entry['SEX1']
	    temp['RELTYP'] = entry['RELTYP']
	    temp['PRIRCAT'] = entry['PRIRCAT']
	    temp['ALCABUS'] = entry['ALCABUS']
	    temp['DRUGAB'] = entry['DRUGAB']
	    temp['RLAGE'] = entry['RLAGE']
	    temp['TMSRVC'] = entry['TMSRVC']
	    temp['NFRCTNS'] = entry['NFRCTNS']
	    temp['RACE'] = entry['RACE']
	    try:
		bdate = datetime.date(int(entry['YEAROB2']),int(entry['MNTHOB2']), int(entry['DAYOB2']))
		first_arrest = datetime.date(int(entry['A001YR']),int(entry['A001MO']),int(entry['A001DA']))
		first_arrest_age = first_arrest - bdate
		temp['age_1st_arrest'] = first_arrest_age.days
	    except:
		temp['age_1st_arrest'] = 0
    
	new_data.append(temp)


    # convert from dictionary to list of lists
    fin = [[int(entry[key]) for key in entry.keys()] for entry in new_data]
    """
    with open("brandon_testing/test_"+str(time.clock())+".csv","w") as f:
	writer = csv.writer(f,delimiter=",")
	for row in fin:
	    writer.writerow(row)
    """

    return fin