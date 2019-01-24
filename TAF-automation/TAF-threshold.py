#!/usr/bin/env python3
# -*- coding:utf8 -*-
'''
xiaojias@cn.ibm.com
###################################################################
# changes :                                                       #
# 20181218-XJS : Translate all the JSON files to new format for TA#
###################################################################

'''
# Tool Agnotisc Fromat for Threshold

import json
import os
import re
import sys
import logging
import copy

def usage():
    print('''Usage:
    %s -i <input directoy> -o <output directory> [-f <New format rules>]''' % script )
    logging.error('Exit: on input')
    sys.exit(1)

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

def generateDefaults(ruleFile):
    '''
    Generate the Default values for both Update & Add items from the parameter file
    :param rulefile: A text parameters file which defines the default values for every specific item, every line looks like:
    Update;label;visible:Yes;editable:No
    :return: 2 dictional objects of new formats for both Update & Add items
    '''
    myUpdate = {}
    myAdd = {}
    if os.path.isfile(ruleFile):
        with open(ruleFile, 'r') as fileObj:
            for line in fileObj.readlines():
                # process
                # TBD
                # exclude the comments
                p = re.compile(r'^#|\s+#|\s+')
                a = p.match(line)
                if not a:
                    # not a comment line
                    # print("Valid line is: %s" % line)
                    str = line.split(";")

                    if len(str) < 4:
                        # Wrong configuration
                        print("Invalid line:%s" % line)
                        continue
                    key = str[1]
                    if str[0] == "Update":
                        # update obj of myUpdate
                        myUpdate[key] = {"value": ""}

                        # Validate string for 'visible' and 'editable'
                        pass

                        for i in range(2,4):
                            str1 = str[i].split(":")
                            # remove the break line
                            myUpdate[key][str1[0]] = re.subn("\n", "", str1[1])[0]
    #                    print("Update:%s line is:%s" % (str[0], line))
                    elif str[0] == "Add":
                        # update obj of myListUpdate
                        myAdd[key] = {"value": ""}

                        # Validate string for 'visible' and 'editable'
                        pass

                        for i in range(2, 4):
                            str1 = str[i].split(":")
                            # myAdd[key][str1[0]] = re.subn("\n", "", str1[1])[0]
                            myAdd[key][str1[0]] = re.subn("\n", "", str1[1])[0]
                        #print("Add:%s line is:%s" % (str[0], line))
                    else:
                        print("Invalid line:%s" % line)
                        pass
    return myUpdate,myAdd

