#!/usr/bin/env python
# -*- coding:utf8 -*- 
"""
xiaojias@cn.ibm.com
Supports create .xls file/s for: threshold
The directory structure of .json files should be as (one-layer subdirectory):
--<account name>
  |-------<threshold type name> e.g Linux, GSMA Linux
       |-----.json files
  |-------<threshold type name> e.g Linux, GSMA Linux
  ....
 ###################################################################
 # changes :                                                       #
 # 20180713-XJS : Add rules for Agnostic BP Thresholds spreadsheet #
 # 20180821-XJS : Fix the issue on removing K* arrtibutes in new   #
 #                formula, e.g for KZC_KEYSPACEDETAILS.KeySpaceReadLatency *GE 5#
 # 20180822-XJS : Remove all possible Attribute Groups from a      #
 #                a predefined list                                #
 #                                                                 #
 ###################################################################
"""
import sys
import os
import json
import re

import xlwt

import logging

FORMULARULE = "./Formula_replacement_rules.param"
MONITOREDMETRICRULE = "./MonitorResource-hash-table.param"

def usage():
    print('''
    Usage:
    %s -d <directoy>  [-f <Formula Replacement rules file>] [-m <Monitored Metrics Replacement rules file>]''' % script )
    logging.error('Exit: on input')
    sys.exit(1)

def convert(obj, objtype,  objdict, suffix="."):
    #convert a nested json data (dict, list) to a non-nested (one-level) dictionary type of data
    s = suffix
    if isinstance(obj, dict):
        for k, v in obj.items():
            s1 = "%s.%s" % (s, k)   #put the key as a part of identifier
            if isinstance(v, dict) or isinstance(v, list):
                #process for threshold' .json file espacially
                logging.debug('Process for threshold espacilly on formula')
                if objtype == "threshold" and k == "formulaElements":
                    formula = ""
                    operator = ""
                    if "operator" in obj.keys() and obj.get("operator"):
                        operator = obj["operator"]
                        for item in obj[k]:
                            formula += ' {{{function} {metricName} {operator} {threshold}}} '.format(**item) + obj['operator']
                        formula = formula.strip(obj['operator'])
                    elif k in obj.keys() and len(obj[k]) == 1 and type(obj[k]) is list:
                        item = obj[k][0]
                        formula += '{{{function} {metricName} {operator} {threshold}}} '.format(**item)
                    objdict[s1] = formula.strip()
                else:
                    convert(v, objtype, objdict, suffix=s1)
            else:
                objdict[s1] = v
    elif isinstance(obj, list):
        s1 = "%s." % s
        if not obj:
            objdict[s] = "NULL"
        else:
            k = 0
            for v in obj:
                s1 = s1 + str(k)     #add the index as a suffix
                if isinstance(v, dict) or isinstance(v, list):
                    convert(v, objtype, objdict, suffix=s1)
                else:
                    objdict[s1] = v
                k += 1
    else:
        logging.error('data type in .json file is not supported')
        print('Not supported so far')
        sys.exit(1)
    return(objdict)
    
def set_style(name, bold=False): 
    style = xlwt.XFStyle() # intial style
    font = xlwt.Font()
    font.name = name # 'Times New Roman' 
    font.bold = bold 
    style.font = font 
    return(style)

def changeLabelForShown(label):
    """Apply Situation Naming convention Standard for label

    Show threshold name as Rule name, e.g: "all_fss_nlzw_linux_1" should be shown as "linux_fss_warning_1"

    :param label: it is label properity of threshold' .json file
    :return: the changed label with new format
    """
    newLabel = label
    # RegExp for Naming convention Standard for IPM8 threshold
    p = re.compile(r'(?P<CustomerCode>[a-z]{3})_'
                   r'(?P<MonResource>[a-z0-9]{3,7})_'
                   r'(?P<dummy>[a-z0-9]{3})(?P<severity>[cwf1-6])_'
                   r'(?P<MonSol>[a-z]+)'
                   r'(?P<others>(.)*)')
    a = p.match(label)
    if a:
        # value matches the RegExp
        if a.group("severity") == "c" or a.group("severity") == '2':
            severityValue = "critical"
        elif a.group("severity") == "w" or a.group("severity") == '4':
            severityValue = "warning"
        elif a.group("severity") == "f"  or a.group("severity") == '1':
            severityValue = "fatal"
        elif a.group("severity") == '3':
            severityValue = "major"
        elif a.group("severity") == '5':
            severityValue = "harmless"
        else:
            # other character ( might be invalid)
            severityValue = "xxxxx"

        newLabel = "%s_%s_%s%s" % (a.group("MonSol"), a.group("MonResource"), severityValue, a.group("others"))
    else:
        newLabel = "Invalid_Threshold_name"
    return(newLabel)

