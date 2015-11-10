Scripts and Datasource **************************************************************

<afl-cio.py>
AFL-CIO http://www.aflcio.org/Legislation-and-Politics

<acu.py>
American Conservative Union, http://acuratings.conservative.org

<cc.py>
Chamber of Commerce, https://www.uschamber.com/report/how-they-voted

Usage **************************************************************

python <scripts> [-o] <output_filename> [-y] <year1,year2,...,yearN>

Example:
To scrape votes that ACU are interested in in year 2012 and 2013, and store in out.txt:
$ python acu.py -o out.txt -y 2012,2013

Sample output **************************************************************

		========= ACU Result of year 2012 ========= 

('h71-112.2012        ', datetime.date(2012, 2, 16), 'Protecting Investment in Oil Shale the Next Generation of Environmental, Energy, and Resource Security Act')
{'vote_date' : '2012-02-16'
'vote_number' : '71'
'vote_description' : 'The House passed a bill that would open up a small portion
of the Alaska National Wildlife Refuge (ANWR), approve the
Keystone XL oil pipeline from Canada blocked by the Obama
Administration, and shift permitting authority for the project
from the State Department to the Federal Energy Regulatory
Commission. ACU supports increased domestic energy
production and supported this bill. The bill passed the House
on February 16, 2012, by a vote of 237-187.'
'vote_title' : 'Domestic Energy Production. H.R. 3408 (Roll Call 71)'}

('h149-112.2012       ', datetime.date(2012, 3, 29), None)
{'vote_date' : '2012-03-29'
'vote_number' : '149'
'vote_description' : 'The House defeated a conservative alternative to the budget
that would freeze total discretionary spending to slightly
below 2008 levels beginning in 2013 and would balance the
budget within five years. The bill would overhaul the tax code
to give taxpayers the choice between the current system or
one with two tax brackets, cut the corporate tax rate from 35
to 25 percent, and eliminate the Death Tax. The bill would
also move to make Medicare solvent by creating a premium
support system and converting Medicaid spending into block
grants to the states. It also calls for the gradual increase in
the retirement age for Medicare and Social Security. ACU
supported this alternative as a reasonable attempt to eliminate
our trillion-dollar annual deficit. The amendment failed on
March 29, 2012, by a vote of 136-285.'
'vote_title' : 'Conservative Budget. H. Con. Res. 112 (Roll Call 149)'}

('h164-112.2012       ', datetime.date(2012, 4, 17), 'Sportsmen’s Heritage Act of 2012')
{'vote_date' : '2012-04-17'
'vote_number' : '164'
'vote_description' : 'The House passed a bill that requires federal officials to
facilitate the use of and access to federal lands for the purpose
of recreational shooting and hunting. The bill also prohibits a
national monument designation by presidential proclamation
from being valid until each affected state approves the designation.
ACU supports this expansion of Second Amendment
rights and reasonable limits on presidential power and supported
this bill. The bill passed the House on April 17, 2012,
by a vote of 274-146.'
'vote_title' : 'Federal Land Management. H.R. 4089 (Roll Call 164)'}

('h207-112.2012       ', datetime.date(2012, 5, 8), None)
{'vote_date' : '2012-05-08'
'vote_number' : '207'
'vote_description' : 'The House defeated the Pompeo amendment to the Commerce,
Justice, State Appropriations bill that would eliminate
the Economic Development Administration. ACU has long
opposed this agency that uses taxpayer money to pick winners
and losers among local projects across the country and supported
this amendment. The House defeated this amendment
on May 8, 2012, by a vote of 129-279.'
'vote_title' : 'Wasteful Spending. H.R. 5326 (Roll Call 207)'}

('h215-112.2012       ', datetime.date(2012, 5, 8), None)
{'vote_date' : '2012-05-08'
'vote_number' : '215'
'vote_description' : 'The House defeated the Huizenga amendment to the Commerce,
Justice, State Appropriations bill that would have
removed language from the bill prohibiting public-private
sector competition within the Bureau of Prisons and Federal
Prison Industries. ACU supports increased opportunities for
the private sector to compete with government programs and
supported this amendment. The amendment was defeated on
May 8, 2012, by a vote of 199-211.'
'vote_title' : 'Government Reform. H.R. 5326 (Roll Call 215)'}