def changeJsonToNewFormat(infile, outfile, defaultvaluesForupdate, defaultvaluesForadd):
    '''
    :param infile: The to be translated threshold JSON file
    :param outfile: The translated JSON file with new format
    :param defaultvaluesForupdate: The default values for to-be-update items
    :param defaultvaluesForadd: The default valuse for to-be-add items
    :return:
    '''
    # Read JSON file to Threshold object
    with open(infile, "r") as f:
        data = f.read()
        obj = json.loads(data)

    # Debugging
    # display the JSON file without modification
    TempFile = "/tmp/threshold-temp.json"
    dataString = json.dumps(obj, sort_keys=True, indent=4)
    # Save Threshold to JSON file
    with open(TempFile, "w") as f:
        f.write(dataString)

    # Init the new Threshold object
    NewThreshold = {}
    for key in obj.keys():
        # Process for . (Top layer)
        if key in defaultvaluesForupdate.keys():
            # Change the value to new format
            NewValue = defaultvaluesForupdate[key]
            NewValue["value"] = obj[key]
            NewThreshold[key] = NewValue
        else:
            # Copy others to new Threshold object
            NewThreshold[key] = obj[key]
    if obj.get("configuration"):
        NewThreshold["configuration"] = {}
        for key in obj["configuration"].keys():
            # Process for .configuration
            if key in ["payload"]:
                # Process for .configuration.payload
                NewThreshold["configuration"]["payload"] = {}
                for subkey in obj["configuration"]["payload"].keys():
                    NewValue = {}
                    if subkey == "operator":
                        # process especially
                        if "operator0" in defaultvaluesForupdate.keys():
                            NewValue = defaultvaluesForupdate["operator0"]
                            NewValue["value"] = obj["configuration"]["payload"][subkey]
                            NewThreshold["configuration"]["payload"][subkey] = NewValue
                        else:
                            # copy it to new Threshold object
                            NewThreshold["configuration"][key] = obj["configuration"][key]
                    elif subkey in defaultvaluesForupdate.keys():
                        #                print("key is %s" % subkey)
                        NewValue = defaultvaluesForupdate[subkey]
                        NewValue["value"] = obj["configuration"]["payload"][subkey]
                        NewThreshold["configuration"]["payload"][subkey] = NewValue
                    elif subkey in ["actions"]:
                        NewThreshold["configuration"]["payload"]["actions"] = None
                    elif subkey in ["formulaElements"]:
                        # Process for .configuration.payload.formulaElements
                        NewThreshold["configuration"]["payload"]["formulaElements"] = []

                        for i in range(len(obj["configuration"]["payload"]["formulaElements"])):
                            item = obj["configuration"]["payload"]["formulaElements"][i]
                            # Process for .configuration.payload.formulaElements.[*]
                            element = {}

                            for subkey2 in item.keys():
                                if subkey2 in defaultvaluesForupdate.keys():
                                    #                        print("key is %s" % subkey2)
                                    NewValue = defaultvaluesForupdate[subkey2]
                                    NewValue["value"] = item[subkey2]
                                    element[subkey2] = copy.deepcopy(NewValue)   # Using Deepcopy instead, since NewValue might be nested dictionary data
                                else:
                                    # copy to new
                                    element[subkey2] = item[subkey2]

                            # add element into new Threshold object
                            NewThreshold["configuration"]["payload"]["formulaElements"].append(element)
                    else:
                        # copy others to new Threshold object
                        NewThreshold["configuration"]["payload"][subkey] = obj["configuration"]["payload"][subkey]
            else:
                # copy others to new Threshold object
                NewThreshold["configuration"][key] = obj["configuration"][key]
    else:
        print("Warning: %s may not be a Standard Threshold JSON file" % infile)
        logging.error("%s may not be a Standard Threshold JSON file" % infile)
    # Add new keys into Threshold
    NewThreshold["supportedByAll"] = "False"
    NewThreshold["supported_tools"] = ["IPM"]

    # Add new keys into top level
    # TBD

    # Save Threshold to JSON file
    dataString = json.dumps(NewThreshold, sort_keys=True, indent=4)

    with open(outfile, "w") as f:
        f.write(dataString)
        logging.info("%s was transferred." % infile)

def listAllJsonFiles(mydir):
    '''
    List all the JSON file and the directory and its subdirectories, and save it to a List object
    :param mydir:
    :return: a List Object
    '''
    files = []
    list = os.listdir(mydir)   # list all the files and subdirectories
    for i in range(0, len(list)):
        path = os.path.join(mydir, list[i])
        if list[i] == "CEIM":
        # skip for CEIM .json files
            continue
        if os.path.isdir(path):
            files.extend(listAllJsonFiles(path))
        elif os.path.isfile(path) and path.endswith(".json"):
            files.append(path)
    return files

def main():
    global FORMATRULE, script
    global DefaultsUpdate, DefaultsAdd
    DefaultsUpdate = {}
    DefaultsAdd = {}
    script = os.path.basename(__file__)

    logFile = '/tmp/%s' % script.replace(".py", ".log")

    logging.basicConfig(filename=logFile,
                        level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    #capture arguments
    mydict = getArgvDic(sys.argv)
    if not (mydict.get("-i") or mydict.get("-o")):    #required parameters
        usage()
    inDirName = mydict.get("-i")
    outDirName = mydict.get("-o")
    if mydict.get("-f"):
        FORMATRULE = mydict.get("-f")
    else:
        FORMATRULE = "./TAF-threshold.param"
    if not os.path.isdir(inDirName):
        usage()

    # Generate defaults for every specified items
    (DefaultsUpdate, DefaultsAdd) = generateDefaults(FORMATRULE)

    logging.info('Process .json file/s in: %s' % inDirName)

    list = listAllJsonFiles(inDirName)
    print("Processing the JSON files\n...")
    for i in range(len(list)):
        infile = list[i]
        #print("infile is: %s" % infile)
        logging.info('Process file: %s' % infile)
        # Generate the outfile name

        if not inDirName.endswith("/"):
            inDirName = "%s/" % inDirName
        if not outDirName.endswith("/"):
            outDirName = "%s/" % outDirName

        outfile = infile.replace(inDirName, outDirName)

        path = os.path.split(outfile)[0]
        if not os.path.isdir(path):
            os.makedirs(path)

        # Translate to new format for one file
        changeJsonToNewFormat(infile, outfile, DefaultsUpdate, DefaultsAdd)
        #print("outfile is: %s" % outfile)
        logging.info('Translated to file: %s' % outfile)
    print("Completed.\nPlease check for details in logfile: %s" % logFile)

if __name__ == '__main__':
    main()
