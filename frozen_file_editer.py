# -*- coding: utf8 -*-
# this is a general tool for manipulating one or more csv files to match the
# structure of another csv frozen file

# import packages
import os
import csv
import re

# set working directory for reading in and writing out files
#path_dir = "C:\Users\johnsonbriand01\Desktop"
path_dir = "/Users/brianjohnson/Desktop"


###########################################################################
########################### INITIAL USER CHOICES ##########################
###########################################################################



### select a category of frozen file for manipulation (either courses_taken or demo)
print "\n\n"
print "\t         ---------------------------------------------------------------------------------------------------"
print "\t        IIIIIIIIIIIIII    IIIIIIIIII        IIIIIIIIIIIIII    IIIIIIIIII       IIIIIIII    IIIIIIIIIIIIIIII"
print "\t       II                II        II      II                II        II        II              II"
print "\t      II                II         II     II                II          II      II              II"
print "\t     IIIIIIIII         IIIIIIIIIIIII     IIIIIIII          II           II     II              II"
print "\t    II                II    II          II                II            II    II              II"
print "\t   II                II      II        II                II           II     II              II"
print "\t  II                II        II      II                II         III      II              II"
print "\t II                II          II    IIIIIIIIIIIIII    IIIIIIIIIIII     IIIIIIII           II"
print "\t---------------------------------------------------------------------------------------------------"
print "\n\n"


print "-----------------------------------------------------------"
categories = ['demo', 'courses_taken', 'awards_conferred', 'faculty_section']
cat_choice = raw_input(
    "Enter corresponding integer to select frozen file category:\n1) demographics  2) courses_taken  3) awards_conferred  4) faculty_section\n")

category = categories[int(cat_choice) - 1]

print "\n"



### establish which csv files are available in the given directory

all_files = os.listdir(path_dir)

csv_files = []
for i in all_files:
    if not os.path.isdir("{}/{}".format(path_dir, i)):
        if i.split('.')[1] == "csv":
            csv_files.append(i)

print "--------------------"
print "Available CSV files:"
count = 0
for x in csv_files:
        print "{}{}".format(count, ")"), x
        count += 1

print "\n"



### select the csv file whose structure should be replicated

print "-----------------------------------------------"
ref_choice = raw_input("Enter correspnding index of reference csv file:\n")

reference = csv_files[int(ref_choice)]



### select the csv files whose structures should be changed to replicate the reference file
# allow people to pick whether to enter a list or range of indices
print "--------------------"
edit_choices_types = ['list', 'range']
edit_choices_type = raw_input("For files to edit, select whether to enter a range or list of indices:\n1) list  2) range\n")

if edit_choices_types[int(edit_choices_type)-1] == 'list':
    edit_choices = raw_input("Enter desired indices of files to edit, separated by commas:\n")
    edit_choices_l = [int(x) for x in edit_choices.split(',')]
elif edit_choices_types[int(edit_choices_type)-1] == 'range':
    edit_choices = raw_input("Enter desired starting and ending indices of range, separated by commas:\n")
    edit_choices_l = range(int(edit_choices.split(',')[0]), int(edit_choices.split(',')[1])+1)

# turn the user inputs into the list of files to edit, making sure you don't include the file selected as the reference
edits = []
for i in edit_choices_l:
    if csv_files[i] != reference:
        edits.append(csv_files[i])




###########################################################################
########################## CREATION OF CLASSES ############################
###########################################################################