('h219-112.2012       ', datetime.date(2012, 5, 9), None)
{'vote_date' : '2012-05-09'
'vote_number' : '219'
'vote_description' : 'The House defeated the Austin Scott amendment to the
Commerce, Justice, State Appropriations Bill that would have
killed all funding for the Legal Services Corporation. ACU
has long opposed this wasteful program used primarily to expand
the welfare state and that a GAO study found to be rife
with waste, fraud and abuse. ACU supported this amendment
which was defeated on May 9, 2012, by a vote of 122-289.'
'vote_title' : 'Wasteful Spending. H.R. 5326 (Roll Call 219)'}

('h228-112.2012       ', datetime.date(2012, 5, 9), None)
{'vote_date' : '2012-05-09'
'vote_number' : '228'
'vote_description' : 'The House passed the Blackburn amendment to the Commerce,
State, Justice Appropriations Bill that bars the use of
taxpayer funds to defend any action challenging a provision of
the Health Care Overhaul bill passed in 2010. ACU opposed
that government takeover of our healthcare system and supported
this amendment. The House passed the amendment
on May 9, 2012, by a vote of 229-194.'
'vote_title' : 'Healthcare Litigation. H.R. 5326 (Roll Call 228)'}

('h235-112.2012       ', datetime.date(2012, 5, 9), None)
{'vote_date' : '2012-05-09'
'vote_number' : '235'
'vote_description' : 'The House passed the Huelskamp amendment to the Commerce,
State, Justice Appropriations bill that would bar the
use of funds for activities that would violate the Defense of
Marriage Act of 1996. That act defined marriage as the union
of one man and woman. ACU supports traditional marriage
and supported this amendment. The amendment passed on
May 9, 2012, by a vote of 245-171.'
'vote_title' : 'Traditional Marriage. H.R. 5326 (Roll Call 235)'}

('h243-112.2012       ', datetime.date(2012, 5, 9), None)
{'vote_date' : '2012-05-09'
'vote_number' : '243'
'vote_description' : 'The House passed the Flake amendment to the Commerce,
State, Justice Appropriations bill that would have prohibited
the National Science Foundation from using taxpayer dollars
to fund political science research. ACU opposes these frivolous
programs that give grants to wealthy universities at a time
of trillion-dollar-a-year deficits and supported this amendment.
The House passed the amendment on May 9, 2012, by
a vote of 218-208.'
'vote_title' : 'Science Funding. H.R. 5326 (Roll Call 243)'}

('h264-112.2012       ', datetime.date(2012, 5, 17), None)
{'vote_date' : '2012-05-17'
'vote_number' : '264'
'vote_description' : 'The House defeated the Lee amendment to the Defense
Authorization bill that would bar defense funds from being
used for any purpose in Afghanistan other than withdrawing
troops. ACU opposes this type of precipitous withdrawal and
opposed this amendment. The amendment was defeated on
May 17, 2012, by a vote of 113-303.'
'vote_title' : 'Defense Spending. H.R. 4310 (Roll Call 264)'}

('h266-112.2012       ', datetime.date(2012, 5, 17), None)
{'vote_date' : '2012-05-17'
'vote_number' : '266'
'vote_description' : 'The House passed the Rooney amendment to the Defense
Authorization bill that directs the Defense Department to hold
trials of suspected terrorists by military tribunals at Guantanamo
Bay rather than by civilian courts in the United States. ACU
opposes treating terrorists as common criminals and supported
this amendment. The amendment passed the House on May 17,
2012, by a vote of 249-171.'
'vote_title' : 'Terrorist Trials. H.R. 4310 (Roll Call 266)'}

('h269-112.2012       ', datetime.date(2012, 5, 17), None)
{'vote_date' : '2012-05-17'
'vote_number' : '269'
'vote_description' : 'The House defeated the Polis amendment to the Defense
Authorization bill that would have cut $400 million from the
missile defense program. ACU supports a strong missile defense
system for the United States and opposed this amendment. The
House defeated the amendment on May 17, 2012, by a vote of
165-252.'
'vote_title' : 'Missile Defense. H.R. 4310 (Roll Call 269)'}

