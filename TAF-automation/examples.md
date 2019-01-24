Examples
===

Copy and DeepCopy
---
Usecase: 
1. Process all the threshold JSON files in the specific directory;
2. Translate the threshold JSON files to new format;
3. Add Tool Agnostic properties (visible: Yes/No, editable: Yes/No) to the keys in threhsold JSON file, the the keys can be defined in parameter file;
4. 

Scripts: [TAF-threshold.py](https://github.com/xiaojias/python/blob/master/TAF-automation/TAF-threshold.py) [TAF-threshold.param](https://github.com/xiaojias/python/blob/master/TAF-automation/TAF-threshold.param)

example of usage:

```
$ ./TAF-threshold.py -i ./in -o ./out -f ./TAF-threshold.param
Processing the JSON files
...
Completed.
Please check for details in logfile: /tmp/TAF-threshold.log

$ ls -lrt ./out
total 4
-rw-rw-r--. 1 xiaojias xiaojias 651 Jan 24 10:24 jdt_zom_rlzc_ipcenter.json

```

example codes in [script](https://github.com/xiaojias/python/blob/master/TAF-automation/TAF-threshold.py):
```
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

```