def changeFormulaForShown(formula):
    """Apply rules for formula

    Change formula displaying by applying the rules defined from a rulesfile

    :param formula: threshold's formula
    :global param FORMULARULE: which includes all formula replacement rules
    :return: the changed formula with new format
    """
    global FORMULARULE

    newFormula = formula
    mylist = []
    # get the rules from the file
    mylist = generateRules(FORMULARULE)
    #mylist = generateRules("./Formula_replacement_rules.param")

    # remove Attribute name from formula which starts with "K"
    # define all the attribute groups' identifiers (starts with)
    attrGroups=["K", "NT_", "MS_SQL_", "Domain_Controller_"]
    # K : is for K<pc> for almost agents
    # NT_ : is for Windows, e.g NT_Event_log
    # MS_SQL_ : is for MSSQL
    # Domain_Controller_Availability : is for AD. e.g Domain_Controller_Availability

    for i in range(len(attrGroups)):
        p = re.compile(r'(?P<dummy1>(.)*) %s(?P<attribute>[a-zA-Z0-9_]+)\.(?P<dummy2>(.)*)' % attrGroups[i])
        a = p.match(newFormula)

        while a:
            # for debugging
            #print("formula is: %s") % newFormula
            #print("Attribute is: %s") % a.group("attribute")
            newFormula = "%s %s".strip() % (a.group("dummy1"), a.group("dummy2"))
            formula = newFormula

            # remove all the Attributes from formula
            p = re.compile(r'(?P<dummy1>(.)*) %s(?P<attribute>[a-zA-Z0-9_]+)\.(?P<dummy2>(.)*)' % attrGroups[i])
            a = p.match(newFormula)

    # apply the rules one by one
    for i in range(len(mylist)):
        str1 = mylist[i]["string"]
        str2 = mylist[i]["replacement"]
        newFormula = re.subn(str1, str2, formula)[0]
        formula = newFormula
    # remove the 'line break' character and blank character
    newFormula = re.subn("\n", "", formula)[0].strip()


    return(newFormula)

def changeIntervalForShown(interval):
    """Apply some rule for interval

    Change interval displaying. e.g 011500 will be shown as "1 hour 15 minutes"

    :param interval: threshold's interval properity
    :return: displaying with new format

    """
    newInterval = interval
    #RegExp for interval
    p = re.compile(r'(?P<hour>[0-9]{2})'
                   r'(?P<minute>[0-9]{2})'
                   r'(?P<second>[0-9]{2})')
    a = p.match(interval.strip())

    if a:
        # value matches the RegExp
        newInterval = ""
        hour = a.group("hour").lstrip("0").lstrip("0")
        if hour:
            if hour == "1":
                newInterval = "%s hour" % (hour)
            else:
                newInterval = "%s hours" % hour
        minute = a.group("minute").lstrip("0").lstrip("0")
        if minute:
            if minute == "1":
                newInterval = "%s %s minute".strip() % (newInterval, minute)
            else:
                newInterval = "%s %s minutes".strip() % (newInterval, minute)
        second = a.group("second").lstrip("0").lstrip("0")
        if second:
            if second == "1":
                newInterval = "%s %s second".strip() % (newInterval, second)
            else:
                newInterval = "%s %s seconds".strip() % (newInterval, second)
        if not hour and not minute and not second:
            newInterval = "N/A"
    else:
        # value matches the RegExp
        newInterval = "Invalid interval"

    return(newInterval)

def changeMonitoredMetricForShown(thresholdName):
    """Show the Monitored Metric (Monitored resources) from threshold name

    :param thresholdName: threshold name
    :global param MONITOREDMETRICRULE: which includes all monitored metric replacement rules
    :return: the monitored metric, should be a value of Resource slot from threshold name
             (second slot); second column in the file should be a human readable metric name
    """
    global MONITOREDMETRICRULE

    # get the 2nd slot of threshold
    slot2 = thresholdName.split("_")[1]

    mylist = []
    # get the rules from the file
    mylist = generateRules(MONITOREDMETRICRULE)

    # It shows Default
    strMonitoredMetric = "To-be-defined"

    for i in range(len(mylist)):
        if mylist[i]["string"] == slot2:
            strMonitoredMetric = mylist[i]["replacement"]
            break

    return(strMonitoredMetric)