('h272-112.2012       ', datetime.date(2012, 5, 18), None)
{'vote_date' : '2012-05-18'
'vote_number' : '272'
'vote_description' : 'The House defeated the Coffman amendment to the Defense
Authorization bill that would have repealed the prohibition
against private-public competition for certain Defense Department
functions. ACU supports expanding private-sector opportunities
in the government and supported this amendment.
The House defeated the amendment on May 18, 2012, by a vote
of 209-211.'
'vote_title' : 'Government Reform. H.R. 4310 (Roll Call 272)'}

('h299-112.2012       ', datetime.date(2012, 5, 31), 'Prenatal Non-discrimination Act (PRENDA) of 2012')
{'vote_date' : '2012-05-31'
'vote_number' : '299'
'vote_description' : 'The House failed to pass a bill to ban abortions based on the
sex of the fetus. It would have imposed fines and a possible jail
sentence on those who knowingly perform such abortions. ACU
supports restrictions on abortions and supported this bill. The
House voted in favor of the bill on May 31, 2012 by a vote of
246-168, but the vote did not meet the two-thirds vote requirement
under the fast-track procedure used.'
'vote_title' : 'Sex-Selection Abortion. H.R. 3541 (Roll Call 299)'}

('h302-112.2012       ', datetime.date(2012, 5, 31), None)
{'vote_date' : '2012-05-31'
'vote_number' : '302'
'vote_description' : 'The House passed the Grimm amendment to the Military Construction
and Veterans Administration Appropriations bill that
eliminates language prohibiting federal government construction
contracts from requiring project labor agreements that force
companies that seek government contracts to agree to union
demands. ACU opposes Project Labor Agreements and opposed
this amendment. The House passed the amendment on May 31,
2012, by a vote of 218-198.'
'vote_title' : 'Project Labor Agreements. H.R. 5854 (Roll Call 302)'}

('h309-112.2012       ', datetime.date(2012, 6, 1), None)
{'vote_date' : '2012-06-01'
'vote_number' : '309'
'vote_description' : 'The House defeated the Hultgren amendment to the Energy
and Water Appropriations bill that would have reduced increases
in funding for renewable energy projects and applied the funds
to basic scientific research and deficit reduction. ACU opposes
increased funding for industrial policy programs that shortchange
basic science and supported this amendment. The House
defeated the amendment on June 1, 2012 by a vote of 130-256.'
'vote_title' : 'Science Funding. H.R. 5325 (Roll Call 309)'}

('h338-112.2012       ', datetime.date(2012, 6, 6), None)
{'vote_date' : '2012-06-06'
'vote_number' : '338'
'vote_description' : 'The House defeated the King amendment to the Energy and
Water Appropriations bill that would have barred the use
of funds to enforce the Davis-Bacon Act. That act requires
federal projects to pay workers the “prevailing” wage, usually
union wage rates well above the local market rate. This
requirement adds billions of dollars to the cost of federal
projects. ACU opposes this federal mandate and supported
this amendment. The House defeated the amendment on
June 6, 2012, by a vote of 184-235.'
'vote_title' : 'Davis-Bacon Wage Rate Requirements. H.R. 5325 (Roll Call 338)'}

('h385-112.2012       ', datetime.date(2012, 6, 19), None)
{'vote_date' : '2012-06-19'
'vote_number' : '385'
'vote_description' : 'The House defeated the Grijalva amendment to the Conservation
and Economic Growth Act. The amendment would
have eliminated language in the Conservation and Economic
Growth Act that exempts border security programs from
those environmental and land use laws that block enforcement.
ACU supports strengthened border security and opposed
this amendment. The House defeated the amendment
on June 19, 2012, by a vote of 177-247.'
'vote_title' : 'Border Security. H.R. 2578 (Roll Call 385)'}

('h417-112.2012       ', datetime.date(2012, 6, 26), None)
{'vote_date' : '2012-06-26'
'vote_number' : '417'
'vote_description' : 'The House defeated the McClintock amendment to the
Transportation and Housing and Urban Development Appropriations
bill that would have eliminated a $200 million
program that subsidizes air service to rural airports with little
passenger traffic. ACU opposes this wasteful spending that
distorts the free market and supported this amendment. The
House defeated the amendment on June 26, 2012, by a vote
of 164-238.'
'vote_title' : 'Air Service Subsidies. H.R. 5972 (Roll Call 417)'}

