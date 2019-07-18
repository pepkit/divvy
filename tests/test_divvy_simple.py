import divvy
import yacman
import os
# For interactive debugging:
# import logmuse
# logmuse.init_logger("divvy", "DEBUG")


def test_activate_package():
	dcc = divvy.ComputingConfiguration()
	dcc
	dcc.activate_package("default")
	t = dcc.compute.submission_template
	t2 = dcc["compute"]["submission_template"]
	assert(t == t2)
	dcc.activate_package("slurm")
	t = dcc.compute.submission_template
	t2 = dcc["compute"]["submission_template"]
	assert(t == t2)

def test_write_script():
	dcc = divvy.ComputingConfiguration()
	dcc
	dcc.activate_package("singularity_slurm")
	extra_vars = {
		"singularity_image": "simg",
		"jobname": "jbname",
		"code": "mycode"
		}
	dcc.write_script("test.sub", extra_vars)
	with open("test.sub", 'r') as f:
		contents = f.read()
		assert(contents.find("mycode")>0)
		assert(contents.find("{SINGULARITY_ARGS}") <0)

	os.remove("test.sub")


# class ptest(object):
# 	@property
# 	def doubleslash(self):
# 		return '//'

# p = ptest()
# p.doubleslash
