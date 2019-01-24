class Threshold(object):
    # define
    '''
    Class of threshold from attributes setting
        """

        :param label:
        :param description:
        :param severity:
        :param interval:
        :param occur:
        """
    '''
    def __init__(self, label, description, severity, interval, occur):
        """

        :param label:
        :param description:
        :param severity:
        :param interval:
        :param occur:
        """
        self.name = label
        self.description = description
        self.severity = severity
        self.interval = period
        self.occur = periods

    def keys_and_values(self):
        return self.__dict__

    def generate_configuration(self):
        print("Generating the configuration with template")
        pass

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_severity(self):
        return self.serverity

    def get_interval(self):
        return self.interval

    def get_occur(self):
        return self.occur

    def explain(self):
        return self.__doc__

    def change_name(self, newName):
        print("Changing name from %s to %s" % (self.name, newName))
        self.name = newName

    def get_monsol(self):
        # get the Monsol, e.g the Monsol for all_ams_nlz2_linux should be 'linux'
        Monsol = self.name.split("_")[3]
        return Monsol

    def export_to_json(self, file):
        ''''
        export to a JSON file
        '''
        self.file = file

        print("Export threshold to a JSON file: %s" % self.file)

        pass

        return self.file


class ThresholdObj(object):
    # define
    '''
    Class of threshold
        :param obj: coming from the threshold's configuration JSON file
    '''
    def __init__(self, obj):
        '''
        :param obj:
        '''
        self.name = obj["label"]
        self.description = obj["description"]
        self.severity = obj["configuration"]["payload"]["severity"]
        self.interval = obj["configuration"]["payload"]["period"]
        self.occur = obj["configuration"]["payload"]["periods"]

    def keys_and_values(self):
        return self.__dict__

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_severity(self):
        return self.severity

    def get_interval(self):
        return self.interval

    def get_occur(self):
        return self.occur

    def get_formular(self):
        formula = "TBD"
        print("Getting its formular...")
        return formula

    def get_interval_refined(self):
        interval = self.get_interval()
        interval_new = "new_for_%s" % interval
        return interval_new

    def explain(self):
        return self.__doc__

    def get_monsol(self):
        # get the Monsol, e.g the Monsol for all_ams_nlz2_linux should be 'linux'
        Monsol = self.name.split("_")[3]
        return Monsol

    def change_name(self, newName):
        print("Changing name from %s to %s" % (self.name, newName))
        self.name = newName
    def export_to_json(self, file):
        ''''
        export to a JSON file
        '''
        self.file = file

        print("Export threshold to a JSON file: %s" % self.file)

        pass

        return self.file