{'vote_date' : '2013-06-27'
'vote_number' : '434'
'vote_description' : 'The House defeated the McClintock amendment to the
Transportation and Housing and Urban Development Appropriations
bill that would have eliminated funding for the
$3.4 billion Community Development Block Grant program.
This program, unauthorized since 1994, has been used primarily
as a federal slush fund for pet projects of local politicians.
HUD’s own Inspector General has found this program
rife with waste, fraud and abuse. ACU has long opposed this
type of wasteful spending and supported this amendment.
The House defeated the amendment on June 27, 2013 by a
vote of 80-342.'
'vote_title' : 'Community Development Block Grants. H.R. 5972 (Roll Call 434)'}

('h460-112.2012       ', datetime.date(2012, 7, 11), 'To repeal the Patient Protection and Affordable Care Act and health care-related provisions in the Health Care and Education Reconciliation Act 2010')
{'vote_date' : '2012-07-11'
'vote_number' : '460'
'vote_description' : 'The House passed this bill that would repeal the 2010 health
care overhaul law that requires most people to purchase
government-approved health insurance and gives the Secretary
of Health and Human Services control over many aspects of
the health care system. ACU strongly opposes the federal government
takeover of health care and supported this bill. The
House passed the bill on July 11, 2012, by a vote of 244-185.'
'vote_title' : 'Health Care. H.R. 6079 (Roll Call 460)'}

('h511-112.2012       ', datetime.date(2012, 7, 25), 'Congressional Replacement of President Obama’s Energy-Restricting and Job-Limiting Offshore Drilling Plan')
{'vote_date' : '2012-07-25'
'vote_number' : '511'
'vote_description' : 'The House passed this bill that would replace the Interior
Department’s current offshore oil and gas drilling plan with
a timeline to nearly double the current number of leases and
restore the 2009 leasing plan blocked by the Obama Administration.
ACU supports increased domestic energy production
and supported this bill. The House passed the bill on July 25,
2012, by a vote of 253-170.'
'vote_title' : 'Domestic Energy Production. H.R. 6082 (Roll Call 511)'}

('h582-112.2012       ', datetime.date(2012, 9, 14), None)
{'vote_date' : '2012-09-14'
'vote_number' : '582'
'vote_description' : 'The House defeated the Waxman amendment to the “No
More Solyndras” bill that would have eliminated provisions
in the bill that end the loan guarantee program for energy
projects that led to the Solyndra scandal. ACU opposes this
program and opposed this amendment that would have gutted
the bill. The House defeated the amendment on September
14, 2012, by a vote of 170-241.'
'vote_title' : 'Energy Project Loan Guarantees. HR 6213 (Roll Call 582)'}

('h589-112.2012       ', datetime.date(2012, 9, 20), 'Providing for congressional disapproval of the rule submitted by the Office of Family Assistance of the Administration for Children and Families of the Department of HHS relating to waiver and expenditure authority under the Social Security Act with respect to the Temporary Assistance for Needy Families program')
{'vote_date' : '2012-09-20'
'vote_number' : '589'
'vote_description' : 'The House passed a resolution of disapproval of a ruling by
the Health and Human Services Department that guts the
work requirements in the welfare reform legislation passed
in 1996. ACU opposes efforts to weaken welfare reform and
supported this resolution. The House passed the resolution on
September 20, 2012, by a vote of 250-164.'
'vote_title' : 'Welfare Reform. H.J. Res 118 (Roll Call 589)'}

('h603-112.2012       ', datetime.date(2012, 9, 21), 'To limit the authority of the Secretary of the Interior to issue regulations before December 31, 2013, under the Surface Mining Control and Reclamation Act of 1977')
{'vote_date' : '2012-09-21'
'vote_number' : '603'
'vote_description' : 'The House passed a bill that would bar the EPA from issuing
regulations on greenhouse gas emissions in the name of
global warming and transferring authority from the EPA to
the states on issues regarding water quality standards. ACU
opposes EPA’s attempt to use the issue of global warming to
control American manufacturing and supported this bill. The
bill passed the House on September 21, 2012, by a vote of
233-175.'
'vote_title' : 'Climate Change Regulations. HR 3409 (Roll Call 603)'}