### create a class for courses_taken csv files
class froCourses_taken():      # make each of the csv files a class with headers and data
    """class for courses_taken csv files"""

    def __init__(self, fro_file):

        # basic file info
        self.type = "courses_taken"
        self.name = fro_file

        # set original data, headers, and row dimensions
        fro_file_hand = open(os.path.join(path_dir, fro_file))
        fro_file_read = csv.reader(fro_file_hand)
        self.headers = next(fro_file_read)
        self.data = []
        for x in fro_file_read:
            self.data += [x]
        self.nrow = len(self.data)

        # attributes for creating new files
        self.new_indices = []
        self.new_headers = []
        self.unmatched_headers = []


    def setRegEx(self):

            # regular expressions based on reference headers
            reg_exps = {}

            reg_exps['Person ID'] = re.compile('Person\s*ID')
            reg_exps['Enrollment Term'] = re.compile('^Term$|^Enrollment Term$')
            reg_exps['Enrolled Course Subject'] = re.compile('^Discipline$|^Enrolled Course Subject$|^Subject$')
            reg_exps['Enrolled Course Name'] = re.compile('^STC.CRS.NAME$|^Enrolled Course Name$')
            reg_exps['Enrolled Course Section Number'] = re.compile('^Section$|^Enrolled Course Section Number$')
            reg_exps['Enrolled Course Full Name (J10)'] = re.compile('^Section.Name$|^Section\s*Name$|^Enrolled Course Full Name \(J10\)$')
            reg_exps['Enrollment Course Title'] = re.compile('^Title$|^Enrollment Course Title$')
            reg_exps['Section Credit Value (J10)'] = re.compile('^Reg.Cred$|^Reg\s*Cred$|^Section Credit Value \(J10\)$')
            reg_exps['Completed Credits For Course (J10)'] = re.compile('^Cmpl.Cred$|^Cmpl\s*Cred$|^Completed Credits For Course\(J10\)$|^Completed Credits For Course \(J10\)$')
            reg_exps['Enrolled Verified Grade (J10)'] = re.compile('^Vrfd.Grades$|^Vrfd\s*Grade$|^Enrolled Verified Grade\(J10\)$|^Enrolled Verified Grade \(J10\)$')
            reg_exps['Billing Cred (J10)'] = re.compile('^BILL.CRED$|^BILL\s*CRED$|^Billing Cred \(J10\)$')
            reg_exps['Enrolled Course Location'] = re.compile('^Location$|^Enrolled Course Location$')
            reg_exps['Enrollment Current Status'] = re.compile('^Current.Status$|^Current\s*Status$|^Enrollment Current Status$')
            reg_exps['Enrollment Current Status Date'] = re.compile('^Current\s*Status\s*Date$|^Enrollment Current Status Date$')
            reg_exps['Scs Mid Term Grade1 (J10)'] = re.compile('^Midterm Grade 1$|^Scs Mid Term Grade1 \(J10\)$|^Scs Mid Term Grade1  \(J10\)$')
            reg_exps['Scs Mid Term Grade2 (J10)'] = re.compile('^Midterm Grade 2$|^Scs Mid Term Grade2 \(J10\)$|^Scs Mid Term Grade2  \(J10\)$')
            reg_exps['Scs Mid Term Grade3 (J10)'] = re.compile('^Midterm Grade 3$|^Scs Mid Term Grade3 \(J10\)$|^Scs Mid Term Grade3  \(J10\)$')
            reg_exps['Scs Mid Term Grade4 (J10)'] = re.compile('^Midterm Grade 4$|^Scs Mid Term Grade4 \(J10\)$|^Scs Mid Term Grade4  \(J10\)$')
            reg_exps['Enrolled Course Academic Level'] = re.compile('^Acad.Level$|^Acad Level$|^Enrolled Course Academic Level$')
            reg_exps['Enrolled Course Credit Type'] = re.compile('^Cred.Type$|^Cred Type$|^Enrolled Course Credit Type$')
            reg_exps['Enrollment Term Start Date'] = re.compile('^Enrollment.Term.Start.Date$|^Enrollment Term Start Date$')
            reg_exps['Enrollment Start Date'] = re.compile('^Start.Date$|^Start Date$|^Enrollment Start Date$')
            reg_exps['Enrollment Course Type (J10)'] = re.compile('^Course\s*Types$|^Enrollment Course Type \(J10\)$')
            reg_exps['Enrollment Registration Method (J10)'] = re.compile('^Reg Method$|^Enrollment Registration Method \(J10\)$')

            return reg_exps


    def setIndices(self, inp_head):      # method to set the new index order based on reference headers

        # immediately set the new headers of the file to be the input headers
        self.new_headers = inp_head

        # find the matches if there are any
        indices = []
        indices_running = []

        print self.name
        print "---"
        print "Ref", ',', "Match"

        reg_exps = self.setRegEx()
        for i in inp_head:
            pat = reg_exps[i]
            result = [x for x, y in enumerate(self.headers) if pat.search(y)]
            indices_running += result
            if len(result) == 1:
                indices += result
                print i, ',', self.headers[result[0]]
            elif len(result) > 1:
                indices += [result[0]]
                mult_match = [self.headers[x] for x in result]
                print i, ',', mult_match, 2*"\t" + "** multiple **"
            elif len(result) == 0:
                indices += ['']
                print i, ',', 2*"\t" + "** no match **"

        self.new_indices = indices

        # make note of any old headers that did not match with any new headers
        self.unmatched_headers = [self.headers[i] for i in range(len(self.headers)) if i not in indices_running]


    def getHeaders(self):   # method to retrieve initial headers for each csv object
        return self.headers


    def getUnmatchedHeaders(self): # method to retrieve initial headers that were unmatched to any new headers
        return self.unmatched_headers


    def setFileExt(self):
        return "_courses_taken.csv"


    def writeOut(self):  # method to write out new file

        # name the new file based on what has been found to be the term of the file
        term = self.data[0][self.new_indices[1]]
        file_write_name = os.path.join(path_dir, term.translate(None, '/') + self.setFileExt())
        fhand = open(file_write_name, "wb")

        # write out the data in the newfound order, with non-header-matched data as just blanks
        fwriter = csv.writer(fhand)
        fwriter.writerow(self.new_headers)
        for i in self.data:
            new_row = []
            cnt = 0
            for x in self.new_indices:
                if type(x) != type(''):
                    new_row.append(i[x])
                elif self.type == "courses_taken" and type(x) == type('') and cnt == 2: # get course subject from class name if subject blank
                    new_row.append(i[3].split('-')[0])
                else:
                    new_row.append('')
                cnt += 1
            fwriter.writerow(new_row)

        fhand.close()

        # check that dimensions match
        fhand = open(file_write_name)
        new_reader = csv.reader(fhand)
        new_headers = next(new_reader)
        new_data = []
        for x in new_reader:
            new_data += [x]
        new_nrow = len(new_data)
        print self.name, file_write_name.split("\\")[-1]
        print "{}\t{}".format(self.nrow, new_nrow)
        print self.nrow == new_nrow



