#!/usr/bin/env python
# -*- coding:utf8 -*-
#
'''
testing for ipm modules
'''
from ipm import resources
from ipm import trans

#threshold01 = resource.Threshold(label="jdt_zom_rlzc_ipcenter", description="Too many zombie processes (Critical)", period="5", periods="1", severity="Warning")

#print(threshold01.__dict__)
#print(threshold01.get_monsol())

#print(threshold01.explain())
#print(threshold01.keys_and_values())

obj01 = trans.read_file_to_obj("jdt_zom_rlzc_ipcenter.json")

print(obj01)

#str_obj01 = u.encode(obj01)

#print("string is: %s" % str_obj01)

threshold01 = resources.ThresholdObj(obj01)

print(threshold01.explain())
print(threshold01.get_name())
print(threshold01.get_description())
print(threshold01.get_severity())
new_serity={}

print(threshold01.get_interval())
print(threshold01.get_occur())
print(threshold01.get_formular())

print(threshold01.get_interval_refined())

threshold01.change_name("new_name")

print(threshold01.get_name())

threshold01.export_to_json("/tmp/new.json")
#obj02 = "sadkfjskajf"

#print(type(obj01))

#obj02 = {"name": "xiao", "id": "999"}

trans.write_obj_to_file( threshold01, /tmp/aa.json")

#print(threshold01.export_to_json("/tmp/aa.out"))

#rg01 = resource.ResourceGroup("test-group", "testing group", "AgentGroup")

#print(rg01.get_name())