def changeThresholdLevel(formula):
    """

    :param formula: threshold formula
    :return: Threshold level/s
    """
    levels = []
    operators = ['*NE', '*EQ', '*LT', '*LE', '*GT', '*GE']

    strLevel = ""
    for op in operators:
        # get the value for every operator if there is
        p = re.compile(r'(?P<dummy1>(.)*) '+ op +' (?P<value>[0-9.\'a-zA-Z _-]+)}(?P<dummy2>(.)*)')
        a = p.match(formula)

        while a:
            levels.append(a.group("value"))

            formula = a.group("dummy1")

            p = re.compile(r'(?P<dummy1>(.)*) '+ op +' (?P<value>[0-9.\'a-zA-Z _-]+)}(?P<dummy2>(.)*)')
            a = p.match(formula)

    if len(levels) > 0:
        strLevel = levels.sort()
        for i in range(len(levels)):
            strLevel = "%s, %s" % (strLevel, levels[i])
        strLevel = strLevel.strip("None").strip(",").strip()
        # remove the character of '
        strLevel = re.subn("'", "", strLevel)[0]
    else:
        strLevel = ""

    return(strLevel)

def applyRuleForShown(sheetname, headername, value):
    """Apply rule for Agnostic BP Thresholds spreadsheet

    Change the displaying for readable purpose.

    :param sheetname: the sheet name of .xls file mapping the directory name of .json files
    :param headername: the header name of .xls file
    :param value: the actual value to be changed on displaying

    :Global param rulesList : rules for formula replacement, e.g [{string:\*AND, replacement:AND}, {string:*EQ, replacement:=}]

    :return: a string which will be shown in .xls file
    """
    if headername == 'Rule name':
        # generate 'Rule name' from 'Threshold name'
        newValue = changeLabelForShown(value)
    elif headername == 'Formula (tool agnostic)':
        # change formula
        newValue = changeFormulaForShown(value)
        #print("Changed formula is: %s" % newValue)
    elif headername == 'Sample interval':
        # for "Sample interval", it requires to be changed
        newValue = changeIntervalForShown(value)
    elif headername == 'Monitored metric':
        newValue = changeMonitoredMetricForShown(value)
    elif headername == 'Threshold/Level':
        newValue = changeThresholdLevel(value)
    else:
        newValue = value

    return(newValue)

def writeJsontoXls(mydir, templates=None):
    logging.info('Process .json file/s in: %s' % mydir)

    if templates is None:
        templates = []
    dir1 = os.path.split(mydir)
    name = "Monitoring_IPM8_%s.xls" % dir1[1]   #set the xls file name
    xls_name = os.path.join(mydir, name)

    f = xlwt.Workbook()
    writeOrnot = False    #If there is not any subdirectory, will not create .xls file, since sheet name missing

    for dir1 in sorted(os.listdir(mydir)):
        dira = os.path.join(mydir, dir1)
        if not os.path.isdir(dira):
            continue
        else:
            writeOrnot = True
        sheet_name = dir1
        logging.info('Sheet name:%s is created for %s directory' % (sheet_name, sheet_name))

        tname = sheet_name.lower()
        if not tname in ("resourcegroup", "agent", "threshold"):
            tname = "threshold"    #set the default template
        for i in range(len(templates)):
            if templates[i]["templatename"] == tname:
                template = templates[i]
        subdir1 = os.path.join(mydir, dir1)
        filenames = os.listdir(subdir1)

        #start to write data into
        row = 0
        for fname in filenames:
            if not fname.endswith(".json"):
                continue
            jsonFile = os.path.join(mydir, dir1)
            jsonFile = os.path.join(jsonFile, fname)    #generate the full name of .json file

            logging.info('Processing file:%s' % jsonFile)
            jf = open(jsonFile, "r")
            data = jf.read()
            jsonobj = json.loads(data)
            jf.close()

            mydict = {}
            mydict = convert(jsonobj, tname, mydict, suffix="")

            #change the key of mydict to the shortname (last identifier)
            logging.debug('Change the key to shortname')
            keys = mydict.keys()
            logging.debug('long keys:')
            logging.debug(keys)
            new_keys = []
            for k in keys:
                names = k.split(".")
                if k == ".entityTypes.0":   #especaily for resourcegroup' .json file
                    new_k = "entityTypes.0"
                    new_keys.append(new_k)
                else:
                    new_k = names[-1]
                    new_keys.append(new_k)
                mydict[new_k] = mydict.pop(k)
            if tname == "threshold":
                mydict["formula"] = mydict["formulaElements"]
            logging.debug('short keys:')
            logging.debug(new_keys)

            if row == 0:
                #new sheet
                logging.info('Create new sheet:%s' % sheet_name)
                sheet = f.add_sheet(sheet_name)
                #set the cloumn width
                logging.debug('column width is:')
                logging.debug(template['colWidth'])
                for i, v in enumerate(template["colWidth"]):
                    sheet.col(i).width = v
                    #set column as invisible for column A (Threshold name), E (formula)
                    #
                #write header additionally
                col = 0
                logging.info('Set the headers')
                logging.info(template["headerdata"])

                for k, v in enumerate(template["headers"]):
                    col = k
                    sheet.write(row, col, v, set_style('Times New Roman', True))

                row += 1
            #write data into
            col = 0
            logging.info('Write data into row: %d' % row)
            for k,v in enumerate(template["headerdata"]):
                if mydict.get(v):
                    data = mydict[v]
                else:
                    data = ""

                header = template["headers"][k]

                # Apply rules for shown
                data = applyRuleForShown(sheet_name, header, data)
                sheet.write(row, col, data)
                col += 1
                #sheet.write(row, col, data)
                #col += 1
            row += 1
    if writeOrnot :
        f.save(xls_name)
        return(xls_name)
    else:
        logging.error('Subdirectory must be created, as it will be taken as sheet name in xls file')
        return ""