### create the object class for demographics csv frozen files, inheriting from the courses_taken frozen file class
class froDemo(froCourses_taken):
    """class for demographics csv files"""

    def __init__(self, fro_file):
        froCourses_taken.__init__(self, fro_file)
        self.type = "demographics"


    def setRegEx(self):

        # regular expressions based on reference headers
        reg_exps = {}

        reg_exps['Person ID'] = re.compile('^Person\s*ID$')
        reg_exps['Enrollment Term'] = re.compile('^Enrollment Term$|^Term$')
        reg_exps['Person UIC ID (J10)'] = re.compile('^Person UIC ID \(J10\)$')
        reg_exps['Person First Name'] = re.compile('^Person First Name$|^First Name$')
        reg_exps['Person Middle Name'] = re.compile('^Person Middle Name$|^Middle Name$')
        reg_exps['Person Last Name'] = re.compile('^Person Last Name$|^Last Name$')
        reg_exps['Person Suffix'] = re.compile('^Person Suffix$|^SUFFIX$')
        reg_exps['Person Address County'] = re.compile('^Person Address County$|^COUNTY$')
        reg_exps['Person Address County Desc'] = re.compile('^Person Address County Desc$')
        reg_exps['Student Current Type'] = re.compile('^Student Current Type$|^Cur Stu Type$')
        reg_exps['Person Birth Date'] = re.compile('^Person Birth Date$|^Birthday$')
        reg_exps['Person Age'] = re.compile('^Person Age$|^Age$')
        reg_exps['Person Age Band (J10)'] = re.compile('^Person Age Band \(J10\)$')
        reg_exps['Person Gender'] = re.compile('^Person Gender$|^Gender$')
        reg_exps['Person Alien Status'] = re.compile('^Person Alien Status$|^Alien\s*Status$')
        reg_exps['Person Alien Status Desc'] = re.compile('^Person Alien Status Desc$')
        reg_exps['Person Ethnic 1'] = re.compile('^Person Ethnic 1$|^Primary Ethnic$')
        reg_exps['Person Ethnic 2'] = re.compile('^Person Ethnic 2$')
        reg_exps['Person Race 1'] = re.compile('^Person Race 1$|^Primary Races$')
        reg_exps['Person Race 2'] = re.compile('^Person Race 2$')
        reg_exps['Person Race 3'] = re.compile('^Person Race 3$')
        reg_exps['Person Disability 1 ID'] = re.compile('^Person Disability 1 ID$|^DISABILITIES$')
        reg_exps['Person Disability 2 ID'] = re.compile('^Person Disability 2 ID$')
        reg_exps['Person Disability 3 Desc'] = re.compile('^Person Disability 3 Desc$')
        reg_exps['Person Veteran Type 1 (J10)'] = re.compile('^Person Veteran Type 1 \(J10\)$|^Person Veteran Type \(J10\)$')
        reg_exps['Person Veteran Type 2 (J10)'] = re.compile('^Person Veteran Type 2 \(J10\)$')
        reg_exps['Person Primary Language'] = re.compile('^Person Primary Language$|^PERSON.PRIMARY.LANGUAGE$')
        reg_exps['Person Primary Language Desc'] = re.compile('^Person Primary Language Desc$')
        reg_exps['Person Phone Number'] = re.compile('^Person Phone Number$')
        reg_exps['Person Privacy Flag (J10)'] = re.compile('^Person Privacy Flag \(J10\)$')
        reg_exps['Person Preferred Email Address'] = re.compile('^Person Preferred Email Address$|^Student Email$')
        reg_exps['Person Citizenship'] = re.compile('^Person Citizenship$|^CITIZENSHIP$')
        reg_exps['Person Citizenship Desc'] = re.compile('^Person Citizenship Desc$')
        reg_exps['Person Birth Name Last'] = re.compile('^Person Birth Name Last$|^NAME.HISTORY.LAST.NAME$')
        reg_exps['Person 771 Username (J10)'] = re.compile('^Person 771 Username \(J10\)$|^JCC.CONCATENATE.771$')
        reg_exps['Person Address State'] = re.compile('^Person Address State$|^STATE$|^Person Residence State$')
        reg_exps['Person Address Zip'] = re.compile('^Person Address Zip$|^ZipCode$|^Zip Code$')
        reg_exps['Person Birth Country'] = re.compile('^Person Birth Country$')
        reg_exps['Person Address Country'] = re.compile('^Person Address Country$')
        reg_exps['Person Address Country Desc'] = re.compile('^Person Address Country Desc$')
        reg_exps['Current Program 1 (J10)'] = re.compile('^Current Program 1 \(J10\)$|^PROGRAMClean$|^PROGRAM$')
        reg_exps['Current Program 2 (J10)'] = re.compile('^Current Program 2 \(J10\)$')
        reg_exps['Current Program 3 (J10)'] = re.compile('^Current Program 3 \(J10\)$')

        return reg_exps


    def setFileExt(self):
        return "_demo.csv"


