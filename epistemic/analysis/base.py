import logging
log = logging.getLogger("analysis")
import os

# Make it so we can import the parents stuff
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 

class Analysis(object):
    def __init__(self, config):
        self.config = config

    def get_file(self, name):
        """Makes a file and puts it in the appropriate place"""
        pth = self.get_file_name(name)
        log.info("creating %s", pth)
        return open(pth, 'wb')

    def get_file_name(self, name):
        pth = os.path.join(self.config.output_path, self.make_part_name(name))
        return pth

    @property
    def name(self):
        return self.__class__.__name__


class ExperimentAnalysis(Analysis):
    def __init__(self, settings):
        Analysis.__init__(self, settings)

    def make_part_name(self, nm):
        return nm

class TreatmentAnalysis(Analysis):
    def __init__(self, settings, treatment): 
        Analysis.__init__(self, settings)
        self.treatment = treatment

    def make_part_name(self, nm):
        nm, ext = os.path.splitext(nm)
        name = "%s_%s%s" % (self.treatment.name, nm, ext)
        return name

class ReplicateAnalysis(Analysis):
    def __init__(self, settings, treatment):
        Analysis.__init__(self, settings)
        self.treatment = treatment
        self.replicate = treatment.replicate

    def make_part_name(self, nm):
        nm, ext = os.path.splitext(nm)
        name = "%s_%s_%04d%s" % (self.treatment.name, nm, self.treatment.replicate, ext)
        return name

# This allows us to export them to the namespace in the config_loader
analyses = set()
def register_analysis(a):
    global analyses
    analyses.add(a)
    return a