def generateRules(ruleFile):
    """
    Generate the replacement rules from a specific file
    The file should contain semicolon separated rules in format:
    <regexp pattern1>;<replacement string1>
    <regexp pattern2>;<replacement string2>
    ...
    and comments are acceptable which starts with "#" in the line or a blank line
    :param ruleFile: the file, e.g Formula_replacement_rules.param
    :return: a list which contains the strings and their replacement
    """
    mylist = []

    if os.path.isfile(ruleFile):
        fileObj = open(ruleFile, 'r')
        for line in fileObj.readlines():
            #process
            #TBD
            # exclude the comments
            p = re.compile(r'^#|\s+#|\s+')
            a = p.match(line)
            if not a:
                #not a comment line
                #print("Valid line is: %s" % line)
                mydict = {}
                str = line.split(";")

                if len(str) < 2:
                    #will be replaced with "" as cleared
                    mydict["string"] = str[0]
                    mydict["replacement"] = ""
                else:
                    mydict["string"] = str[0]
                    # remove the line break at the end
                    mydict["replacement"] = re.subn("\n", "", str[1])[0]
                mylist.append(mydict)
        fileObj.close()

    return mylist

def getArgvDic(argv):
    #get all arguments, and save it into dictionary type
    optd = {}
    optd["script"] = argv[0]
    argv = argv[1:]
    while argv:
        if len(argv) >= 2:
            optd[argv[0]] = argv[1]
            argv = argv[2:]
        else:
            usage()
    return(optd)

def main():
    global FORMULARULE, MONITOREDMETRICRULE
    script = os.path.basename(__file__)
    logging.basicConfig(filename='/tmp/%s' % script.replace(".py", ".log"),
                        level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    #capture arguments
    mydict = getArgvDic(sys.argv)
    if not mydict.get("-d"):    #required parameters
        usage()
    dirName = mydict.get("-d")
    if not os.path.isdir(dirName):
        usage()

    # add parameter for Formula_replacement_rules file
    mydict = getArgvDic(sys.argv)

    if mydict.get("-f"):    #optional
        FORMULARULE = mydict.get("-f")
        if not os.path.isfile(FORMULARULE):
            usage()

    if mydict.get("-m"):  # optional
        MONITOREDMETRICRULE = mydict.get("-m")
        if not os.path.isfile(MONITOREDMETRICRULE):
            usage()

    # checking
    #logging.debug('Formula replacement rules are:')
    #for i in range(len(rulesList)):
    #    print("%s will be replaced by: %s" % (rulesList[i]["string"], rulesList[i]["replacement"]))

    #define the template of sheets for resources
    templates = []

    #template for threshold
    t = {}
    col_unit = 3333    ##pixels per inch

    t["templatename"] = "threshold"
    #list the data of threshold .json file for every column
    # add one more column for "label" and "formula" for implementation while the 2nd one
    # is displaying in different format
    t["headerdata"] = ["label", "label", "description", "severity", "formula",
                       "formula", "period", "periods", "matchBy", "actions", "formula", "label"]

    #cloumn width for every list
    t["colWidth"] = [1.6, 2.3, 4, 1, 2, 10, 1, 0.4, 2.4, 1.2, 10, 2.3]
    t["colWidth"] = [int(col_unit * i) for i in t["colWidth"]]
    logging.debug(t['colWidth'])

    #define the header for every column of raw data (required for every one)
    t["headers"] = ["Monitored metric", "Rule name", "Description", "Severity", "Threshold/Level",
                    "Formula (tool agnostic)", "Sample interval", "Occurrence", "Display Item", "Actions",
                    "Formula (IPM8 implementation example)", "Threshold name"]
    templates.append(t)

    cust = []    #remember on which directory should be processed
    cust.append(dirName)   #one-layer subdirectory
    
    for k in cust:
        file1 = writeJsontoXls(k, templates)
        if file1:
            logging.info('Created xls file is: %s' % file1)
            print("Created xls file is:\n %s" % file1)
        else:
            logging.error('xls file was not created for directory: %s' % dirName)
            print("Failed! xls file was not created for directory: %s" % dirName)
    print('Details refer to logfile: /tmp/%s' % script.replace(".py", ".log"))

if __name__ == '__main__':
    main()