### create the object class for awards_conferred csv frozen files, inheriting from courses_taken class
class froAwards(froCourses_taken):
    "class for awards_conferred csv files"

    def __init__(self, fro_file):
        froCourses_taken.__init__(self, fro_file)
        self.type = "awards_conferred"


    def setRegEx(self):

        # regular expressions based on reference headers
        reg_exps = {}

        reg_exps['ID'] = re.compile('^ID$|^ACAD.PERSON.ID$')
        reg_exps['Credential Term (J10)'] = re.compile('^Credential Term \(J10\)$|^Term$')
        reg_exps['Last'] = re.compile('^Last$|^LAST NAME$')
        reg_exps['First'] = re.compile('^First$|^FIRST NAME$')
        reg_exps['Middle'] = re.compile('^Middle$')
        reg_exps['Gender'] = re.compile('^Gender$|^GENDER$')
        reg_exps['Person Birth Date'] = re.compile('^Person Birth Date$|^Birth Date$')
        reg_exps['Address Phone 1'] = re.compile('^Address Phone 1$')
        reg_exps['Person Age'] = re.compile('^Person Age$')
        reg_exps['Person Age Band (J10)'] = re.compile('^Person Age Band \(J10\)$')
        reg_exps['State'] = re.compile('^State$')
        reg_exps['Credential CCD 1'] = re.compile('^Credential CCD 1$|^CCD$')
        reg_exps['Credential CCD 1 Date'] = re.compile('^Credential CCD 1 Date$|^ACAD.CCD.DATE$')
        reg_exps['Credential Degree'] = re.compile('^Credential Degree$|^Degree$')
        reg_exps['Credential Degree Date'] = re.compile('^Credential Degree Date$|^Date$')
        reg_exps['Credential Program CIP'] = re.compile('^Credential Program CIP$|^Acad Program CIP$')
        reg_exps['Credential Academic Program'] = re.compile('^Credential Academic Program$|^Acad Program$')
        reg_exps['Program Title'] = re.compile('^Program Title$')
        reg_exps['Date'] = re.compile('^Date$')
        reg_exps['Credential Honors 1'] = re.compile('^Credential Honors 1$|^Honors$')
        reg_exps['Credential Honors 1 Desc'] = re.compile('^Credential Honors 1 Desc$')
        reg_exps['Person Ethnic 1'] = re.compile('^Person Ethnic 1$|^Ethnics$')
        reg_exps['Person Ethnic 2'] = re.compile('^Person Ethnic 2$')
        reg_exps['Person Race 1'] = re.compile('^Person Race 1$|^Races$')
        reg_exps['Person Race 2'] = re.compile('^Person Race 2$')
        reg_exps['Person Race 3'] = re.compile('^Person Race 3$')

        return reg_exps


    def setFileExt(self):
        return "_awards.csv"



### create the object class for faculty_section frozen file objects, inheriting from courses_taken
class froFaculty(froCourses_taken):
    "class for faculty_section frozen files"

    def __init__(self, fro_file):
        froCourses_taken.__init__(self, fro_file)
        self.type = "faculty_section"

    def setRegEx(self):

        # regular expressions based on reference headers
        reg_exps = {}

        reg_exps['Section Term'] = re.compile('^Section Term$|^Term$')
        reg_exps['Section Subject'] = re.compile('^Section Subject$|^Subject$')
        reg_exps['Section Name'] = re.compile('^Section Name$|^Section Name$')
        reg_exps['Section Location'] = re.compile('^Section Location$|^Location$')
        reg_exps['Section Capacity'] = re.compile('^Section Capacity$|^Capacity$')
        reg_exps['Section Active Student Count'] = re.compile('^Section Active Student Count$|^Active Student Count$')
        reg_exps['Assignment Instructional Method'] = re.compile('^Assignment Instructional Method$|^Instr Methods$')
        reg_exps['Meeting Instructional Method'] = re.compile('^Meeting Instructional Method$|^Instr Methods$')
        reg_exps['Section Minimum Credits'] = re.compile('^Section Minimum Credits$|^Min Cred$')
        reg_exps['Section Start Date'] = re.compile('^Section Start Date$|^START.DATE$')
        reg_exps['Section End Date'] = re.compile('^Section End Date$|^END.DATE$')
        reg_exps['Section Billing Credits (J10)'] = re.compile('^Section Billing Credits \(J10\)$|^Billing Credits$')
        reg_exps['Days'] = re.compile('^Days$|^Days$')
        reg_exps['Meeting Start Time'] = re.compile('^Meeting Start Time$|^START TIME$')
        reg_exps['Meeting End Time'] = re.compile('^Meeting End Time$|^Meeting End Time$')
        reg_exps['Section Number of Weeks (J10)'] = re.compile('^Section Number of Weeks \(J10\)$|^No Weeks$')
        reg_exps['Person Last Name'] = re.compile('^Person Last Name$|^SEC.FACULTY.LAST.NAME$')
        reg_exps['Person First Name'] = re.compile('^Person First Name$|^SEC.FACULTY.FIRST.NAME$')
        reg_exps['Faculty Assignment Position Class (J10)'] = re.compile('^Faculty Assignment Position Class \(J10\)$|^SEC.POS.CLASS$|^Position Class$')

        return reg_exps


    def setFileExt(self):
        return "_faculty_section.csv"


    def writeOut(self):  # method to write out new file, different from other classes because of concatenated fields

        # name the new file based on what has been found to be the term of the file
        term = self.data[0][self.new_indices[0]]
        file_write_name = os.path.join(path_dir, term.translate(None, '/') + self.setFileExt())
        fhand = open(file_write_name, "wb")

        # write out the data in the newfound order, with non-header-matched data as just blanks
        fwriter = csv.writer(fhand)
        fwriter.writerow(self.new_headers)

        for i in self.data:
            new_row = []
            cnt = 0
            for x in self.new_indices:
                if type(x) != type(''):
                    if cnt == 6: # add first method as the assigned course instr method
                        methods = re.findall('[^ý_Ìü]+', i[x])
                        if len(methods) > 0:
                            new_row.append(methods[0])
                        else:
                            new_row.append('')
                    elif cnt == 7: # add second method, if there is one, as the meeting course instr method
                        methods = re.findall('[^ý_Ìü]+', i[x])
                        if len(methods) > 1:
                            new_row.append(methods[1])
                        elif len(methods) == 1:
                            new_row.append(methods[0])
                        else:
                            new_row.append('')
                    elif cnt == 12: # concatenate meeting days together
                        days = re.findall('[^ý_Ìü]+', i[x])
                        if len(days) > 0:
                            new_row.append(''.join(days))
                        else:
                            new_row.append('')
                    elif cnt == 13:
                        times = re.findall('[^ý_Ìü]+', i[x])
                        if len(times) > 0:
                            new_row.append(''.join(times))
                        else:
                            new_row.append('')
                    elif cnt == 18:
                        pos_classes = re.findall('[^ý_Ìü]+', i[x])
                        if len(pos_classes) > 0:
                            new_row.append(pos_classes[0])
                        else:
                            new_row.append('')
                    else:
                        new_row.append(i[x])
                else:
                    new_row.append('')
                cnt += 1
            fwriter.writerow(new_row)

        fhand.close()

        # check that dimensions match
        fhand = open(file_write_name)
        new_reader = csv.reader(fhand)
        new_headers = next(new_reader)
        new_data = []
        for x in new_reader:
            new_data += [x]
        new_nrow = len(new_data)
        print self.name, file_write_name.split("\\")[-1]
        print "{}\t{}".format(self.nrow, new_nrow)
        print self.nrow == new_nrow




###########################################################################
############################# FILE MANIPULATION ###########################
###########################################################################


### establish the reference header list; print out the list

ref_hand = open(os.path.join(path_dir, reference))

ref_read = csv.reader(ref_hand)

ref_head = next(ref_read)

print "\n"
print "-----------------------"
print "Reference Headers List"
cnt = 1
for i in ref_head:
    print cnt, i
    cnt += 1
print "\n"


### create the csv file objects using class type that corresponds to frozen file type selected earlier
if category == 'courses_taken':
    csv_objects = [froCourses_taken(i) for i in edits]
elif category == 'demo':
    csv_objects = [froDemo(i) for i in edits]
elif category == 'awards_conferred':
    csv_objects = [froAwards(i) for i in edits]
elif category == 'faculty_section':
    csv_objects = [froFaculty(i) for i in edits]


### establish the list and counts of headers to be mapped to reference headers; print out list and counts
all_headers = []

for x in csv_objects:
    all_headers += x.getHeaders()

header_tallies = {}
for x in all_headers:
    header_tallies[x] = header_tallies.get(x, 0) + 1

header_tallies_s = sorted(header_tallies, key = lambda x: header_tallies[x], reverse = True)

print "--------------------------"
print "To-Be-Edited Headers List"

for i in header_tallies_s:
    print i, header_tallies[i]


### use regex to find the corresponding to-be-edited indices in the reference header list
print "\n"
print "----------------"
print "Header Mappings"
print "\n"
for x in csv_objects:
    x.setIndices(ref_head)
    print "\n"


### write out the new csv files with the newly reordered headers and a check for matching dimensions
print "----------------------------------------"
print "Writing Out Files with Dimensions Check"
for i in csv_objects:
    i.writeOut()


### assess the old headers that were never matched to any new headers; print out the list
print "\n"
print "-----------------------"
print "Unmatched Header Counts"

unmatched_headers = []
for x in csv_objects:
    unmatched_headers += x.getUnmatchedHeaders()

unmatched_headers_counts = {}
for i in unmatched_headers:
    unmatched_headers_counts[i] = unmatched_headers_counts.get(i, 0) + 1

unmatched_headers_counts_s = sorted(unmatched_headers_counts, key = lambda x: unmatched_headers_counts[x], reverse = True)
for i in unmatched_headers_counts_s:
    print i, unmatched_headers_counts[i]

print "\n"
print "-----------------------"
print "Unmatched Header Lists"

for x in csv_objects:
    if len(x.getUnmatchedHeaders()) > 0:
        print x.name, x.getUnmatchedHeaders()
